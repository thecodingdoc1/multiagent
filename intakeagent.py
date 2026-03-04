from logging import log

import agentstate
from ppdantic import BaseModel, Field

class IntakeIssue(BaseModel):
    location: str = Field(description="The extracted issue location from the raw lead")
    problem: str = Field(description="The extracted issue problem from the raw lead")

class IntakeOutput(BaseModel):
    name: str = Field(description="The extracted name from the raw lead")
    phone: str = Field(description="The extracted phone number from the raw lead")
    issue: IntakeIssue = Field(description="The extracted issue details from the raw lead")
   
    
    
    
def intake_node(state: agentstate.AgentState, llm) -> dict:
    new_count = state.get('count', 0) + 1
    raw_lead = state['raw_lead']
    structured_llm = llm.with_structured_output(IntakeOutput)
    try:
        result = structured_llm.invoke(f"Extract information from raw lead: {raw_lead}")
    except Exception as e:
        log.error(f"Error during LLM invocation: {e}")
        if (new_count > 3):
            return {
                'error_flag': "fatal"
            }
        else:
            return {
                'error_flag': "retry",
                'count': new_count
            }
    
    if (result.issue.problem == "" or result.issue.location == ""):    
        if (new_count > 3):
            return {
                'error_flag': "fatal"
            }
        else:
            return {
                'error_flag': "retry",
                'count': new_count
            }
    return {
        'name': result.name,
        'phone': result.phone,
        'issue': result.issue.dict()
    }
