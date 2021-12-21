from dash import Dash
from dash.dependencies import Input, Output, State

from . import outputs
from .functions import filter_dataframe
from utils_demo.callbacks import select_all_callback
from .data import scalars


def register(app: Dash):
    # Function to register the select_all callbacks, receive the checkbox id and the dropdown id.

    @app.callback(
        Output('loss_type_selection', 'value'),
        [
            Input('loss_type_selection', 'value')
        ]
    )
    def countries_selection(loss_types):
        values = list(loss_types)
        return values

    @app.callback(
        [
            Output('scalars', 'figure'),
        ],
        [
            Input('configuration_apply_scalars', 'n_clicks'),
        ],
        [
            State('loss_type_selection', 'value'),
        ])
    def apply_configuration(apply_click, loss_types):
        filtered_data = filter_dataframe(scalars, loss_types)
        return [
            outputs.scalars(filtered_data),
        ]
