import os

import streamlit as st
from dotenv import load_dotenv

from f1.ai import FormulaOneAI
from f1.functions import f1_data

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

f1_ai = FormulaOneAI(openai_api_key, f1_data)

st.title("Formula One AI")

response = None

with st.form(key="my_form"):
    user_input = st.text_input(
        "Formula 1 Question:",
        "Who won the 2023 Spanish Grand Prix?",
    )
    submit_button = st.form_submit_button("Submit")
    question = user_input.strip()

    if submit_button:
        response = f1_ai.ask(question)

if response:
    st.markdown(response)

st.write("---")

if f1_ai.messages:
    st.markdown("**Messages:**")
    st.write(f1_ai.messages)
