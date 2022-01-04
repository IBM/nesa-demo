import dash_carbon_components as dca
import dash_html_components as html

from .filters_layout import filters_layout

configuration_layout = [
    html.Div(style={'display': 'flex',
                    'height': '40px',
                    'alignItems': 'center'}, children=[
        html.H5(style={'paddingLeft': '16px'}, children='Configuration'),
    ]),
    dca.Tabs(children=[
        dca.Tab(value='filters', label='Games', children=[
            html.Div(
                style={
                    'width': '100%',
                    'height': 'calc(100% - 130px)',
                    'overflow': 'auto',
                    'padding': '8px',
                    'paddingBottom': '96px'
                },
                children=filters_layout
            )
        ])
    ]),
    html.Div(
        style={
            'borderTop': '1px solid #ddd',
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'flex-end',
            'width': '100%',
            'padding': '8px',
        },
        children=[
            dca.Button(id='configuration_interact_games_reset',
                       size='sm', children='Reset', kind='secondary',
                       style={'marginRight': '1px'}),
            dca.Button(id='configuration_interact_games_apply',
                       size='sm', children='Apply', kind='primary')
        ])
]
