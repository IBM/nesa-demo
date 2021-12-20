import dash_carbon_components as dca
from .editor_layout import editor_layout
from .inspector_layout import inspector_layout

graphs_layout = [
    dca.Tabs(
        style={'width': '100%', 'backgroundColor': 'white'},
        id='graphs_tabs',
        headerSizes=['lg-10'],
        value='editor_tab',
        children=[
            dca.Tab(value='editor_tab', label='Edit Network', children=editor_layout),
            dca.Tab(value='inspector_tab', label='Inspect Network', children=inspector_layout),
        ])
]
