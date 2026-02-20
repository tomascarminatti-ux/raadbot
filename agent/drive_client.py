"""
drive_client.py – Cliente de Google Drive para leer inputs de candidatos.
"""

import io
import os
from typing import Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
TOKEN_FILE = "token.json"


class DriveClient:
    """Cliente para leer archivos desde Google Drive."""

    def __init__(self, credentials_path: str = "credentials.json"):
        self.credentials_path = credentials_path
        self.service = self._authenticate()

    def _authenticate(self):
        """Autenticación OAuth2 con token cacheado."""
        creds = None
        base_dir = os.path.dirname(os.path.abspath(self.credentials_path))
        token_path = os.path.join(base_dir, TOKEN_FILE)

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"No se encontró {self.credentials_path}. "
                        "Descargalo desde Google Cloud Console > APIs > Credentials > OAuth 2.0."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(token_path, "w") as token:
                token.write(creds.to_json())

        return build("drive", "v3", credentials=creds)

    def list_files(self, folder_id: str) -> list[dict]:
        """
        Lista archivos en una carpeta de Drive.

        Returns:
            Lista de dicts con id, name, mimeType
        """
        query = f"'{folder_id}' in parents and trashed = false"
        results = (
            self.service.files()
            .list(q=query, fields="files(id, name, mimeType)", pageSize=100)
            .execute()
        )
        return results.get("files", [])

    def list_folders(self, folder_id: str) -> list[dict]:
        """Lista subcarpetas en una carpeta de Drive."""
        query = (
            f"'{folder_id}' in parents "
            "and mimeType = 'application/vnd.google-apps.folder' "
            "and trashed = false"
        )
        results = (
            self.service.files()
            .list(q=query, fields="files(id, name)", pageSize=100)
            .execute()
        )
        return results.get("files", [])

    def download_file(self, file_id: str, mime_type: Optional[str] = None) -> str:
        """
        Descarga el contenido de un archivo como texto.

        Soporta:
        - Google Docs → exporta como texto plano
        - PDFs → descarga binario (requiere parsing externo)
        - Archivos de texto → descarga directa
        """
        if mime_type == "application/vnd.google-apps.document":
            # Exportar Google Doc como texto plano
            request = self.service.files().export_media(
                fileId=file_id, mimeType="text/plain"
            )
        else:
            # Descargar archivo directamente
            request = self.service.files().get_media(fileId=file_id)

        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

        content = buffer.getvalue()

        # Intentar decodificar como texto
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return content.decode("latin-1")

    def download_folder_as_inputs(
        self, folder_id: str, target_dir: str
    ) -> dict[str, str]:
        """
        Descarga todos los archivos de una carpeta de Drive a un directorio local.

        Returns:
            Dict de filename → contenido de texto
        """
        os.makedirs(target_dir, exist_ok=True)
        files = self.list_files(folder_id)
        inputs = {}

        for file_info in files:
            name = file_info["name"]
            mime = file_info["mimeType"]

            # Saltar carpetas
            if mime == "application/vnd.google-apps.folder":
                continue

            print(f"  📥 Descargando: {name}")
            content = self.download_file(file_info["id"], mime)

            # Guardar localmente
            safe_name = name.replace("/", "_")

            if "google-apps" in mime:
                if not safe_name.endswith(".txt"):
                    safe_name += ".txt"
            else:
                if mime == "application/pdf" or "wordprocessing" in mime:
                    raise ValueError(
                        f"El archivo '{name}' es un binario ({mime}). Por favor súbelo en formato texto (.txt) o como Google Docs exportable. Los PDFs y Word crudos corrompen el output del LLM."
                    )
                if not safe_name.endswith(".txt") and mime.startswith("text/"):
                    safe_name += ".txt"

            filepath = os.path.join(target_dir, safe_name)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            inputs[safe_name] = content

        return inputs

    def discover_search_structure(self, folder_id: str) -> dict:
        """
        Descubre la estructura de una carpeta de búsqueda en Drive.

        Espera estructura:
        <folder>/
          brief_jd.txt (o .doc)
          kickoff_notes.txt
          company_context.txt
          <candidate_name_or_id>/
            cv.txt
            interview_notes.txt
            tests.txt
            case_notes.txt
            references.txt

        Returns:
            Dict con search_inputs y candidates
        """
        search_inputs: dict[str, str] = {}
        candidates: dict[str, dict[str, str]] = {}

        files = self.list_files(folder_id)
        folders = self.list_folders(folder_id)

        # Archivos de nivel raíz = inputs de la búsqueda
        for f in files:
            name = f["name"].lower()
            content = self.download_file(f["id"], f["mimeType"])

            if "brief" in name or "jd" in name or "job" in name:
                search_inputs["jd_text"] = content
            elif "kickoff" in name or "kick-off" in name or "kick_off" in name:
                search_inputs["kickoff_notes"] = content
            elif "company" in name or "context" in name or "compañía" in name:
                search_inputs["company_context"] = content
            elif "culture" in name or "cultura" in name:
                search_inputs["client_culture"] = content

        # Subcarpetas = candidatos
        for folder in folders:
            candidate_id = folder["name"]
            print(f"  👤 Candidato encontrado: {candidate_id}")
            candidate_files = self.list_files(folder["id"])
            candidate_inputs = {}

            for f in candidate_files:
                name = f["name"].lower()
                content = self.download_file(f["id"], f["mimeType"])

                if "cv" in name or "resume" in name or "curriculum" in name:
                    candidate_inputs["cv_text"] = content
                elif "interview" in name or "entrevista" in name:
                    candidate_inputs["interview_notes"] = content
                elif "test" in name or "assessment" in name:
                    candidate_inputs["tests_text"] = content
                elif "case" in name or "caso" in name or "conductual" in name:
                    candidate_inputs["case_notes"] = content
                elif "reference" in name or "referencia" in name:
                    candidate_inputs["references_text"] = content
                elif "culture" in name or "cultura" in name:
                    candidate_inputs["client_culture"] = content

            candidates[candidate_id] = candidate_inputs

        return {
            "search_inputs": search_inputs,
            "candidates": candidates,
        }
