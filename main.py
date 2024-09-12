import requests
import datetime
from twilio.rest import Client

account_sid = ""  #Can be found in twilio
auth_token = ""  #Can be found in twilio
twilio_number = ""  #make your own number through twilio
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = ""
YESTERDAY_DATE = ""
DAY_BEFORE_YESTERDAY_DATE = ""
YESTERDAY_CLOSING = ""
DAY_BEFORE_YESTERDAY_CLOSING = ""

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY
}

response = requests.get("https://www.alphavantage.co/query", parameters)
response_data = response.json()


# print(data["Time Series (Daily)"]["2024-09-11"]["4. close"])
# close_value = data.get("Time Series (Daily)", {}).get("2024-09-11", {}).get("4. close", None)
# print(close_value)


def closing_data_prices(data):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    day_before_yesterday = today - datetime.timedelta(days=2)
    global YESTERDAY_DATE, DAY_BEFORE_YESTERDAY_DATE
    YESTERDAY_DATE = yesterday.strftime('%Y-%m-%d')
    DAY_BEFORE_YESTERDAY_DATE = day_before_yesterday.strftime('%Y-%m-%d')

    yesterday_closing = data.get("Time Series (Daily)", {}).get(f"{YESTERDAY_DATE}", {}).get("4. close", None)
    day_before_yesterday_closing = data.get("Time Series (Daily)", {}).get(f"{DAY_BEFORE_YESTERDAY_DATE}", {}).get(
        "4. close", None)

    # print(f"{YESTERDAY_DATE} : {yesterday_closing}")
    # print(f"{DAY_BEFORE_YESTERDAY_DATE} : {day_before_yesterday_closing}")
    global YESTERDAY_CLOSING, DAY_BEFORE_YESTERDAY_CLOSING
    YESTERDAY_CLOSING = 250.57
    DAY_BEFORE_YESTERDAY_CLOSING = 210.10


closing_data_prices(response_data)


#-------------------------------------PERCENTAGE FORMULA-----------------------------------------#

def get_change(current: float, previous: float) -> float:
    if current == previous:
        return 0.0  # No change
    try:
        return ((current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0.0


change = get_change(YESTERDAY_CLOSING, DAY_BEFORE_YESTERDAY_CLOSING)


#-------------------------NEWS FETCH---------------------------------------------------------------#

def get_news(changes):
    news_parameters = {
        "function": "NEWS_SENTIMENT",
        "tickers": STOCK,
        "time_from": DAY_BEFORE_YESTERDAY_DATE + "T0000",
        "time_to": YESTERDAY_DATE + "T2359",
        "limit": 1,
        "apikey": API_KEY
    }

    news_response = requests.get("https://www.alphavantage.co/query", params=news_parameters)
    news_data = news_response.json()
    # Extract and print titles and summaries
    articles = news_data.get("feed", [])
    for article in articles:
        title = article.get("title", "No Title")
        summary = article.get("summary", "No Summary")
        if changes >= 5:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f"{STOCK}: 🔺{changes}%\nHEADLINE: {title}\nBRIEF: {summary}",
                from_=twilio_number,
                to="+8801722382459656",
            )
            print(message.status)
        elif changes < -5:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f"{STOCK}: 🔻{changes}%\nHEADLINE: {title}\nBRIEF: {summary}",
                from_=twilio_number,
                to="+880172238245972",
            )
            print(message.status)


if change >= 5:
    get_news(change)
elif change < -5:
    get_news(change)
