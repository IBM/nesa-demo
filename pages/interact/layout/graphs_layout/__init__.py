import dash_carbon_components as dca

from .inspect_layout import inspect_layout
from .interact_layout import interact_layout

graphs_layout = [
    dca.Tabs(
        style={'width': '100%', 'backgroundColor': 'white'},
        id='interact_tabs',
        headerSizes=['lg-10'],
        value='interact_tab',
        children=[
            dca.Tab(value='interact_tab',
                    label='Interaction Page',
                    children=interact_layout),
            dca.Tab(value='inspect_tab',
                    label='Inside of NeSA',
                    children=inspect_layout),
        ])
]
