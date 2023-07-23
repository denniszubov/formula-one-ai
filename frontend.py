import streamlit as st
import pandas as pd

st.write("Ask anything about F1")
question = st.text_input('Formula 1 Question:', 'When was the last time Fernando Alonso won a race?')

st.write(f"Question = '{question}'")

st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))
