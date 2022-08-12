import dash_html_components as html
import dash_core_components as dcc
from ... import RIGHT_TOP_MESSAGE
from .configuration_layout import configuration_layout
from .filters_layout import filters_layout
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
            html.H4(children=['Interact with Agent']),
            html.Div(style={'display': 'flex', 'alignItems': 'flex-end'},
                     children=[
                         html.Span(id='TCV_value'),
                         html.Span(style={'margin-left': '8px'},
                                   id='Entitled_value'),
                         html.Span(style={'margin-left': '8px'},
                                   children=[RIGHT_TOP_MESSAGE])
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
                'width': 'calc(100% - 344px)',
                'height': '100%'
            }, children=graphs_layout),
            html.Div(style={
                'width': '344px',
                'height': '100%',
                'borderLeft': '1px solid #ddd',
                'backgroundColor': 'white'
            }, children=configuration_layout),
        ]
    ),
    dcc.Store(id='lnn_state'),
    dcc.Store(id='use_recommendation'),
    dcc.Store(id='inspector_state'),
]
