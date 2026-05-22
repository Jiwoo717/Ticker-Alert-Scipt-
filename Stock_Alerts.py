import os
import smtplib
import requests
from email.message import EmailMessage

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
EMAIL_USER = os.getenv("ALERT_EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("ALERT_EMAIL_PASSWORD")
EMAIL_TO = os.getenv("ALERT_EMAIL_TO", EMAIL_USER)

WATCHLIST = ["AAPL", "GOOGL", "AMZN"]
SPIKE_THRESHOLD = 0.10


def fetch_daily_prices(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "apikey": API_KEY,
    }

    try:
        res = requests.get(url, params=params, timeout=15)
        res.raise_for_status()
        data = res.json()
    except requests.RequestException as err:
        print(f"{symbol}: request failed - {err}")
        return None

    if "Time Series (Daily)" not in data:
        print(f"{symbol}: unexpected response from Alpha Vantage")
        print(data)
        return None

    return data["Time Series (Daily)"]


def send_alert(symbol, percent_change, latest_close, previous_close):
    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("Email credentials are missing.")
        return

    msg = EmailMessage()
    msg["Subject"] = f"{symbol} price alert"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    msg.set_content(
        f"{symbol} moved up {percent_change:.2f}%.\n\n"
        f"Previous close: ${previous_close:.2f}\n"
        f"Latest close: ${latest_close:.2f}"
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"{symbol}: alert sent")

    except smtplib.SMTPException as err:
        print(f"{symbol}: email failed - {err}")


def check_symbol(symbol):
    prices = fetch_daily_prices(symbol)

    if not prices:
        return

    dates = list(prices.keys())

    if len(dates) < 2:
        print(f"{symbol}: not enough price history")
        return

    latest = dates[0]
    previous = dates[1]

    latest_close = float(prices[latest]["4. close"])
    previous_close = float(prices[previous]["4. close"])

    percent_change = (latest_close - previous_close) / previous_close

    print(f"{symbol}: {percent_change * 100:.2f}%")

    if percent_change >= SPIKE_THRESHOLD:
        send_alert(
            symbol=symbol,
            percent_change=percent_change * 100,
            latest_close=latest_close,
            previous_close=previous_close,
        )


def main():
    if not API_KEY:
        print("Missing ALPHA_VANTAGE_API_KEY.")
        return

    for symbol in WATCHLIST:
        check_symbol(symbol)


if __name__ == "__main__":
    main()
