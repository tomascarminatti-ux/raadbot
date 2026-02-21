import json
import re
import time
from typing import TypedDict, Any, Optional
from google import genai
from rich.console import Console

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
    """Cliente para interactuar con Gemini API."""

    def __init__(self, api_key: str, model: str = config.DEFAULT_MODEL):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def run_gem(self, prompt: str, max_retries: int = config.MAX_RETRIES_ON_BLOCK) -> GeminiResult:
        """
        Envía un prompt al modelo Gemini y parsea la respuesta.

        Returns:
            GeminiResult con el contenido parseado y metadatos de uso.
        """
        for attempt in range(max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config={
                        "temperature": 0.3,
                        "max_output_tokens": 8192,
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
                    time.sleep(wait)
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
                # Separar markdown (lo que queda fuera del bloque JSON detectado)
                # Usamos una versión segura del reemplazo para evitar errores si json_match.group(0) aparece múltiples veces
                markdown = raw_text.replace(json_match.group(0), "").strip()
            except json.JSONDecodeError as e:
                # Si falla, intentar cargar el texto crudo si parece un objeto
                try:
                    json_data = json.loads(raw_text.strip())
                    markdown = ""
                except json.JSONDecodeError:
                    console.print(f"[dim]  ⚠️  JSON parse error: {e}[/dim]")
                    json_data = {"_raw_json": json_str, "_parse_error": str(e)}
        else:
            # Fallback final: ¿Es todo el texto un JSON?
            try:
                json_data = json.loads(raw_text.strip())
                markdown = ""
            except json.JSONDecodeError:
                pass

        return {
            "json": json_data,
            "markdown": markdown,
        }
