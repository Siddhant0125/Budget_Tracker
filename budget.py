import streamlit as st
from groq import Groq

# Fetch the API key from Streamlit Secrets
import os
os.environ['GROQ_API_KEY'] = st.secrets["GROQ_API_KEY"]
# print(f"API Key: {api_key}")
# Initialize Groq API client
client = Groq()
response = client.chat.completions.create(model="llama3-8b-8192",
messages=[
    {"role": "system", "content": "You are a medical assistant AI with expertise in prognosis, diagnosis, and medication recommendations."},
    {"role": "user", "content": "i am having headache"}
]
)
analysis = response['choices'][0]['message']['content']
print(analysis)
