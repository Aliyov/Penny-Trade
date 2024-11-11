import requests
from time import sleep
from transformers import pipeline
import json

# Sentiment analysis and summarization functions
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
    sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    result = sentiment_model(text)
    return result

def summarize_text(text):
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

    truncated_text = truncate_text(article_text)

    sentiment_result = analyze_sentiment(truncated_text)
    score = score_sentiment(sentiment_result)

    summary = summarize_text(truncated_text)

    print(f"Sentiment Score (out of 5): {score}")
    print(f"Sentiment Analysis Details: {sentiment_result}")
    print(f"Summarize: {summary}")
    print(url)

def fetch_news_data(api_key, url):
    try:
        # Make a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check for any request errors

        # Extract the JSON content from the response
        data = response.json()

        # Check if 'results' key exists and process the links
        if data.get("results"):
            links = [article.get("link") for article in data["results"] if article.get("link")]
            if links:
                for link in links:
                    main(link)
            else:
                print("No links found in the response.")
        else:
            print("'results' field is missing or empty.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")


def callMain():
    api_key = "pub_58917cdb453f9da429d45bd3e56b11450dc11"
    query_url = f"https://newsdata.io/api/1/news?apikey={api_key}&country=il,ua&language=en&category=business"
    
    while True:
        fetch_news_data(api_key, query_url)
        sleep(30)  # Sleep for 5 minutes before fetching again

# Example usage
callMain()
