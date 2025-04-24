import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Read in CSV
df = pd.read_csv(r'C:\Users\grayd\Downloads\timeline_posts.csv')
# Remove $ and , from the Price column, then convert to numeric
df['Price'] = df['Price'].replace('[\$,]', '', regex=True)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
# df['Price'] = pd.to_numeric(df['Price'], errors='coerce') # Load price as numeric
# df = df.dropna(subset=['Price']) # Remove NA values if they exist

# Ensure 'Date' is a datetime type
df['Date'] = pd.to_datetime(df['Date'])

# Sort the DataFrame by date
df = df.sort_values('Date')

# Filter for rows where 'Post' is not empty or null
df_posts = df[df['Post'].notna() & (df['Post'].str.strip() != '')]

# Create the fig
fig = px.line(df, x='Date', y='Price', title='Bitcoin Price Over Time')

# Line chart for Bitcoin price
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Price'],
    mode='lines',
    name='BTC Price'
))

# Plot dots only where a post exists
fig.add_trace(go.Scatter(
    x=df_posts['Date'],
    y=df_posts['Price'],
    mode='markers',
    marker=dict(size=10, color='red'),
    name='Your Posts',
    text=df_posts['Post'],
    hoverinfo='text'
))

fig.update_layout(
    title='Bitcoin Price with Posts',
    xaxis_title='Date',
    yaxis_title='Price'
)

fig.show()

# Save chart as interactive HTML file
# fig.write_html("my_chart.html")