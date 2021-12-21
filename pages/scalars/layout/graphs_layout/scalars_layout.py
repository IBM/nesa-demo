import dash_carbon_components as dca
from components import graph_card

scalars_layout = dca.Grid(
    style={'padding': '16px',
           'height': 'calc(100% - 40px)',
           'overflow': 'auto'},
    className='bx--grid--narrow bx--grid--full-width',
    children=[
        dca.Row(children=[
            dca.Column(columnSizes=['sm-4'], children=[
                graph_card(
                    graph_id='scalars',
                    graph_name='Logical Neural Network Losses by Epoch',
                    graph_info='Logical Neural Network Losses by Epoch',
                    height=500
                ),
            ]),
        ]),
    ])
