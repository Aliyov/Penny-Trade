import numpy as np
import matplotlib.pyplot as plt
import re
import sys

def calculate_sma(prices, window_length):
    """Helper function to calculate Simple Moving Average (SMA)."""
    sma = np.convolve(prices, np.ones(window_length) / window_length, mode='valid')
    
    # Pad the moving average with None to align with the original array length
    pad_length = len(prices) - len(sma)
    return [None] * pad_length + list(sma)

def three_musketeers_indicator(prices, ma200_length=200, ma30_length=17):
    """Implements the Three Musketeers trading logic."""
    # Calculate moving averages
    ma200 = calculate_sma(prices, ma200_length)
    ma30 = calculate_sma(prices, ma30_length)

    # Adjusted moving averages
    ma200_div2 = [x / 1.1 if x is not None else None for x in ma200]
    ma200_mul2 = [x * 1.1 if x is not None else None for x in ma200]

    return ma200_div2, ma200_mul2, ma30

def visualize_prices_with_trading_logic(filename):
    try:
        # Read prices from the specified text file
        with open(filename, 'r') as file:
            prices = []
            for line in file:
                match = re.search(r'Price \[\d+\]: (\d+),', line)
                if match:
                    prices.append(int(match.group(1)))
                else:
                    print(f"Warning: No price found in line: {line.strip()}")

        if not prices:
            print("No prices found in the file.")
            return

        # Prepare data for plotting
        x = list(range(1, len(prices) + 1))

        # Calculate moving averages and indicators
        ma200_div2, ma200_mul2, ma30 = three_musketeers_indicator(prices)

        # Initialize trading variables
        balance = 100.0
        trade_size = None
        buy_price = None
        last_signal = None
        trade_counter = 0

        # Plotting setup for dark theme
        plt.style.use('dark_background')
        plt.figure(figsize=(12, 6))

        # Plot the price
        plt.plot(x, prices, label="Price", color='white', alpha=0.5)

        # Plot moving averages
        plt.plot(x, ma200_div2, label="MA 200 Divided by 1.1", color='blue', linewidth=2)
        plt.plot(x, ma200_mul2, label="MA 200 Multiplied by 1.1", color='red', linewidth=2)
        plt.plot(x, ma30, label="MA 30", color='green', linewidth=2)

        # Trading logic
        for i in range(1, len(prices)):
            if i >= len(ma200_div2) or i >= len(ma30):
                break

            # Skip comparison if either moving average is None
            if ma30[i] is None or ma200_div2[i] is None or ma30[i - 1] is None or ma200_div2[i - 1] is None:
                continue

            # BUY signal
            if ma30[i] > ma200_div2[i] and ma30[i - 1] <= ma200_div2[i - 1]:
                if last_signal != "BUY":  # Prevent duplicate BUYs
                    trade_counter += 1
                    trade_size = balance / prices[i]
                    buy_price = prices[i]
                    last_signal = "BUY"
                    plt.text(x[i], prices[i], f'{trade_counter} - BUY\nPrice: {prices[i]} USD\nPut: {balance:.2f} USD',
                             color='green', fontsize=10, ha='center', va='bottom', bbox=dict(facecolor='white', alpha=0.5, edgecolor='green'))

            # SELL signal
            if ma30[i] < ma200_mul2[i] and ma30[i - 1] >= ma200_mul2[i - 1]:
                if last_signal == "BUY":  # Only sell after a buy
                    sell_value = trade_size * prices[i]
                    profit = sell_value - balance
                    potential_profit_percentage = profit / balance * 100
                    if potential_profit_percentage >= 10:  # Only sell if profit >= 10%
                        trade_counter += 1
                        plt.text(x[i], prices[i], f'{trade_counter} - SELL\nPrice: {prices[i]} USD\nTake: {sell_value:.2f} USD\nProfit: {profit:.2f} USD\n{potential_profit_percentage:.2f}%',
                                 color='red', fontsize=10, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.5, edgecolor='red'))
                        balance = sell_value
                        trade_size = None
                        last_signal = "SELL"

        # Add labels and title
        plt.title('Three Musketeers Trading Visualization', color='white')
        plt.xlabel('Data Index', color='white')
        plt.ylabel('Price', color='white')
        plt.legend(loc='upper left')
        plt.grid(True)

        # Show the plot
        plt.show()

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except ValueError:
        print(f"Error: File '{filename}' contains invalid data.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        filename = sys.argv[1]
        visualize_prices_with_trading_logic(filename)
