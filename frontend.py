import os

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

from f1.ai import FormulaOneAI
from f1.functions import f1_data

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

f1_ai = FormulaOneAI(openai_api_key, f1_data)

st.title("Formula One AI")

response = None

# Directory where the graphs are stored
dir_name = "f1/graphs"

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

# Get list of all files inside graphs directory
files = os.listdir(dir_name)

# Get list of all png files
graphs = [f for f in files if f.endswith(".png")]

if graphs:
    st.markdown("**Generated Graphs:**")
    for graph in graphs:
        file_path = os.path.join(dir_name, graph)
        image = Image.open(file_path)
        st.image(image)

if f1_ai.messages:
    st.write("---")
    st.markdown("**Messages:**")
    st.write(f1_ai.messages)
