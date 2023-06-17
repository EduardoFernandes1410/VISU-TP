import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash
import re
from dash import dcc
from dash import html, callback
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
import pandas as pd
import plotly.graph_objs as go

athlete = pd.read_csv("./olympic_games/athlete_events.csv")
hosts = pd.read_csv("./olympic_games/olympic_hosts.csv")

athlete = athlete.dropna()

athlete.Year = pd.to_numeric(athlete.Year, errors='coerce')
athlete = athlete[(athlete.Year >= 1920)]

def get_color( val ):
    season = list(hosts[ hosts.game_year == val ]['game_season'])[0]
    if season == 'Summer':
        return '#f3872f'
    return '#add8e6'

def initialize_type_vs_year():
    return [html.Div([
        html.H1('Biotype of Athletes vs Year of the Events', style={'text-align': 'center', 'fontFamily': 'Open Sans, sans-serif'}),
        html.Div(style={'display': 'flex', 'justify-content': 'space-between'},
                children=[       
            html.Div([
                dcc.Dropdown(
                    id='type-dropdown',
                    value='Age',
                    options=[{'label': val, 'value': val} for val in [ 'Age', 'Weight', 'Height' ]],
                    placeholder='Select a characteristic'
                )
            ], style={'flex': '1' }),
        ]),
        # Gráfico de linha
        dcc.Graph(id='box-line')
    ])]

@callback(
    Output(component_id='box-line', component_property='figure'),
    Input(component_id='type-dropdown', component_property='value')
)

def update_chart(type):
    filtered_df = athlete.copy()

    layout = go.Layout(
        yaxis={'title': f'{type}'},
        xaxis={'title': 'Year'},
        margin={'t':10},
        showlegend=False,
        height=550,
        font=dict(size=18)
    )

    fig = go.Figure(layout=layout)

    for year in np.sort(filtered_df['Year'].unique()):
        year_df = filtered_df[(filtered_df['Year'] == year)]
        fig.add_trace( go.Box(
            y=year_df[type],
            line=dict(color=get_color(year)),
            name=str(int(year)),
            # legend=None,
        ))

    return fig