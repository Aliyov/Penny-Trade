import torch
from transformers import pipeline
import requests

def fetch_news_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article: {e}")
        return ""

def truncate_text(text, max_tokens=512):
    return text[:max_tokens]

def analyze_sentiment(text):
    # Initialize the sentiment analysis pipeline with a BERT model
    sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    result = sentiment_model(text)
    return result

def summarize_text(text):
    # Initialize the summarization pipeline
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    summary = summarizer(text, max_length=80, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def score_sentiment(sentiment_result):
    label = sentiment_result[0]["label"]
    score = int(label.split()[0])  # Assuming the label is in the format like '4 stars'
    return score

def main(url):
    article_text = fetch_news_article(url)
    if not article_text:
        print("Failed to fetch article. Exiting.")
        return

    # Truncate the article to fit model's max input length
    truncated_text = truncate_text(article_text)

    # Sentiment analysis on truncated text
    sentiment_result = analyze_sentiment(truncated_text)
    score = score_sentiment(sentiment_result)


    summary = summarize_text(truncated_text)
    print("Scoring\n1-Strongly Negative\n2-Negative\n3-Neutral\n4-Positive\n5-Strongly Positive\n")
    print(f"Scoring (out of 5): {score}")
    print(f"Reliability: {sentiment_result}")
    print(f"Summarization: {summary}")


news_url = "https://www.politifact.com/article/2024/oct/14/a-third-assassination-attempt-against-trump-heres/"  # Replace with a real news URL
#news_url = "https://www.bbc.com/news/live/cly0gzxgzrmt"
#news_url = "https://www.theguardian.com/world/2024/nov/25/dhl-cargo-plane-crashes-near-lithuania-airport"
main(news_url)

