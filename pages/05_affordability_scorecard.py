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
st.title("Affordability & Accessibility Scorecard")

st.markdown("""
**Components**:
- Trends in Food Pricing: Plant vs. Animal-Based Commodities (interactive)
- Price Index (Table with colour grading)
- Volatility Insights (Table with colour grading)
""")

price_df = pd.read_csv("00_Datasets/05 Food Price/producer-prices_mys.csv")
price_df.columns = price_df.columns.str.strip().str.lower().str.replace(" ", "_")

# Interactive Trend Line Chart: Plant vs Animal Based
ppi_df = price_df[price_df['element'] == 'Producer Price Index (2014-2016 = 100)'].copy()
ppi_df['value'] = pd.to_numeric(ppi_df['value'], errors='coerce')
ppi_df = ppi_df.dropna(subset=['value', 'year'])

plant_keywords = [
    "vegetable", "legume", "fruit", "cruciferous", "greens", "beans",
    "nuts", "seeds", "herb", "spices", "whole grain", "maize", "cassava", "ginger",
    "lettuce", "mangoes", "cabbages", "carrots", "broccoli", "cucumbers",
    "cauliflowers", "bananas", "eggplants", "leeks", "coffee", "cocoa", "coconut",
    "pepper", "asparagus", "corn", "turnips", "chillies", "onion", "garlic"
]
animal_keywords = [
    "meat", "egg", "milk", "dairy", "livestock", "buffalo", "cattle", "chicken", "duck", "goat", "pig", "horse"
]

def classify_item(item):
    item_lower = str(item).lower()
    if any(k in item_lower for k in plant_keywords):
        return "Plant-Based"
    elif any(k in item_lower for k in animal_keywords):
        return "Animal-Based"
    else:
        return "Other"

ppi_df['category'] = ppi_df['item'].apply(classify_item)
filtered_ppi = ppi_df[ppi_df['category'].isin(['Plant-Based', 'Animal-Based'])]
avg_ppi = filtered_ppi.groupby(['year', 'category'])['value'].mean().reset_index()
avg_ppi.columns = ['Year', 'Food Category', 'Producer Price Index']

st.subheader("Trends in Food Pricing: Plant vs. Animal-Based Commodities")
fig_ppi = px.line(
    avg_ppi,
    x='Year',
    y='Producer Price Index',
    color='Food Category',
    title="Time Series of Producer Price Index in Malaysia by Food Category",
    markers=True
)
st.plotly_chart(fig_ppi, use_container_width=True)

# Two Column Tables
col5, col6 = st.columns(2)

with col5:
    st.subheader("Top 20 Commodities by Average Producer Price Index")
    avg_price_by_commodity = (
        filtered_ppi.groupby(['item', 'category'])['value']
        .mean()
        .reset_index()
        .rename(columns={'value': 'Value'})
        .sort_values(by='Value', ascending=False)
    )
    st.dataframe(
        avg_price_by_commodity.head(20).style
        .format({"Value": "{:.2f}"})
        .background_gradient(cmap="YlOrRd", subset="Value")
    )

with col6:
    st.subheader("Top 20 Commodities by Price Volatility (Standard Deviation)")
    volatility_df = (
        filtered_ppi.groupby(['item', 'category'])['value']
        .std()
        .reset_index()
        .rename(columns={'value': 'Volatility'})
        .sort_values(by='Volatility', ascending=False)
    )
    volatility_df['Volatility'] = volatility_df['Volatility'].round(2)
    st.dataframe(
        volatility_df.head(20).style
        .format({"Volatility": "{:.2f}"})
        .background_gradient(cmap="YlOrRd", subset="Volatility")
    )
