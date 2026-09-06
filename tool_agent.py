from langchain.agents import create_agent

from llm import get_llm
from agent_tools import get_machine_history


# ============================================================
# BUILD TOOL-USING MANUFACTURING AGENT
# ============================================================

def build_tool_agent():

    llm = get_llm()

    tools = [
        get_machine_history
    ]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""
You are an AI Manufacturing Operations Engineer.

Your job is to investigate manufacturing machines
using available telemetry and tools.

When you need historical telemetry for a machine,
use the get_machine_history tool.

Analyze the machine carefully.

Your final answer MUST be valid JSON.

Return exactly this structure:

{
    "root_cause": "explanation of the likely root cause",
    "severity": "NORMAL, WARNING, HIGH, or CRITICAL",
    "recommendation": "recommended operational action"
}

Rules:

- Return ONLY valid JSON.
- Do not use Markdown.
- Do not use ```json.
- Do not add explanations outside the JSON.
- Do not invent sensor values.
- Base your analysis only on the available telemetry.
- If the evidence is insufficient, clearly say so.
"""
    )

    return agent


# ============================================================
# TEST THE TOOL-USING AGENT
# ============================================================

if __name__ == "__main__":

    agent = build_tool_agent()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": """
Investigate manufacturing machine CNC-04.

Use the get_machine_history tool to retrieve
the recent telemetry history for CNC-04.

Then determine:

1. What is happening
2. Likely root cause
3. Severity
4. Recommended action

Return the final result using the required JSON format.
"""
                }
            ]
        }
    )

    print("\n")
    print("=" * 70)
    print("TOOL-USING MANUFACTURING AGENT")
    print("=" * 70)

    print("\nAgent Messages:")

    for message in result["messages"]:

        print(f"\n[{message.type}]")

        if message.content:
            print(message.content)

    print("\n")
    print("=" * 70)
    print("FINAL AI RESPONSE")
    print("=" * 70)

    final_message = result["messages"][-1]

    print(final_message.content)

    print("=" * 70)