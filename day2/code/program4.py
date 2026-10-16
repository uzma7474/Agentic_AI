from langchain_core.tools import BaseTool

# create a custom tool class
class GetWeather(BaseTool):
    # set the metadata
    name: str = "get_weather"
    description: str = "this tool is used to get a weather information of a city"

    # overide the _run method
    def _run(self, city: str) -> str:
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

# instantiate the tool class to create a tool object
get_weather_tool = GetWeather()

# invoke the tool and get the result
print(get_weather_tool.invoke(input={'city': 'pune'}))
#print(get_weather_tool.description)