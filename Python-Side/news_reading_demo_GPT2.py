import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Initialize the GPT-2 generator
gpt2_generator = pipeline("text-generation", model="gpt2")

# Set the pad token ID to the end-of-sequence token ID
gpt2_generator.model.config.pad_token_id = gpt2_generator.model.config.eos_token_id

def fetch_news_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Use BeautifulSoup to parse the HTML and extract text
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Assuming the article text is inside a <div> with class "article-body" (change as needed for the site structure)
        article_text = soup.get_text()
        return article_text.strip()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article: {e}")
        return ""

def truncate_text(text, max_tokens=512):
    # Truncate the text to fit within the specified token limit
    return text[:max_tokens]

def generate_commentary(text):
    prompt = f"Provide a creative commentary based on this news:\n\n{text}\n\nCommentary:"
    # Use `max_new_tokens` instead of `max_length`
    result = gpt2_generator(prompt, max_new_tokens=200, num_return_sequences=1, truncation=True)
    return result[0]["generated_text"]

def main(url):
    article_text = fetch_news_article(url)
    if not article_text:
        print("Failed to fetch article. Exiting.")
        return

    # Truncate the article text to fit model's max input length
    truncated_text = truncate_text(article_text)

    # Generate commentary using GPT-2
    commentary = generate_commentary(truncated_text)

    print("Generated Commentary:\n")
    print(commentary)

# Example usage:
news_url = "https://www.bbc.co.uk/news/live/czxrnw5qrprt"  # Replace with a real news URL
main(news_url)
