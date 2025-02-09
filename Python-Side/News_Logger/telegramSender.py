import re
import time
import requests

# Replace with your bot's token and chat ID
BOT_TOKEN = "7433459681:AAHBnT3Xg0Vyum9dmy9UEBYfC7JXfxvtLHk"
CHAT_ID = "-1002365804593"
FILE_PATH = "news_content.txt"
FILE_TGCHECK = "telegramCheck.txt"
FILE_COUNTRIES = "countriesCheck.txt"

# Telegram bot API URL
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}"

# Global variable
num1 = 0  # Default value

def read_integers_from_file(file_path):
    """Reads two integers from a file, expecting them to be on a single line separated by space."""
    with open(file_path, 'r') as file:
        line = file.readline().strip()
        num1, num2 = map(int, line.split())  # Convert each part into an integer
    return num1, num2

def parse_countries_file(file_path):
    """Reads the countries file and returns a list of country names or 'NA' if specified."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if len(lines) == 1 and lines[0].strip() == "NA":
            return ["NA"]
        countries = [line.split()[0] for line in lines if len(line.split()) >= 2]
    return countries

def parse_news_file(file_path):
    """Parses the news file and returns a dictionary of news."""
    news_dict = {}
    with open(file_path, "r") as file:
        content = file.read()
        matches = re.findall(r"NEWScounter\s*=\s*(\d+)\n(.*?)=+", content, re.DOTALL)
        for match in matches:
            counter, news = match
            counter = int(counter)
            first_two_sentences = ". ".join(news.strip().split(". ")[:2])
            news_dict[counter] = first_two_sentences.strip()
    return news_dict

def send_telegram_message(message):
    """Sends a message to a Telegram channel using the Telegram Bot API."""
    global num1  # Access the global num1 variable
    if num1 > 0:
        payload = {
            'chat_id': CHAT_ID,
            'text': message
        }
        try:
            response = requests.post(API_URL, data=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")

def monitor_file(file_path):
    """Monitors the file for new entries and sends them to Telegram."""
    global num1  # Access and modify the global num1 variable
    try:
        # Parse the news file
        news_dict = parse_news_file(file_path)
        if news_dict:
            # Parse the countries file
            countries = parse_countries_file(FILE_COUNTRIES)
            countries_list = ", ".join(countries) if countries else "None"
            
            for counter, news in news_dict.items():
                # Read integers from the telegram check file
                num1, num2 = read_integers_from_file(FILE_TGCHECK)
                # Construct the message
                message = f">Relativity: {num1} Positivity: {num2}\n>Countries mentioned: {countries_list}\n______\nVersion 2.1\n_______\n{news}"
                # Send the message
                send_telegram_message(message)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    monitor_file(FILE_PATH)

