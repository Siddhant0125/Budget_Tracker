import streamlit as st
from groq import Groq

# Fetch the API key from Streamlit Secrets
api_key = st.secrets["GROQ_API_KEY"]

# Initialize Groq API client
client = Groq(api_key=api_key)
