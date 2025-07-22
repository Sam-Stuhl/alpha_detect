from .strategy import Strategy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PriceThreshold(Strategy):
    
    # Stative variables
    time_periods = [
            '1W',
            '1M',
            '3M',
            '6M',
            '1Y',
            '5Y',
        ]
    
    name = "Price Threshold"
    
    def __init__(self, ticker: str, capital: float, time_period: str, buy_price: int = None, sell_price: int = None):
        super().__init__("Price Threshold", ticker, capital, time_period)
            
        self.buy_threshold, self.sell_threshold = self.get_buy_and_sell_thresholds() if not(buy_price and sell_price) else (buy_price, sell_price)
            
        self.back_test()
        
    def get_buy_and_sell_thresholds(self) -> tuple[float, float]:
        
        while True:
            buy_threshold = float(input(f'\nEnter the price to buy {self.ticker} at: '))
            sell_threshold = float(input(f'Enter the price to sell {self.ticker} at: '))
            
            if buy_threshold > self.capital:
                print(f"The buy price cannot be greater than the starting capital. Either enter a lower buy price or restart.")
            elif buy_threshold > sell_threshold:
                print(f"The buy price cannot be greater than the sell price. Try again.")
            else:
                break
        
        return (buy_threshold, sell_threshold)

    def back_test(self) -> None:
        trade_history_df = pd.DataFrame(columns=['date', 'action', 'shares', 'price_per_share', 'total_price', 'total_val', 'trade_index'])
        trade_history_df.loc[len(trade_history_df)] = [self.ticker_data_df['Date'][0], 'START', np.nan, np.nan, np.nan, self.capital, np.nan] # Add starting capital
        
        buy_count = 0
        sell_count = 0
        
        cash = self.capital
        shares = 0
        
        # Iterate through ticker data, then buy and sell when it passes thresholds
        for index, row in self.ticker_data_df.iterrows():
            price = row['Close']
            
            # Buy Stock
            if price <= self.buy_threshold and shares == 0:
                shares = int(cash // price)
                cash -= shares * price
                buy_count += 1
                trade_history_df.loc[len(trade_history_df)] = [row['Date'], 'buy', shares, price, price * shares, cash, index]
                
            # Sell Stock
            elif price >= self.sell_threshold and shares > 0:
                cash += shares * price
                sell_count += 1
                trade_history_df.loc[len(trade_history_df)] = [row['Date'], 'sell', shares, price, price * shares, cash, index]
                shares = 0
        
        # Liquidate remaining shares at final price
        final_price = self.ticker_data_df['Close'].iloc[-1]
        if shares > 0:
            cash += shares * final_price
            shares = 0
        
        summary_text = (
            f"Start Capital: ${self.capital:.2f}\n"
            f"End Capital: ${cash:.2f}\n"
            f"Net Profit: ${(cash - self.capital):.2f}\n"
            f"Return: {((cash - self.capital) / self.capital) * 100:.2f}%\n"
            f"Buys: {buy_count} | Sells: {sell_count}"
        )
        
        trade_history_df.loc[len(trade_history_df)] = [self.ticker_data_df['Date'].iloc[-1], 'END', np.nan, np.nan, np.nan, cash, np.nan] # Add ending capital
        
        print(f"\n{trade_history_df}")
        
        self.plot_backtest_results(trade_history_df, summary_text)
        
    def plot_backtest_results(self, trade_history_df: pd.DataFrame, summary_text: str) -> None:
        # Get Strategy values
        strategy_dates = trade_history_df['date']
        strategy_values = trade_history_df['total_val']
        
        # Get stock price history
        stock_dates = self.ticker_data_df['Date']
        stock_prices = self.ticker_data_df['Close']
        
        # Simulate buy-and-hold values
        first_price = stock_prices.iloc[0]
        shares_bought = int(self.capital // first_price)
        leftover_cash = self.capital - shares_bought * first_price
        buy_and_hold_values = stock_prices * shares_bought + leftover_cash
        
        # Create the plot
        fig, ax1 = plt.subplots(figsize=(12,6))
        
        # Plot portfolio values
        portfolio_line = ax1.plot(strategy_dates, strategy_values, color='purple', label=f'Portfolio Value', linewidth=2)
        buy_hold_line = ax1.plot(stock_dates, buy_and_hold_values, color='brown', linestyle='--', label='Buy & Hold Value')
        
        ax1.set_xlabel('')
        ax1.set_ylabel(f'Portfolio Value ($USD)', color='black')
        ax1.tick_params(axis='y')
        
        # Plot stock price on secondary y-axis
        ax2 = ax1.twinx()
        ax2.plot(stock_dates, stock_prices, color='gray', alpha=0.6, label=f'{self.ticker} Stock Price')
        ax2.set_ylabel('Stock Price ($USD)', color='gray')
        ax2.tick_params(axis='y', labelcolor='gray')
        
        # Plot threshold lines
        plt.axhline(y=self.buy_threshold, color='red', linestyle='--', label='Buy Threshold')
        plt.axhline(y=self.sell_threshold, color='green', linestyle='--', label='Sell Threshold')
        
        # Plot Buy and Sell Markers
        buys = trade_history_df[trade_history_df['action'] == 'buy']
        sells = trade_history_df[trade_history_df['action'] == 'sell']
        
        plt.scatter(buys['date'], buys['price_per_share'], color='red', marker='^', label='Buy')
        plt.scatter(sells['date'], sells['price_per_share'], color='green', marker='v', label='Sell')
        
        # Add Summary
        plt.text(
            0.5, 0.98, summary_text,
            transform=plt.gca().transAxes,
            va='top',
            ha='center',
            multialignment='left',
            fontsize=10,
            bbox=dict(facecolor='white', alpha=0.8, boxstyle='round')
        )
        
        # Title and Legends
        plt.title(f'{self.ticker} Backtest: {self.type} Strategy vs. Buy & Hold')
        legend1 = ax1.legend(loc='upper left')
        legend2 = ax2.legend(loc='upper right')
        
        plt.tight_layout()
        plt.show()
                