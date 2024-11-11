import torch
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize
import requests

# Download NLTK data for sentence tokenization
try:
    nltk.download("punkt")
except Exception as e:
    print(f"Error downloading NLTK data: {e}")

def fetch_news_article(url):
    # This function simulates fetching a news article text from a URL
    # You would replace this with actual scraping code or an API request for real news sources.
    # Here, we'll use a placeholder text as an example.
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article: {e}")
        return ""

def summarize_article(article_text, max_sentences=3):
    sentences = sent_tokenize(article_text)
    summary = " ".join(sentences[:max_sentences])
    return summary

def analyze_sentiment(text):
    # Initialize the sentiment analysis pipeline with a BERT model
    sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    result = sentiment_model(text)
    return result

def score_sentiment(sentiment_result):
    # Extract the score from sentiment result
    label = sentiment_result[0]["label"]
    score = int(label.split()[0])  # Assuming the label is in the format like '4 stars'
    return score

def main(url):
    # Step 1: Fetch and summarize the article
    article_text = fetch_news_article(url)
    if not article_text:
        print("Failed to fetch article. Exiting.")
        return
    
    # If article is too short for summarization, handle it
    if len(article_text.split()) < 20:
        print("Article is too short to summarize. Exiting.")
        return

    summary = summarize_article(article_text)

    # Step 2: Analyze the sentiment of the summary
    sentiment_result = analyze_sentiment(summary)
    score = score_sentiment(sentiment_result)

    # Step 3: Display results
    print(f"Summary of the Article:\n{summary}\n")
    print(f"Sentiment Score (out of 5): {score}")
    print(f"Sentiment Analysis Details: {sentiment_result}")

# Example usage:
news_url = "https://edition.cnn.com/2024/11/11/politics/trump-massive-power-disruption-analysis/index.html"  # Replace with a real news URL
main(news_url)
