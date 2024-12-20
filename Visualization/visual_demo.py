import sys
import re
import numpy as np
import matplotlib.pyplot as plt

def calculate_long_MA(prices, window_length, mul_val):
    if len(prices) < window_length:
        raise ValueError("Not enough data")

    long_ma = []
    sum_prices = 0
    upper_border = []
    down_border = []

    for i in range(len(prices)):
        if i < window_length:
            # Sum up the first `window_length` elements

            sum_prices += prices[i]
            long_ma.append(prices[i])
            
        else:
            # Calculate the moving average
            sum_prices += prices[i] - prices[i - window_length]
            long_ma.append(sum_prices / window_length)
            
        upper_border.append(round(long_ma[-1] * mul_val, 2))
        down_border.append(round(long_ma[-1] / mul_val, 2))

    return long_ma, upper_border, down_border

def calculate_short_MA(prices, window_length):
    if len(prices) < window_length:
        raise ValueError("Not enough data")

    short_ma = []
    sum_prices = 0

    for i in range(len(prices)):
        if i < window_length:
            sum_prices += prices[i]
            short_ma.append(prices[i])
        else:
            sum_prices += prices[i] - prices[i - window_length]
            short_ma.append(sum_prices / window_length)

    return short_ma

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

        x = list(range(1, len(prices) + 1))

        long_ma, upper_border, down_border = calculate_long_MA(prices, window_len_1, mul_val)
        short_ma = calculate_short_MA(prices, window_len_2)

        balance = 100.0
        trade_size = None
        buy_price = None
        last_signal = None
        trade_counter = 0

        plt.style.use('dark_background')
        plt.figure(figsize=(12, 6))

        # Plot the price
        plt.plot(x, prices, label="Price", color='white', alpha=0.5)
        plt.plot(x, down_border, label="Down Border", color='blue', linewidth=2)
        plt.plot(x, upper_border, label="Upper Border", color='red', linewidth=2)
        plt.plot(x, short_ma, label="Short MA", color='green', linewidth=2)

        for i in range(1, len(prices)):
            if short_ma[i] < down_border[i] and short_ma[i - 1] > down_border[i - 1]:
                if last_signal != "BUY":
                    trade_counter += 1
                    trade_size = balance / prices[i]
                    buy_price = prices[i]
                    last_signal = "BUY"
                    plt.text(x[i], prices[i], f'{trade_counter} - BUY\nPrice: {prices[i]} USD\nPut: {balance:.2f} USD',
                             color='green', fontsize=10, ha='center', va='bottom',
                             bbox=dict(facecolor='white', alpha=0.5, edgecolor='green'))

            if short_ma[i] < upper_border[i] and short_ma[i-1] > upper_border[i-1]:
                if last_signal == "BUY":
                    sell_value = trade_size * prices[i]
                    profit = sell_value - balance
                    potential_profit_percentage = profit / balance * 100
                    if potential_profit_percentage >= 10:
                        trade_counter += 1
                        plt.text(x[i], prices[i], f'{trade_counter} - SELL\nPrice: {prices[i]} USD\nTake: {sell_value:.2f} USD\nProfit: {profit:.2f} USD\n{potential_profit_percentage:.2f}%',
                                 color='red', fontsize=10, ha='center', va='top',
                                 bbox=dict(facecolor='white', alpha=0.5, edgecolor='red'))
                        balance = sell_value
                        trade_size = None
                        last_signal = "SELL"

        plt.title('Three Musketeers Trading Visualization', color='white')
        plt.xlabel('Data Index', color='white')
        plt.ylabel('Price', color='white')
        plt.legend(loc='upper left')
        plt.grid(True)
        plt.show()

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except ValueError:
        print(f"Error: File '{filename}' contains invalid data.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    window_len_1 = 200
    window_len_2 = 17
    mul_val = 1.1

    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        filename = sys.argv[1]
        visualize_prices_with_trading_logic(filename)
