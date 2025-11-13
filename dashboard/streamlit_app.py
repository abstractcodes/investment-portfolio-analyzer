"""
Streamlit Dashboard for Investment Portfolio Analyzer
Interactive web application for portfolio analysis and visualization
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.portfolio_analyzer import PortfolioAnalyzer
from src.portfolio_chat import PortfolioChatAssistant

# Page configuration
st.set_page_config(
    page_title="Portfolio Risk Analyzer",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = PortfolioAnalyzer()
    st.session_state.data_loaded = False

# Title and description
st.title("📊 Investment Portfolio Risk Analyzer")
st.markdown("""
Automated portfolio risk assessment system for retail banking clients.
Upload your holdings and get comprehensive risk analysis with rebalancing recommendations.
""")

# Sidebar - Portfolio Input
st.sidebar.header("Portfolio Configuration")

# Input method selection
input_method = st.sidebar.radio(
    "Choose input method:",
    ["Manual Entry", "Sample Portfolio"]
)

if input_method == "Manual Entry":
    st.sidebar.subheader("Add Holdings")
    
    with st.sidebar.form("add_holding"):
        ticker = st.text_input("Ticker Symbol", placeholder="e.g., AAPL").upper()
        shares = st.number_input("Number of Shares", min_value=0.0, step=0.1)
        purchase_price = st.number_input("Purchase Price ($)", min_value=0.0, step=0.01)
        
        submitted = st.form_submit_button("Add to Portfolio")
        
        if submitted and ticker and shares > 0:
            st.session_state.analyzer.add_holding(ticker, shares, purchase_price)
            st.sidebar.success(f"Added {shares} shares of {ticker}")

else:
    if st.sidebar.button("Load Sample Portfolio"):
        # Sample portfolio
        st.session_state.analyzer = PortfolioAnalyzer()
        st.session_state.analyzer.add_holding('AAPL', 10, 150.00)
        st.session_state.analyzer.add_holding('MSFT', 15, 300.00)
        st.session_state.analyzer.add_holding('GOOGL', 5, 120.00)
        st.session_state.analyzer.add_holding('AMZN', 8, 130.00)
        st.session_state.analyzer.add_holding('TSLA', 12, 200.00)
        st.sidebar.success("Sample portfolio loaded!")

# Display current holdings
if st.session_state.analyzer.holdings:
    st.sidebar.subheader("Current Holdings")
    for ticker, holding in st.session_state.analyzer.holdings.items():
        st.sidebar.text(f"{ticker}: {holding['shares']} shares")
    
    if st.sidebar.button("Clear Portfolio"):
        st.session_state.analyzer = PortfolioAnalyzer()
        st.session_state.data_loaded = False
        st.sidebar.success("Portfolio cleared!")

# Analysis period selection
analysis_period = st.sidebar.selectbox(
    "Analysis Period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=3
)

# Load data button
if st.sidebar.button("🔄 Analyze Portfolio", type="primary"):
    if not st.session_state.analyzer.holdings:
        st.sidebar.error("Please add holdings first!")
    else:
        with st.spinner("Loading market data and calculating metrics..."):
            if st.session_state.analyzer.load_portfolio_data(analysis_period):
                st.session_state.data_loaded = True
                st.sidebar.success("Analysis complete!")
            else:
                st.sidebar.error("Failed to load data. Check ticker symbols.")

# Main dashboard
if st.session_state.data_loaded:
    # Generate report
    report = st.session_state.analyzer.generate_portfolio_report()
    
    # Key Metrics Row
    st.header("📈 Portfolio Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Portfolio Value",
            f"${report['valuation']['total_value']:,.2f}"
        )
    
    with col2:
        total_gain_loss = sum(
            pos['gain_loss'] for pos in report['valuation']['positions'].values()
            if pos['gain_loss'] is not None
        )
        st.metric(
            "Total Gain/Loss",
            f"${total_gain_loss:,.2f}",
            delta=f"{(total_gain_loss/report['valuation']['total_value'])*100:.2f}%"
        )
    
    with col3:
        st.metric(
            "Diversification Score",
            f"{report['diversification']['diversification_score']}/10"
        )
    
    with col4:
        if report['risk_metrics']:
            risk_color = {
                "Low Risk": "🟢",
                "Medium Risk": "🟡",
                "High Risk": "🔴"
            }
            risk_level = report['risk_metrics']['risk_level']
            st.metric(
                "Risk Level",
                f"{risk_color.get(risk_level, '')} {risk_level}"
            )
    
    # Portfolio Composition
    st.header("💼 Portfolio Composition")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Position allocation pie chart
        positions = report['valuation']['positions']
        fig_pie = go.Figure(data=[go.Pie(
            labels=list(positions.keys()),
            values=[pos['position_value'] for pos in positions.values()],
            hole=0.3
        )])
        fig_pie.update_layout(title="Position Allocation")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Sector allocation
        if report['diversification']['sector_allocation']:
            fig_sector = go.Figure(data=[go.Pie(
                labels=list(report['diversification']['sector_allocation'].keys()),
                values=list(report['diversification']['sector_allocation'].values()),
                hole=0.3
            )])
            fig_sector.update_layout(title="Sector Allocation")
            st.plotly_chart(fig_sector, use_container_width=True)
    
    # Holdings Table
    st.subheader("📋 Holdings Details")
    
    holdings_data = []
    for ticker, pos in report['valuation']['positions'].items():
        holdings_data.append({
            'Ticker': ticker,
            'Shares': pos['shares'],
            'Current Price': f"${pos['current_price']:.2f}",
            'Position Value': f"${pos['position_value']:,.2f}",
            'Weight': f"{pos['weight']*100:.1f}%",
            'Gain/Loss': f"${pos['gain_loss']:,.2f}" if pos['gain_loss'] else "N/A",
            'Return %': f"{pos['gain_loss_pct']:.2f}%" if pos['gain_loss_pct'] else "N/A"
        })
    
    st.dataframe(pd.DataFrame(holdings_data), use_container_width=True)
    
    # Risk Metrics
    st.header("⚠️ Risk Analysis")
    
    if report['risk_metrics']:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Annual Return",
                f"{report['risk_metrics']['annual_return']*100:.2f}%"
            )
        
        with col2:
            st.metric(
                "Volatility",
                f"{report['risk_metrics']['volatility']*100:.2f}%"
            )
        
        with col3:
            st.metric(
                "Sharpe Ratio",
                f"{report['risk_metrics']['sharpe_ratio']:.2f}"
            )
        
        with col4:
            st.metric(
                "Max Drawdown",
                f"{report['risk_metrics']['max_drawdown']*100:.2f}%"
            )
        
        # Risk interpretation
        st.subheader("📊 Risk Metrics Interpretation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **Sharpe Ratio: {report['risk_metrics']['sharpe_ratio']:.2f}**
            - Above 1.0: Excellent risk-adjusted returns
            - 0.5 to 1.0: Good risk-adjusted returns
            - Below 0.5: Poor risk-adjusted returns
            """)
        
        with col2:
            st.info(f"""
            **Volatility: {report['risk_metrics']['volatility']*100:.2f}%**
            - Below 15%: Low volatility
            - 15% to 25%: Moderate volatility
            - Above 25%: High volatility
            """)
    
    # Rebalancing Recommendations
    st.header("⚖️ Rebalancing Recommendations")
    
    rebalancing = st.session_state.analyzer.get_rebalancing_recommendations()
    
    rebal_data = []
    for ticker, rec in rebalancing.items():
        if abs(rec['difference_pct']) > 0.02:  # Only show if >2% difference
            rebal_data.append({
                'Ticker': ticker,
                'Current Weight': f"{rec['current_weight']*100:.1f}%",
                'Target Weight': f"{rec['target_weight']*100:.1f}%",
                'Action': rec['action'],
                'Shares to Trade': f"{abs(rec['shares_to_trade']):.2f}",
                'Dollar Amount': f"${abs(rec['dollar_difference']):,.2f}"
            })
    
    if rebal_data:
        st.dataframe(pd.DataFrame(rebal_data), use_container_width=True)
    else:
        st.success("✅ Portfolio is well-balanced! No rebalancing needed.")
    
    # Diversification Analysis
    st.header("🎯 Diversification Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Number of Holdings", report['diversification']['num_holdings'])
        st.metric("Number of Sectors", report['diversification']['num_sectors'])
    
    with col2:
        st.metric(
            "Largest Position",
            f"{report['diversification']['top_position_weight']*100:.1f}%"
        )
        st.metric(
            "Top 3 Concentration",
            f"{report['diversification']['top_3_weight']*100:.1f}%"
        )
    
    # Recommendations
    st.subheader("💡 Recommendations")
    
    score = report['diversification']['diversification_score']
    
    if score >= 7:
        st.success("✅ Well diversified portfolio!")
    elif score >= 4:
        st.warning("⚠️ Moderate diversification. Consider adding more positions or sectors.")
    else:
        st.error("🔴 Poor diversification. High concentration risk detected!")
    
    if report['diversification']['top_position_weight'] > 0.40:
        st.warning("⚠️ Your largest position exceeds 40% of portfolio. Consider reducing concentration.")
    
    if report['diversification']['top_3_weight'] > 0.70:
        st.warning("⚠️ Top 3 positions exceed 70% of portfolio. Increase diversification.")
    
    # AI Chat Assistant
    st.header("💬 AI Financial Advisor")
    
    # Initialize chat assistant in session state
    if 'chat_assistant' not in st.session_state:
        try:
            st.session_state.chat_assistant = PortfolioChatAssistant()
            st.session_state.chat_history = []
        except ValueError as e:
            st.error("⚠️ API key not configured. Add your Anthropic API key to .env file to enable chat.")
            st.session_state.chat_assistant = None
    
    if st.session_state.chat_assistant:
        # Build portfolio context from report
        portfolio_context = {
            'total_value': report['valuation']['total_value'],
            'risk_level': report['risk_metrics']['risk_level'] if report['risk_metrics'] else 'Unknown',
            'sharpe_ratio': f"{report['risk_metrics']['sharpe_ratio']:.2f}" if report['risk_metrics'] else 'N/A',
            'volatility': f"{report['risk_metrics']['volatility']*100:.2f}%" if report['risk_metrics'] else 'N/A',
            'diversification_score': report['diversification']['diversification_score'],
            'num_holdings': report['diversification']['num_holdings']
        }
        
        # Chat interface
        st.markdown("""
        Ask questions about your portfolio, risk metrics, or get investment advice based on your data.
        
        **Example questions:**
        - What does my Sharpe Ratio mean?
        - Is my portfolio too risky?
        - Should I rebalance now?
        - How can I improve diversification?
        """)
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.chat_message("user").write(message['content'])
            else:
                st.chat_message("assistant").write(message['content'])
        
        # Chat input
        user_question = st.chat_input("Ask about your portfolio...")
        
        if user_question:
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_question
            })
            
            # Display user message
            st.chat_message("user").write(user_question)
            
            # Get AI response with portfolio context
            with st.spinner("Thinking..."):
                response = st.session_state.chat_assistant.chat(
                    user_question, 
                    portfolio_context
                )
            
            # Add assistant response to history
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response
            })
            
            # Display assistant response
            st.chat_message("assistant").write(response)
        
        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.chat_assistant.reset_conversation()
            st.session_state.chat_history = []
            st.rerun()

else:
    # Welcome screen
    st.info("👈 Add your holdings in the sidebar and click 'Analyze Portfolio' to get started!")
    
    st.subheader("Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📊 Risk Analysis
        - Sharpe Ratio
        - Volatility
        - Beta & VaR
        - Max Drawdown
        """)
    
    with col2:
        st.markdown("""
        ### 💼 Portfolio Metrics
        - Real-time valuation
        - Gain/Loss tracking
        - Diversification score
        - Sector allocation
        """)
    
    with col3:
        st.markdown("""
        ### ⚖️ Recommendations
        - Rebalancing suggestions
        - Risk assessment
        - Concentration alerts
        - Action items
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built by Rishi | Business Systems Analyst Portfolio Project</p>
    <p>Data provided by Yahoo Finance | For educational purposes only</p>
</div>
""", unsafe_allow_html=True)