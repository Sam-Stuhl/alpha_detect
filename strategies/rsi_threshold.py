from .strategy import Strategy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class RSIThreshold(Strategy):
    def __init__(self, ticker: str, capital: float, time_period: str, buy_threshold: float = 30, sell_threshold: float = 70):
        super().__init__("RSI Threshold", "RSI", ticker, capital, time_period, buy_threshold, sell_threshold)
        
        self.back_test()
        
    def back_test(self) -> None:
        trade_history_df = pd.DataFrame(columns=['date', 'action', 'rsi', 'shares', 'price_per_share', 'total_price', 'total_val', 'trade_index'])
        trade_history_df.loc[len(trade_history_df)] = [self.ticker_data_df['Date'][0], 'START', np.nan, np.nan, np.nan, np.nan, self.capital, np.nan] # Add starting capital
        
        buy_count = 0
        sell_count = 0
        
        cash = self.capital
        shares = 0
        
        # Calculate RSI
        rsi_values = {}
        
        first_14_closes = self.ticker_data_df.head(14)['Close']
        
        gains = []
        losses = []
        prev_close = first_14_closes[0]
        
        for current_close in first_14_closes[1:]:
            change = current_close - prev_close
            if change < 0:
                losses.append(abs(change))
                gains.append(0)
            else:
                gains.append(change)
                losses.append(0)
        
        prev_avg_gain = sum(gains) / 14
        prev_avg_loss = sum(losses) / 14

        # Iterate through ticker data, then buy and sell when it passes thresholds
        for index in range(14, len(self.ticker_data_df)):
            row = self.ticker_data_df.iloc[index]
            price = row['Close']
            
            # Get new RSI
            prev_close = self.ticker_data_df.iloc[index-1]['Close']
            change = price - prev_close
            if change > 0:
                gain = change
                loss = 0
            else:
                loss = abs(change)
                gain = 0
                
            avg_gain = ((prev_avg_gain * 13) + gain) / 14
            avg_loss = ((prev_avg_loss * 13) + loss) / 14
            
            RSI = self.calc_RSI(avg_gain, avg_loss)
            rsi_values[row['Date']] = RSI
            
            # Buy Stock
            if RSI <= self.buy_threshold and shares == 0:
                shares = int(cash // price)
                cash -= shares * price
                buy_count += shares
                trade_history_df.loc[len(trade_history_df)] = [row['Date'], 'buy', RSI, shares, price, price * shares, cash, index]
                
            # Sell Stock
            elif RSI >= self.sell_threshold and shares != 0:
                cash += shares * price
                sell_count += shares
                trade_history_df.loc[len(trade_history_df)] = [row['Date'], 'sell', RSI, shares, price, price * shares, cash, index]
                shares = 0
            
            prev_avg_gain = avg_gain
            prev_avg_loss = avg_loss
                
                
                
        # print(f"\nPrice Threshold ({self.ticker}) Back Test Results")
        
        # Liquidate remaining shares at final price
        final_price = self.ticker_data_df['Close'].iloc[-1]
        if shares > 0:
            cash += shares * final_price
            #print(f"   Liquidated {shares} shares at final price ${final_price:.2f}")
            shares = 0
            
        # print(f"   Starting Capital: ${self.capital}")
        # print(f"   End Capital: ${cash:.2f}")
        # print(f"   Net Profit: ${(cash - self.capital):.2f}")
        # print(f"   Percentage Return: {((cash - self.capital) / self.capital) * 100:.2f}%")
        # print(f"   Number of shares bought: {buy_count}")
        # print(f"   Number of times sold: {sell_count}")
        
        summary_text = (
            f"Start Capital: ${self.capital:.2f}\n"
            f"End Capital: ${cash:.2f}\n"
            f"Net Profit: ${(cash - self.capital):.2f}\n"
            f"Return: {((cash - self.capital) / self.capital) * 100:.2f}%\n"
            f"Buys: {buy_count} | Sells: {sell_count}"
        )
        
        trade_history_df.loc[len(trade_history_df)] = [self.ticker_data_df['Date'][len(self.ticker_data_df['Date']) - 1], 'END', np.nan, np.nan, np.nan, np.nan, cash, np.nan] # Add ending capital
        
        print(f"\n{trade_history_df}")
        
        self.plot_backtest_results(trade_history_df, summary_text, rsi_values)
    
    def calc_RSI(self, avg_gain: float, avg_loss: float) -> float:
        if avg_loss == 0:
            return 100
        RS = avg_gain / avg_loss
        RSI = 100 - (100 / (1 + RS))
        
        return RSI
    
    def plot_backtest_results(self, trade_history_df: pd.DataFrame, summary_text: str, rsi_values: dict) -> None:
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
        #fig, ax1 = plt.subplots(figsize=(12,6))
        
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
        
        #Plot RSI on second subplot
        ax3.plot(list(rsi_values.keys()), list(rsi_values.values()), color='blue', label='RSI')
        ax3.axhline(y=self.sell_threshold, color='orange', linestyle='--', alpha=0.6, label='RSI Overbought')
        ax3.axhline(y=self.buy_threshold, color='cyan', linestyle='--', alpha=0.6, label='RSI Oversold')
        ax3.set_ylabel('RSI')
        ax3.set_xlabel('Date')
        ax3.legend(loc='upper right')
        
        # # Plot the RSI
        # ax3 = ax1.twinx()
        # ax3.spines['right'].set_position(('axes', 1.1))
        # ax3.plot(list(rsi_values.keys()), list(rsi_values.values()), color='blue', linestyle='-', label='RSI')
        # ax3.set_ylabel('RSI', color='blue')
        # ax3.tick_params(axis='y', labelcolor='blue')
        
        # # Plot RSI thresholds
        # ax3.axhline(y=self.sell_threshold, color='orange', linestyle='--', alpha=0.6, label='RSI Overbought')
        # ax3.axhline(y=self.buy_threshold, color='cyan', linestyle='--', alpha=0.6, label='RSI Oversold')
        
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
        # fig.text(
        #     0.01, -0.15, summary_text,
        #     ha='left', va='top', fontsize=10, wrap=True
        # )
        
        # Title and Legends
        plt.title(f'{self.ticker} Backtest: {self.type} Strategy vs. Buy & Hold')
        legend1 = ax1.legend(loc='upper left')
        legend2 = ax2.legend(loc='upper right')
        
        plt.tight_layout()
        plt.show()