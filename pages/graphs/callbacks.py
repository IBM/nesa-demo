from dash import Dash
from dash.dependencies import Input, Output, State
import pandas as pd

from . import outputs
from .functions.data_processing import create_slider_transform_function
from .data import *


def register(app: Dash):

    @app.callback(Output('network_editor', 'children'),
                  Input('ui-shell', 'name'))
    def edit_network_graph(input):
        return outputs.network_editor(edges, nodes, roots_names, cytolayout='dagre')

    @app.callback(Output('network_inspector', 'children'),
                  [Input('ui-shell', 'name')])
    def edit_network_graph(input):
        return outputs.network_inspector(edges, nodes, roots_names, cytolayout='dagre')

    @app.callback(
        Output('network_editor_graph', 'elements'),
        [
            Input('network_editor_table', 'data'),
            Input('network_editor_table', 'columns'),
        ],
        [
            State('network_editor_graph', 'elements')
        ])
    def edit_network_graph_weights(rows, columns, elements):
        df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
        for i, data in enumerate(elements):
            if 'source' in data['data']:
                sub_df = df[(df['Parent'] == data['data']['source']) & (df['Child'] == data['data']['target'])]
                if not sub_df.empty:
                    elements[i]['data']['weight'] = float(sub_df['Weight'].iloc[0])

        return elements

    @app.callback(
        Output('network_editor_table', 'data'),
        Input('network_editor_graph', 'tapEdgeData'))
    def display_input_table(edge):
        if edge is None:
            return [dict(Parent='', Child='', Weight='')]
        return [dict(Parent=edge['source'], Child=edge['target'], Weight=edge['weight'])]

    @app.callback(
        [
            Output('network_inspector_graph', 'elements'),
            Output('network_inspector_slider', 'marks'),
            Output('network_inspector_slider', 'max'),
        ],
        [
            Input('network_inspector_slider', 'value'),
        ],
        [
            State('network_inspector_graph', 'elements')
        ])
    def update_network_training_inspector_graph(selected_epoch, elements):
        slider_transform_function = create_slider_transform_function(network['epochs'])
        for i, edge in enumerate(edges[slider_transform_function(selected_epoch)]):
            for j, data in enumerate(elements):
                if 'source' in data['data']:
                    if (data['data']['source'] == edge['data']['source']) & (
                            data['data']['target'] == edge['data']['target']):
                        elements[j]['data']['weight'] = float(edge['data']['weight'])
        return elements, slider_dict, network['epochs']
