# Ticker-Alert-Scipt-
Designed monitor stock price movements and fire alerts through email. Searches specified tickers thru alphavantage, looks out for significant prices spikes (the percentage spike can be changed), at which point alerts me through email.


## Features
- **Stock Monitoring**: Monitors a predefined list of stock tickers for price spikes on alphavantage
- **Email Alerts**: Sends alerts to a specified email address when a stock spikes beyond a predefined threshold.
- **Temporary Mail Integration**: Incorporates the use of temporary mail services to send out alerts without needing personal email credentials.


### Prerequisites
- Python 3.x
- Required Python packages: `requests`, `smtplib`

### Installation 
If you found this useful, try it on your local computer.
1. Clone this repository:
```bash
git clone 
