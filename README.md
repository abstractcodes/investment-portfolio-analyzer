# Investment Portfolio Analyzer with Risk Assessment

A comprehensive portfolio analysis system that automates risk assessment and delivers actionable investment recommendations for retail banking clients. Built to showcase Business Systems Analyst capabilities with end-to-end implementation from requirements gathering to technical delivery.

## 📊 Overview

This application addresses a critical need in retail banking: providing fast, accurate, and consistent portfolio risk assessments without the time-intensive manual analysis traditionally required. By leveraging real-time market data and industry-standard financial metrics, the system empowers both advisors and clients to make informed investment decisions backed by quantitative analysis.

**Key Value Proposition:** Reduce manual portfolio analysis time by 40% while maintaining regulatory compliance and improving decision accuracy.

## ✨ Core Features

### Risk Analytics Engine
- **Sharpe Ratio Calculation** - Measures risk-adjusted returns to evaluate portfolio efficiency
- **Volatility Analysis** - Quantifies price fluctuations to assess portfolio stability
- **Value at Risk (VaR)** - Estimates potential losses at given confidence levels
- **Maximum Drawdown** - Identifies largest peak-to-trough declines
- **Risk Classification** - Categorizes portfolios as Low, Medium, or High risk based on multiple factors

### Portfolio Intelligence
- **Real-time Valuation** - Live portfolio value tracking with gain/loss calculations
- **Diversification Scoring** - 0-10 scale assessment of portfolio concentration risk
- **Sector Allocation Analysis** - Breakdown of investments across market sectors
- **Position Weighting** - Individual holding percentages with concentration alerts
- **Rebalancing Recommendations** - Actionable buy/sell suggestions with exact share quantities

### AI-Powered Advisory (Optional)
- **Conversational Interface** - Ask questions about your portfolio in plain English
- **Context-Aware Responses** - AI advisor has full visibility into your portfolio metrics
- **Educational Explanations** - Demystifies complex financial terminology
- **Personalized Guidance** - Investment recommendations based on your specific holdings

> **Note:** The AI chat assistant requires an Anthropic API key. See [AI Assistant Setup](#-ai-assistant-setup-optional) below.

## 🛠 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Python 3.10+ | Core calculation engine |
| **Data Processing** | Pandas, NumPy | Financial data manipulation |
| **Market Data** | yfinance API | Real-time stock prices and historical data |
| **Risk Calculations** | SciPy, scikit-learn | Statistical modeling and analysis |
| **Visualization** | Plotly | Interactive charts and graphs |
| **Dashboard** | Streamlit | Web-based user interface |
| **AI Assistant** | Anthropic Claude API | Natural language financial advisor |

## 📁 Project Structure
```
investment-portfolio-analyzer/
│
├── src/                          # Core business logic
│   ├── data_fetcher.py          # Market data retrieval (yfinance)
│   ├── risk_calculator.py       # Financial metrics computation
│   ├── portfolio_analyzer.py    # Main analysis engine
│   └── portfolio_chat.py        # AI assistant integration
│
├── dashboard/
│   └── streamlit_app.py         # Interactive web dashboard
│
├── docs/                         # Business analysis artifacts
│   ├── requirements/            # Functional & non-functional requirements
│   ├── process_flows/           # Current vs. future state diagrams
│   └── test_plans/              # UAT scenarios and acceptance criteria
│
├── tests/                        # Test cases and quality assurance
│
├── .env                          # Environment variables (API keys)
├── .gitignore                   # Git exclusions
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/abstractcodes/investment-portfolio-analyzer.git
cd investment-portfolio-analyzer
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
streamlit run dashboard/streamlit_app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

### Basic Usage

1. **Add Holdings**
   - Choose "Sample Portfolio" for a pre-loaded demo, or
   - Use "Manual Entry" to add your own stock positions

2. **Analyze Portfolio**
   - Select analysis period (1 month to 5 years)
   - Click "🔄 Analyze Portfolio" button

3. **Review Results**
   - Portfolio Overview: Total value, gains/losses, risk level
   - Risk Metrics: Sharpe ratio, volatility, max drawdown
   - Diversification: Sector allocation and concentration analysis
   - Recommendations: Rebalancing suggestions and action items

## 🤖 AI Assistant Setup (Optional)

The AI financial advisor provides conversational explanations of portfolio metrics and personalized investment guidance.

### Prerequisites
- Anthropic API account (sign up at https://console.anthropic.com/)
- Valid API key with Claude Sonnet access

### Configuration

1. **Create `.env` file** in project root:
```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

2. **Verify installation**
```bash
pip install anthropic python-dotenv
```

3. **Restart the application**
   - The AI assistant will automatically activate
   - Ask questions like:
     - "What does my Sharpe Ratio mean?"
     - "Should I rebalance my portfolio?"
     - "How can I improve diversification?"

> **Important:** Keep your API key secure. The `.env` file is excluded from version control via `.gitignore`. Never commit API keys to public repositories.

### Without API Key
The application works perfectly without the AI assistant. You'll see all portfolio analytics, risk metrics, and recommendations - just without the conversational chat feature.

## 📊 Understanding Key Metrics

### Sharpe Ratio
Measures risk-adjusted returns. Higher is better.
- **Above 1.0:** Excellent - Strong returns relative to risk taken
- **0.5 to 1.0:** Good - Acceptable risk-adjusted performance
- **Below 0.5:** Poor - Returns don't justify the risk

### Volatility
Measures price fluctuation intensity (annual standard deviation).
- **Below 15%:** Low volatility - Stable, conservative investments
- **15% to 25%:** Moderate volatility - Balanced risk profile
- **Above 25%:** High volatility - Aggressive, fluctuating returns

### Diversification Score (0-10)
Evaluates concentration risk across holdings and sectors.
- **7-10:** Well diversified - Risk spread across multiple positions
- **4-6:** Moderate - Some concentration concerns
- **0-3:** Poor - High concentration risk detected

### Value at Risk (VaR)
Maximum expected loss at 95% confidence level.
- Example: VaR of 5% means 95% confidence that daily losses won't exceed 5%

## 📋 Business Analysis Deliverables

This project demonstrates comprehensive BA capabilities through:

- **Requirements Documentation** - Functional and non-functional requirements with traceability
- **Process Flow Diagrams** - Current state vs. future state workflow mapping
- **User Stories & Acceptance Criteria** - Agile-formatted feature specifications
- **Stakeholder Analysis** - Identification of key users and their needs
- **Requirements Traceability Matrix** - Links between requirements, design, and testing
- **UAT Test Plans** - User acceptance testing scenarios and validation criteria
- **ROI Analysis** - Business case with quantified benefits (40% time reduction)
- **Compliance Mapping** - Alignment with retail banking regulatory requirements

## 🎯 Project Goals

This portfolio project showcases:

1. **Business Analysis Skills**
   - Requirements elicitation and documentation
   - Process mapping and improvement
   - Stakeholder communication
   - Acceptance criteria definition

2. **Technical Competency**
   - Python development
   - Financial domain knowledge
   - API integration
   - Data visualization

3. **End-to-End Delivery**
   - From requirements to working product
   - Professional documentation
   - Version control and collaboration

## ⚠️ Disclaimer

This application is for **educational and demonstration purposes only**. It should not be used as the sole basis for investment decisions. Always consult with qualified financial advisors before making investment choices. Market data is provided by Yahoo Finance and may have delays or inaccuracies.

## 👤 Author

**Rishit Singh Grover**  
Business Systems Analyst  
University of Alberta - Computing Science

*This project demonstrates BA capabilities in requirements analysis, process improvement, and technical implementation for retail banking applications.*

## 📄 License

This project is open source and available for educational purposes.

---

**Status:** ✅ Fully Functional | 🚧 Documentation In Progress

**Last Updated:** November 2025