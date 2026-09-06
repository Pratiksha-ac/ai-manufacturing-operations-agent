from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.types import Command

from agent_graph import build_graph


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="AI Manufacturing Operations Agent",
    description="AI-powered manufacturing monitoring and operations API",
    version="1.0.0"
)


# ============================================================
# BUILD GRAPH ONCE
# ============================================================

agent = build_graph()


# ============================================================
# REQUEST MODELS
# ============================================================

class InvestigationRequest(BaseModel):
    machine_id: str


class ApprovalRequest(BaseModel):
    thread_id: str
    approved: bool


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def health_check():

    return {
        "status": "online",
        "service": "AI Manufacturing Operations Agent"
    }


# ============================================================
# INVESTIGATE MACHINE
# ============================================================

@app.post("/api/v1/investigate")
def investigate_machine(
    request: InvestigationRequest
):

    thread_id = f"{request.machine_id}-api"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    initial_state = {
        "machine_id": request.machine_id
    }

    result = agent.invoke(
        initial_state,
        config=config
    )

    # --------------------------------------------------------
    # CHECK IF HUMAN APPROVAL IS REQUIRED
    # --------------------------------------------------------

    interrupt_data = result.get("__interrupt__")

    if interrupt_data:

        approval_request = interrupt_data[0].value

        return {
            "status": "WAITING_FOR_APPROVAL",
            "thread_id": thread_id,
            "approval_request": approval_request
        }

    # --------------------------------------------------------
    # WORKFLOW COMPLETED WITHOUT APPROVAL
    # --------------------------------------------------------

    return {
        "status": "COMPLETED",
        "thread_id": thread_id,
        "result": {
            "machine_id": result.get("machine_id"),
            "anomaly": result.get("anomaly"),
            "temperature": result.get("temperature"),
            "vibration": result.get("vibration"),
            "pressure": result.get("pressure"),
            "rpm": result.get("rpm"),
            "energy_consumption": result.get(
                "energy_consumption"
            ),
            "root_cause": result.get("root_cause"),
            "severity": result.get("severity"),
            "recommendation": result.get(
                "recommendation"
            ),
            "requires_approval": result.get(
                "requires_approval"
            ),
            "human_approved": result.get(
                "human_approved"
            ),
            "action_status": result.get(
                "action_status"
            )
        }
    }


# ============================================================
# HUMAN APPROVAL
# ============================================================

@app.post("/api/v1/approve")
def approve_action(
    request: ApprovalRequest
):

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    result = agent.invoke(
        Command(
            resume=request.approved
        ),
        config=config
    )

    return {
        "status": "COMPLETED",
        "thread_id": request.thread_id,
        "result": {
            "machine_id": result.get("machine_id"),
            "severity": result.get("severity"),
            "root_cause": result.get(
                "root_cause"
            ),
            "recommendation": result.get(
                "recommendation"
            ),
            "human_approved": result.get(
                "human_approved"
            ),
            "action_status": result.get(
                "action_status"
            )
        }
    }