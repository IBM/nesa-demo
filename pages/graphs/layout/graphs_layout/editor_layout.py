import dash_carbon_components as dca
from components import network_card

editor_layout = dca.Grid(
    style={'padding': '16px',
           'height': 'calc(100% - 40px)',
           'overflow': 'auto'},
    className='bx--grid--narrow bx--grid--full-width',
    children=[
        dca.Row(children=[
            dca.Column(columnSizes=['sm-4'], children=[
                network_card(
                    graph_id='network_editor',
                    graph_name='Edit Logical Neural Network Weights',
                    graph_info='Edit Logical Neural Network Weights',
                    table=True,
                    height=500,
                ),
            ]),
        ]),
    ])
