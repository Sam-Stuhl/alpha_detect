# Alpha Detect - A Backtesting Engine for Simple Trading Strategies

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Overview
Alpha Detect is a Python tool that lets you define simple rule-based strategies (like moving average crossovers, RSI oversold signals, etc.), runs backtests on historical market data, and generates performance reports.

## Features
### Command Line Interface
- Alpha Detect has a built in CLI which allows the user to choose the strategy they'd like to back test on, the stock to be tested, the time period to test during, and specific information to each strategy (i.e. buy and sell thresholds)
### Strategies
- Price Threshold
    - Buy shares when stock price drops below specified threshold, and sell shares when it rises above specified threshold
    - Example: AMD stock with buy threshold set to \$110, sell threshold set to \$145, over a 5 year time period
    ![Price Threshold Example](https://github.com/user-attachments/assets/c468b48d-a69f-4005-a7f2-631e850c8dc0)
- RSI Threshold
    - Buy shares when the Relative Strength Index (RSI) of the stock drops below specified threshold, and sell shares when it rises above specified threshold
    - Example: AMD stock with buy threshold set to 30 (RSI), sell threshold set to 70 (RSI), over a 5 year time period
    ![RSI Threshold Example](https://github.com/user-attachments/assets/6fd03412-b4de-4374-9de6-b5f8c34c2d05)
- SMA Crossover
    - Buy shares when the short Simple Moving Average (SMA) crosses over the long SMA. The SMA is calculated from specified time periods
    - Example: AMD stock with short SMA set to 10 days, long SMA set to 50 days, over a 5 year time period
    ![SMA Threshold Example](https://github.com/user-attachments/assets/b685da0f-a36d-4198-a825-ea499fec9211)

## Prerequisites
- Python 3.9+
- pip

## Installation
#### Run:
```bash
git clone https://github.com/Sam-Stuhl/alpha_detect.git
cd alpha_detect
pip install -r requirements.txt
```

## Usage
After installing dependencies, run the tool with:
```bash
python main.py
```
Follow the CLI prompts to:
- Select a strategy
- Choose a stock ticker (e.g. AAPL, MSFT, etc.)
- Set the capital that the back tester will begin with (default \$1000)
- Choose a time period (e.g. 1Y, 5Y, etc.)
- Enter any strategy-specific parameters (e.g. RSI thresholds, SMA window size)

Example:
```text
(1) Price Threshold
(2) RSI Threshold
(3) SMA Crossover
Choose a Strategy: 1

Enter the stock symbol you would like to test on: AMD

Enter starting capital (enter for $1000): 1000

(1) 1W
(2) 1M
(3) 3M
(4) 6M
(5) 1Y
(6) 5Y
Choose a time period to backtest: 6

Enter the price to buy AMD at: 110
Enter the price to sell AMD at: 145
```
See above example for the plotted report.

## Future Improvements
- Add support for exponential moving averages (EMA)
- Add portfolio simulation (multi-stock)
- Possible add a web-based frontend

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

Feel free to fork the repo and make your own strategy extensions.

## License
This project is licensed under the MIT License.