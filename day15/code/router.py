from agents import Agent, Runner
from config import MODEL
from pydantic import BaseModel

# used to get structured output from the routing agent
class RoutingDecision(BaseModel):
    route: str
    confidence: float
    reason: str


# set the system prompt for the router agent
system_prompt = """
You are a healthcare navigator router. 
Your ONLY job is to classify the user's request into one of these routes 
and return a structured JSON response.

Routes:
- appointment: Booking, rescheduling, canceling, or checking appointments
- billing: Invoice questions, payment status, insurance coverage
- medical_info: General medical/health questions (what is X, explain Y)
- records: Finding reports, explaining report contents, discharge documents
- emergency: Urgent/emergency situations (chest pain, difficulty breathing, severe symptoms)
- general: All other queries which are not matching with the previous categories

EMERGENCY DETECTION RULES:
- If the user describes severe symptoms (chest pain, difficulty breathing, severe bleeding,
  allergic reactions, loss of consciousness, stroke symptoms, severe pain), ALWAYS route to emergency.
- If the user mentions wanting to harm themselves or others, route to emergency.
- When in doubt about severity, route to emergency.

Respond with ONLY a JSON object matching this schema:
{
  "route": "<route_name>",
  "confidence": <0.0 to 1.0>,
  "reason": "<brief explanation>"
}
"""

router_agent = Agent(
    name="Router",
    instructions=system_prompt,
    model=MODEL,
    output_type=RoutingDecision
)

def route_user_query(user_query: str):
    """get user query and decide the agent to execute the query"""
    result = Runner.run_sync(
        starting_agent=router_agent, 
        input=user_query)
    return result.final_output