from langchain.tools import tool
import yfinance as yf
import requests
import os

# configurations
openweathermap_api_key = os.environ['OPENWEATHERMAP_API_KEY']
openweathermap_base_url = os.environ['OPENWEATHERMAP_URL']
joke_url = os.environ['JOKE_URL']

@tool
def get_weather(city: str) -> str:
    """
    Description: used to get the real time weather information of a city.
    Arguments:
        city: the city of which weather information is required.
    Returns: JSON formatted string which contains the real time weather information of a city.
    """

    # build the final url
    url = f"{openweathermap_base_url}?appid={openweathermap_api_key}&units=metric&q={city}"
    # print(f"sending request to url: {url}")
    # print(f"fetching weather information of city = {city}")

    # send the request and get the response
    response = requests.get(url)

    # check if the response is success
    if response.status_code == 200:
        # return the response body
        return response.text
    else:
        # error while sending the request
        return f"No weather information is avaialable for {city}"

@tool
def get_stock_info(symbol: str) -> str:
    """
    Description: returns the stock information of selected symbol.
    Arguments:
        symbol: symbol whose stock information is required.
    Returns: Stock price in $ of selected stock symbol.
    """
    # get the stock info
    # stock_info = yfinance.download(symbol)
    # return stock_info

    stock = yf.Ticker(symbol)
    price = stock.info['regularMarketPrice']
    return f"current price of {symbol} is ${price}"

@tool
def tell_me_a_joke():
    """
    Description: Returns a randome joke.
    """
    # send the request
    response = requests.get(joke_url)

    # check if the response is success
    if response.status_code == 200:
        # return the response body
        return response.text
    else:
        # error while sending the request
        return f"No joke available at the moment"

@tool
def convert_currency(amount: float, to_currency: str):
    """
    Description: this function is used for currency conversion.
    Arguments:
        amount: amount to be converted
        to_currency: the conversion of a currency to this currency
    Returns: converted amount
    """
    # currency conerversion rates
    rates = {
        'USD': 1,
        'AED': 3.6725,
        'AFN': 65.131812,
        'ALL': 79.594616,
        'AMD': 364.280486,
        'ANG': 1.79,
        'AOA': 926.860561,
        'ARS': 1512.7304,
        'AUD': 1.399159,
        'AWG': 1.79,
        'AZN': 1.700179,
        'BAM': 1.686921,
        'BBD': 2,
        'BDT': 122.692712,
        'BGN': 1.686921,
        'BHD': 0.376,
        'BIF': 2993.411366,
        'BMD': 1,
        'BND': 1.273026,
        'BOB': 11.879488,
        'BRL': 5.176012,
        'BSD': 1,
        'BTN': 95.00455,
        'BWP': 13.773889,
        'BYN': 3.083177,
        'BZD': 2,
        'CAD': 1.389063,
        'CDF': 2294.595327,
        'CHF': 0.811346,
        'CLF': 0.023644,
        'CLP': 934.544536,
        'INR': 95.000907
    }

    # get the conversion rate
    conversion_rate = rates[to_currency]

    return amount * conversion_rate

# test the weather tool
# print(get_weather.invoke({'city': 'pune'}))

# test the get_stock_info tool
# print(get_stock_info.invoke({'symbol': 'AAPL'}))

# test the joke tool
# print(tell_me_a_joke.invoke({}))