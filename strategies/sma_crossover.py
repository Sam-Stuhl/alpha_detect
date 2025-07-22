from .strategy import Strategy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class SMACrossover(Strategy):
    
    # Static variable
    time_periods = [
            '1M',
            '3M',
            '6M',
            '1Y',
            '3Y',
            '5Y',
        ]
    
    name = 'SMA Crossover'
    
    def __init__(self, ticker: str, capital: float, time_period: str, short_sma: float = None, long_sma: float = None):
        super().__init__("SMA Crossover", ticker, capital, time_period)
        
        self.short_sma, self.long_sma = self.get_sma() if not(short_sma and long_sma) else (short_sma, long_sma)
        
        self.ticker_data_df['SMA_short'] = self.ticker_data_df['Close'].rolling(window=int(self.short_sma)).mean()
        self.ticker_data_df['SMA_long'] = self.ticker_data_df['Close'].rolling(window=int(self.long_sma)).mean()
        
        self.back_test()
        
    def get_sma(self) -> tuple[float, float]:
        while True:
            try:
                short_sma = float(input('\nEnter the window for the short SMA (in days) (default 10 days): '))
                long_sma = float(input('Enter the window for the long SMA (in days) (default 50 days): '))
            except Exception:
                short_sma = 10
                long_sma = 50
            
            if short_sma >= long_sma:
                print(f'The short SMA must have a smaller window than the long SMA. Try again.')
            else:
                break
            
        return (short_sma, long_sma)
        
    def back_test(self) -> None:
        trade_history_df = pd.DataFrame(columns=['date', 'action', 'SMA_short', 'SMA_long', 'shares', 'price_per_share', 'total_price', 'total_val', 'trade_index'])
        trade_history_df.loc[len(trade_history_df)] = [self.ticker_data_df['Date'][0], 'START', np.nan, np.nan, np.nan, np.nan, np.nan, self.capital, np.nan] # Add starting capital
        
        buy_count = 0
        sell_count = 0
        
        cash = self.capital
        shares = 0
        
        # Iterate through ticker data, then buy and sell when it passes thresholds
        for index, row in self.ticker_data_df.iterrows():
            price = row['Close']
            
            short_sma = row['SMA_short']
            long_sma = row['SMA_long']
            
            if not(pd.isna(short_sma) or pd.isna(long_sma)):
            
                # Buy Stock
                if short_sma > long_sma and shares == 0:
                    shares = int(cash // price)
                    cash -= shares * price
                    buy_count += 1
                    trade_history_df.loc[len(trade_history_df)] = [row['Date'], 'buy', short_sma, long_sma, shares, price, price * shares, cash, index]
                    
                # Sell Stock
                elif short_sma < long_sma and shares > 0:
                    cash += shares * price
                    sell_count += 1
                    trade_history_df.loc[len(trade_history_df)] = [row['Date'], 'sell', short_sma, long_sma, shares, price, price * shares, cash, index]
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
        
        trade_history_df.loc[len(trade_history_df)] = [self.ticker_data_df['Date'].iloc[-1], 'END', np.nan, np.nan, np.nan, np.nan, np.nan, cash, np.nan] # Add ending capital
        
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
        fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(12,6), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
        
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
        
        #Plot SMAs on second subplot
        ax3.plot(trade_history_df['date'], trade_history_df['SMA_short'], color='blue', label='Short SMA')
        ax3.plot(trade_history_df['date'], trade_history_df['SMA_long'], color='red', label='Long SMA')
        ax3.set_ylabel('SMA Value')
        ax3.set_xlabel('')
        ax3.legend(loc='upper right')
        
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