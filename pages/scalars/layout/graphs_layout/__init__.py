import dash_carbon_components as dca
from .scalars_layout import scalars_layout

graphs_layout = [
    dca.Tabs(
        style={'width': '100%', 'backgroundColor': 'white'},
        id='scalars_tabs',
        headerSizes=['lg-10'],
        value='training_tab',
        children=[
            dca.Tab(value='training_tab', label='Training', children=scalars_layout),
        ])
]
