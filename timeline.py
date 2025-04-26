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
df_posts['HasLink'] = df_posts['Link'].notna() & (df_posts['Link'].str.strip() != '')   # Add HasLink boolean to find columns with links

# Split data between rows with and without links
linked_posts = df_posts[df_posts['HasLink']]
nonlinked_posts = df_posts[~df_posts['HasLink']]


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

# Non-linked posts (keep as blue circles)
fig.add_trace(go.Scatter(
    x=nonlinked_posts['Date'],
    y=nonlinked_posts['Price'],
    mode='markers',
    marker=dict(size=9, color='#0483A5', symbol='circle-open-dot'),  # blue circle
    name='My Posts (No Link)',
    text=nonlinked_posts['Post_wrapped'],
    customdata=nonlinked_posts['Link'],
    hovertemplate=(
        '<b>Date:</b> %{x}<br>' +
        '<b>Price:</b> $%{y:,.0f}<br>' +
        '<b>Post:</b> %{text}<extra></extra>'
    ),
    hoverlabel=dict(
        bgcolor='thistle',                   # Hover box background
        # bgcolor='lightslategray',          # Hover box background
        font=dict(color='black', size=14)  # Hover text color and size

    )
))

# Linked posts (change color and/or shape)
fig.add_trace(go.Scatter(
    x=linked_posts['Date'],
    y=linked_posts['Price'],
    mode='markers',
    marker=dict(size=9, color='yellow', symbol='star-open-dot'),  # orange diamond
    name='My Posts (With Link)',
    text=linked_posts['Post_wrapped'],
    customdata=linked_posts['Link'],
    hovertemplate=(
        '<b>Date:</b> %{x}<br>' +
        '<b>Price:</b> $%{y:,.0f}<br>' +
        '<b>Post:</b> %{text}<extra></extra>'
    ),
    hoverlabel=dict(
        bgcolor='lightblue',                 # Hover box background
        font=dict(color='black', size=14)  # Hover text color and size
    )
))

fig.update_layout(
    title="Study Bitcoin",
    title_font=dict(
        size=36,
        color='#BBC0C6',  # Title color
        family='Arial'
    ),
    xaxis_title='',
    yaxis_title='',
    paper_bgcolor="#101414",  # Page background color
    plot_bgcolor="#101414",   # Plot area background color
    yaxis=dict(gridcolor="#BBC0C6"),
    legend=dict( # Move legend from here
        orientation="h",
        xanchor="left",
        yanchor="top",
        x=0.02,  # Increase this value to move legend further to the right
        y=1.02,  # Adjust this value if you want the legend closer or farther from the title
        font=dict(size=14, color="#BBC0C6")  # Optional: legend font styling
    ),
    xaxis=dict( # X Axis information here
        gridcolor="#BBC0C6",
        range=[
            df['Date'].min(),  # Start at the earliest date in your data
            df['Date'].max()   # End at the latest date in your data
        ]
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
    tickprefix='$',
    tickformat=',.0f',  # comma as thousands separator, no decimals
    color='white',  # Y-axis line and tick color
    tickfont=dict(
        color='#BBC0C6',  # Y-axis tick label color
        size=16,
        family='Arial'
    )
)

# Annotations
fig.add_annotation(
    text="Created by Daniel Gray, 04/26/2025.",
    xref="paper", yref="paper",
    x=.9, y=0.025,  # bottom left
    xanchor="left", yanchor="bottom",
    showarrow=False,
    font=dict(size=12, color="#BBC0C6"),
    align="left",
    bgcolor="rgba(16,20,20,0.7)",  # Optional: semi-transparent background
    # bordercolor="#BBC0C6",         # Optional: border color
    borderwidth=1,                 # Optional: border width
    borderpad=4                    # Optional: padding inside the box
)

fig.show()

# Save chart as interactive HTML file
fig.write_html("studyBitcoin_894105.html")