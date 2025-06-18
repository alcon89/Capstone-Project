import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import ast
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
import re
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import plotly.express as px

st.set_page_config(page_title="Plant Based Public Health Intelligence Hub", layout="wide")

st.title("Welcome to the Plant Based Public Health Intelligence Hub")
st.markdown("""
This public health intelligence platform is designed to explore the dynamics of Malaysia’s food system across trade, consumption, production, and pricing.
Use the **sidebar** to navigate across different analytical insights. Each section offers **interactive visualizations** powered by real datasets.

---
""")

st.subheader("🔍 Explore These Key Sections")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚜 Agriculture & Trade Health")
    st.markdown("""
    - Track Malaysia’s **import/export trends**
    - See **crop production patterns** (2017–2022)
    - Analyze **industry outputs** by segment
    """)

    st.markdown("### 📈 F&B Industry Dynamics")
    st.markdown("""
    - Compare **gross output** of food establishments
    - Track the **number of outlets** by type
    """)

with col2:
    st.markdown("### 🛒 Food Consumption & Sentiment Tracker")
    st.markdown("""
    - Analyze preferences: **Fast food vs Home cooked**
    - Review **sentiment scores** by food topic
    """)

    st.markdown("### 💸 Affordability & Accessibility Scorecard")
    st.markdown("""
    - Visualize **food price volatility** by commodity
    - Compare **plant vs animal-based food pricing**
    """)

st.markdown("---")
st.markdown("Built for data-informed policy and innovation. 📊")



