from langchain.tools import tool
from datetime import datetime
import requests

@tool
def get_current_time() -> str:
    """
    Description: returns the current time of machine
    """
    # print("- get_current_time is called")
    return datetime.now().strftime("%Y-%m-%d %H:%M%S")

@tool
def get_daily_quote() -> str:
    """
    Description: return quote of the day
    """
    # print("- get_daily_quote called")

    # send the request
    response = requests.get('https://zenquotes.io/api/random')

    # check if the resopnse is success
    if response.status_code == 200:

        # read the result in JSON format
        result = response.json()

        # return the quote from result
        return result[0]['q']

    else:
        return "error while getting a quote"
