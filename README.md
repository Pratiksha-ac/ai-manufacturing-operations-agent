# 🏭 AI Manufacturing Operations Agent

An enterprise-style **AI-powered manufacturing operations platform** that monitors machine telemetry, detects anomalies using Machine Learning, investigates incidents using an Agentic AI workflow, performs root-cause analysis, determines severity, handles human approval for high-risk actions, executes simulated machine actions, exposes APIs through FastAPI, and automates operational alerts using n8n.

---

## 🚀 Project Overview

The **AI Manufacturing Operations Agent** combines Industrial IoT, Machine Learning, Agentic AI, APIs, human-in-the-loop workflows, and automation into an end-to-end manufacturing operations system.

The system continuously processes telemetry from simulated CNC machines and uses an **Isolation Forest anomaly detection model** to identify abnormal machine behavior.

When an anomaly is detected, a **LangGraph-based AI agent** investigates the machine, retrieves historical telemetry from PostgreSQL, identifies a probable root cause, determines incident severity, and generates an operational recommendation.

High-risk incidents require **human approval** before a simulated machine shutdown is executed.

The completed system provides an end-to-end flow:

```text
Factory Machines
      ↓
MQTT
      ↓
Telemetry Processing
      ↓
PostgreSQL
      ↓
Feature Engineering
      ↓
ML Anomaly Detection
      ↓
LangGraph AI Investigation
      ↓
Root Cause Analysis
      ↓
Severity Classification
      ↓
Decision Engine
      ↓
Human-in-the-Loop
      ↓
Simulated Machine Action
      ↓
FastAPI
      ↓
n8n Automation
      ↓
Operational Notification
```

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │   Factory Simulator   │
                         │                      │
                         │ CNC-01               │
                         │ CNC-02               │
                         │ CNC-03               │
                         │ CNC-04               │
                         └──────────┬───────────┘
                                    │
                                    │ MQTT
                                    ▼
                         ┌──────────────────────┐
                         │      Mosquitto       │
                         │     MQTT Broker      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Telemetry Subscriber  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Telemetry Processor   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     PostgreSQL       │
                         │   manufacturing_db   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Feature Engineering  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Isolation Forest    │
                         │  Anomaly Detection   │
                         └──────────┬───────────┘
                                    │
                             Anomaly Detected
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      LangGraph       │
                         │   AI Investigation   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Machine History Tool │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Root Cause Analysis │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Severity Decision  │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴───────────┐
                         │                      │
                      Normal/Warning         High/Critical
                         │                      │
                         ▼                      ▼
                     Monitor /              Human Approval
                     No Action                   │
                                                 ▼
                                        Simulated Action
                                                 │
                                                 ▼
                                            FastAPI API
                                                 │
                                                 ▼
                                              n8n
                                                 │
                                                 ▼
                                        Alert / Notification
```

---

# ✨ Key Features

## 1. Factory Machine Simulation

The project contains a virtual factory environment with four CNC machines:

```text
CNC-01
CNC-02
CNC-03
CNC-04
```

`CNC-04` is configured to produce anomalous telemetry for testing the anomaly detection and AI investigation pipeline.

---

## 2. MQTT-Based Industrial IoT Communication

Machine telemetry is transmitted using MQTT.

Topics:

```text
factory/CNC-01/telemetry
factory/CNC-02/telemetry
factory/CNC-03/telemetry
factory/CNC-04/telemetry
```

The subscriber listens using:

```text
factory/+/telemetry
```

Technology:

- Mosquitto
- Paho MQTT

---

## 3. Telemetry Processing

The telemetry processing layer receives MQTT messages and prepares machine data for storage and analysis.

Telemetry includes:

```text
machine_id
timestamp
temperature
vibration
pressure
rpm
energy_consumption
status
```

---

## 4. PostgreSQL Database

The system stores telemetry in PostgreSQL.

Database:

```text
manufacturing_db
```

Table:

```text
telemetry
```

Schema:

```sql
CREATE TABLE telemetry (
    id SERIAL PRIMARY KEY,
    machine_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    temperature DOUBLE PRECISION,
    vibration DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    rpm INTEGER,
    energy_consumption DOUBLE PRECISION,
    status VARCHAR(20)
);
```

---

# 🤖 Machine Learning Anomaly Detection

The project uses **Isolation Forest** for unsupervised anomaly detection.

Model:

```python
IsolationForest(
    contamination=0.05,
    random_state=42
)
```

The model analyzes machine telemetry and identifies unusual operating patterns.

Example:

```text
CNC-04 → ANOMALY DETECTED
```

The anomaly result is converted to a native Python boolean before entering the LangGraph state to ensure compatibility with checkpoint serialization.

---

# 🧠 Agentic AI Investigation

Once an anomaly is detected, the system launches a LangGraph AI investigation workflow.

The agent:

1. Receives the anomalous machine information.
2. Retrieves recent machine telemetry.
3. Analyzes historical behavior.
4. Determines a probable root cause.
5. Classifies incident severity.
6. Generates an operational recommendation.
7. Determines whether human approval is required.
8. Executes a simulated action after approval.

---

# 🔗 LangGraph Workflow

```text
START
  │
  ▼
Load Machine Telemetry
  │
  ▼
Anomaly Detection
  │
  ▼
Retrieve Machine History
  │
  ▼
AI Investigation
  │
  ▼
Root Cause Analysis
  │
  ▼
Severity Classification
  │
  ▼
Decision Engine
  │
  ├───────────────┐
  │               │
NORMAL/WARNING  HIGH/CRITICAL
  │               │
  ▼               ▼
No Action      Human Approval
                  │
            ┌─────┴─────┐
            │           │
         Approved     Rejected
            │           │
            ▼           ▼
      Simulated       Stop
        Action
            │
            ▼
           END
```

---

# 🔎 Machine History Tool

The AI agent uses the LangChain tool:

```text
get_machine_history
```

The tool retrieves recent telemetry for a machine from PostgreSQL.

Example:

```python
get_machine_history.invoke({
    "machine_id": "CNC-04",
    "limit": 10
})
```

This allows the agent to investigate historical machine behavior instead of making decisions from a single telemetry reading.

---

# 🧠 LLM Integration

The project uses Groq for LLM inference.

Model:

```text
openai/gpt-oss-120b
```

Temperature:

```text
0
```

The AI agent produces structured investigation results:

```json
{
  "root_cause": "Abnormal machine operating conditions",
  "severity": "HIGH",
  "recommendation": "Inspect the machine and stop operation if the condition persists"
}
```

Supported severity levels:

```text
NORMAL
WARNING
HIGH
CRITICAL
```

The agent is instructed to:

- Return structured JSON.
- Avoid unnecessary explanations.
- Avoid Markdown in the model output.
- Avoid inventing telemetry values.
- Base conclusions on available machine data.

---

# ⚠️ Decision Engine

The decision engine converts AI severity into an operational response.

| Severity | Decision | Approval Required | Action |
|---|---|---|---|
| NORMAL | NO_ACTION | No | None |
| WARNING | MONITOR | No | None |
| HIGH | HUMAN_REVIEW | Yes | Shutdown |
| CRITICAL | HUMAN_REVIEW | Yes | Shutdown |

This separates AI reasoning from operational control logic.

---

# 🛑 Human-in-the-Loop

High-risk actions are paused until a human approves them.

LangGraph uses:

```python
interrupt()
```

and:

```python
MemorySaver
```

Example:

```text
CNC-04
   ↓
Anomaly
   ↓
AI Investigation
   ↓
HIGH
   ↓
Human Approval Required
   ↓
Approved
   ↓
Simulated Shutdown
```

The workflow can resume using the same thread after approval.

---

# 🧰 Simulated Machine Actions

The system includes safe simulated operational tools:

```text
shutdown_machine()
restart_machine()
```

These functions simulate machine operations.

They **do not control real industrial equipment**.

This makes the project suitable for development, testing, and demonstration.

---

# 🌐 FastAPI

FastAPI exposes the manufacturing operations agent through REST APIs.

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Health Check

```http
GET /
```

## Investigate Machine

```http
POST /api/v1/investigate
```

Request:

```json
{
  "machine_id": "CNC-04"
}
```

## Human Approval

```http
POST /api/v1/approve
```

Request:

```json
{
  "thread_id": "CNC-04-api",
  "approved": true
}
```

---

# 🔄 n8n Automation

n8n is used as the automation layer after the FastAPI workflow.

Workflow:

```text
Webhook
   ↓
IF
   │
   ├── severity = HIGH
   │
   └── severity = CRITICAL
          ↓
      Edit Fields
          ↓
    Notification / Alert
          ↓
    Respond to Webhook
```

The webhook receives manufacturing incident information such as:

```json
{
  "machine_id": "CNC-04",
  "severity": "HIGH",
  "root_cause": "Abnormal vibration detected",
  "recommendation": "Inspect machine bearings",
  "status": "WAITING_FOR_APPROVAL"
}
```

---

# 📁 Project Structure

```text
ai-manufacturing-operations-agent/
│
└── simulator/
    │
    ├── api/
    │   ├── __init__.py
    │   └── main.py
    │
    ├── action_tools.py
    ├── agent_graph.py
    ├── agent_state.py
    ├── agent_tools.py
    ├── analysis.py
    ├── anomaly_detector.py
    ├── database.py
    ├── decision.py
    ├── features.py
    ├── llm.py
    ├── machine.py
    ├── ml_detector.py
    ├── mqtt_publisher.py
    ├── mqtt_subscriber.py
    ├── telemetry_processor.py
    ├── test_llm.py
    ├── tool_agent.py
    │
    ├── .gitignore
    ├── .env
    └── README.md
```

> `.env` contains secrets and is excluded from Git using `.gitignore`.

---

# 📂 File Responsibilities

| File | Responsibility |
|---|---|
| `machine.py` | Simulates CNC machine telemetry |
| `mqtt_publisher.py` | Publishes machine telemetry through MQTT |
| `mqtt_subscriber.py` | Subscribes to machine telemetry |
| `telemetry_processor.py` | Processes incoming telemetry |
| `database.py` | PostgreSQL database connection and operations |
| `features.py` | Feature engineering for ML |
| `analysis.py` | Telemetry/data analysis |
| `anomaly_detector.py` | Anomaly detection functionality |
| `ml_detector.py` | Machine Learning anomaly detection |
| `agent_state.py` | Defines LangGraph manufacturing state |
| `agent_tools.py` | LangChain tools for machine investigation |
| `tool_agent.py` | AI investigation agent |
| `agent_graph.py` | LangGraph workflow and human approval |
| `decision.py` | Severity-to-action decision logic |
| `action_tools.py` | Simulated machine actions |
| `llm.py` | Groq LLM configuration |
| `test_llm.py` | LLM testing |
| `api/main.py` | FastAPI application and endpoints |
| `api/__init__.py` | API package initialization |
| `.gitignore` | Prevents secrets and generated files from being committed |
| `.env` | Local environment configuration and API secrets |
| `README.md` | Project documentation |

---

# 🛠️ Technology Stack

## Programming

- Python

## Machine Learning

- Scikit-learn
- Isolation Forest
- Pandas
- NumPy

## Agentic AI

- LangChain
- LangGraph
- Groq
- `openai/gpt-oss-120b`

## Backend

- FastAPI
- Uvicorn

## Database

- PostgreSQL

## Industrial IoT

- MQTT
- Mosquitto
- Paho MQTT

## Automation

- n8n

## Development Tools

- PowerShell
- Git
- GitHub
- Python Virtual Environment

---

# ⚙️ Environment Configuration

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit API keys or secrets to GitHub.

The repository uses `.gitignore` to exclude:

```text
.env
.venv/
__pycache__/
*.pyc
*.log
node_modules/
.n8n/
```

---

# ▶️ Running the Project

## 1. Activate Virtual Environment

```powershell
.venv\Scripts\activate
```

## 2. Start PostgreSQL

Make sure PostgreSQL is running and the database exists:

```text
manufacturing_db
```

## 3. Start Mosquitto

Ensure the Mosquitto MQTT service is running.

## 4. Start Machine Simulation

```powershell
python machine.py
```

## 5. Start MQTT Publisher

```powershell
python mqtt_publisher.py
```

## 6. Start MQTT Subscriber

```powershell
python mqtt_subscriber.py
```

## 7. Run the FastAPI Application

```powershell
uvicorn api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## 8. Start n8n

```powershell
$env:N8N_USER_FOLDER="D:\n8n-data"
$env:Path="D:\npm-global;$env:Path"
$env:NODE_OPTIONS="--max-old-space-size=4096"
n8n
```

Open:

```text
http://localhost:5678
```

---

# 🧪 End-to-End Example

The following scenario demonstrates the complete system.

### Step 1 — Machine Telemetry

```text
CNC-04
Temperature: Abnormal
Vibration: Abnormal
RPM: Abnormal
```

### Step 2 — MQTT

```text
factory/CNC-04/telemetry
```

### Step 3 — Database

Telemetry is stored in PostgreSQL.

### Step 4 — Machine Learning

Isolation Forest identifies the telemetry as anomalous.

```text
CNC-04 → ANOMALY
```

### Step 5 — AI Investigation

LangGraph starts the investigation.

The agent retrieves machine history using:

```text
get_machine_history
```

### Step 6 — Root Cause

The LLM analyzes current and historical telemetry.

### Step 7 — Severity

Example:

```text
HIGH
```

### Step 8 — Human Approval

The workflow pauses.

```text
WAITING FOR HUMAN APPROVAL
```

### Step 9 — Approval

```json
{
  "thread_id": "CNC-04-api",
  "approved": true
}
```

### Step 10 — Simulated Action

```text
Simulated shutdown of CNC-04
```

### Step 11 — FastAPI

The workflow is exposed through the REST API.

### Step 12 — n8n

The incident is sent to the n8n automation workflow.

### Step 13 — Alert

n8n processes the high-severity incident and triggers the configured notification workflow.

---

# 🔐 Safety & Security

This project follows a simulation-first architecture.

### Safety

- No real industrial machinery is controlled.
- Machine shutdown/restart operations are simulated.
- High-risk actions require human approval.
- AI recommendations are separated from action execution.

### Security

- API keys are stored in environment variables.
- `.env` is excluded from Git.
- Operational actions are simulated.
- Human approval is required for high-risk decisions.

---

# 📊 Completed Components

| Component | Status |
|---|---|
| Factory Machine Simulation | ✅ Complete |
| MQTT Communication | ✅ Complete |
| Mosquitto MQTT Broker | ✅ Complete |
| Telemetry Processing | ✅ Complete |
| PostgreSQL Storage | ✅ Complete |
| Feature Engineering | ✅ Complete |
| ML Anomaly Detection | ✅ Complete |
| Isolation Forest | ✅ Complete |
| LangGraph Agent | ✅ Complete |
| Machine History Tool | ✅ Complete |
| Root Cause Analysis | ✅ Complete |
| Severity Classification | ✅ Complete |
| Decision Engine | ✅ Complete |
| Simulated Machine Actions | ✅ Complete |
| Human-in-the-Loop | ✅ Complete |
| LangGraph Checkpointing | ✅ Complete |
| FastAPI Integration | ✅ Complete |
| n8n Automation | ✅ Complete |
| Git/GitHub Integration | ✅ Complete |

---

# 🎯 Project Highlights

This project demonstrates practical experience with:

- Agentic AI systems
- LangGraph stateful workflows
- Human-in-the-loop AI
- LLM-based root-cause analysis
- Machine Learning anomaly detection
- Industrial IoT telemetry
- MQTT communication
- PostgreSQL data pipelines
- FastAPI backend development
- Workflow automation with n8n
- AI-assisted operational decision making
- Safe simulation of industrial actions
- Git/GitHub project management

---

# 👩‍💻 Author

**Pratiksha Chandanshiv**

AI/ML Engineer

GitHub:

https://github.com/Pratiksha-ac

---

# ⭐ Repository

**AI Manufacturing Operations Agent**

https://github.com/Pratiksha-ac/ai-manufacturing-operations-agent
