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
    html.Div('Below is a plot of NBA player data taken from the Advanced Stats page of NBA.com.'),
    html.Label('X-axis: '),
    dcc.Dropdown(
        id = 'x_axis_content',
        options=[{'label': str(x), 'value': x} for x in df.columns],
        value='AST'
    ),
    html.Label('Y-axis: '),
    dcc.Dropdown(
        id = 'y_axis_content',
        options=[{'label': str(x), 'value': x} for x in df.columns],
        value='PTS'
    ),
    dcc.Graph(id='raptors_table')
    #generate_table(df[df['TEAM'] == team]
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
                x=df[df['TEAM'] == i][x_content],
                y=df[df['TEAM'] == i][y_content],
                mode='markers',
                opacity=0.6,
                marker={
                    'size': np.sqrt(df[df['TEAM'] == i]['MIN']),
                    'line': {'width': 0.5, 'color': 'white'}
                },
                text=df[df['TEAM'] == i]['PLAYER'],
                name=i
            ) for i in df['TEAM'].unique()
        ],
        'layout': go.Layout(
            xaxis={'title': x_content},
            yaxis={'title': y_content},
            margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
            legend={'x': -0.2, 'y': 1},
            hovermode='closest'
        )
    }
    

if __name__ == '__main__':
    app.run_server(debug=True)