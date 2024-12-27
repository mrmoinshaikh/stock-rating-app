from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve the API key and model name from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("model_name")

# Initialize the Groq Cloud LLM
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name=model_name
)

def analyze_stock(prompt):
    """
    Pass the stock analysis prompt to the LLM and get a response.
    """
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error in LLM response: {str(e)}"
