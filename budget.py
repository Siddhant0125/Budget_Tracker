import streamlit as st
from groq import Groq

# Fetch the API key from Streamlit Secrets
import os
os.environ['GROQ_API_KEY'] = st.secrets["GROQ_API_KEY"]
# print(f"API Key: {api_key}")
# Initialize Groq API client
client = Groq()
