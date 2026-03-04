from intakeagent import intake_node
from qualificationagent import qualification_node
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

workflow = StateGraph(agentstate.AgentState)

def route_by_priority(state: agentstate.AgentState):
    priority = state.get('priority')
    
    if (priority is not None):
        if (priority == 'High'):
            return "urgent_drafting_node"
        elif (priority == 'Medium' or priority == 'Low'):
            return "standard_drafting_node"
    
    return "redo_priority"



def main():
    workflow.add_node("intake", intake_node)
    workflow.add_node("qualify", qualification_node)
    workflow.add_edge(START, "intake")
    workflow.add_edge("intake", "qualify")
    workflow.add_conditional_edges("qualify", route_by_priority)
    memory = MemorySaver()
    workflow.add_node("send_email", send_email_node)
    app = workflow.compile(checkpointer=memory, interrupt_before=["send_email"])