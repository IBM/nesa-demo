import dash_carbon_components as dca
import dash_cytoscape as cyto
import dash_html_components as html


def fired_rule_card(graph_id: str, graph_name: str,
                    graph_info: str = '', height: int = 250) -> dca.Card:
    children = [
        html.Div(id=f'{graph_id}',
                 style={'height': f'{height}px', 'width': '100%'},
                 children=cyto.Cytoscape(
                     id=f'{graph_id}_graph',
                     elements=[],
                     style={'height': '100%', 'width': '100%'})),
    ]

    return dca.Card(
        id=f'{graph_id}_card',
        title=graph_name,
        info=graph_info,
        actions=[{'displayName': 'Download CSV',
                  'actionPropName': 'download'},
                 {'displayName': 'Download Excel',
                 'actionPropName': 'download_excel'}],
        children=children)
