import sys
import re
import plotly.graph_objects as go

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

        # Add title and labels
        fig.update_layout(
            title='Price Trend Visualization',
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
