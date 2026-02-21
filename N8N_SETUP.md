# Uso de Raadbot con n8n

Raadbot ahora está preparado para integrarse de forma nativa con n8n mediante una API HTTP interna y comandos CLI.

## Iniciar los servicios localmente

1. **Iniciar la API de Raadbot:**
   La API debe estar corriendo en segundo plano para que n8n pueda enviarle peticiones.
   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```

2. **Iniciar n8n:**
   Si instalaste n8n globalmente vía npm, ejecútalo en otra pestaña de tu terminal:
   ```bash
   n8n start
   ```
   n8n estará disponible en `http://localhost:5678`.

---

## Configurar el Workflow en n8n

La forma más limpia y robusta de conectar Raadbot con n8n es utilizando un nodo **HTTP Request**.

### 1. Añade un nodo "HTTP Request" en n8n
- **Method**: `POST`
- **URL**: `http://localhost:8000/api/v1/run`

### 2. Configura el Body (Payload)
- Activa la opción **Send Body**
- Selecciona el Body Content Type como **JSON**
- Como valor del JSON de envío, usa la siguiente estructura (Añade `webhook_url` si quieres que no exeda los limites de timeout):

**Ejemplo usando Google Drive y Webhooks:**
```json
{
  "search_id": "SEARCH-2026-N8N",
  "drive_folder": "1aBcDeFgHiJkLmNoPqRsT",
  "webhook_url": "http://tu-instancia-n8n/webhook-test/pipeline-ready"
}
```

### 3. Extraer los datos (Asíncrono vs Síncrono)
Dado que los pipelines pueden tardar varios minutos (3-5 min), es **altamente probable** que si no configuras `webhook_url`, el Request HTTP intercepte un timeout (504).
Usando webhook, Raadbot retornará de inmediato `{"status": "processing"}` y hará POST al finalizar a tu URL con el JSON final:

```json
{
  "status": "success",
  "search_id": "SEARCH-2026-N8N",
  "output_dir": "runs/SEARCH-2026-N8N/outputs",
  "summary": {  // <--- ¡Acá están los resultados!
    "candidatos_totales": 1,
    "candidatos_aprobados": 1,
    "candidatos_rechazados": 0,
    "detalles": {
      "CAND-001": {
        "status": "APPROVED",
        "final_score": 8.0,
        "gates": {...}
      }
    }
  }
}
```

Puedes conectar nodos posteriores en n8n para leer estas variables `{{ $json.summary.candidatos_aprobados }}` y enviar correos, escribir en Slack o actualizar una base de datos.
