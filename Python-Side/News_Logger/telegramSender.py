import re
import time
import requests

# Replace with your bot's token and chat ID
BOT_TOKEN = "7433459681:AAHBnT3Xg0Vyum9dmy9UEBYfC7JXfxvtLHk"
CHAT_ID = "-4796752894"
FILE_PATH = "news_content.txt"
LAST_COUNTER_FILE = "last_counter.txt"

# Telegram bot API URL
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Load the last processed counter from file (if exists)
def load_last_counter():
    try:
        with open(LAST_COUNTER_FILE, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

# Save the last processed counter to file
def save_last_counter(counter):
    with open(LAST_COUNTER_FILE, "w") as file:
        file.write(str(counter))

# Function to parse the file and return new entries as a dictionary
def parse_news_file(file_path, last_news_counter):
    news_dict = {}
    with open(file_path, "r") as file:
        content = file.read()
        # Regex to match news entries
        matches = re.findall(r"NEWScounter\s*=\s*(\d+)\n(.*?)=+", content, re.DOTALL)
        for match in matches:
            counter, news = match
            counter = int(counter)
            if counter > last_news_counter:
                # Extract the first two sentences
                first_two_sentences = ". ".join(news.strip().split(". ")[:2])
                news_dict[counter] = first_two_sentences.strip()
    return news_dict

# Send a message via Telegram Bot API using requests
def send_telegram_message(message):
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(API_URL, data=payload)
        response.raise_for_status()  # Check for errors in the response
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

# Monitor the file for changes
def monitor_file(file_path):
    last_news_counter = load_last_counter()  # Load the last processed news counter
    #while True:
    try:
        # Parse file for new entries
        news_dict = parse_news_file(file_path, last_news_counter)
        if news_dict:
            for counter, news in news_dict.items():
                message = f"{news}"
                send_telegram_message(message)  # Send new news entry
            last_news_counter = max(news_dict.keys())  # Update last processed counter
            save_last_counter(last_news_counter)  # Save the new counter to file

    except Exception as e:
        print(f"Error: {e}")
        
        # Check for changes every 10 seconds
    #time.sleep(60 * 10)

# Run the file monitor
if __name__ == "__main__":
    monitor_file(FILE_PATH)
