import plotly.graph_objects as go

# Read prices from the text file
with open('../Visualization/log8.txt', 'r') as file:
    prices = [int(line.strip()) for line in file if line.strip().isdigit()]

# Prepare the data for plotting
x = list(range(1, len(prices) + 1))

# Create the figure
fig = go.Figure()

# Plot the price increases (blue)
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

