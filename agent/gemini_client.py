import json
import re
import asyncio
import os
from typing import TypedDict, Any, Optional
from google import genai
from rich.console import Console
import httpx

import config

console = Console()


class GeminiUsage(TypedDict):
    prompt_tokens: int
    candidates_tokens: int
    total_tokens: int
    finish_reason: str


class GeminiResult(TypedDict):
    json: Optional[dict[str, Any]]
    markdown: str
    raw: str
    usage: GeminiUsage


class GeminiClient:
    """Cliente para interactuar con Gemini API u Ollama."""

    def __init__(self, api_key: str, model: str = config.DEFAULT_MODEL):
        self.provider = config.LLM_PROVIDER
        if self.provider == "gemini":
            self.client = genai.Client(api_key=api_key)
        self.model = model if self.provider == "gemini" else config.OLLAMA_MODEL
        # Use a single client for the instance to allow connection pooling
        self._async_client = httpx.AsyncClient(timeout=120.0)

    async def close(self):
        """Closes the underlying HTTP client."""
        await self._async_client.aclose()

    async def run_gem(
        self,
        prompt: str,
        gem_name: Optional[str] = None,
        max_retries: int = config.MAX_RETRIES_ON_BLOCK
    ) -> GeminiResult:
        if self.provider == "ollama":
            return await self._run_ollama(prompt, gem_name, max_retries)
        return await self._run_gemini(prompt, gem_name, max_retries)

    async def _run_ollama(self, prompt: str, gem_name: Optional[str], max_retries: int) -> GeminiResult:
        """Envía un prompt a Ollama."""
        url = f"{config.OLLAMA_BASE_URL}/api/generate"
        cfg = config.GEM_CONFIGS.get(gem_name, {"temperature": 0.3, "top_p": 0.8, "max_tokens": 4096})

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": cfg.get("temperature", 0.3),
                "top_p": cfg.get("top_p", 0.8),
                "num_predict": cfg.get("max_tokens", 4096),
                "seed": int(os.getenv("SEED", "42"))
            }
        }

        for attempt in range(max_retries + 1):
            try:
                response = await self._async_client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()

                raw_text = data.get("response", "")

                usage: GeminiUsage = {
                    "prompt_tokens": data.get("prompt_eval_count", 0),
                    "candidates_tokens": data.get("eval_count", 0),
                    "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0),
                    "finish_reason": "STOP"
                }

                result_content = self._parse_response(raw_text)

                return {
                    "json": result_content["json"],
                    "markdown": result_content["markdown"],
                    "raw": raw_text,
                    "usage": usage
                }
            except Exception as e:
                if attempt < max_retries:
                    await asyncio.sleep(2 ** (attempt + 1))
                else:
                    raise RuntimeError(f"Ollama falló: {e}")
        raise RuntimeError("Unreachable")

    async def _run_gemini(
        self,
        prompt: str,
        gem_name: Optional[str] = None,
        max_retries: int = config.MAX_RETRIES_ON_BLOCK
    ) -> GeminiResult:
        """
        Envía un prompt al modelo Gemini y parsea la respuesta.
        """
        cfg = config.GEM_CONFIGS.get(gem_name, {"temperature": 0.3, "top_p": 0.8, "max_tokens": 4096})

        for attempt in range(max_retries + 1):
            try:
                # Use aio for non-blocking calls
                response = await self.client.aio.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config={
                        "temperature": cfg.get("temperature"),
                        "top_p": cfg.get("top_p"),
                        "max_output_tokens": cfg.get("max_tokens"),
                    },
                )

                raw_text = response.text

                usage_dict: GeminiUsage = {
                    "prompt_tokens": 0,
                    "candidates_tokens": 0,
                    "total_tokens": 0,
                    "finish_reason": "UNKNOWN"
                }

                if hasattr(response, "usage_metadata") and response.usage_metadata:
                    usage_dict["prompt_tokens"] = getattr(
                        response.usage_metadata, "prompt_token_count", 0
                    )
                    usage_dict["candidates_tokens"] = getattr(
                        response.usage_metadata, "candidates_token_count", 0
                    )
                    usage_dict["total_tokens"] = getattr(
                        response.usage_metadata, "total_token_count", 0
                    )

                if hasattr(response, "candidates") and response.candidates:
                    usage_dict["finish_reason"] = getattr(response.candidates[0], "finish_reason", "STOP")

                result_content = self._parse_response(raw_text)

                return {
                    "json": result_content["json"],
                    "markdown": result_content["markdown"],
                    "raw": raw_text,
                    "usage": usage_dict
                }

            except Exception as e:
                if attempt < max_retries:
                    wait = 2 ** (attempt + 1)
                    console.print(f"[yellow]  ⚠️  Error (intento {attempt + 1}/{max_retries + 1}): {e}[/yellow]")
                    console.print(f"[dim]  ⏳ Reintentando en {wait}s...[/dim]")
                    await asyncio.sleep(wait)
                else:
                    raise RuntimeError(
                        f"Gemini API falló después de {max_retries + 1} intentos: {e}"
                    )
        raise RuntimeError("Unreachable")

    def _parse_response(self, raw_text: str) -> dict[str, Any]:
        """Parsea la respuesta de Gemini separando JSON y Markdown."""
        json_data = None
        markdown = raw_text

        # Intentar encontrar bloques de código JSON
        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)

        if not json_match:
            # Intentar encontrar cualquier bloque que empiece con { y termine con }
            json_match = re.search(r"(\{.*\})", raw_text, re.DOTALL)

        if json_match:
            json_str = json_match.group(1).strip()

            # Limpieza básica de JSON: eliminar comas finales antes de cerrar llaves/corchetes
            json_str = re.sub(r",\s*([\]}])", r"\1", json_str)

            try:
                json_data = json.loads(json_str)
                markdown = raw_text.replace(json_match.group(0), "").strip()
            except json.JSONDecodeError as e:
                try:
                    json_data = json.loads(raw_text.strip())
                    markdown = ""
                except json.JSONDecodeError:
                    console.print(f"[dim]  ⚠️  JSON parse error: {e}[/dim]")
                    json_data = {"_raw_json": json_str, "_parse_error": str(e)}
        else:
            try:
                json_data = json.loads(raw_text.strip())
                markdown = ""
            except json.JSONDecodeError:
                pass

        return {
            "json": json_data,
            "markdown": markdown,
        }
