from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """
    Description: this function is used to get weather information for a city.

    Arguments:
        param1 (city): city name for which the weather information is required.

    Returns: Weather information of a selected if available.
    """

    # temperature data
    data = {
        'pune': 'rainy with 22c temperature',
        'mumbai': 'rainy with 18c temperature',
        'delhi': 'cloudy with 6c temperature'
    }

    # get the city weather
    if city.lower() in data:
        return data[city.lower()]

    # city does not exist
    return f'weather information in {city} does not exist'

# note: since get_weather is a tool, it can not be called directly
# print(get_weather('karad'))

# get the metadata of a tool
print(get_weather)

# invoke or execute the tool
print(get_weather.invoke({'city': 'pune'}))
    