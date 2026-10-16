from agent_framework import Agent

def check_budget(total: float, budget: float):
    """Compare the total budget against the user's budget"""
    remaining_amount = budget - total

    if remaining_amount > 0:
        return {
            "status": "ok",
            "total": total,
            "budget": budget,
            "remaining": remaining_amount,
            "message": f"{remaining_amount} INR is under the required budget"
        }
    else:
        return {
            "status": "over",
            "total": total,
            "budget": budget,
            "remaining": remaining_amount,
            "message": f"budget is over by {remaining_amount} INR"
        }

def create_budget_agent(client):
    """Creates a budget agent to prepare to budget for a trip"""
    return Agent(
        name="Budget-Agent",
        client=client,
        instructions=(
            "You track trip costs in INR. Calculate total to sum line items, "
            "passing a list of objects each with exactly two keys: "
            '{"category": "<flights|hotels|activities|transport>", "amount": <number>}. '
            "If the result includes unparsed_items, fix those objects and call it again. "
            "Then use check_budget to compare against the user's budget. "
            "Always report the status (OK or OVER) and remaining amount. "
            "You do NOT search flights, hotels, or activities."
        ),
        tools=[check_budget]
    )