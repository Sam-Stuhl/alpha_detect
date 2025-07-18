from .strategy import Strategy

import pandas as pd
import matplotlib.pyplot as plt

class PriceThreshold(Strategy):
    def __init__(self, ticker: str, capital: float = 1000.0, buy_price: int = None, sell_price: int = None):
        super().__init__("Price Threshold", ticker, capital) # Gives access to type, ticker, and ticker_price_data_df
        
        if not(buy_price and sell_price):
            self.buy_price, self.sell_price = self.get_buy_and_sell()
        else:
            self.buy_price = buy_price
            self.sell_price = sell_price
            
        self.back_test()
        
    def get_buy_and_sell(self) -> tuple[float, float]:
        while True:
            buy_price = float(input(f'\nEnter the price to buy {self.ticker} at: '))
            if buy_price > self.capital:
                print("The buy price cannot be greater than the starting capital. Either enter a lower buy price or restart.")
            else:
                break
        sell_price = float(input(f'Enter the price to sell {self.ticker} at: '))
        
        return (buy_price, sell_price)

    def back_test(self) -> None:
        trade_history_df = pd.DataFrame(columns=['date', 'action', 'shares', 'price_per_share', 'total_price', 'total_val', 'trade_index'])
        trade_history_df.loc[len(trade_history_df)] = [self.ticker_price_data_df['Date'][0], 'init', 0, 0, 0, self.capital, 0] # Initialize using starting capital (mostly needed for plotting)
        
        buy_count = 0
        sell_count = 0
        
        cash = self.capital
        shares = 0
        
        # Iterate through ticker data, then buy and sell when it passes thresholds
        for index, row in self.ticker_price_data_df.iterrows():
            price = row['Close']
            
            # Buy Stock
            if price <= self.buy_price and shares == 0:
                shares = int(cash // price)
                cash -= shares * price
                buy_count += shares
                trade_history_df.loc[len(trade_history_df)] = [row['Date'], 'buy', shares, price, price * shares, cash, index]
                #print(f"Bought at index {index} for {ticker_price}\nis_bought: {is_bought}\n") # Debug
                
            # Sell Stock
            elif price >= self.sell_price and shares != 0:
                cash += shares * price
                sell_count += shares
                trade_history_df.loc[len(trade_history_df)] = [row['Date'], 'sell', shares, price, price * shares, cash, index]
                shares = 0
                #print(f"Sold at index {index} for {ticker_price}\nis_bought: {is_bought}\n") # Debug
                
        print(f"\nPrice Threshold ({self.ticker}) Back Test Results")
        
        # Liquidate remaining shares at final price
        final_price = self.ticker_price_data_df['Close'].iloc[-1]
        if shares > 0:
            cash += shares * final_price
            print(f"   Liquidated {shares} shares at final price ${final_price:.2f}")
            shares = 0
            
        print(f"   Starting Capital: ${self.capital}")
        print(f"   End Capital: ${cash:.2f}")
        print(f"   Net Profit: ${(cash - self.capital):.2f}")
        print(f"   Percentage Return: {((cash - self.capital) / self.capital) * 100:.2f}%")
        print(f"   Number of shares bought: {buy_count}")
        print(f"   Number of times sold: {sell_count}")
        
        print(f"\n{trade_history_df}")
        
        self.plot_backtest_results(trade_history_df)
    
        # Debug
        # for index in indexes_bought:
        #     print(f"Bought at index {index} for {self.ticker_price_data_df.loc[index, 'Close']}")
            
        # for index in indexes_sold:
        #     print(f"Sold at index {index} for {self.ticker_price_data_df.loc[index, 'Close']}")
        
    def plot_backtest_results(self, trade_history_df: pd.DataFrame) -> None:
        # Get Strategy values
        strategy_dates = trade_history_df['date']
        strategy_values = trade_history_df['total_val']
        
        # Get stock price history
        stock_dates = self.ticker_price_data_df['Date']
        stock_prices = self.ticker_price_data_df['Close']
        
        # Simulate buy-and-hold values
        first_price = stock_prices.iloc[0]
        shares_bought = int(self.capital // first_price)
        leftover_cash = self.capital - shares_bought * first_price
        buy_and_hold_values = stock_prices * shares_bought + leftover_cash
        
        # Create the plot
        fig, ax1 = plt.subplots(figsize=(12,6))
        
        # Plot portfolio values
        ax1.plot(strategy_dates, strategy_values, color='purple', label=f'Portfolio Value', linewidth=2)
        ax1.plot(stock_dates, buy_and_hold_values, color='green', linestyle='--', label='Buy & Hold Value')
        
        ax1.set_xlabel('')
        ax1.set_ylabel(f'Portfolio Value ($USD)', color='black')
        ax1.tick_params(axis='y')
        
        # Plot stock price on secondary y-axis
        ax2 = ax1.twinx()
        ax2.plot(stock_dates, stock_prices, color='gray', alpha=0.6, label='Stock Price')
        ax2.set_ylabel('Stock Price ($USD)', color='gray')
        ax2.tick_params(axis='y', labelcolor='gray')
        
        # Plot threshold lines
        plt.axhline(y=self.buy_price, color='red', linestyle='--', label='Buy Threshold')
        plt.axhline(y=self.sell_price, color='green', linestyle='--', label='Sell Threshold')
        
        # Plot Buy and Sell Markers
        buys = trade_history_df[trade_history_df['action'] == 'buy']
        sells = trade_history_df[trade_history_df['action'] == 'sell']
        
        plt.scatter(buys['date'], buys['price_per_share'], color='red', marker='^', label='Buy')
        plt.scatter(sells['date'], sells['price_per_share'], color='green', marker='v', label='Sell')
        
        # Title and Legends
        plt.title(f'{self.ticker} Backtest: {self.type} Strategy vs. Buy & Hold')
        ax1.legend(loc='upper left')
        ax2. legend(loc='upper right')
        
        plt.tight_layout()
        plt.show()
        
        