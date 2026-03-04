from typing import Literal
import agentstate
from pydantic import BaseModel, Field

class QualificationOutput(BaseModel):
    priority: Literal["High", "Medium", "Low"] = Field(description="The priority of the submitted request")
    reasoning: str = Field(description="chain of thought thinking that was performed to come up with priority")

def qualification_node(state: agentstate.AgentState):
    issue_data = state["issue"]
    structured_llm = llm.with_structured_output(QualificationOutput)
    result = structured_llm.invoke(f"Evaluate this issue: {issue_data}. High = active leaks/structural. Medium = appliance failure. Low = aesthetic. Assign a priority and explain your reasoning.")
    return {
        'priority': result.priority,
        'reasoning': result.reasoning
    }
