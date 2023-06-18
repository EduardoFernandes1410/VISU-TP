from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.graph_objects as go
import pandas as pd

# Incorporate data
df_summer = pd.read_parquet("data/summer_world_map.parquet")
df_winter = pd.read_parquet("data/winter_world_map.parquet")

DUMMY = {
        'Year': [],
        'Occurances': []
    }
for year in sorted(df_summer["Year"].unique()):
        DUMMY['Year'].append(year)
        DUMMY['Occurances'].append(int(0))
DUMMY_DF = pd.DataFrame(DUMMY)

# Defining medal comparison
def initialize_compare_medals():
    dropdown_div = html.Div(
        id='compare-medals-options',
        children=[
            dcc.Dropdown(
                    options = [ 
                            {'label': 'Summer', 'value': 'Summer'},
                            {'label': 'Winter', 'value': 'Winter'}
                        ],
                    id='edition-dropdown',
                    value='Summer',
                    placeholder='Select an edition'
            )
        ]
    )

    dropdown_div2 = html.Div(
        id='compare-medals-options',
        children=[
            dcc.Dropdown(
                multi=True,
                id='compare-dropdown'
            )
        ]
    )

    graph = dcc.Graph(figure={}, id='compare-medals')
    return [
        html.Hr(),
        html.H3('Choose Participants'),
        dropdown_div,
        html.Hr(),
        dropdown_div2,
        graph]

@callback(
    Output('compare-dropdown', 'options'),
    Input('edition-dropdown', 'value')
)
def update_dropdown_event(edition):
    if edition == 'Winter':
        country_options = [country for country in sorted(df_winter["Country"].unique())]
    else:
        country_options = [country for country in sorted(df_summer["Country"].unique())]
    return country_options

# Updating the medals comparison
@callback(
    Output(component_id='compare-medals', component_property='figure'),
    Input(component_id='compare-dropdown', component_property='value'),
    Input(component_id='edition-dropdown', component_property='value')
)
def update_compare_medals(selected_options, edition):
    if edition == 'Winter':
         df = df_winter
    else:
         df = df_summer

    fig = go.Figure()

    print("\n\n\n\n")
    print(selected_options)
    print(edition)
    print("\n\n\n\n")

    if selected_options:
        for option in selected_options:
            df_filtered = df[df["Country"] == option]
            df_filtered = pd.concat([df_filtered, DUMMY_DF]).groupby(by="Year").sum()
            fig.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered.Occurances,
                                    mode='lines+markers', name=option))

        fig.update_layout(title='Medal Comparison per Edition',
                        xaxis_title='Editions', yaxis_title='Sum of Medals',
                        height=800)

    fig.update_layout(title='Medal Comparison per Edition',
                      xaxis_title='Editions', yaxis_title='Sum of Medals',
                      height=800)
    return fig