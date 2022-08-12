import dash_carbon_components as dca
import dash_html_components as html

from .filters_layout import filters_layout

configuration_layout = [
    html.Div(style={'display': 'flex', 'height': '40px',
                    'alignItems': 'center'},
             children=[
                 html.H5(style={'padding-left': '16px'},
                         children='Configuration'),
    ]),
    dca.Tabs(children=[
        dca.Tab(value='filters', label='Filters', children=[
            html.Div(
                style={
                    'width': '100%',
                    'height': 'calc(100% - 130px)',
                    'overflow': 'auto',
                    'padding': '8px',
                    'padding-bottom': '96px'
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
            dca.Button(id='configuration_scalars_filters_reset',
                       size='sm', children='Reset', kind='secondary',
                       style={'margin-right': '1px'}),
            dca.Button(id='configuration_scalars_filters_apply',
                       size='sm', children='Apply', kind='primary')
        ])
]
