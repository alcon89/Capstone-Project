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

st.title("Agriculture & Trade Health")

st.markdown("""
**Purpose**: Track supply-side feasibility for plant-based transitions.

**Components**:
- Malaysia Overall Import & Export
- Malaysia Trade - Food & Live Animals
- Malaysia's Total Crop Production (2017–2022)
- Total Production by Crop Type (Log Scale)
""")

# Load real import/export data
trade_df = pd.read_csv("00_Datasets/04 Import Export/trade_sitc_1d.csv")

# Clean column names for safety
trade_df.columns = trade_df.columns.str.strip().str.lower().str.replace(" ", "_")

# Convert 'date' to 'year'
if 'date' in trade_df.columns:
    trade_df['year'] = pd.to_datetime(trade_df['date'], errors='coerce').dt.year

col1, col2 = st.columns(2)

with col1:
    st.subheader("Malaysia Overall Import & Export")
    if {'year', 'exports', 'imports'}.issubset(trade_df.columns):
        trade_overall = trade_df.groupby('year')[['exports', 'imports']].sum().reset_index()
        trade_overall.columns = ['Year', 'Exports (RM Billion)', 'Imports (RM Billion)']

        fig1 = px.line(
            trade_overall,
            x='Year',
            y=['Exports (RM Billion)', 'Imports (RM Billion)'],
            title="Malaysia Overall Trade (2000–2025)",
            markers=True,
            labels={"value": "Trade Value (RM Billion)", "variable": "Trade Type"}
        )
        fig1.update_layout(legend_title_text="Trade Type")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("Required columns missing for overall trade view.")

with col2:
    st.subheader("Malaysia Trade - Food & Live Animals")
    if {'year', 'section', 'exports', 'imports'}.issubset(trade_df.columns):
        # Use string match for section == '0'
        food_df = trade_df[trade_df['section'] == '0']
        food_summary = food_df.groupby('year')[['exports', 'imports']].sum().reset_index()
        food_summary.columns = ['Year', 'Exports (RM Billion)', 'Imports (RM Billion)']

        # Plotly interactive chart
        fig2 = px.line(
            food_summary,
            x='Year',
            y=['Exports (RM Billion)', 'Imports (RM Billion)'],
            title="Malaysia Trade – Food & Live Animals (2000–2025)",
            markers=True,
            labels={"value": "Trade Value (RM Billion)", "variable": "Trade Type"}
        )
        fig2.update_layout(legend_title_text="Trade Type")
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.warning("Required columns missing for food trade view.")

crop_df = pd.read_csv("00_Datasets/03 Crop Production/crops_state.csv")
crop_df.columns = crop_df.columns.str.strip().str.lower().str.replace(" ", "_")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Total Production by Crop Type")
    if 'crop_type' in crop_df.columns and 'production' in crop_df.columns:
        crop_type_totals = crop_df.groupby('crop_type')['production'].sum().reset_index().sort_values(by='production', ascending=False)
        fig_crop = px.bar(
            crop_type_totals,
            x='crop_type',
            y='production',
            title='Total Production by Crop Type (Log Scale)',
            log_y=True,
            labels={'production': 'Total Production (Metric Tonnes)', 'crop_type': 'Crop Type'}
        )
        fig_crop.update_traces(marker_color='lightblue')
        st.plotly_chart(fig_crop, use_container_width=True)
    else:
        st.warning("Required columns missing for crop type chart.")

with col4:
    st.subheader("Malaysia's Total Crop Production by Year (2017–2022)")
    if 'date' in crop_df.columns and 'production' in crop_df.columns:
        crop_df['year'] = pd.to_datetime(crop_df['date'], errors='coerce').dt.year
        crop_year_totals = crop_df.groupby('year')['production'].sum().reset_index()
        fig_year = px.line(
            crop_year_totals,
            x='year',
            y='production',
            title="Total Crop Production by Year",
            markers=True,
            labels={'production': 'Total Production (Metric Tonnes)', 'year': 'Year'}
        )
        fig_year.update_traces(line=dict(color='green'))
        st.plotly_chart(fig_year, use_container_width=True)
    else:
        st.warning("Required columns missing for yearly crop production chart.")
