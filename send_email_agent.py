import agentstate
import logging

def send_email_node(state: agentstate.AgentState):
    # In a real implementation, you would integrate with an email service here.
    # For this example, we'll just print the email contents to the console.
    name = state.get('name', 'Unknown')
    phone = state.get('phone', 'Unknown')
    issue = state.get('issue', {})
    priority = state.get('priority', 'Unknown')
    schedule = state.get('schedule', 'Unknown')

    
    # construct the email content to be sent to a customer
    email_content = f"""Subject: Service Request for {name} - Priority: {priority}

        Hi {name},

        We have received your service request regarding the following issue: {issue.get('problem', 'No problem details provided')} at {issue.get('location', 'No location provided')}.
        Based on our evaluation, we have assigned a priority level of {priority} to your request. We are scheduling a service appointment for {schedule}.
        If you have any questions or need to reschedule, please contact us at 314-257-0000.

        Best regards,
        Customer Service Team
        """

    logging.info(f"Email content prepared for {name} with priority {priority}.")
    return {"email_content": email_content}
