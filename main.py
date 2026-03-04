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
    config = {"configurable": {"thread-id": "12345"}}
    final_state = app.invoke({"raw_lead": "Hello, my name is John Doe. I have a leaking faucet in the kitchen. Please help! My phone number is 555-1234."
    }, config=config)
    print(final_state)
    app.invoke(None, config=config) # This will trigger the send_email_node since we set it to interrupt before.

if __name__ == "__main__":    
    main()