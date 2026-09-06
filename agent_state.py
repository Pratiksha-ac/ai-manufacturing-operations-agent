from typing import TypedDict


class ManufacturingState(TypedDict, total=False):

    machine_id: str

    temperature: float
    vibration: float
    pressure: float
    rpm: float
    energy_consumption: float

    anomaly: bool

    machine_history: list

    root_cause: str
    severity: str
    recommendation: str

    requires_approval: bool
    human_approved: bool
    action_status: str