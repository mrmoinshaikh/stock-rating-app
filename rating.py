# rating.py
def calculate_rating(pe_ratio, debt_to_equity, yoy_growth, analyst_rating):
    # Validate and assign default values if necessary (already handled in preprocess_stock_data)
    
    total_score = 0

    # P/E Ratio Rating Logic
    if pe_ratio < 15:
        total_score += 9
    elif 15 <= pe_ratio <= 25:
        total_score += 7
    elif 25 < pe_ratio <= 35:
        total_score += 5
    else:
        total_score += 2

    # Debt-to-Equity Rating Logic
    if debt_to_equity < 50:
        total_score += 9
    elif 50 <= debt_to_equity <= 100:
        total_score += 6
    elif 100 < debt_to_equity <= 150:
        total_score += 4
    else:
        total_score += 1

    # YoY Growth Rating Logic
    if yoy_growth > 15:
        total_score += 9
    elif 10 < yoy_growth <= 15:
        total_score += 7
    elif 5 < yoy_growth <= 10:
        total_score += 5
    else:
        total_score += 2

    # Analyst Rating Logic
    if analyst_rating.lower() == "buy":
        total_score += 8
    elif analyst_rating.lower() == "neutral":
        total_score += 5
    elif analyst_rating.lower() == "sell":
        total_score += 2
    else:
        total_score += 5  # Default for unexpected values

    # Normalize the score to a 1-10 scale
    final_rating = total_score / 4
    final_rating = round(final_rating)

    # Ensure rating stays within the 1-10 range
    final_rating = max(1, min(final_rating, 10))

    return final_rating
