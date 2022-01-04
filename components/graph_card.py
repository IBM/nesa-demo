import dash_carbon_components as dca
import dash_html_components as html
import dash_table
from dash_core_components import Graph
from dash_extensions import Download


def graph_card(graph_id: str, graph_name: str, graph_info: str = '',
               radios=None, height: int = 250) -> dca.Card:
    if radios is None:
        radios = []
    children = [
        Graph(id=f'{graph_id}', style={'height': f'{height}px'}),
        Download(id=f'{graph_id}_download'),
    ]
    i = 0
    for radio in radios:
        i += 1
        children.append(
            dca.RadioButtonGroup(
                id=f'{graph_id}_radio{i}',
                radiosButtons=radio.buttons,
                value=radio.value
            )
        )
    return dca.Card(
        id=f'{graph_id}_card',
        title=graph_name,
        info=graph_info,
        actions=[{'displayName': 'Download CSV',
                  'actionPropName': 'download'},
                 {'displayName': 'Download Excel',
                 'actionPropName': 'download_excel'}],
        children=children)
