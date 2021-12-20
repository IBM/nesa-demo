from dash import Dash
from dash.dependencies import Output, Input, ALL, State


def reset_page_callback(app: Dash):
    # Callback to reload the page when the user press the reset button
    @app.callback(
        Output('url', 'pathname'),
        Input({'type': 'reset', 'page': ALL}, 'n_clicks'),
        State('url', 'pathname'),
        prevent_initial_call=True
    )
    def __reset_page_callback(reset, pathname):
        return pathname
