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
st.title("📊 F&B Industry Revenue Trend (2010–2017)")

st.markdown("""
**Purpose**: Show which F&B category booming.

**Focus**:
- Gross Output by category (2010–2017)
""")

activity_df = pd.read_csv("C:/Users/PC/02_Forward School/Capstone Project-Alcon Marshall/00_Datasets/01 F&B by Industry/dataset _activity.csv")
activity_df = activity_df[(activity_df['Year'] >= 2010) & (activity_df['Year'] <= 2017)]

pivot_table = activity_df.pivot(index='Year', columns='Activity', values="Value of gross output (RM'000)").reset_index()
fig_rev = px.line(
    pivot_table,
    x='Year',
    y=pivot_table.columns[1:],
    markers=True,
    title="Value of Gross Output (2010–2017) by Category",
    labels={'value': "Gross Output (RM'000)", 'variable': 'Activity'}
)
st.plotly_chart(fig_rev, use_container_width=True)