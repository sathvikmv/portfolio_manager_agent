import streamlit as st
from ai_engine import ask_ai

st.title("🤖 AI Chatbot Assistant")

query = st.text_input("Ask something about investing:")

if st.button("Ask"):
    if query.strip() == "":
        st.warning("Please enter a question.")
    else:
        response = ask_ai(query)
        st.write(response)
