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
    
    fig, ax = plt.subplots()
    data.Close.plot(ax=ax)
    ax.set_title(f'{ticker_symbol} Stock Price\nCurrent Price: ${current_price:.2f}')
    
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Create the main window
window = tk.Tk()
window.title("Stock Ticker")

# Create and place the input field and button
tk.Label(window, text="Enter the ticker symbol:").pack()
entry = tk.Entry(window)
entry.pack()
tk.Button(window, text="Fetch Data", command=fetch_data).pack()

# Run the application
window.mainloop()