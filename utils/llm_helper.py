from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the Groq Cloud LLM
llm = ChatGroq(
    groq_api_key=os.getenv("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"),
    model_name="llama3-8b-8192"
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