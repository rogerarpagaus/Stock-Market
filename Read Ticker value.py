import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
ticker_symbol = input("Enter the ticker symbol: ")
end_date = datetime.now().strftime('%Y-%m-%d')
data = yf.download(ticker_symbol, start='2024-01-01', end=end_date)
data.Close.plot()
ticker = yf.Ticker(ticker_symbol)
current_price = ticker.history(period='1d')['Close'][0]
plt.title(f'{ticker_symbol} Stock Price\nCurrent Price: ${current_price:.2f}')
plt.show()