import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

# Define the API key and endpoint
API_KEY = "bc6a8eaddc7aed3ed4a9150079a8addf"
ENDPOINT = "https://gnews.io/api/v4/search"
OUTPUT_FILE = "news_content.txt"
URL_LOG_FILE = "news_urls.txt"

# Parameters for the API request
parameters = {
    "apikey": API_KEY,    # API Key
    "q": "example",       # Search query
    "lang": "en",         # Language (English)
    "country": "us",      # Country code
    "max": 10             # Maximum number of results
}

# Initialize the global variables
logged_urls = set()
DATE_THRESHOLD = datetime.strptime("2024-11-10", "%Y-%m-%d")  # Define the cutoff date
news_counter = 1  # Default start for the news counter


def load_logged_data():
    """Load previously logged URLs and the last counter value."""
    global news_counter, logged_urls

    # Load URLs from URL log file
    try:
        with open(URL_LOG_FILE, "r", encoding="utf-8") as url_file:
            logged_urls = set(url.strip() for url in url_file if url.strip())
    except FileNotFoundError:
        pass  # If file doesn't exist, proceed with an empty set

    # Find the last used counter in the content file
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as content_file:
            for line in content_file:
                if line.startswith("NEWScounter = "):
                    news_counter = int(line.split('=')[1].strip()) + 1
    except FileNotFoundError:
        pass  # If file doesn't exist, start from counter 1


def fetch_full_content(url):
    """Fetch full article content from the URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Use BeautifulSoup to parse the HTML and extract the main content
        soup = BeautifulSoup(response.text, 'html.parser')
        article_text = ""
        
        # Extract text from paragraphs
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            article_text += p.get_text() + "\n"

        return article_text.strip()
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching full article content from URL: {e}")
        return None

def clear_file(file_path):
    """Clear the content of a file."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("")  # Write an empty string to clear the file



def fetch_and_write_news():
    global news_counter

    try:
        # Make the API request
        response = requests.get(ENDPOINT, params=parameters)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Check if articles exist in the response
        if "articles" in data:
            articles = data["articles"]
            file_path = "news_logger.txt"
            clear_file(file_path)


            with open(OUTPUT_FILE, "w", encoding="utf-8") as content_file, \
                 open(URL_LOG_FILE, "a", encoding="utf-8") as url_file:

                for article in articles:
                    # Get publication date, content, and URL
                    published_at = article.get("publishedAt", None)
                    content = article.get("content", "No Content Available")
                    url = article.get("url", "No URL Available")

                    # Skip if no date, content, or duplicate URL
                    if not published_at or not content or url in logged_urls:
                        continue

                    # Parse and filter by date
                    article_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                    if article_date < DATE_THRESHOLD:
                        continue

                    # Fetch the full content from the URL
                    full_content = fetch_full_content(url)
                    if not full_content:
                        print(f"Could not fetch full content for article: {url}")
                        continue

                    # Write the article to the files
                    formatted_content = f"URL: {url}\n\n{full_content}"
                    content_file.write(f"NEWScounter = {news_counter}\n")
                    content_file.write(formatted_content + "\n" + "=" * 80 + "\n")
                    url_file.write(url + "\n")

                    # Log the URL in the set and increment counter
                    logged_urls.add(url)
                    print(f"New article logged: {formatted_content[:50]}...")
                    news_counter += 1
                    return  # Log only one article and stop
        else:
            print("No articles found in the response.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


# Main execution loop
load_logged_data()  # Load previous logs and counter
try:
    #while True:
    fetch_and_write_news()
    time.sleep(5)  # Wait for 5 seconds before fetching again
except KeyboardInterrupt:
    print("News updating stopped.")
