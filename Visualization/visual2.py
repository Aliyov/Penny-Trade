import numpy as np
import matplotlib.pyplot as plt
import re
import sys

def calculate_sma(prices, window_length):
    """Helper function to calculate Simple Moving Average (SMA)."""
    return np.convolve(prices, np.ones(window_length) / window_length, mode='valid')

def plot_custom_moving_averages(prices, ma200_length=200, ma30_length=17):
    """Plots custom moving averages and their modified versions."""
    # Calculate moving averages
    ma200 = calculate_sma(prices, ma200_length)  # Correct ma200 for the 200-period moving average
    ma30 = calculate_sma(prices, ma30_length)

    # Calculate modified moving averages
    ma200_div2 = ma200 / 1.1
    ma200_mul2 = ma200 * 1.1

    return ma200_div2, ma200_mul2, ma30

def visualize_prices(filename):
    try:
        # Read prices from the specified text file
        with open(filename, 'r') as file:
            prices = []
            for line in file:
                # Match lines that contain 'Price' and extract the price using a regular expression
                match = re.search(r'Price \[\d+\]: (\d+),', line)
                if match:
                    prices.append(int(match.group(1)))  # Extracted price
                else:
                    print(f"Warning: No price found in line: {line.strip()}")
        
        # Check if prices were extracted
        if not prices:
            print("No prices found in the file.")
            return
        
        # Prepare the data for plotting
        x = list(range(1, len(prices) + 1))

        # Calculate the moving averages
        ma200_div2, ma200_mul2, ma30 = plot_custom_moving_averages(prices)

        # Initialize variables for signals
        buy_price = None
        last_signal = None

        # Plotting setup for dark theme
        plt.style.use('dark_background')
        plt.figure(figsize=(12, 6))
        
        # Plot the price
        plt.plot(x, prices, label="Price", color='white', alpha=0.5)

        # Plot the price increases (green) and decreases (red)
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:  # Price increase
                plt.plot([x[i - 1], x[i]], [prices[i - 1], prices[i]], color='green')
            elif prices[i] < prices[i - 1]:  # Price decrease
                plt.plot([x[i - 1], x[i]], [prices[i - 1], prices[i]], color='red')

        # Plot the moving averages
        plt.plot(x[len(x)-len(ma200_div2):], ma200_div2, label="MA 200 Divided by 1.1", color='blue', linewidth=2)
        plt.plot(x[len(x)-len(ma200_mul2):], ma200_mul2, label="MA 200 Multiplied by 1.1", color='yellow', linewidth=2)
        plt.plot(x[len(x)-len(ma30):], ma30, label="MA 30", color='orange', linewidth=2)

        # Buy and Sell Signals
        for i in range(1, len(prices)):
            if i >= len(ma200_div2) or i >= len(ma30):
                break
            # Ensure BUY signal when ma30 crosses ma200_div2 from above
            if ma30[i] > ma200_div2[i] and ma30[i - 1] <= ma200_div2[i - 1] and (last_signal == "SELL" or last_signal is None):
                buy_price = prices[i]
                last_signal = "BUY"
                plt.text(x[i], prices[i], 'BUY', color='green', fontsize=12, ha='center', va='bottom',bbox=dict(facecolor='white', alpha=0.5, edgecolor='green', boxstyle='round,pad=0.3'))

            # Ensure SELL signal when ma30 crosses ma200_mul2 from above and the price is at least 10% greater than the buy price
            if ma30[i] < ma200_mul2[i] and ma30[i - 1] >= ma200_mul2[i - 1] and last_signal == "BUY":
                if prices[i] >= buy_price * 1.1:  # 10% greater than BUY price
                    last_signal = "SELL"
                    plt.text(x[i], prices[i], 'SELL', color='red', fontsize=12, ha='center', va='top',bbox=dict(facecolor='white', alpha=0.5, edgecolor='red', boxstyle='round,pad=0.3'))

        # Add labels and title
        plt.title('Penny Trade Visualization', color='white')
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
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        filename = sys.argv[1]
        visualize_prices(filename)
