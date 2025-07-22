# Alpha Detect - A Backtesting Engine for SImple Trading Strategies

## Overview
AlphaDetect is a Python tool that lets you define simple rule-based strategies (like moving average crossovers, RSI oversold signals, etc.), runs backtests on historical market data, and generates performance reports (returns, Sharpe ratio, drawdown, etc.). The tool can later be extended to use live data or paper trade.

## Core Features
| Feature                               | Description                                                                |
| ------------------------------------- | -------------------------------------------------------------------------- |
| **Strategy Engine**                   | Define basic strategies using rules (e.g., `buy if SMA(20) > SMA(50)`)     |
| **Backtester**                        | Run historical simulations over data using your strategy                   |
| **Performance Analytics**             | Output stats like CAGR, max drawdown, Sharpe ratio, win/loss ratio         |
| **Plotting Module**                   | Generate equity curve and buy/sell markers on price chart using Matplotlib |
| **Data Loader**                       | Use yfinance or Alpaca to get OHLCV data for stocks, ETFs, or crypto       |
| *(Optional)* **Portfolio Simulation** | Simulate trades with slippage and fees across multiple assets              |
