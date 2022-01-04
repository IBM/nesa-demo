import dash_html_components as html

from ... import RIGHT_TOP_MESSAGE
from .graphs_layout import graphs_layout

layout = [
    html.Div(
        style={
            'width': '100%',
            'display': 'flex',
            'flexDirection': 'row',
            'alignItems': 'flex-end',
            'justifyContent': 'space-between',
            'backgroundColor': 'white',
            'padding': '8px 24px',
            'borderBottom': '1px solid #ddd'
        },
        children=[
            html.H4(children=['Explore Logical Nueral Network Graphs']),
            html.Div(style={'display': 'flex', 'alignItems': 'flex-end'},
                     children=[
                html.Span(id='TCV_value'),
                html.Span(style={'marginLeft': '8px'},
                          id='Entitled_value'),
                html.Span(
                    style={'marginLeft': '8px'},
                    children=[RIGHT_TOP_MESSAGE]
                )
            ])
        ]
    ),
    html.Div(
        style={
            'display': 'flex',
            'flexDirection': 'row',
            # UIShell header = 48px. Page Title = 64px
            'height': 'calc(100% - 45px)',
            'width': '100%'
        },
        children=[
            html.Div(style={
                'width': '100%',
                'height': '100%'
            }, children=graphs_layout),
        ]
    )
]
