#it sends news but summary part has error !doctype error 
import os
import logging
import requests
from time import sleep
from transformers import pipeline
import time


# Telegram sending
def send_to_telegram(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'  # Optional: use Markdown for formatting
    }
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        logging.info("Message successfully sent to Telegram group.")
        print("Message successfully sent to Telegram.")
    else:
        logging.error(f"Failed to send message. Status code: {response.status_code}")
        logging.error(response.json())  # Output the response for debugging
        print(f"Failed to send message. Error: {response.json()}")


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

def main(url, bot_token, chat_id):
    article_text = fetch_news_article(url)
    if not article_text:
        print("Failed to fetch article. Exiting.")
        return

    truncated_text = truncate_text(article_text)

    sentiment_result = analyze_sentiment(truncated_text)
    score = score_sentiment(sentiment_result)

    summary = summarize_text(truncated_text)

    # Prepare the message to send
    message = (f"**Sentiment Analysis and Summary**\n\n"
               f"**Sentiment Score (out of 5):** {score}\n"
               f"**Summary:** {summary}\n\n"
               f"**URL:** {url}")

    # Send the summary and sentiment analysis to Telegram
    send_to_telegram(bot_token, chat_id, message)

def fetch_news_data(api_key, query_url, bot_token, chat_id):
    try:
        # Make a GET request to the URL
        response = requests.get(query_url)
        response.raise_for_status()  # Check for any request errors

        # Extract the JSON content from the response
        data = response.json()

        # Check if 'results' key exists and process the links
        if data.get("results"):
            links = [article.get("link") for article in data["results"] if article.get("link")]
            if links:
                for link in links:
                    main(link, bot_token, chat_id)
            else:
                print("No links found in the response.")
        else:
            print("'results' field is missing or empty.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")


def callMain():
    api_key = "pub_58917cdb453f9da429d45bd3e56b11450dc11"  # Replace with your News API key
    query_url = f"https://newsdata.io/api/1/news?apikey={api_key}&country=il,ua&language=en&category=business"
    bot_token = "7433459681:AAHBnT3Xg0Vyum9dmy9UEBYfC7JXfxvtLHk"  # Replace with your Telegram bot token
    chat_id = "-4796752894"  # Replace with your Telegram chat ID
    
    while True:
        fetch_news_data(api_key, query_url, bot_token, chat_id)
        sleep(30)  # Wait before fetching again

callMain()
