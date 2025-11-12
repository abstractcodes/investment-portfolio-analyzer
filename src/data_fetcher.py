"""
Data Fetcher Module
Fetches historical stock data using yfinance API
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class StockDataFetcher:
    """Fetches and processes stock market data"""
    
    def __init__(self):
        self.data = None
    
    def fetch_stock_data(self, ticker, period='1y'):
        """
        Fetch historical stock data for a given ticker
        
        Args:
            ticker (str): Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
            period (str): Time period ('1mo', '3mo', '6mo', '1y', '2y', '5y')
        
        Returns:
            pd.DataFrame: Historical stock data with OHLCV columns
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            
            if data.empty:
                print(f"Warning: No data found for {ticker}")
                return None
            
            return data
        
        except Exception as e:
            print(f"Error fetching data for {ticker}: {str(e)}")
            return None
    
    def fetch_portfolio_data(self, tickers, period='1y'):
        """
        Fetch data for multiple stocks (portfolio)
        
        Args:
            tickers (list): List of ticker symbols
            period (str): Time period for historical data
        
        Returns:
            dict: Dictionary with ticker as key and DataFrame as value
        """
        portfolio_data = {}
        
        for ticker in tickers:
            print(f"Fetching data for {ticker}...")
            data = self.fetch_stock_data(ticker, period)
            
            if data is not None:
                portfolio_data[ticker] = data
        
        return portfolio_data
    
    def get_current_price(self, ticker):
        """
        Get current/latest price for a ticker
        
        Args:
            ticker (str): Stock ticker symbol
        
        Returns:
            float: Current stock price
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period='1d')
            
            if not data.empty:
                return data['Close'].iloc[-1]
            else:
                return None
        
        except Exception as e:
            print(f"Error getting current price for {ticker}: {str(e)}")
            return None
    
    def get_stock_info(self, ticker):
        """
        Get detailed stock information
        
        Args:
            ticker (str): Stock ticker symbol
        
        Returns:
            dict: Stock information including sector, industry, market cap
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0)
            }
        
        except Exception as e:
            print(f"Error getting info for {ticker}: {str(e)}")
            return None


# Test function
if __name__ == "__main__":
    # Test the fetcher
    fetcher = StockDataFetcher()
    
    # Test single stock
    print("Testing single stock fetch...")
    aapl_data = fetcher.fetch_stock_data('AAPL', '3mo')
    print(f"AAPL data shape: {aapl_data.shape if aapl_data is not None else 'None'}")
    
    # Test portfolio
    print("\nTesting portfolio fetch...")
    portfolio = ['AAPL', 'MSFT', 'GOOGL']
    portfolio_data = fetcher.fetch_portfolio_data(portfolio, '1mo')
    print(f"Fetched data for {len(portfolio_data)} stocks")
    
    # Test current price
    print("\nTesting current price...")
    price = fetcher.get_current_price('AAPL')
    print(f"AAPL current price: ${price:.2f}" if price else "Price not available")