# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.graph_objs as go
import numpy as np

df = pd.read_csv(
    './nba_players.csv')

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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(children=[
    html.H4(children='NBA players'),
    html.Label('Dropdown'),
    dcc.Dropdown(
    	id = 'team_list',
        options=[
            {'label': 'Toronto Raptors', 'value': 'TOR'},
            {'label': 'New York Knicks', 'value': 'NYK'},
            {'label': 'Golden State Warriors', 'value': 'GSW'},
            {'label': 'Portland Trailblazers', 'value': 'POR'},
        ],
        value='TOR'
    ),
    dcc.Graph(id='raptors_table')
    #generate_table(df[df['TEAM'] == team]
])

@app.callback(
    dash.dependencies.Output(component_id='raptors_table', component_property='figure'),
    [dash.dependencies.Input(component_id='team_list', component_property='value')]
)
def update_graph(input_value):
    
    team = input_value
    return {
        'data': [
            go.Scatter(
                x=df[df['PLAYER'] == i]['AST'],
                y=df[df['PLAYER'] == i]['PTS'],
                mode='markers',
                opacity=0.8,
                marker={
                    'size': np.sqrt(df[df['PLAYER'] == i]['MIN']),
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in df[df['TEAM'] == team]['PLAYER'].unique()
        ],
        'layout': go.Layout(
            xaxis={'title': 'Total Assists'},
            yaxis={'title': 'Total Points'},
            margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
            legend={'x': 1.05, 'y': 1},
            hovermode='closest'
        )
    }
    

if __name__ == '__main__':
    app.run_server(debug=True)