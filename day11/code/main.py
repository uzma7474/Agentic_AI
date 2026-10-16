import logging
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s - %(message)s"
)

# load the configurations from .env file
load_dotenv()

# create the application graph
from graph import create_graph
app = create_graph()

while True:

    # plan family trip to Goa for 3 days from 15 nov to 18 nov from pune under budget of 50000 Rs.
    # get the input from user
    user_input = input("> ")
    if user_input in ['exit', 'quit']:
        break

    # create a state
    state = {"user_request": user_input}
    
    response = app.invoke(state)
    console.print(Markdown(response['final_result']))
    print()