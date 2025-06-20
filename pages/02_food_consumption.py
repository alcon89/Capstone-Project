import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Ensure necessary NLTK resources are available
def ensure_nltk_resource(resource, path):
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(resource)

ensure_nltk_resource('punkt', 'tokenizers/punkt')
ensure_nltk_resource('stopwords', 'corpora/stopwords')
ensure_nltk_resource('wordnet', 'corpora/wordnet')

import streamlit as st
import requests
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import os
import re

st.markdown("---")
st.title("Food Consumption & Sentiment Tracker")

st.markdown("""
**Purpose**: Monitor what Malaysians are eating and talking about.

**Components**:
- Top Trending Food Keywords (from web scraping)
- Sentiment Trend Line: Healthy vs Unhealthy mentions
- Fast Food vs Home Cooked Meal Frequency (simulated)

Note: please give few moments for the page to load the web scrapping + NLTK elements
""")

# Scrape and clean text from food-related blogs
urls = [
    "https://www.travejar.com/blog/",
    "https://morueats.com/blogs/",
    "https://www.thestar.com.my",
    "https://www.eatdrink.my/kl/",
    "https://klfoodie.com",
    "https://www.bangsarbabe.com",
    "https://www.kenhuntfood.com/",
    "https://www.theyumlist.net/",
    "https://www.malaysianfoodie.com",
    "https://penangfoodie.com/",
    "https://themalaysiankitchen.com/",
    "https://www.migrationology.com/kuala-lumpur-travel-guide-food-lovers/",
    "https://www.marionskitchen.com/category/malaysian-cuisine/",
    "https://www.seriouseats.com/malaysian-recipes-5117240",
    "https://hungrygowhere.com/tag/malaysia/",
    "https://www.bibzeats.com/",
]

def scrape_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find('article') or soup.find('main')
        return article.get_text() if article else soup.get_text()
    except:
        return ""

corpus = " ".join([scrape_text(url) for url in urls])
custom_stopwords = set(["malaysia", "malaysian", "connect", "market", "consumer", "trend", "year", "industry", "data", "price", "products", "meal"])

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Manual two-step tokenization
    sentences = sent_tokenize(text, language="english")  # Forces use of punkt/english.pickle
    tokens = []
    for sentence in sentences:
        tokens.extend(word_tokenize(sentence, language="english"))

    stop_words = set(stopwords.words("english")).union(custom_stopwords)
    return [w for w in tokens if w not in stop_words and len(w) > 2]

tokens = clean_text(corpus)
lemmatizer = WordNetLemmatizer()
tokens = [lemmatizer.lemmatize(w) for w in tokens]

food_keywords = set([
    'plantbased', 'vegan', 'mala', 'matcha', 'nasi', 'lemak', 'ayam', 'sambal', 'oat', 'bubble', 'tea',
    'salted', 'egg', 'glutenfree', 'keto', 'tofu', 'durian', 'kopi', 'noodles', 'biryani', 'curry',
    'rendang', 'satay', 'hawker', 'bak', 'kueh', 'soup', 'fried', 'steamed', 'spicy', 'local', 'fusion',
    'sugar', 'snacks', 'herbs', 'tempeh', 'jackfruit', 'mushroom', 'grains', 'greens', 'fruit',
    'char kway teow', 'roti canai', 'maggi goreng', 'asam laksa', 'cendol', 'mee goreng',
    'ikan bakar', 'nasi kerabu', 'laksa johor', 'belacan', 'gula melaka', 'pandan', 'lemongrass',
    'tamarind', 'ikan bilis', 'onde-onde', 'pisang goreng', 'ice kacang', 'ais batu campur',
    'milo dinosaur', 'teh tarik', 'bandung', 'white coffee', 'deepfried', 'grilled', 'braised', 'stirfried'
])

tokens = [w for w in tokens if w in food_keywords]
word_freq = Counter(tokens)

if not tokens:
    st.warning("No food-related keywords found in the scraped content.")
    st.stop()

st.subheader("Top Trending Food Keywords")
wordcloud = WordCloud(width=600, height=300, background_color='white').generate_from_frequencies(word_freq)
st.image(wordcloud.to_array(), use_container_width=True)

with st.spinner("Scraping food blogs... please wait."):
    corpus = " ".join([scrape_text(url) for url in urls])
