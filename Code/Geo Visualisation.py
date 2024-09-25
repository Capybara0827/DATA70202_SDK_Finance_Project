# this was the code for geo visualisation 

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Assuming final_df has all necessary columns properly formatted and ready to use
# Convert 'date' column to datetime if not already
final_df['date'] = pd.to_datetime(final_df['date'], errors='coerce')

# Dash layout
app.layout = html.Div([
    dcc.Dropdown(
        id='wallet-dropdown',
        options=[{'label': wallet, 'value': wallet} for wallet in final_df['wallet_number_from'].unique()],
        value=final_df['wallet_number_from'].unique()[0],  # Set the default value to the first entry
        style={'color': 'black'}  # Dropdown styling
    ),
    dcc.Graph(id='map-graph', style={'height': '800px'})  # Increase the size of the map
])

# Callback to update the map based on the wallet selection
@app.callback(
    Output('map-graph', 'figure'),
    [Input('wallet-dropdown', 'value')]
)
def update_map(selected_wallet):
    # Filter the DataFrame based on the selected wallet
    filtered_df = final_df[final_df['wallet_number_from'] == selected_wallet]
    
    # Convert 'date' to string for display in hover data, ensure it's datetime first
    if pd.api.types.is_datetime64_any_dtype(filtered_df['date']):
        filtered_df['date_str'] = filtered_df['date'].dt.strftime('%Y-%m-%d')
    else:
        filtered_df['date_str'] = 'Not Available'

    # Generate a scatter geo map
    fig = px.scatter_geo(filtered_df,
                         lat='lat',
                         lon='long',
                         text='city',  # Show city names on the markers
                         hover_name='country',  # Main hover information is the country
                         hover_data={'region': True, 'date_str': True},  # Additional hover info: region and transaction date
                         projection='natural earth',
                         title=f'Transactions for Wallet: {selected_wallet}',
                         color_discrete_sequence=['pink'])  # Set markers to pink

    # Update map layout to dark mode with white text
    fig.update_layout(
        geo=dict(
            bgcolor='rgb(10,10,10)',  # Dark background for the globe
            lakecolor='rgb(10,10,10)',  # Dark lakes
            landcolor='rgb(50,50,50)',  # Dark land
            subunitcolor='rgb(100,100,100)'  # Darker borders
        ),
        paper_bgcolor='rgb(10,10,10)',  # Background color around the map
        plot_bgcolor='rgb(10,10,10)',  # Plot background color
        title_font=dict(color='white'),  # Set the title font color to white
        font=dict(color='white')  # Set global font color to white for all text
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)