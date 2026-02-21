# Setup de Workflows de n8n

He creado la carpeta `n8n_workflows` que contiene **dos plantillas** listas para importar en tu instancia de n8n.

### 1. Importar Workflow Local
1. Abre n8n (generalmente `http://localhost:5678`).
2. Sube a la parte superior derecha `...` -> `Import from file`.
3. Selecciona `n8n_workflows/sync_pipeline_manual_trigger.json`.
4. Éste test utiliza `SEARCH-TEST-001` con la carpeta de archivos plana que tengas allí. Haz click en "Test Workflow" para ver cómo el nodo absorbe los datos y parsea el resultado JSON.

*(Nota: Este test es síncrono. Si tarda más de 60 segundos por múltiples candidatos simulados, podría generarte un Warning en la UI de n8n. Para pipelines reales masivos, usa la plantilla asincrónica de abajo).*

### 2. Importar el Workflow Asíncrono de Producción
1. Descarga el JSON y arrástralo a la interfaz. `n8n_workflows/async_pipeline_trigger.json`.
2. Este workflow despliega dos Webhooks:
   - **Trigger (Receptor)**: A donde tú mandas un POST con tu payload `{ "search_id": "XY", "drive_folder": "ID" }`.
   - **Receiver (Final)**: A donde la API de Raadbot hará el POST una vez concluido el proceso en background.

**IMPORTANTE DE RED PARA N8N LOCAL:**
Si estás probando n8n de manera local, los Webhooks generarán URLs de prueba bajo `localhost` (o tunelizados via webhook.site).
Debes revisar que en el nodo de Raadbot ("Call API"), la variable de entorno para enviar la URL del webhook apunte a una URL accesible por la API.

Para usarlo por primera vez:
1. Activa o haz click derecho en ambos Nodos de Webhook para ponerles URL de *Modo Test*.
2. Aprieta "Listen for Event" en el Webhook de resultados listos, y ejecuta.
