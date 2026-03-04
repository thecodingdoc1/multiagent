from typing import TypedDict

class AgentState(TypedDict):
    raw_lead: str
    name: str
    phone: str
    issue: dict
    priority: str
    reasoning: str
    schecdule: str