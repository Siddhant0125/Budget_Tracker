import streamlit as st
import datetime
import json
from collections import defaultdict
from groq import Groq
import pandas as pd
import plotly.express as px

# Fetch the API key from Streamlit Secrets
api_key = st.secrets["GROQ_API_KEY"]

# Initialize Groq API client
client = Groq(api_key=api_key)
