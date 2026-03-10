import os, json 

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


portfolio = Portfolio("Tavian's Portfolio")
portfolio.save_portfolio("portfolio.json")

while True:
        print("\n" + "="*40)
        print("    Stock Portfolio Tracker ")
        print("="*40)
        print("1. Add Stock") # Done
        print("2. View Portfolio") # Done
        print("3. View Stock within Portfolio")  # Done
        print("4. Search for stock")                    # Gathers data from API to display a stock and its data 
        print("5. Remove Stock from Portfolio") # Done
        print("6. Trending this week")
        print("7. Portfolio Analysis")
        print("8. Exit")
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
                buy_price = float(input("Please enter the buy price: "))  
                if buy_price <= 0:
                    print("Buy price must be greater than value 0")
                    continue
                shares = float(input("Please enter the amount of shares purchased: "))   
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
            pass
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
            pass
        elif choice ==8:
            choice_leave = input("Are you sure you would like to leave the current session? (y/n): ").lower()
            if choice_leave == "y":
                #save the applicaiton upon exit
                portfolio.save_portfolio("portfolio.json")
                print("Gracefully exiting.. Thank you.")
                break
            else:
                print("Cancelling exit...")
                continue
                



            




            
