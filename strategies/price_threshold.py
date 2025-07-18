from .strategy import Strategy

import pandas as pd

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
            break
        sell_price = float(input(f'Enter the price to sell {self.ticker} at: '))
        
        return (buy_price, sell_price)

    def back_test(self) -> None:
        trade_history_df = pd.DataFrame(columns=['date', 'action', 'shares', 'price_per_share', 'total_price', 'trade_index'])
        
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
                trade_history_df.loc[len(trade_history_df)] = [row['Date'], 'buy', shares, price, price * shares, index]
                #print(f"Bought at index {index} for {ticker_price}\nis_bought: {is_bought}\n") # Debug
                
            # Sell Stock
            elif price >= self.sell_price and shares != 0:
                cash += shares * price
                sell_count += shares
                trade_history_df.loc[len(trade_history_df)] = [row['Date'], 'sell', shares, price, price * shares, index]
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
    
        # Debug
        # for index in indexes_bought:
        #     print(f"Bought at index {index} for {self.ticker_price_data_df.loc[index, 'Close']}")
            
        # for index in indexes_sold:
        #     print(f"Sold at index {index} for {self.ticker_price_data_df.loc[index, 'Close']}")
           
        
        