import plotly.graph_objs as go
from dash import Dash
from dash.dependencies import Input, Output, State
from dash_extensions.snippets import send_data_frame
from pandas import DataFrame


def download_callback(app: Dash, card_id: str, graph_id: str, download_id: str) -> None:
    @app.callback(
        Output(download_id, "data"),
        Input(card_id, "action_click"),
        State(graph_id, "figure"),
        State(card_id, "title"),
        prevent_initial_call=True
    )
    def __download_callback(action_click: str, figure: go.Figure, title: str):
        if figure:
            d = figure['data']
            # Fell free to extend the download callback to support more graphs types
            if d[0]['type'] == 'scattergl':
                output = __download_scatter(d)
            else:
                output = __download_bar(d)
            if action_click.startswith('download_excel'):
                return send_data_frame(output.to_excel, title + '.xlsx', index=False)
            return send_data_frame(output.to_csv, title + '.csv', index=False)
        return ''

    def __download_scatter(d):
        output = DataFrame()
        for element in d:
            df = DataFrame()
            df[element['xaxis']] = element['x']
            df[element['yaxis']] = element['y']
            df['name'] = element['name']
            df['customdata'] = element['customdata']
            output = output.append(df)
        return output

    def __download_bar(d):
        output = DataFrame()
        output['x'] = d[0]['x']
        for element in d:
            output[element['name']] = element['y']
        return output
