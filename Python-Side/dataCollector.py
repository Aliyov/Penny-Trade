import requests
import time

def get_btc_price():
    url = "https://min-api.cryptocompare.com/data/price"
    parameters = {
        'fsym': 'BTC',  # From symbol: Bitcoin
        'tsyms': 'USD'  # To symbol: US Dollar
    }
    
    try:
        response = requests.get(url, params=parameters)
        # Check if the response is successful (status code 200)
        if response.status_code != 200:
            print(f"Error: Failed to fetch data (Status code: {response.status_code})")
            return None
        
        data = response.json()
        
        # Check if 'USD' key exists in the response
        if "USD" in data:
            return data["USD"]
        else:
            print("Error: 'USD' key not found in the response.")
            return None
    except requests.exceptions.RequestException as e:
        # Handle any other issues that occur during the request
        print(f"Error: {e}")
        return None

def write_price_to_file():
    with open("btc_price.txt", "a") as file:
        while True:
            price = get_btc_price()
            if price is not None:
                file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - BTC Price: ${price}\n")
                print(f"Logged BTC price: ${price}")
            else:
                print("Could not retrieve the BTC price.")
            time.sleep(5)  # Log every 5 seconds (adjust as needed)

write_price_to_file()
