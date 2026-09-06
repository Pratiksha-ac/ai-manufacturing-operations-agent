from langchain_core.tools import tool


@tool
def shutdown_machine(machine_id: str):
    """
    Simulate shutting down a manufacturing machine.

    This is a safe demo action. It does not control
    any real machine or industrial equipment.
    """

    print("\n")
    print("=" * 60)
    print("SIMULATED MACHINE ACTION")
    print("=" * 60)

    print(f"Machine: {machine_id}")
    print("Action: SHUTDOWN")
    print("Status: SUCCESS")

    print("=" * 60)

    return {
        "machine_id": machine_id,
        "action": "SHUTDOWN",
        "status": "SUCCESS"
    }


@tool
def restart_machine(machine_id: str):
    """
    Simulate restarting a manufacturing machine.

    This is a safe demo action. It does not control
    any real machine or industrial equipment.
    """

    print("\n")
    print("=" * 60)
    print("SIMULATED MACHINE ACTION")
    print("=" * 60)

    print(f"Machine: {machine_id}")
    print("Action: RESTART")
    print("Status: SUCCESS")

    print("=" * 60)

    return {
        "machine_id": machine_id,
        "action": "RESTART",
        "status": "SUCCESS"
    }


if __name__ == "__main__":

    result = shutdown_machine.invoke({
        "machine_id": "CNC-04"
    })

    print("\nReturned result:")
    print(result)