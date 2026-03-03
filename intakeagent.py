import agentstate
from ppdantic import BaseModel, Field

class IntakeIssue(BaseModel):
    location: str = Field(description="The extracted issue location from the raw lead")
    problem: str = Field(description="The extracted issue problem from the raw lead")

class IntakeOutput(BaseModel):
    name: str = Field(description="The extracted name from the raw lead")
    phone: str = Field(description="The extracted phone number from the raw lead")
    issue: IntakeIssue = Field(description="The extracted issue details from the raw lead")
   
    
    
    
def intakeagent(state: agentstate.AgentState, llm) -> dict:
    
    raw_lead = state['raw_lead']
    structured_llm = llm.with_structured_output(IntakeOutput)
    result = structured_llm.invoke(f"Extract information from raw lead: {raw_lead}")
    return {
        'name': result.name,
        'phone': result.phone,
        'issue': result.issue.dict()
    }
