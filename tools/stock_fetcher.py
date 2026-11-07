import yfinance as yf


def get_stock_data(symbol):
    try:
        stock=yf.Ticker(symbol) #create an object representing a specific stock
        hist= stock.history(period="1mo") # this result in pandas dataframe
        price=hist["Close"].iloc[-1] # select last row of close column

        prices=hist["Close"].tolist()
# convert pandas series to pandas list

        return{
            "price":round(price,2),
            "prices":prices
        }
    except Exception as e :
        print("Stock fetch error:",e)
        return None        