import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash import dcc
from dash import html, callback
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
import pandas as pd
import plotly.graph_objs as go

to_plot = pd.read_csv("./data/rank_and_type.csv")

discipline_options = to_plot.Sport.unique()
discipline_options = np.append( discipline_options, ['All'] )

def get_color( val ):
    if val == 1:
        return '#ffd700'
    if val == 2:
        return '#c0c0c0'
    if val == 3:
        return '#cd7f32'
    return '#add8e6'

def initialize_type_vs_rank():
    return [html.Div([
        html.H1('Biotype of Athlete vs Ranking in Event', style={'text-align': 'center', 'fontFamily': 'Open Sans, sans-serif'}),
        html.Div(style={'display': 'flex', 'justify-content': 'space-between'},
                children=[
            html.Div([
                dcc.Dropdown(
                    id='sport-dropdown',
                    value='All',
                    options=[{'label': discipline, 'value': discipline} for discipline in discipline_options],
                    placeholder='Select a Sport'
                )
            ], style={'flex': '1'}),
            
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
        dcc.Graph(id='box-plot')
    ])]

@callback(
    Output(component_id='box-plot', component_property='figure'),
    Input(component_id='sport-dropdown', component_property='value'),
    Input(component_id='type-dropdown', component_property='value')
)

def update_chart(sport, type):
    filtered_df = to_plot.copy()

    # Filtrando por esporte, se selecionado e se for diferente de All
    if sport and sport != 'All':
        filtered_df = filtered_df[filtered_df['Sport'] == sport]

    layout = go.Layout(
        yaxis={'title': f'{type}'},
        xaxis={'title': 'Ranking position'},
        margin={'t':10},
        showlegend=False,
        height=550,
        font=dict(size=18)
    )

    fig = go.Figure(layout=layout)
    median_values = []

    for rank in np.sort(filtered_df['rank_position'].unique()):
        rank_df = filtered_df[(filtered_df['rank_position'] == rank)]
        fig.add_trace( go.Box(
            y=rank_df[type],
            line=dict(color=get_color(rank)),
            name=str(int(rank)),
            # legend=None,
        ))

        median_y = rank_df[type].median()  # Calculate the median value
        median_values.append(median_y)  # Store the median value

    fig.add_trace(go.Scatter(  # Add a line connecting the median values
        x=np.sort(filtered_df['rank_position'].unique()),
        y=median_values,
        mode='lines',
        line=dict(color='black', width=2)
    ))

    return fig