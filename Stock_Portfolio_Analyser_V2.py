import os, json, pandas as pd , yfinance as yf

class Asset:      #Parent class which will be inherited via the stock class for the variables
    def __init__(self, name, buy_price, shares):
        self.name = name
        self.buy_price = buy_price
        self.shares = shares

    def total_value(self):
        return self.buy_price * self.shares

class Stock(Asset):
    def __init__(self, name, buy_price, shares, ticker):
        super().__init__(name, buy_price, shares)  # Runs Asset's init
        self.ticker = ticker  # Then adds Stock's unique property

    def __str__(self):
        return f"{self.name} ({self.ticker}) - buy_price: {self.buy_price} shares: {self.shares}"
    
    
class Portfolio:
    def __init__(self, name):
        self.name = name    # Portfolios name
        self.stocks = {} #Store the stocks the user will input within the CRUD menu 

    def save_portfolio(self, filename):
        data = []

        for stock in self.stocks.values():
            data.append({
                "name": stock.name,
                "buy_price": stock.buy_price,
                "shares": stock.shares,
                "ticker": stock.ticker
            })
        try:
            if os.path.exists(filename):                            # Create backup of existing file BEFORE overwriting
                with open(filename, 'r') as f:
                    old_data = f.read()
                with open(filename + ".backup", 'w') as f:
                    f.write(old_data)
            
            with open(filename, 'w') as f:                
                json.dump(data, f, indent=4) # Now save new data
            
            print(f"Data saved to {filename}")
            return True
            
        except Exception as e:
            print(f"Save failed: {e}")
            return False
        
    def load_portfolio(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            for stock_data in data:
                stock = Stock(
                    stock_data["name"],
                    stock_data["buy_price"],
                    stock_data["shares"],
                    stock_data["ticker"]
                )
                self.stocks[stock.ticker] = stock

            with open(filename + ".backup", 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Loaded data from {filename}")

        except FileNotFoundError:
            print("Portfolio not found, Starting fresh!")
            return {}
        except json.JSONDecodeError:
            print(f"Corruption of your {filename} file")
            backup = filename + ".corrupted"
            print(f"Saving corrupted file as {backup}")   

            try:
                os.rename(filename, backup)             
            except:
                pass                                       
            print("Starting with empty portfolio.")
            return {}  

    def to_dict_list(self):
        data = []
        for stock in self.stocks.values():
            data.append({
                "ticker": stock.ticker,
                "name": stock.name,
                "buy_price": stock.buy_price,
                "shares": stock.shares,
                "total_value": stock.total_value()
            })
        return data       

    def export_to_CSV(self, filename):   

        data = self.to_dict_list()
        df = pd.DataFrame(data) 
        df.to_csv(filename, index=False)
        print(f"Successfully exported Portfolio to {filename}")                    
        
    def add_stock(self, stock):
        self.stocks[stock.ticker] = stock

    def total_value(self):
        total = 0
        for stock in self.stocks.values(): 
            total += stock.total_value()
        return total 
    
    def view_all_stocks(self):
        if not self.stocks:
            print("You have no stocks within your portfolio")
            return

        print("Current Stocks held:")
        for ticker, stock in self.stocks.items():
            print(f"Ticker: {ticker} | Shares: {stock.shares} | Buy Price: {stock.buy_price} | Total Value: {stock.total_value()}") # add total value to this once we import the api to find the current value buy_price * shares = total amount spent
        print(f"Your total portfolio Value is {self.total_value()}")
        print("="*40)
        
    def view_single_stock(self, ticker):
        if ticker in self.stocks:
                stock = self.stocks[ticker]
                print(f"Ticker: {ticker} | Shares: {stock.shares} | Buy Price: {stock.buy_price} | Total Value: {stock.total_value()}")
        else:
            print(f"{ticker} not found in your portfolio")
            print("="*40)

    def current_stock_value(self, ticker): 
        try:
            stock_data = yf.Ticker(ticker)
            history = stock_data.history(period ="1d")
            price =  history["Close"].iloc[-1]
            return price
        except Exception as e:  
            print(f"Error fetching price for {ticker}: {e}")  
        return None

    def portfolio_analysis(self):
        if not self.stocks:
            print("You have no stocks within your portfolio")
            return False
            
        print("/====== Current Portfolio Analyser ======/")
        print("="*40)
        total_PL = 0
        for ticker, stock in self.stocks.items():
            shares = stock.shares
            buy_price = stock.buy_price
            current_price = self.current_stock_value(ticker)
            if current_price is None:
                print(f"{ticker} Price is unavailable")
                continue
            PL = (current_price - buy_price) * shares
            total_sign = "+" if total_PL > 0 else ""
            total_PL += PL
            if PL > 0:
                sign = "+"
            elif PL < 0:
                sign = ""  
            else:
                sign = ""
            print(f"{ticker}  | Shares: {shares}  | Avg Buy: £{buy_price}  | Current: £{current_price:.2f} | Total P&L: £{sign}{PL:.2f}")
            
     
        print(f"Total Portfolio P&L: {total_sign} {total_PL:.2f}")

    def search_stock(self, ticker):
        try:
            stock_data = yf.Ticker(ticker)
            history = stock_data.history(period ="1d")
            Current_price =  history["Close"].iloc[-1]
            high = history["High"].iloc[-1]
            low = history["Low"].iloc[-1]
            volume = history["Volume"].iloc[-1]
            print(f"{ticker}  | Current Price: {Current_price:.2f}  | 1D High: £{high:.2f}  | 1D low: £{low:.2f} | Volume: {volume}")
            return Current_price, high, low, volume
        except Exception as e:  
            print(f"Error fetching price for {ticker}: {e}")  
        return None

    def Pandas_analysis(self):
        df = pd.read_csv("portfolio.csv")
        
        while True:
            print("=================== Pandas Portfolio Analysis ===================")
            print("1.) Portfolio Statistics ")
            print("2.) Filter Portfolio Weight per stock")
            print("3.) Identify Largest Position")
            print("4.) Identify Smallest Position")
            print("5.) Arrange Stocks, sort by value ")
            print("6.) Return back to application")
            print("============================================")
            try:
                analyse = int(input("Choose menu option (1-6): "))
                print("============================================")
            except ValueError:
                print("Please input a valid integer!")
                print("============================================")
            
            if analyse == 1: # Portfolio statistics
                print(df.describe()) 

            elif analyse == 2:   #Portfolio Weight per stock
                df["portfolio_%"] = (df["total_value"] / df["total_value"].sum()) * 100
                print("Your Weights per stocks are: ")
                print(df[["ticker", "portfolio_%"]])

            elif analyse == 3: # Largest Position
                best = df.loc[df["total_value"].idxmax()]
                print("Your biggest positioned stock is: ")
                print(best[["ticker", "total_value"]])

            elif analyse == 4: # Smallest Position
                worst = df.loc[df["total_value"].idxmin()]
                print("Your Smallest positioned stock is: ")
                print(worst[["ticker", "total_value"]])

            elif analyse == 5: # Stocks sorted by value 
                print(df.sort_values("total_value", ascending=False))

            elif analyse == 6:  # Return to menu 
               break

portfolio = Portfolio("portfolio.json")
portfolio.load_portfolio("portfolio.json")
while True:
        print("\n" + "="*40)
        print("    Stock Portfolio Tracker ")
        print("="*40)
        print("1. Add Stock") # Done
        print("2. View Portfolio") # Done
        print("3. View Stock within Portfolio")  # Done
        print("4. Search for stock")       # Done
        print("5. Remove Stock from Portfolio") # Done
        print("6. Trending this week")
        print("7. Portfolio Analysis & CSV Export") #Done
        print("8. Exit") #Done
        print("="*40)
        try:
            choice = int(input("Choose menu option (1-8): "))
            print("============================================")
        except ValueError:
            print("Please input a valid menu integer!")
            print("============================================")

        if choice == 1:
            ticker = input("Please input the stocks Ticker symbol: ").upper()
            if not ticker.strip():
                print("This field cannot be left empty!")
                print("=====================================================")
                continue
            try:
                buy_price = float(input("Please enter the buy price: "))  #append to position if it already exists
                if buy_price <= 0:
                    print("Buy price must be greater than value 0")
                    continue
                shares = float(input("Please enter the amount of shares purchased: "))   #append to position if it already exists
                print(f"{ticker} has successfully been added to your Portfolio!")
                if shares < 0: 
                    print("Shares must be greater than 0")
                    continue
            except ValueError:
                print("Please enter a valid number!")
                print("=====================================================")
                continue
            new_stock = Stock(ticker, buy_price, shares, ticker)
            portfolio.add_stock(new_stock)
            portfolio.save_portfolio("portfolio.json")
        elif choice == 2:
            portfolio.view_all_stocks()
        elif choice ==3:
            ticker = input("Input stock ticker to view: ").upper()
            portfolio.view_single_stock(ticker)
        elif choice ==4:
            ticker = input("Please input the ticker you would like to find data on: ").upper()
            portfolio.search_stock(ticker)
        elif choice ==5:
            ticker = input("Please input the stock you would like to remove from your portfolio: ").upper()
            if ticker in portfolio.stocks:
                confirm = input(f"Are you sure you would like to remove {portfolio.stocks[ticker]} (y/n): ").lower()
                if confirm == "y":
                    del portfolio.stocks[ticker]
                    portfolio.save_portfolio("portfolio.json")
                    print(f"Successfully removed {ticker} from the Inventory System!")
                    
                else:
                    print("Cancelled...")
            
        elif choice ==6:
            pass    
        elif choice ==7: 
            request = input("Would you like to export your portfolio? or 'n' for the current analysis  (y/n): ").lower()
            if request == "y":
                print("Exporting your CSV file...")
                portfolio.export_to_CSV("portfolio.CSV")
            portfolio.portfolio_analysis()
            portfolio.Pandas_analysis()
        elif choice ==8:
            choice_leave = input("Are you sure you would like to leave the current session? (y/n): ").lower()
            if choice_leave == "y":
                portfolio.save_portfolio("portfolio.json")
                print("Gracefully exiting.. Thank you.")
                break
            else:
                print("Cancelling exit...")
                continue
                



            




            


