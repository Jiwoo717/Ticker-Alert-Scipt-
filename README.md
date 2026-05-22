# Ticker-Alert-Scipt-

Designed monitor stock price movements and fire alerts through email. Structurally it searches specified tickers, looks out for significant prices spikes (the percentage spike can be changed), at which point alerts me through email.

## Features

- **Stock Monitoring**: Monitors a predefined list of stock tickers for price spikes.
- **Email Alerts**: Sends alerts to a specified email address when a stock spikes beyond a predefined threshold.
- **Temporary Mail Integration**: Incorporates the use of temporary mail services to send out alerts without needing personal email credentials.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages: `requests`, `smtplib`

### Installation

1. Clone this repository:
```bash
git clone [repository-link]
