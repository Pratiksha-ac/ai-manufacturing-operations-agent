# ============================================================
# MANUFACTURING DECISION ENGINE
# ============================================================


def evaluate_decision(severity: str):

    severity = severity.upper().strip()

    # --------------------------------------------------------
    # NORMAL
    # --------------------------------------------------------

    if severity == "NORMAL":

        return {
            "requires_approval": False,
            "decision": "NO_ACTION",
            "action": None
        }

    # --------------------------------------------------------
    # WARNING
    # --------------------------------------------------------

    elif severity == "WARNING":

        return {
            "requires_approval": False,
            "decision": "MONITOR",
            "action": None
        }

    # --------------------------------------------------------
    # HIGH
    # --------------------------------------------------------

    elif severity == "HIGH":

        return {
            "requires_approval": True,
            "decision": "HUMAN_REVIEW",
            "action": "SHUTDOWN"
        }

    # --------------------------------------------------------
    # CRITICAL
    # --------------------------------------------------------

    elif severity == "CRITICAL":

        return {
            "requires_approval": True,
            "decision": "HUMAN_REVIEW",
            "action": "SHUTDOWN"
        }

    # --------------------------------------------------------
    # UNKNOWN SEVERITY
    # --------------------------------------------------------

    else:

        return {
            "requires_approval": True,
            "decision": "HUMAN_REVIEW",
            "action": None
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    severities = [
        "NORMAL",
        "WARNING",
        "HIGH",
        "CRITICAL"
    ]

    print("\nMANUFACTURING DECISION ENGINE")
    print("=" * 60)

    for severity in severities:

        result = evaluate_decision(severity)

        print(f"\nSeverity: {severity}")
        print(f"Decision: {result['decision']}")
        print(
            f"Requires Approval: "
            f"{result['requires_approval']}"
        )
        print(f"Action: {result['action']}")

    print("\n" + "=" * 60)