import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fetch_data():
    ticker_symbol = entry.get()
    if not ticker_symbol:
        messagebox.showerror("Input Error", "Please enter a ticker symbol")
        return
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    data = yf.download(ticker_symbol, start='2024-01-01', end=end_date)
    
    if data.empty:
        messagebox.showerror("Data Error", "No data found for the ticker symbol")
        return
    
    ticker = yf.Ticker(ticker_symbol)
    current_price = ticker.history(period='1d')['Close'][0]
    initial_price = data['Close'][0]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot historical data
    data.Close.plot(ax=ax1)
    ax1.set_title(f'{ticker_symbol} Stock Price\nCurrent Price: ${current_price:.2f}')
    
    # Plot for live updates
    ax2.set_title(f'{ticker_symbol} Live Ticker')
    live_line, = ax2.plot([], [], 'r-')
    ax2.set_xlim(0, 10)
    ax2.set_ylim(current_price * 0.95, current_price * 1.05)
    
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    update_ticker_price(ticker_symbol, live_line, ax2, canvas, initial_price)
    fetch_news(ticker_symbol)

def update_ticker_price(ticker_symbol, live_line, ax, canvas, initial_price):
    ticker = yf.Ticker(ticker_symbol)
    current_price = ticker.history(period='1d')['Close'][0]
    
    xdata = live_line.get_xdata()
    ydata = live_line.get_ydata()
    
    if len(xdata) == 0:
        xdata = [0]
        ydata = [current_price]
    else:
        xdata = list(xdata) + [xdata[-1] + 1]
        ydata = list(ydata) + [current_price]
    
    live_line.set_xdata(xdata)
    live_line.set_ydata(ydata)
    
    ax.set_xlim(0, max(10, len(xdata)))
    ax.set_ylim(min(ydata) * 0.95, max(ydata) * 1.05)
    
    canvas.draw()
    
    # Calculate the percentage change
    percentage_change = ((current_price - initial_price) / initial_price) * 100
    
    # Update the alert label
    if percentage_change > 5:
        alert_label.config(text=f"Price increased by {percentage_change:.2f}%", bg="green")
    elif percentage_change < -5:
        alert_label.config(text=f"Price decreased by {percentage_change:.2f}%", bg="red")
    else:
        alert_label.config(text=f"Price change: {percentage_change:.2f}%", bg="yellow")
    
    window.after(60000, update_ticker_price, ticker_symbol, live_line, ax, canvas, initial_price)  # Update every 60 seconds

def fetch_news(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    news = ticker.news
    
    news_text.delete(1.0, tk.END)
    for article in news[:5]:  # Show the latest 5 news articles
        news_text.insert(tk.END, f"{article['title']}\n{article['link']}\n\n")

# Create the main window
window = tk.Tk()
window.title("Stock Ticker")

# Create and place the input field and button
tk.Label(window, text="Enter the ticker symbol:").pack()
entry = tk.Entry(window)
entry.pack()
tk.Button(window, text="Fetch Data", command=fetch_data).pack()

# Create and place the alert label
alert_label = tk.Label(window, text="Price change: 0.00%", bg="yellow", width=80)
alert_label.pack()

# Create and place the text box for news
news_text = tk.Text(window, height=10, width=80)
news_text.pack()

# Run the application
window.mainloop()