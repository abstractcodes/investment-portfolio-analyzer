"""
Portfolio Chat Assistant using Claude API
Provides AI-powered financial advice and metric explanations
"""

import os
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PortfolioChatAssistant:
    """AI chat assistant for portfolio analysis"""
    
    def __init__(self):
        """Initialize Claude API client"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.conversation_history = []
    
    def get_system_prompt(self, portfolio_context=None):
        """
        Generate system prompt with portfolio context
        
        Args:
            portfolio_context (dict): Current portfolio metrics and data
        
        Returns:
            str: System prompt for Claude
        """
        base_prompt = """You are a professional financial advisor assistant helping retail banking clients understand their investment portfolios. 

Your role:
- Explain financial metrics in simple, accessible language
- Provide actionable investment advice based on portfolio data
- Help users understand risk, diversification, and rebalancing
- Be encouraging but honest about risks
- Cite specific numbers from their portfolio when relevant

Keep responses concise (2-3 paragraphs max) unless asked for detailed analysis."""

        if portfolio_context:
            context_str = f"""

Current Portfolio Context:
- Total Value: ${portfolio_context.get('total_value', 0):,.2f}
- Risk Level: {portfolio_context.get('risk_level', 'Unknown')}
- Sharpe Ratio: {portfolio_context.get('sharpe_ratio', 'N/A')}
- Volatility: {portfolio_context.get('volatility', 'N/A')}
- Diversification Score: {portfolio_context.get('diversification_score', 'N/A')}/10
- Number of Holdings: {portfolio_context.get('num_holdings', 0)}

Use this context to provide personalized advice."""
            
            return base_prompt + context_str
        
        return base_prompt
    
    def chat(self, user_message, portfolio_context=None):
        """
        Send message to Claude and get response
        
        Args:
            user_message (str): User's question
            portfolio_context (dict): Current portfolio data
        
        Returns:
            str: Claude's response
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Get system prompt with context
            system_prompt = self.get_system_prompt(portfolio_context)
            
            # Call Claude API
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=system_prompt,
                messages=self.conversation_history
            )
            
            # Extract response text
            assistant_message = response.content[0].text
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
        
        except Exception as e:
            return f"Error: Unable to get response from AI assistant. {str(e)}"
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []


# Test function
if __name__ == "__main__":
    assistant = PortfolioChatAssistant()
    
    # Test without context
    response = assistant.chat("What is a Sharpe Ratio?")
    print("Response:", response)
    
    # Test with context
    context = {
        'total_value': 19107.49,
        'risk_level': 'Medium Risk',
        'sharpe_ratio': 2.25,
        'volatility': 0.2186,
        'diversification_score': 6.0,
        'num_holdings': 5
    }
    
    response2 = assistant.chat("How is my portfolio doing?", context)
    print("\nPersonalized Response:", response2)