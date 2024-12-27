# Stock Rating System

The **Stock Rating System** is a user-friendly web application that allows users to analyze stock metrics and receive a comprehensive rating. It leverages AI to provide insights, helping users make informed decisions about their stock investments.

## Features

- **Stock Analysis**: Fetches key financial metrics such as P/E Ratio, Debt-to-Equity, Year-on-Year Growth, and Analyst Ratings.
- **AI-Powered Insights**: Generates a detailed analysis using Groq Cloud LLM.
- **User Recommendations**: Provides actionable insights, mapping numerical ratings to descriptive labels like "Strong Buy" or "Sell".
- **Interactive Visuals**: Displays key metrics in a bar chart for easy interpretation.

## Tech Stack

- **Python**: Backend development and stock data preprocessing.
- **Streamlit**: User interface for seamless interactions.
- **yFinance**: Fetches stock data and financial metrics.
- **Groq Cloud**: AI model used for generating stock analysis reports.
- **Other Libraries**: pandas, dotenv, etc.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- Required Python libraries listed in `requirements.txt`
- Groq Cloud API key and model name stored in a `.env` file.

## Screenshots

### Stock Analysis Interface
![Screenshot](images/Screenshot%202024-12-26%20172638.png)

### Key Metrics Bar Chart
![Screenshot](images/Screenshot%202024-12-26%20172732.png)

### Detailed AI Analysis
![Screenshot](images/Screenshot%202024-12-26%20172814.png)

### Sidebar Input
![Screenshot](images/Screenshot%202024-12-26%20173017.png)

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/stock-rating-system.git

