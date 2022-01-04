from dash import Dash
from dash.dependencies import Input, Output, State


def select_all_callback(app: Dash, button_id: str, dropdown_id: str):
    @app.callback(
        Output(dropdown_id, 'value'),
        Input(button_id, 'n_clicks'),
        State(dropdown_id, 'options')
    )
    def __select_all_callback(click, options):
        values = [
            e if type(e) != dict else e['value'] for e in
            options
        ]
        return values
