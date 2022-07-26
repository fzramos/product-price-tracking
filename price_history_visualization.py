import pandas as pd
import sqlite3
import plotly.express as px
import dash
from dash import html
from dash import dcc

def product_price_charts():
    """
        Produce charts for all the products in the SQLite3 DB. Produces arbitrary number of price history charts.
        returns HTML Div containing price history charts and hyperlinks to each product's listing webpage
    """
    graphs = []
    conn = sqlite3.connect("price_tracker.db")
    price_histories_df = pd.read_sql_query("select p.price_in_cents, p.timestamp, l.name from price p inner join \
                                            listing l on p.listing_id=l.id order by timestamp desc" \
                                            , conn)
    price_histories_df['price (Dollars)'] = price_histories_df['price_in_cents'] / 100
    products_df = pd.read_sql_query("select name, url from listing", conn)
    for index, row in products_df.iterrows():
            item_price_histories_df = price_histories_df.loc[price_histories_df['name']==row['name']]
            fig_price_history = px.line(item_price_histories_df, x='timestamp', y='price (Dollars)', template="plotly_dark", markers=True)
            fig_price_history.update_layout(
                title=f"Price History for {row['name']}",
                xaxis_title=f"Datetime",
                yaxis_title="Price (Dollars)",
                font = dict(
                    size=18
                )    
            )

            graphs.append(dcc.Graph(
                    id=f'graph-{index}',
                    figure=fig_price_history
            ))
            graphs.append(html.Div(html.A("Link to product webpage", href=row['url'], target="_blank"), className='product-link'))
    return html.Div(graphs)


# Create a dash application
app = dash.Dash(__name__)
app.layout = html.Div(children=[html.H1('Price Trackering Results',
                                        style={'textAlign': 'center',
                                                'color': '#f8f8ff',
                                                'font-size': 40}),
                                html.Div(
                                        children=product_price_charts(),
                                        id='container',
                                )
                                ])


# Run the application
if __name__ == '__main__':
    app.run_server()