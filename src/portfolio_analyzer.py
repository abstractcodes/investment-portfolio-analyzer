"""
Portfolio Analyzer Module
Main analysis engine that combines data fetching and risk calculations
"""

import pandas as pd
import numpy as np
from src.data_fetcher import StockDataFetcher
from src.risk_calculator import RiskCalculator

class PortfolioAnalyzer:
    """Main portfolio analysis class"""
    
    def __init__(self, risk_free_rate=0.04):
        """
        Initialize portfolio analyzer
        
        Args:
            risk_free_rate (float): Annual risk-free rate
        """
        self.fetcher = StockDataFetcher()
        self.calculator = RiskCalculator(risk_free_rate)
        self.portfolio_data = {}
        self.holdings = {}
    
    def add_holding(self, ticker, shares, purchase_price=None):
        """
        Add a stock holding to the portfolio
        
        Args:
            ticker (str): Stock ticker symbol
            shares (float): Number of shares owned
            purchase_price (float): Purchase price per share (optional)
        """
        self.holdings[ticker] = {
            'shares': shares,
            'purchase_price': purchase_price
        }
    
    def load_portfolio_data(self, period='1y'):
        """
        Load historical data for all holdings
        
        Args:
            period (str): Time period for historical data
        
        Returns:
            bool: True if successful
        """
        tickers = list(self.holdings.keys())
        
        if not tickers:
            print("No holdings in portfolio. Add holdings first.")
            return False
        
        print(f"Loading data for {len(tickers)} stocks...")
        self.portfolio_data = self.fetcher.fetch_portfolio_data(tickers, period)
        
        return len(self.portfolio_data) > 0
    
    def calculate_portfolio_value(self):
        """
        Calculate current portfolio value and individual positions
        
        Returns:
            dict: Portfolio valuation details
        """
        total_value = 0
        positions = {}
        
        for ticker, holding in self.holdings.items():
            current_price = self.fetcher.get_current_price(ticker)
            
            if current_price:
                position_value = current_price * holding['shares']
                total_value += position_value
                
                # Calculate gain/loss if purchase price provided
                gain_loss = None
                gain_loss_pct = None
                if holding['purchase_price']:
                    gain_loss = (current_price - holding['purchase_price']) * holding['shares']
                    gain_loss_pct = ((current_price / holding['purchase_price']) - 1) * 100
                
                positions[ticker] = {
                    'shares': holding['shares'],
                    'current_price': current_price,
                    'position_value': position_value,
                    'purchase_price': holding['purchase_price'],
                    'gain_loss': gain_loss,
                    'gain_loss_pct': gain_loss_pct
                }
        
        # Calculate weights
        for ticker in positions:
            positions[ticker]['weight'] = positions[ticker]['position_value'] / total_value
        
        return {
            'total_value': total_value,
            'positions': positions
        }
    
    def analyze_diversification(self):
        """
        Analyze portfolio diversification by sector and concentration
        
        Returns:
            dict: Diversification analysis
        """
        sectors = {}
        portfolio_value = self.calculate_portfolio_value()
        
        for ticker in self.holdings.keys():
            info = self.fetcher.get_stock_info(ticker)
            
            if info and 'sector' in info:
                sector = info['sector']
                position_value = portfolio_value['positions'][ticker]['position_value']
                
                if sector in sectors:
                    sectors[sector] += position_value
                else:
                    sectors[sector] = position_value
        
        # Calculate sector weights
        total_value = portfolio_value['total_value']
        sector_weights = {sector: value/total_value for sector, value in sectors.items()}
        
        # Diversification score (higher is better, max 10)
        num_holdings = len(self.holdings)
        num_sectors = len(sectors)
        
        # Check concentration (if any position > 40% or top 3 > 70%, reduce score)
        sorted_weights = sorted([p['weight'] for p in portfolio_value['positions'].values()], 
                               reverse=True)
        top_position = sorted_weights[0] if sorted_weights else 0
        top_3 = sum(sorted_weights[:3]) if len(sorted_weights) >= 3 else sum(sorted_weights)
        
        diversification_score = min(10, num_holdings * 0.5 + num_sectors * 1.5)
        
        if top_position > 0.40:
            diversification_score -= 2
        if top_3 > 0.70:
            diversification_score -= 1
        
        diversification_score = max(0, diversification_score)
        
        return {
            'num_holdings': num_holdings,
            'num_sectors': num_sectors,
            'sector_allocation': sector_weights,
            'top_position_weight': top_position,
            'top_3_weight': top_3,
            'diversification_score': round(diversification_score, 1)
        }
    
    def calculate_risk_metrics(self):
        """
        Calculate comprehensive risk metrics for the portfolio
        
        Returns:
            dict: Risk metrics
        """
        if not self.portfolio_data:
            print("No data loaded. Run load_portfolio_data() first.")
            return None
        
        # Get portfolio weights
        portfolio_value = self.calculate_portfolio_value()
        weights = {ticker: pos['weight'] 
                  for ticker, pos in portfolio_value['positions'].items()}
        
        # Calculate portfolio metrics
        metrics = self.calculator.calculate_portfolio_metrics(
            self.portfolio_data, 
            weights
        )
        
        # Add risk assessment
        metrics['risk_level'] = self.calculator.assess_risk_level(
            metrics['sharpe_ratio'],
            metrics['volatility']
        )
        
        return metrics
    
    def get_rebalancing_recommendations(self, target_weights=None):
        """
        Generate rebalancing recommendations
        
        Args:
            target_weights (dict): Target weights {ticker: weight}. If None, equal weights
        
        Returns:
            dict: Rebalancing recommendations
        """
        portfolio_value = self.calculate_portfolio_value()
        current_weights = {ticker: pos['weight'] 
                          for ticker, pos in portfolio_value['positions'].items()}
        
        # Default to equal weights
        if target_weights is None:
            target_weights = {ticker: 1/len(self.holdings) 
                            for ticker in self.holdings.keys()}
        
        recommendations = {}
        total_value = portfolio_value['total_value']
        
        for ticker in self.holdings.keys():
            current_weight = current_weights.get(ticker, 0)
            target_weight = target_weights.get(ticker, 0)
            
            difference = target_weight - current_weight
            dollar_difference = difference * total_value
            
            current_price = portfolio_value['positions'][ticker]['current_price']
            shares_to_trade = dollar_difference / current_price
            
            recommendations[ticker] = {
                'current_weight': current_weight,
                'target_weight': target_weight,
                'difference_pct': difference,
                'dollar_difference': dollar_difference,
                'shares_to_trade': shares_to_trade,
                'action': 'BUY' if shares_to_trade > 0 else 'SELL' if shares_to_trade < 0 else 'HOLD'
            }
        
        return recommendations
    
    def generate_portfolio_report(self):
        """
        Generate comprehensive portfolio analysis report
        
        Returns:
            dict: Complete portfolio report
        """
        report = {
            'valuation': self.calculate_portfolio_value(),
            'diversification': self.analyze_diversification(),
            'risk_metrics': self.calculate_risk_metrics(),
        }
        
        return report


# Test function
if __name__ == "__main__":
    print("=== Portfolio Analyzer Test ===\n")
    
    # Create analyzer
    analyzer = PortfolioAnalyzer()
    
    # Add sample holdings
    analyzer.add_holding('AAPL', 10, 150.00)
    analyzer.add_holding('MSFT', 15, 300.00)
    analyzer.add_holding('GOOGL', 5, 120.00)
    
    print("Holdings added: AAPL, MSFT, GOOGL")
    
    # Load data
    print("\nLoading portfolio data...")
    if analyzer.load_portfolio_data('6mo'):
        print("Data loaded successfully!\n")
        
        # Generate report
        report = analyzer.generate_portfolio_report()
        
        print("=== Portfolio Valuation ===")
        print(f"Total Value: ${report['valuation']['total_value']:,.2f}\n")
        
        print("=== Diversification ===")
        print(f"Diversification Score: {report['diversification']['diversification_score']}/10\n")
        
        print("=== Risk Metrics ===")
        if report['risk_metrics']:
            print(f"Annual Return: {report['risk_metrics']['annual_return']:.2%}")
            print(f"Volatility: {report['risk_metrics']['volatility']:.2%}")
            print(f"Sharpe Ratio: {report['risk_metrics']['sharpe_ratio']:.2f}")
            print(f"Risk Level: {report['risk_metrics']['risk_level']}")
    else:
        print("Failed to load data")