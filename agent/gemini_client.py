"""
gemini_client.py – Wrapper para Gemini API usando google-genai SDK.
"""

import json
import re
import time
from google import genai


class GeminiClient:
    """Cliente para interactuar con Gemini API."""

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def run_gem(self, prompt: str, max_retries: int = 2) -> dict:
        """
        Envía un prompt al modelo Gemini y parsea la respuesta.

        Returns:
            dict con keys:
                - "json": dict parseado del bloque JSON
                - "markdown": str con el contenido markdown
                - "raw": str con la respuesta completa
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
                
                usage_dict = {
                    "prompt_tokens": 0,
                    "candidates_tokens": 0,
                    "total_tokens": 0
                }
                if hasattr(response, "usage_metadata") and response.usage_metadata:
                    usage_dict["prompt_tokens"] = getattr(response.usage_metadata, "prompt_token_count", 0)
                    usage_dict["candidates_tokens"] = getattr(response.usage_metadata, "candidates_token_count", 0)
                    usage_dict["total_tokens"] = getattr(response.usage_metadata, "total_token_count", 0)
                
                result = self._parse_response(raw_text)
                result["usage"] = usage_dict
                return result

            except Exception as e:
                if attempt < max_retries:
                    wait = 2 ** (attempt + 1)
                    print(f"  ⚠️  Error (intento {attempt + 1}/{max_retries + 1}): {e}")
                    print(f"  ⏳ Reintentando en {wait}s...")
                    time.sleep(wait)
                else:
                    raise RuntimeError(
                        f"Gemini API falló después de {max_retries + 1} intentos: {e}"
                    )

    def _parse_response(self, raw_text: str) -> dict:
        """Parsea la respuesta de Gemini separando JSON y Markdown."""
        json_data = None
        markdown = raw_text

        # Buscar bloque ```json ... ``` (o similar)
        json_match = re.search(
            r"```(?:json)?\s*\n(.*?)\n\s*```", raw_text, re.DOTALL
        )

        if json_match:
            json_str = json_match.group(1).strip()
            try:
                json_data = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"  ⚠️  JSON parse error in code block: {e}")
                json_data = {"_raw_json": json_str, "_parse_error": str(e)}

            # Markdown es todo lo que NO es el bloque JSON
            markdown = raw_text[: json_match.start()] + raw_text[json_match.end() :]
            markdown = markdown.strip()
        else:
            # Fallback: si el modelo devuelve JSON crudo sin backticks
            try:
                # Intentar parsear el raw_text entero
                json_data = json.loads(raw_text.strip())
                markdown = "" # No hay markdown si es todo JSON
            except json.JSONDecodeError:
                # Si falla, simplemente asumimos que no hay JSON en la respuesta
                pass

        return {
            "json": json_data,
            "markdown": markdown,
            "raw": raw_text,
        }
