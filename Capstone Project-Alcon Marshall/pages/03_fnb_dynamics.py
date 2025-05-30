import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import ast
import nltk
import re
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import plotly.express as px

st.markdown("---")
st.title("F&B Industry Dynamics")

st.markdown("""
**Purpose**: Show how food access and commercialization impacts health.

**Focus**:
- Gross Output by Industry (2010–2017)
- Number of Establishments by Industry (2010–2017)
""")

industry_df = pd.read_csv("C:/Users/PC/02_Forward School/Capstone Project-Alcon Marshall/00_Datasets/02 F&B by Activity/dataset_stalls.csv")
industry_df = industry_df[(industry_df['Year'] >= 2010) & (industry_df['Year'] <= 2017)]
categories = [
    'Restaurants and restaurants cum night clubs',
    'Cafeterias/canteens',
    'Food stalls',
    'Fast food restaurants',
    'Ice cream trucks'
]
industry_df = industry_df[industry_df['Industry'].isin(categories)]

pivot_output = industry_df.pivot(index='Year', columns='Industry', values="Value of gross output (RM'000)").reset_index()
pivot_estab = industry_df.pivot(index='Year', columns='Industry', values='Number of establishments').reset_index()

col_ind1, col_ind2 = st.columns(2)

with col_ind1:
    st.subheader("Gross Output by Industry")
    fig_output = px.line(
        pivot_output,
        x='Year',
        y=pivot_output.columns[1:],
        markers=True,
        title="Gross Output by Industry (2010–2017)",
        labels={"value": "Gross Output (RM'000)", "variable": "Industry"}
    )
    st.plotly_chart(fig_output, use_container_width=True)

with col_ind2:
    st.subheader("Number of Establishments by Industry")
    fig_estab = px.line(
        pivot_estab,
        x='Year',
        y=pivot_estab.columns[1:],
        markers=True,
        title="Number of Establishments by Industry (2010–2017)",
        labels={"value": "Establishments", "variable": "Industry"}
    )
    st.plotly_chart(fig_estab, use_container_width=True)
