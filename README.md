# 🤖 Raadbot v3.0 — Industrial Multi-Agent Intelligence

> 🎯 **Objetivo**
>
> Raadbot v3.0 es un ecosistema multi-agente industrial basado en el framework GEM, orquestado por **GEM 6 (The Architect)** bajo una arquitectura **Hub-and-Spoke 3.0**. Diseñado para procesamiento masivo de candidatos, trazabilidad total y decisiones autónomas de alta precisión.

---

## 🏗️ Arquitectura del Sistema: Hub-and-Spoke 3.0

A diferencia de las versiones anteriores secuenciales, Raadbot v3.0 utiliza un modelo de **Orquestación Autónoma**. GEM 6 actúa como el cerebro central que decide dinámicamente qué agentes invocar basándose en el contexto del candidato y los objetivos del mandato.

### 📊 Diagrama de Arquitectura Detallada

```mermaid
graph TB
    subgraph "Ecosistema Externo"
        User([Usuario / Cliente])
        n8n[n8n Workflow Engine]
        Sheets[Google Sheets Dashboard]
        Drive[Google Drive Storage]
    end

    subgraph "Raadbot Core (Docker Stack)"
        API[FastAPI Gateway]
        DB[(Source of Truth - SQLite/PG)]

        subgraph "Capa de Inteligencia (Hub)"
            GEM6{{"🧠 GEM 6<br/>Orchestrator<br/>(The Architect)"}}
        end

        subgraph "Agentes Especializados (Spokes)"
            GEM1["🔵 GEM 1<br/>Discovery & Facts"]
            GEM2["🟢 GEM 2<br/>Scoring & Fit"]
            GEM3["🟡 GEM 3<br/>Decision & Veredict"]
            GEM4["🔴 GEM 4<br/>QA & Audit"]
            GEM5["🟣 GEM 5<br/>Strategy & Mandate"]
        end

        subgraph "Capa de Validación"
            Contracts{{"📜 JSON Contracts<br/>(jsonschema)"}}
        end
    end

    User -->|POST /api/v1/run| API
    n8n -->|Webhook Trigger| API
    API -->|Background Task| GEM6
    API <--> DB

    GEM6 <-->|Reasoning Loop| GEM1
    GEM6 <-->|Reasoning Loop| GEM2
    GEM6 <-->|Reasoning Loop| GEM3
    GEM6 <-->|Reasoning Loop| GEM4
    GEM6 <-->|Reasoning Loop| GEM5

    GEM1 & GEM2 & GEM3 & GEM4 & GEM5 -.->|Check| Contracts

    GEM6 -->|Final Veredict| API
    API -->|Webhook Response| n8n
    API -->|Sync| Sheets
    API -->|Read Inputs| Drive
```

---

## 🧠 Ciclo de Razonamiento GEM 6

El orquestador no sigue un script lineal; opera en un bucle de **Pensamiento -> Acción -> Observación** (máximo 10 pasos por entidad).

### 🔄 Flujo de Ejecución Autónoma

```mermaid
sequenceDiagram
    participant G6 as GEM 6 (Architect)
    participant DB as Database/Context
    participant AG as Specialized Agent (GEM 1-5)
    participant VAL as Contract Validator

    Note over G6, DB: Inicio del Ciclo (Paso 1 de 10)
    G6->>DB: Leer Memoria de Trabajo & Contexto
    Note right of G6: Thought: Analiza qué falta para el veredicto
    G6->>G6: Decide Acción (Call Agent vs Finalize)

    alt Acción: call_agent
        G6->>AG: Envía Payload con Instrucciones
        AG-->>G6: Retorna JSON con Hallazgos
        G6->>VAL: Valida contra JSON Schema
        VAL-->>G6: Resultado (Valid / Error)
        G6->>DB: Loguea Observación y Actualiza Memoria
    else Acción: finalize
        G6->>DB: Consolida Veredicto Final
        G6->>DB: Marca Entidad como COMPLETED
    end
    Note over G6, DB: Repite bucle si no ha finalizado
```

---

## 🧩 Agentes Especializados (The Spokes)

| Agente | Color | Misión | Tooling Interno |
| :--- | :---: | :--- | :--- |
| **GEM 5** | 🟣 | **Strategy**: Define la radiografía del proyecto y el mandato. | Análisis de JD y Briefing. |
| **GEM 1** | 🔵 | **Discovery**: Extrae hechos, métricas y trayectoria real. | Análisis de CV y Entrevistas. |
| **GEM 2** | 🟢 | **Scoring**: Evalúa el fit técnico y cultural (0.0 a 1.0). | Rúbricas de calibración. |
| **GEM 3** | 🟡 | **Decision**: Genera el veredicto final y argumentos 360°. | Síntesis de evidencia. |
| **GEM 4** | 🔴 | **QA Gate**: Audita el proceso buscando alucinaciones. | Verificación cruzada. |

---

## 🚦 Estados del Candidato (Lifecycle)

El sistema gestiona el ciclo de vida de cada candidato de forma independiente, permitiendo paradas tempranas (*early exits*) si la calidad no es suficiente.

```mermaid
stateDiagram-v2
    [*] --> DISCOVERY: Triggered
    DISCOVERY --> SCORING: GEM 1 Completed
    SCORING --> DECISION: Score >= Threshold (0.4)
    SCORING --> DISCARDED: Score < Threshold
    DECISION --> AUDIT: GEM 3 Completed
    AUDIT --> SUCCESS: QA Passed
    AUDIT --> MANUAL_REVIEW: QA Issues Found (Score < 0.85)
    SUCCESS --> [*]
    DISCARDED --> [*]
    MANUAL_REVIEW --> [*]
```

---

## 🚀 Despliegue y Uso

### Instalación con Docker
```bash
git clone https://github.com/tomascarminatti-ux/raadbot.git
cd raadbot
cp .env.example .env
docker compose up -d --build
```

### Integración con n8n
Raadbot está diseñado para ser "API-First". Puedes disparar el pipeline desde n8n enviando un POST a `/api/v1/run` con un `webhook_url`. El sistema procesará los candidatos en segundo plano y notificará a n8n cuando termine.

### Endpoints Críticos
- `POST /api/v1/run`: Inicia el pipeline autónomo.
- `POST /api/v1/search/setup`: Ejecuta GEM 5 para definir la estrategia de una búsqueda.
- `GET /dashboard`: Visualización en tiempo real del estado de los agentes.
- `GET /health`: Estado del sistema y versión.

---

## 🛡️ Estándares Industriales y Calidad

- **Contratos JSON**: Cada agente tiene un esquema en `contracts/`. Si el LLM falla el contrato, GEM 6 detecta el error y puede reintentar o marcar falla.
- **Trazabilidad (Trace ID)**: Cada decisión de GEM 6 y cada respuesta de los agentes está vinculada a un `trace_id` único en la DB para auditorías.
- **Cost Control**: Implementación de *Early Exit* en GEM 2 para no procesar candidatos de bajo fit en agentes más costosos (GEM 3/4).

---
Version 3.0.0 — Raad Advisory Industrial Platform
