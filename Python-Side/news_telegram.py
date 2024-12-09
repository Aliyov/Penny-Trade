# This program send news url with sentiment analysis. Not comprehensive but only one works in AWS cloud t3.micro tier.
# Keeping it for further improvements. 

import os
import logging
import requests
from newspaper import Article
from textblob import TextBlob
from transformers import pipeline
import time

# Ensure the directory exists
log_directory = '/home/penguin/Trade/C/Python-side'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up logging to file
logging.basicConfig(filename=os.path.join(log_directory, 'news_logfile.log'),
                    level=logging.INFO, format='%(asctime)s - %(message)s')

# File to store URLs of sent articles
sent_articles_file = os.path.join(log_directory, 'sent_articles.txt')

# Load the list of sent articles
def load_sent_articles():
    if os.path.exists(sent_articles_file):
        with open(sent_articles_file, 'r') as file:
            return set(line.strip() for line in file.readlines())
    return set()

# Save the sent article URL
def save_sent_article(url):
    with open(sent_articles_file, 'a') as file:
        file.write(url + '\n')

# Send message to Telegram channel or group
def send_to_telegram(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown' 
    }
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        logging.info("Message successfully sent to Telegram group.")
    else:
        logging.error(f"Failed to send message. Status code: {response.status_code}")
        logging.error(response.json())  # Output the response for debugging

# Fetch news articles using GNews API
def fetch_news(api_token):
    url = f"https://gnews.io/api/v4/search?q=example&lang=en&country=us&max=10&apikey={api_token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        
        if 'articles' in news_data:
            logging.info(f"Fetched {len(news_data['articles'])} articles.")
            return news_data['articles']
        else:
            logging.warning("No articles found.")
            return []
    else:
        logging.error("Failed to fetch news. Response:", response.status_code, response.text)
        return []

# Analyze the content of the article
def analyze_news_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        text = article.text
        title = article.title
        if not text:
            logging.warning("No content found in the article.")
            return None
    except Exception as e:
        logging.error(f"Error extracting article: {e}")
        return None

    # Perform sentiment analysis
    blob = TextBlob(text)
    sentiment = blob.sentiment

    # Summarize the content
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)

    # Prepare the message to send to Telegram
    message = (f"Title: {title}\n\n"
               f"Summary: {summary[0]['summary_text']}\n\n"
               f"Sentiment Analysis:\n"
               f"Polarity: {sentiment.polarity} (ranges from -1 to 1)\n"
               f"Subjectivity: {sentiment.subjectivity} (ranges from 0 to 1)")

    return message

# Main function to fetch, analyze, and send articles
def main(api_token, bot_token, chat_id):
    sent_articles = load_sent_articles()
    
    while True:  # Infinite loop to keep the program running
        # Fetch news articles
        articles = fetch_news(api_token)  
        if not articles:
            logging.info("No articles found. Retrying...")
            time.sleep(60)  # Wait for a minute before retrying
            continue

        # Analyze the first article
        for article in articles:
            article_url = article['url']
            if article_url in sent_articles:
                logging.info(f"Article {article_url} already sent. Skipping...")
                continue

            logging.info(f"Analyzing article: {article_url}")
            message = analyze_news_article(article_url)

            # Send the summary to Telegram
            if message:
                send_to_telegram(bot_token, chat_id, message)
                save_sent_article(article_url)
                sent_articles.add(article_url)

            # Wait for 16 minutes 
            time.sleep(20)  

# Example usage
if __name__ == "__main__":
    api_token = "bc6a8eaddc7aed3ed4a9150079a8addf"  
    bot_token = "7433459681:AAHBnT3Xg0Vyum9dmy9UEBYfC7JXfxvtLHk"  
    chat_id = "-4796752894"  
    main(api_token, bot_token, chat_id)
