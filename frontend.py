import os

import streamlit as st
from dotenv import load_dotenv

from f1.ai import FormulaOneAI
from f1.functions import f1_data

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

f1_ai = FormulaOneAI(openai_api_key, f1_data)

st.write("Ask anything about F1")
question = st.text_input("Formula 1 Question:", "What is the current driver standings?")

if st.button("Submit"):
    response = f1_ai.ask(question)
    st.markdown(response)

st.write("Messages")
st.write(f1_ai.messages)
