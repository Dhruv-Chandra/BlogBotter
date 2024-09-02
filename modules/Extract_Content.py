from bs4 import BeautifulSoup
import requests
import re
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.corpus import stopwords
from collections import Counter
import streamlit as st


@st.cache_data
def fetch_and_process_url(url):
    stop_words = set(stopwords.words("english"))
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract text, excluding script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()

        text = soup.get_text()
        words = re.findall(r'\b\w+\b', text.lower())
        return [lemmatizer.lemmatize(word) for word in words if word not in stop_words and len(word) > 1]
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

@st.cache_data
def get_most_common_keywords(urls, top_n=10):
    word_counter = Counter()
    for url in urls:
        word_counter.update(fetch_and_process_url(url))
    words = [x[0] for x in word_counter.most_common(top_n)]
    # print(words)
    return words