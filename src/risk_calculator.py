"""
Risk Calculator Module
Calculates portfolio risk metrics including Sharpe ratio, beta, volatility, and VaR
"""

import pandas as pd
import numpy as np
from scipy import stats

class RiskCalculator:
    """Calculates various risk metrics for portfolio analysis"""
    
    def __init__(self, risk_free_rate=0.04):
        """
        Initialize risk calculator
        
        Args:
            risk_free_rate (float): Annual risk-free rate (default 4% for 2024)
        """
        self.risk_free_rate = risk_free_rate
    
    def calculate_returns(self, prices):
        """
        Calculate daily returns from price data
        
        Args:
            prices (pd.Series or pd.DataFrame): Historical price data
        
        Returns:
            pd.Series or pd.DataFrame: Daily returns
        """
        return prices.pct_change().dropna()
    
    def calculate_volatility(self, returns, annualize=True):
        """
        Calculate volatility (standard deviation of returns)
        
        Args:
            returns (pd.Series): Daily returns
            annualize (bool): If True, annualize the volatility
        
        Returns:
            float: Volatility (annualized if specified)
        """
        volatility = returns.std()
        
        if annualize:
            # Annualize using 252 trading days
            volatility = volatility * np.sqrt(252)
        
        return volatility
    
    def calculate_sharpe_ratio(self, returns, annualize=True):
        """
        Calculate Sharpe Ratio (risk-adjusted return)
        
        Args:
            returns (pd.Series): Daily returns
            annualize (bool): If True, annualize the ratio
        
        Returns:
            float: Sharpe ratio
        """
        mean_return = returns.mean()
        std_return = returns.std()
        
        if annualize:
            # Annualize mean and std
            mean_return = mean_return * 252
            std_return = std_return * np.sqrt(252)
        
        # Sharpe ratio = (Return - Risk Free Rate) / Volatility
        sharpe = (mean_return - self.risk_free_rate) / std_return
        
        return sharpe
    
    def calculate_beta(self, stock_returns, market_returns):
        """
        Calculate Beta (systematic risk relative to market)
        
        Args:
            stock_returns (pd.Series): Stock daily returns
            market_returns (pd.Series): Market benchmark returns (e.g., S&P 500)
        
        Returns:
            float: Beta value
        """
        # Align the returns
        aligned_data = pd.DataFrame({
            'stock': stock_returns,
            'market': market_returns
        }).dropna()
        
        if len(aligned_data) < 2:
            return None
        
        # Calculate covariance and variance
        covariance = aligned_data['stock'].cov(aligned_data['market'])
        market_variance = aligned_data['market'].var()
        
        beta = covariance / market_variance
        
        return beta
    
    def calculate_var(self, returns, confidence_level=0.95):
        """
        Calculate Value at Risk (VaR) - maximum expected loss
        
        Args:
            returns (pd.Series): Daily returns
            confidence_level (float): Confidence level (default 95%)
        
        Returns:
            float: VaR value (positive number representing potential loss)
        """
        # Using historical method
        var = np.percentile(returns, (1 - confidence_level) * 100)
        
        return abs(var)
    
    def calculate_max_drawdown(self, prices):
        """
        Calculate Maximum Drawdown (largest peak-to-trough decline)
        
        Args:
            prices (pd.Series): Historical price data
        
        Returns:
            float: Maximum drawdown as a percentage
        """
        # Calculate cumulative returns
        cumulative = (1 + self.calculate_returns(prices)).cumprod()
        
        # Calculate running maximum
        running_max = cumulative.expanding().max()
        
        # Calculate drawdown
        drawdown = (cumulative - running_max) / running_max
        
        max_drawdown = drawdown.min()
        
        return abs(max_drawdown)
    
    def calculate_portfolio_metrics(self, portfolio_data, weights=None):
        """
        Calculate comprehensive risk metrics for entire portfolio
        
        Args:
            portfolio_data (dict): Dictionary with ticker as key, price data as value
            weights (dict): Portfolio weights {ticker: weight}. If None, equal weights
        
        Returns:
            dict: Dictionary of portfolio metrics
        """
        tickers = list(portfolio_data.keys())
        
        # Default to equal weights if not provided
        if weights is None:
            weights = {ticker: 1/len(tickers) for ticker in tickers}
        
        # Calculate returns for each stock
        returns_data = {}
        for ticker, data in portfolio_data.items():
            if 'Close' in data.columns:
                returns_data[ticker] = self.calculate_returns(data['Close'])
        
        # Create returns DataFrame
        returns_df = pd.DataFrame(returns_data)
        
        # Calculate weighted portfolio returns
        weighted_returns = sum(returns_df[ticker] * weights[ticker] 
                              for ticker in tickers if ticker in returns_df.columns)
        
        # Calculate metrics
        metrics = {
            'annual_return': weighted_returns.mean() * 252,
            'volatility': self.calculate_volatility(weighted_returns),
            'sharpe_ratio': self.calculate_sharpe_ratio(weighted_returns),
            'var_95': self.calculate_var(weighted_returns, 0.95),
            'max_drawdown': self.calculate_max_drawdown(
                (1 + weighted_returns).cumprod()
            )
        }
        
        return metrics
    
    def assess_risk_level(self, sharpe_ratio, volatility):
        """
        Assess overall risk level based on metrics
        
        Args:
            sharpe_ratio (float): Sharpe ratio
            volatility (float): Annual volatility
        
        Returns:
            str: Risk level ('Low', 'Medium', 'High')
        """
        # Risk assessment logic
        if sharpe_ratio > 1.0 and volatility < 0.20:
            return "Low Risk"
        elif sharpe_ratio > 0.5 and volatility < 0.30:
            return "Medium Risk"
        else:
            return "High Risk"


# Test function
if __name__ == "__main__":
    # Create sample data for testing
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    
    # Simulate stock prices
    prices = pd.Series(
        100 * (1 + np.random.randn(len(dates)).cumsum() * 0.01),
        index=dates
    )
    
    # Test calculator
    calc = RiskCalculator()
    
    returns = calc.calculate_returns(prices)
    print(f"Average Daily Return: {returns.mean():.4f}")
    print(f"Volatility (Annual): {calc.calculate_volatility(returns):.4f}")
    print(f"Sharpe Ratio: {calc.calculate_sharpe_ratio(returns):.4f}")
    print(f"VaR (95%): {calc.calculate_var(returns):.4f}")
    print(f"Max Drawdown: {calc.calculate_max_drawdown(prices):.2%}")