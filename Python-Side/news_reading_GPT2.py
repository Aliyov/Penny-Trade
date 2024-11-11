from transformers import pipeline
import requests
from time import sleep

# Define GPT-2 generator
gpt2_generator = pipeline("text-generation", model="gpt2")

# Function to generate text (or simulate a summary) using GPT-2
def generate_text(prompt):
    return gpt2_generator(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]

# Function to generate a summary with GPT-2
def summarize_with_gpt2(text):
    prompt = f"Summarize the following news article:\n\n{text}\n\nSummary:"
    return generate_text(prompt)

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

def main(url):
    article_text = fetch_news_article(url)
    if not article_text:
        print("Failed to fetch article. Exiting.")
        return

    truncated_text = truncate_text(article_text)

    # Generate a GPT-2-based summary
    summary = summarize_with_gpt2(truncated_text)

    print(f"GPT-2 Generated Summary: {summary}")
    print(url)

def fetch_news_data(api_key, url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

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

def callMain2():
    api_key = "pub_58917cdb453f9da429d45bd3e56b11450dc11"
    query_url = f"https://newsdata.io/api/1/news?apikey={api_key}&country=il,ua&language=en&category=business"
    
    while True:
        fetch_news_data(api_key, query_url)
        sleep(30)  # Sleep for 30 seconds for testing (5 minutes in production)

def callMain():
    demo_url = "https://www.bbc.co.uk/news/live/czxrnw5qrprt"
    fetch_news_article(demo_url)

# Example usage
callMain()
