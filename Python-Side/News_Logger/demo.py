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
    with open(file_path, 'r') as file:
        # Read the integers from the file
        num1 = int(file.readline().strip())  # Read first integer
        num2 = int(file.readline().strip())  # Read second integer
    return num1, num2

# Example usage
num1, num2 = read_integers_from_file(file_path)
print(f"Read integers: {num1}, {num2}")


# Function to parse the file and return new entries as a dictionary
def parse_news_file(file_path):
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
    try:
        # Parse file for new entries
        news_dict = parse_news_file(file_path)
        if news_dict:
            for counter, news in news_dict.items():
                num1, num2 = readSentinent(FILE_TGCHECK)
                message = f"Relativity: num1 Positivity: num2 {news}"
                send_telegram_message(message)  # Send new news entry

    except Exception as e:
        print(f"Error: {e}")

# Run the file monitor
if __name__ == "__main__":
    monitor_file(FILE_PATH)

