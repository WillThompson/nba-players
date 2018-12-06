# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.graph_objs as go
import numpy as np

import nba_db as db


conn = db.db_connect()
df = pd.read_sql("SELECT * FROM players;", conn)

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = ['./css/main.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    
    html.Div([
        html.H4('NBA Player Data (2018/2019 season)'),
        html.Div([
            html.Div('Below is a plot of NBA player data taken from the Advanced Stats page of NBA.com.',style={"margin-bottom":'10px'}),
            html.Label('X-axis: '),
            dcc.Dropdown(
                id = 'x_axis_content',
                options=[{'label': str(x), 'value': x} for x in df.columns],
                value='ast'
            ),
            html.Label('Y-axis: '),
            dcc.Dropdown(
                id = 'y_axis_content',
                options=[{'label': str(x), 'value': x} for x in df.columns],
                value='pts'
            )
        ],className="three columns"),

        html.Div([
            dcc.Graph(id='raptors_table'
            )
        ], className="six columns")

    ], className="row"),

    html.Div([
        
        generate_table(df)

    ], className="row")
    
 ])

@app.callback(
    dash.dependencies.Output(component_id='raptors_table', component_property='figure'),
    [dash.dependencies.Input(component_id='x_axis_content', component_property='value'),
    dash.dependencies.Input(component_id='y_axis_content', component_property='value')]
)
def update_graph(x_content,y_content):
    
    if x_content is None or y_content is None:
        return{}
    return {
        'data': [
            go.Scatter(
                x=df[df['team'] == i][x_content],
                y=df[df['team'] == i][y_content],
                mode='markers',
                opacity=0.6,
                marker={
                    #'size': np.sqrt(df[df['team'] == i]['min']),
                    'line': {'width': 0.5, 'color': 'white'}
                },
                text=df[df['team'] == i]['player'],
                name=i
            ) for i in df['team'].unique()
        ],
        'layout': go.Layout(
            xaxis={'title': x_content},
            yaxis={'title': y_content},
            margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
            legend={'x': 0, 'y': -0.3, 'orientation': "h"},
            hovermode='closest'
        )
    }
    

if __name__ == '__main__':
    app.run_server(debug=True)