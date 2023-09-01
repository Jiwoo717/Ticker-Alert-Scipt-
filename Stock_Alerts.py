import os
import requests
import smtplib
from bs4 import BeautifulSoup
from email.message import EmailMessage

# Fetch environment variables
API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')
EMAIL_PASSWORD = os.environ.get('ALERT_EMAIL_PASSWORD')

STOCK_SYMBOLS = ['AAPL', 'GOOGL', 'AMZN']
ALERT_THRESHOLD = 1.10  # Default 10% spike

# For TempMail
BASE_URL = "https://temp-mail.org/en/"

def get_temp_email():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the email address from the page
    email_elem = soup.find(id="mail")
    if email_elem:
        return email_elem.get("value")
    return None

EMAIL_ADDRESS = get_temp_email()

# Fetch the latest and historical stock prices
def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for HTTP errors
        return response.json()['TIME_SERIES_DAILY']
    except requests.RequestException as e:
        print(f"Failed to fetch data for {symbol}. Error: {e}")
        return None

# Send an email alert
def send_email(subject, content):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

# Main logic
def monitor_stocks():
    for symbol in STOCK_SYMBOLS:
        prices = get_stock_price(symbol)
        if not prices:
            continue

        latest_date = list(prices.keys())[0]
        previous_date = list(prices.keys())[1]

        latest_close = float(prices[latest_date]['4. close'])
        previous_close = float(prices[previous_date]['4. close'])

        if latest_close > ALERT_THRESHOLD * previous_close:
            send_email(
                f"Alert for {symbol}", 
                f"{symbol} has spiked by more than {(ALERT_THRESHOLD - 1) * 100}%!"
            )

if __name__ == '__main__':
    monitor_stocks()
