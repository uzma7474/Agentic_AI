import config
import logging
from router import route_user_query

from specialists.emergency import run_emergency_agent
from specialists.appointment import run_appointment_agent
from specialists.billng import run_billng_agent
from specialists.medial_info import run_medical_info_agent
from specialists.records import run_records_agent

from rich.console import Console
from rich.markdown import Markdown

logger = logging.getLogger(__name__)

console = Console()

while True:
    # get user input
    user_input = input("> ")
    if user_input.lower() in ['exit', 'quit']:
        break

    # check which agent is required to execute the user's query
    result = route_user_query(user_input)
    logger.info(f"result = {result}")

    final_result = None

    # based on the selection, route the request to the required agent
    if result.route == 'emergency':
        final_result = run_emergency_agent(user_input)
    elif result.route == 'appointment':
        final_result = run_appointment_agent(user_input)
    elif result.route == 'billing':
        final_result = run_billng_agent(user_input)
    elif result.route == 'medical_info':
        final_result = run_medical_info_agent(user_input)
    elif result.route == 'records':
        final_result = run_records_agent(user_input)
    elif result.route == 'general':
        console.print(f"[Router]> Sorry, none of the existing agents can answer your question, please try different question.")

    if final_result is not None:
        console.print(Markdown(final_result))

    console.print('')


