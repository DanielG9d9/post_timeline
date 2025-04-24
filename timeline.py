# Written by Daniel Gray
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Functions
# Manual breaks in post
def insert_line_breaks(text, max_length=80):
    import textwrap
    return '<br>'.join(textwrap.wrap(str(text), max_length))

df = pd.read_csv(r'C:\Users\grayd\Downloads\timeline_posts.csv') # Read in CSV

df['Price'] = df['Price'].replace('[\$,]', '', regex=True) # Remove $ and , from the Price column, then convert to numeric
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['Price'] = df['Price'].astype('int')  # or 'int' or 'int32' or 'int64

df['Date'] = pd.to_datetime(df['Date']) # Ensure 'Date' is a datetime type
df = df.sort_values('Date') # Sort the DataFrame by date
df_posts = df[df['Post'].notna() & (df['Post'].str.strip() != '')].copy()
df_posts['Post_wrapped'] = df_posts['Post'].apply(lambda x: insert_line_breaks(x, 60))  # Apply the function to add breaks.

fig = px.line(df, x='Date', y='Price', title='Bitcoin Price Over Time') # Create the fig

# Line chart for Bitcoin price
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Price'],
    mode='lines',
    name='BTC Price',
    line=dict(color='#de5e06', width=2), # Set (price) line color and width
    hovertemplate=(
        '<b>Date:</b> %{x|%b %d, %Y}<br>' +   # Custom date format
        '<b>Price:</b> $%{y:,.0f}<extra></extra>'  # Comma, no decimals
    )
))

# Set Post colors and text stuff here
fig.add_trace(go.Scatter(
    x=df_posts['Date'],
    y=df_posts['Price'],
    mode='markers',
    marker=dict(size=10, color='#b41a4a'), # Marker is the dot on the line
    name='My Posts',
    # text=df_posts['Post'],
    text=df_posts['Post_wrapped'], # Use the new DF with posts using the function for break points in text.
    hovertemplate=(
        '<b>Date:</b> %{x}<br>' +
        '<b>Price:</b> $%{y:,.0f}<br>' +  # .0f for no decimals, comma as thousands separator
        '<b>Post:</b> %{text}<extra></extra>'
    ),
    hoverlabel=dict(
        bgcolor='white',                 # Hover box background
        font=dict(color='black', size=14)  # Hover text color and size
    )
))

fig.update_layout(
    title="Don't Say I Didn't Try...",
    title_font=dict(
        size=36,
        color='#BBC0C6',  # Title color
        family='Arial'
    ),
    xaxis_title='',
    yaxis_title='',
    paper_bgcolor="#101414",  # Page background color
    plot_bgcolor="#101414",   # Plot area background color
    xaxis=dict(gridcolor="#BBC0C6"),
    yaxis=dict(gridcolor="#BBC0C6"),
    legend=dict( # Move legend from here
        orientation="h",
        xanchor="left",
        yanchor="top",
        x=0.02,  # Increase this value to move legend further to the right
        y=1.02,  # Adjust this value if you want the legend closer or farther from the title
        font=dict(size=14, color="#BBC0C6")  # Optional: legend font styling
    )
)

fig.update_xaxes(
    color='white',  # X-axis line and tick color
    tickfont=dict(
        color='#BBC0C6',  # X-axis tick label color
        size=16,
        family='Arial'
    ),
    showgrid=False
)

fig.update_yaxes(
    color='white',  # Y-axis line and tick color
    tickfont=dict(
        color='#BBC0C6',  # Y-axis tick label color
        size=16,
        family='Arial'
    )
)

fig.show()

# Save chart as interactive HTML file
fig.write_html("my_chart.html")