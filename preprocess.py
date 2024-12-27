import yfinance as yf
import logging

logging.basicConfig(level=logging.INFO)

def get_selected_parameters(ticker):
    try:
        # Append ".NS" for Indian stocks
        if not ticker.endswith(".NS"):
            ticker += ".NS"
        
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract specific parameters
        pe_ratio = info.get("trailingPE", None)
        debt_to_equity = info.get("debtToEquity", None)
        yoy_growth = info.get("revenueGrowth", None)
        analyst_rating = info.get("recommendationKey", None)
        stock_name = info.get("shortName", ticker)  # Dynamic stock name
        
        # Format the extracted data
        data = {
            "P/E Ratio": pe_ratio,
            "Debt-to-Equity": debt_to_equity,
            "Year-on-Year Growth (%)": f"{yoy_growth * 100:.2f}%" if yoy_growth else None,
            "Analyst Rating": analyst_rating,
            "Stock Name": stock_name,  # Include stock name
        }
        
        return data

    except Exception as e:
        return {"error": str(e)}


def preprocess_stock_data(data):
    placeholders = {
        "P/E Ratio": 20,  # Default P/E Ratio
        "Debt-to-Equity": 100,  # Default Debt-to-Equity
        "Year-on-Year Growth (%)": "10%",  # Default YoY Growth
        "Analyst Rating": "neutral",  # Default Analyst Rating
        "Stock Name": "Unknown Stock",  # Default stock name
    }

    processed_data = {}
    for key, value in data.items():
        if value is None:
            processed_data[key] = placeholders[key]
        else:
            processed_data[key] = value

    return processed_data

def create_prompt(stock_name, data, calculated_rating, recommendation_label):
    prompt = (
        f"Analyze the following stock '{stock_name}' based on these metrics:\n"
        f"- P/E Ratio: {data.get('P/E Ratio', 'Data not available')}\n"
        f"- Debt-to-Equity Ratio: {data.get('Debt-to-Equity', 'Data not available')}\n"
        f"- Year-on-Year Growth (%): {data.get('Year-on-Year Growth (%)', 'Data not available')}\n"
        f"- Analyst Rating: {data.get('Analyst Rating', 'Data not available')}\n"
        f"The calculated rating for this stock is {calculated_rating}/10, "
        f"which corresponds to a recommendation of '{recommendation_label}'.\n"
        "Do you agree with this rating? Provide your rationale and any additional insights."
    )
    return prompt


def calculate_rating(pe_ratio, debt_to_equity, yoy_growth, analyst_rating):
    # Example scoring mechanism (update as needed)
    score = 0
    if pe_ratio and pe_ratio < 15:
        score += 3
    if debt_to_equity and debt_to_equity < 50:
        score += 3
    if yoy_growth and float(yoy_growth.strip('%')) > 5:
        score += 2
    if analyst_rating and analyst_rating in ["buy", "strong_buy"]:
        score += 2
    return min(score, 10)  # Cap the score at 10


def map_rating_label(rating):
    if rating >= 8:
        return "Strong Buy"
    elif rating >= 6:
        return "Buy"
    elif rating >= 4:
        return "Hold"
    else:
        return "Sell"


def main():
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"

    logging.info(f"Processing data for ticker: {ticker}")
    raw_data = get_selected_parameters(ticker)

    if "error" in raw_data:
        logging.error(raw_data["error"])
        return

    processed_data = preprocess_stock_data(raw_data)
    stock_name = processed_data.get("Stock Name", ticker)  # Use dynamic stock name

    # Calculate stock rating
    stock_rating = calculate_rating(
        processed_data.get("P/E Ratio"),
        processed_data.get("Debt-to-Equity"),
        processed_data.get("Year-on-Year Growth (%)"),
        processed_data.get("Analyst Rating")
    )

    # Map the rating to a label
    rating_label = map_rating_label(stock_rating)

    # Create the prompt
    prompt = create_prompt(stock_name, processed_data, stock_rating, rating_label)
    print("Generated Prompt:\n")
    print(prompt)

if __name__ == "__main__":
    main()
