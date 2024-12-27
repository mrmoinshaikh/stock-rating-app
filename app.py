import streamlit as st
from preprocess import get_selected_parameters, preprocess_stock_data, create_prompt
from utils.llm_helper import analyze_stock
from rating import calculate_rating
import yfinance as yf

# Page configuration
st.set_page_config(
    page_title="Stock Rating App",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Title and header
st.title("📊 Stock Rating System")
st.markdown(
    """
    Welcome to the **Stock Rating App**!  
    Enter a stock ticker symbol to analyze key metrics and get a comprehensive rating.
    """
)

# Sidebar for input
st.sidebar.header("Input Stock Ticker")
ticker = st.sidebar.text_input(
    "Enter Stock Ticker Symbol",
    value="AAPL",
    help="Example: AAPL for Apple, TATAMOTORS.NS for Tata Motors",
)

# Helper functions
def convert_percentage(value):
    """Convert a percentage string to float."""
    try:
        return float(value.strip('%'))
    except (ValueError, AttributeError):
        return None

def map_rating_label(rating):
    """Map numerical rating to descriptive label."""
    if rating >= 9:
        return "🔵 Strong Buy"
    elif 7 <= rating < 9:
        return "🟢 Buy"
    elif 5 <= rating < 7:
        return "🟡 Hold"
    elif 3 <= rating < 5:
        return "🟠 Sell"
    else:
        return "🔴 Strong Sell"

def fetch_stock_name(ticker):
    """Fetch the stock name from yfinance or fallback to the ticker."""
    try:
        stock = yf.Ticker(ticker)
        stock_name = stock.info.get("longName", None)
        return stock_name if stock_name else ticker.upper()
    except Exception:
        return ticker.upper()  # Fallback in case of an error

# Stock analysis
if st.sidebar.button("Analyze Stock"):
    with st.spinner("🔄 Fetching stock data..."):
        stock_name = fetch_stock_name(ticker)
        raw_data = get_selected_parameters(ticker)

    if "error" in raw_data:
        st.error(f"❌ Error fetching data: {raw_data['error']}")
    else:
        # Preprocess stock data
        processed_data = preprocess_stock_data(raw_data)

        # Extract parameters
        pe_ratio = processed_data.get("P/E Ratio", 20)  # Default: 20
        debt_to_equity = processed_data.get("Debt-to-Equity", 100)  # Default: 100
        yoy_growth_str = processed_data.get("Year-on-Year Growth (%)", "10%")  # Default: 10%
        analyst_rating = processed_data.get("Analyst Rating", "neutral").lower()

        # Convert YoY Growth to float
        yoy_growth = convert_percentage(yoy_growth_str)

        # Calculate the stock rating
        stock_rating = calculate_rating(pe_ratio, debt_to_equity, yoy_growth, analyst_rating)

        # Map numerical rating to descriptive label
        rating_label = map_rating_label(stock_rating)

        # Create prompt for LLM analysis
        prompt = create_prompt(stock_name, processed_data, stock_rating, rating_label)

        with st.spinner("🤔 Analyzing stock..."):
            analysis = analyze_stock(prompt)

        # Main content layout
        st.subheader(f"Stock Rating and Key Insights for **{stock_name}**")
        col1, col2 = st.columns(2)

        # Left column: Rating
        with col1:
            st.metric(label="Overall Rating", value=f"{stock_rating}/10")
            st.write(f"### Recommendation: {rating_label}")

        # Right column: Bar chart visualization
        with col2:
            st.write("### Key Metrics")
            st.bar_chart({
                "Metrics": ["P/E Ratio", "Debt-to-Equity", "YoY Growth (%)"],
                "Values": [pe_ratio, debt_to_equity, yoy_growth],
            })

        # Detailed report
        st.subheader("📋 Stock Analysis Report")
        st.write(analysis)

# Footer
st.markdown(
    """
    ---
    **Note:** The analysis is generated based on publicly available data and is for informational purposes only. Always consult a financial advisor for investment decisions.
    """
)
