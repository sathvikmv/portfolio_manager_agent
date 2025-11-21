import os
from groq import Groq
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read API key from .env
GROQ_KEY = os.getenv("GROQ_API_KEY")

# Initialize client
client = Groq(api_key=GROQ_KEY)

# ---------------------------------------------------------
# GENERAL CHATBOT
# ---------------------------------------------------------
def ask_ai(question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error in ask_ai: {e}"


# ---------------------------------------------------------
# PORTFOLIO RECOMMENDATION
# ---------------------------------------------------------
def investment_recommendation(df_units, df_risk):
    prompt = f"""
    Analyze this user's investment portfolio:

    --- Units Owned ---
    {df_units.to_string(index=False)}

    --- Risk Metrics ---
    {df_risk.to_string(index=False)}

    Provide:
    - Overweight assets
    - Underweight assets
    - Risk explanation
    - Increase / decrease suggestions
    - Final portfolio balancing advice
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error in investment_recommendation: {e}"
