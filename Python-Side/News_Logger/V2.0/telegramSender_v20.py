import re
import time
import requests

# Replace with your bot's token and chat ID
BOT_TOKEN = "7433459681:AAHBnT3Xg0Vyum9dmy9UEBYfC7JXfxvtLHk"
CHAT_ID = "-1002365804593"
FILE_PATH = "news_content.txt"
FILE_TGCHECK = "telegramCheck.txt"

# Telegram bot API URL
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}"

def read_integers_from_file(file_path):
    """Reads two integers from a file, expecting them to be on a single line separated by space."""
    with open(file_path, 'r') as file:
        # Read the line and split it into parts based on spaces
        line = file.readline().strip()
        num1, num2 = map(int, line.split())  # Convert each part into an integer
    return num1, num2

# Function to parse the file and return new entries as a dictionary
def parse_news_file(file_path):
    """Parses the news file and returns a dictionary of news."""
    news_dict = {}
    with open(file_path, "r") as file:
        content = file.read()
        # Regex to match news entries
        matches = re.findall(r"NEWScounter\s*=\s*(\d+)\n(.*?)=+", content, re.DOTALL)
        for match in matches:
            counter, news = match
            counter = int(counter)
            # Extract the first two sentences
            first_two_sentences = ". ".join(news.strip().split(". ")[:2])
            news_dict[counter] = first_two_sentences.strip()
    return news_dict

# Send a message via Telegram Bot API using requests
def send_telegram_message(message):
    """Sends a message to a Telegram channel using the Telegram Bot API."""
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
    """Monitors the file for new entries and sends them to Telegram."""
    try:
        # Parse file for new entries
        news_dict = parse_news_file(file_path)
        if news_dict:
            for counter, news in news_dict.items():
                # Read integers from the telegram check file
                num1, num2 = read_integers_from_file(FILE_TGCHECK)
                # Construct the message
                if num1 > 0:
                    message = f"Relativity: {num1} Positivity: {num2}\nVersion 2.1\n{news}"
                    # Send the message
                    send_telegram_message(message)

    except Exception as e:
        print(f"Error: {e}")

# Run the file monitor
if __name__ == "__main__":
    monitor_file(FILE_PATH)

