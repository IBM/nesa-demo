import dash_carbon_components as dca
import dash_html_components as html
from dash_core_components import Location


def ui_shell(name: str, header, sidebar):
    return html.Div([
        Location(id='url', refresh=False),
        dca.UIShell(
            id='ui-shell',
            name=name,
            headerItems=header,
            sidebarItems=sidebar
        ),
        html.Div(
            id='page-content',
            style={
                'height': 'calc(100vh - 48px)',
                'margin': '0',
                'width': '100%',
                'overflow': 'auto',
                'backgroundColor': '#f4f4f4',
                'marginTop': '48px',
            },
        ),
        html.Div(id='dummy_div')
    ])
