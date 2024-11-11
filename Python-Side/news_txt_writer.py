import requests
from bs4 import BeautifulSoup

def fetch_bbc_news_links():
    url = "https://www.bbc.com/business"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all anchor tags and filter based on presence of href
        links = soup.find_all('a', href=True)
        
        # Open the text file for writing
        with open('bbc_news_links.txt', 'w') as file:
            for link in links:
                href = link.get('href')
                if href and href.startswith('/'):
                    full_url = f"https://www.bbc.com/{href}"
                    file.write(full_url + '\n')
        
        print("BBC news links saved to 'bbc_news_links.txt'.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Call the function
fetch_bbc_news_links()
