import json

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

from agent_state import ManufacturingState
from ml_detector import detect_anomalies
from tool_agent import build_tool_agent
from action_tools import shutdown_machine
from decision import evaluate_decision


# ============================================================
# NODE 1: ML ANOMALY DETECTION
# ============================================================

def detect_machine_anomaly(state):

    print("\nRunning ML anomaly detection...")

    results = detect_anomalies()

    machine_id = state["machine_id"]

    machine_results = results[
        results["machine_id"] == machine_id
    ]

    if machine_results.empty:

        print(f"Machine {machine_id} not found.")

        state["anomaly"] = False

        return state

    latest_reading = machine_results.iloc[-1]

    state["temperature"] = float(
        latest_reading["temperature"]
    )

    state["vibration"] = float(
        latest_reading["vibration"]
    )

    state["pressure"] = float(
        latest_reading["pressure"]
    )

    state["rpm"] = float(
        latest_reading["rpm"]
    )

    state["energy_consumption"] = float(
        latest_reading["energy_consumption"]
    )

    state["anomaly"] = bool(
    latest_reading["anomaly"] == -1
)

    print(f"Machine: {machine_id}")
    print(
        f"Temperature: "
        f"{state['temperature']:.2f}"
    )
    print(
        f"Vibration: "
        f"{state['vibration']:.2f}"
    )
    print(
        f"Pressure: "
        f"{state['pressure']:.2f}"
    )
    print(
        f"RPM: "
        f"{state['rpm']:.2f}"
    )
    print(
        f"Energy: "
        f"{state['energy_consumption']:.2f}"
    )
    print(
        f"Anomaly detected: "
        f"{state['anomaly']}"
    )

    return state


# ============================================================
# ROUTER 1
# ============================================================

def route_after_detection(state):

    if state.get("anomaly", False):

        print(
            "\nAnomaly detected "
            "→ sending to AI agent"
        )

        return "investigate_machine"

    print(
        "\nNo anomaly detected "
        "→ normal result"
    )

    return "normal_result"


# ============================================================
# NODE 2: AI INVESTIGATION
# ============================================================

def investigate_machine(state):

    print(
        "\nAI Manufacturing Agent "
        "investigating..."
    )

    agent = build_tool_agent()

    machine_id = state["machine_id"]

    prompt = f"""
Investigate manufacturing machine {machine_id}.

Latest machine telemetry:

Temperature: {state["temperature"]}
Vibration: {state["vibration"]}
Pressure: {state["pressure"]}
RPM: {state["rpm"]}
Energy Consumption: {state["energy_consumption"]}

Use the get_machine_history tool to retrieve
recent telemetry history for this machine.

Analyze the machine condition.

Determine:

1. What is happening
2. Likely root cause
3. Severity
4. Recommended action

Return ONLY valid JSON:

{{
    "root_cause": "...",
    "severity": "...",
    "recommendation": "..."
}}

Severity must be one of:

NORMAL
WARNING
HIGH
CRITICAL

Do not invent sensor values.
Base your analysis only on available telemetry.
"""

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    final_message = result["messages"][-1]

    ai_response = final_message.content

    print("\nAI Agent Final Response:")
    print("=" * 70)
    print(ai_response)
    print("=" * 70)

    try:

        cleaned_response = ai_response.strip()

        if cleaned_response.startswith("```"):

            lines = cleaned_response.splitlines()

            lines = lines[1:]

            if (
                lines
                and lines[-1].strip() == "```"
            ):
                lines = lines[:-1]

            cleaned_response = "\n".join(lines)

        result_json = json.loads(
            cleaned_response
        )

        state["root_cause"] = result_json.get(
            "root_cause",
            "Unable to determine root cause"
        )

        state["severity"] = result_json.get(
            "severity",
            "WARNING"
        ).upper()

        state["recommendation"] = result_json.get(
            "recommendation",
            "Perform manual inspection"
        )

    except json.JSONDecodeError:

        print(
            "\nWARNING: AI returned invalid JSON."
        )

        state["root_cause"] = (
            "Unable to determine root cause"
        )

        state["severity"] = "WARNING"

        state["recommendation"] = (
            "Perform manual inspection"
        )

    return state


# ============================================================
# NODE 3: DECISION ENGINE
# ============================================================

def make_decision(state):

    print("\n")
    print("=" * 70)
    print("MANUFACTURING DECISION ENGINE")
    print("=" * 70)

    severity = state.get(
        "severity",
        "WARNING"
    )

    decision = evaluate_decision(
        severity
    )

    state["requires_approval"] = (
        decision["requires_approval"]
    )

    print(
        f"Severity: {severity}"
    )

    print(
        f"Decision: {decision['decision']}"
    )

    print(
        f"Requires Approval: "
        f"{decision['requires_approval']}"
    )

    print(
        f"Action: {decision['action']}"
    )

    print("=" * 70)

    return state


# ============================================================
# ROUTER 2
# ============================================================

def route_after_decision(state):

    if state.get(
        "requires_approval",
        False
    ):

        return "human_approval"

    return "normal_result"


# ============================================================
# NODE 4: HUMAN APPROVAL
# ============================================================

def human_approval(state):

    print("\n")
    print("=" * 70)
    print("HUMAN APPROVAL REQUIRED")
    print("=" * 70)

    approval_request = {
        "machine_id": state["machine_id"],
        "severity": state["severity"],
        "root_cause": state["root_cause"],
        "recommendation": state["recommendation"]
    }

    print(
        "\nWorkflow paused."
    )

    print(
        "Waiting for human approval..."
    )

    # ========================================================
    # PAUSE GRAPH
    # ========================================================

    approval = interrupt(
        approval_request
    )

    # ========================================================
    # GRAPH RESUMES HERE
    # ========================================================

    approved = (
        approval is True
        or approval == "yes"
    )

    if approved:

        state["human_approved"] = True

        state["action_status"] = "APPROVED"

        print(
            "\nHuman approved the action."
        )

    else:

        state["human_approved"] = False

        state["action_status"] = "REJECTED"

        print(
            "\nHuman rejected the action."
        )

    return state


# ============================================================
# ROUTER 3
# ============================================================

def route_after_approval(state):

    if state.get(
        "human_approved",
        False
    ):

        return "execute_action"

    return "end"


# ============================================================
# NODE 5: EXECUTE ACTION
# ============================================================

def execute_action(state):

    print("\n")
    print("=" * 70)
    print("EXECUTING APPROVED ACTION")
    print("=" * 70)

    machine_id = state["machine_id"]

    result = shutdown_machine.invoke(
        {
            "machine_id": machine_id
        }
    )

    state["action_status"] = result["status"]

    print(
        "\nAction completed successfully."
    )

    return state


# ============================================================
# NODE 6: NORMAL RESULT
# ============================================================

def normal_result(state):

    state["root_cause"] = (
        "No abnormal condition detected"
    )

    state["severity"] = "NORMAL"

    state["recommendation"] = (
        "Continue normal operation"
    )

    state["requires_approval"] = False

    state["human_approved"] = False

    state["action_status"] = (
        "NO_ACTION_REQUIRED"
    )

    print(
        "\nMachine operating normally."
    )

    return state


# ============================================================
# BUILD GRAPH
# ============================================================

def build_graph():

    graph = StateGraph(
        ManufacturingState
    )

    # --------------------------------------------------------
    # Nodes
    # --------------------------------------------------------

    graph.add_node(
        "detect_machine_anomaly",
        detect_machine_anomaly
    )

    graph.add_node(
        "investigate_machine",
        investigate_machine
    )

    graph.add_node(
        "make_decision",
        make_decision
    )

    graph.add_node(
        "human_approval",
        human_approval
    )

    graph.add_node(
        "execute_action",
        execute_action
    )

    graph.add_node(
        "normal_result",
        normal_result
    )

    # --------------------------------------------------------
    # START → ML
    # --------------------------------------------------------

    graph.add_edge(
        START,
        "detect_machine_anomaly"
    )

    # --------------------------------------------------------
    # ML → AI / NORMAL
    # --------------------------------------------------------

    graph.add_conditional_edges(
        "detect_machine_anomaly",
        route_after_detection,
        {
            "investigate_machine":
                "investigate_machine",

            "normal_result":
                "normal_result"
        }
    )

    # --------------------------------------------------------
    # AI → DECISION
    # --------------------------------------------------------

    graph.add_edge(
        "investigate_machine",
        "make_decision"
    )

    # --------------------------------------------------------
    # DECISION → HUMAN / NORMAL
    # --------------------------------------------------------

    graph.add_conditional_edges(
        "make_decision",
        route_after_decision,
        {
            "human_approval":
                "human_approval",

            "normal_result":
                "normal_result"
        }
    )

    # --------------------------------------------------------
    # HUMAN → ACTION / END
    # --------------------------------------------------------

    graph.add_conditional_edges(
        "human_approval",
        route_after_approval,
        {
            "execute_action":
                "execute_action",

            "end":
                END
        }
    )

    # --------------------------------------------------------
    # ACTION → END
    # --------------------------------------------------------

    graph.add_edge(
        "execute_action",
        END
    )

    # --------------------------------------------------------
    # NORMAL → END
    # --------------------------------------------------------

    graph.add_edge(
        "normal_result",
        END
    )

    # --------------------------------------------------------
    # CHECKPOINTER
    # --------------------------------------------------------

    memory = MemorySaver()

    return graph.compile(
        checkpointer=memory
    )


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    agent = build_graph()

    initial_state: ManufacturingState = {
        "machine_id": "CNC-04"
    }

    config = {
        "configurable": {
            "thread_id": "CNC-04-test"
        }
    }

    result = agent.invoke(
        initial_state,
        config=config
    )

    print("\n")
    print("=" * 70)
    print("GRAPH EXECUTION RESULT")
    print("=" * 70)

    print(result)

    print("=" * 70)