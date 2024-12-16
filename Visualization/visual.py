import sys
import re
import plotly.graph_objects as go
import numpy as np

def calculate_sma(prices, window_length):
    """Helper function to calculate Simple Moving Average (SMA)."""
    return np.convolve(prices, np.ones(window_length) / window_length, mode='valid')

def plot_custom_moving_averages(prices, ma200_length=200, ma30_length=17):
    """Plots custom moving averages and their modified versions."""
    
    # Calculate moving averages
    ma200 = calculate_sma(prices, ma200_length)
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

        # Create the figure
        fig = go.Figure()

        # Plot the price increases (green)
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:  # Price increase
                fig.add_trace(go.Scatter(
                    x=[x[i - 1], x[i]], y=[prices[i - 1], prices[i]],
                    mode='lines', line=dict(color='green'), showlegend=False
                ))

        # Plot the price decreases (red)
        for i in range(1, len(prices)):
            if prices[i] < prices[i - 1]:  # Price decrease
                fig.add_trace(go.Scatter(
                    x=[x[i - 1], x[i]], y=[prices[i - 1], prices[i]],
                    mode='lines', line=dict(color='red'), showlegend=False
                ))

        # Plot the moving averages
        fig.add_trace(go.Scatter(
            x=x[200-1:], y=ma200_div2, mode='lines', line=dict(color='blue', width=2),
            name="MA 100 Divided by 1.1"
        ))
        fig.add_trace(go.Scatter(
            x=x[200-1:], y=ma200_mul2, mode='lines', line=dict(color='red', width=2),
            name="MA 100 Multiplied by 1.1"
        ))
        fig.add_trace(go.Scatter(
            x=x[17-1:], y=ma30, mode='lines', line=dict(color='green', width=2),
            name="MA 30"
        ))
        
        

        # Add title and labels
        fig.update_layout(
            title='Price Trend Visualization with Custom Moving Averages',
            xaxis_title='Data Index',
            yaxis_title='Prices',
            template='plotly_dark'  # Dark background for better contrast
        )

        # Show the interactive chart
        fig.show()
    
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
