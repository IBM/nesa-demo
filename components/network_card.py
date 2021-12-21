import dash_carbon_components as dca
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_cytoscape as cyto


def network_card(graph_id: str, graph_name: str, graph_info: str = '', slider: bool = False, table: bool = False, height: int = 250) -> dca.Card:
    children = [
        html.Div(id=f'{graph_id}', style={'height': f'{height}px', 'width': '100%'},
                 children=cyto.Cytoscape(
                     id=f'{graph_id}_graph', elements=[], style={'height': '100%', 'width': '100%'})),
    ]

    if slider:
        slider_component = html.Div(
            id=f'{graph_id}_slider_parent', style={'width': '25%', 'padding': '25px', 'paddingBottom': '50px'},
            children=[html.H4("Select Epoch:"),
                      dcc.Slider(id=f'{graph_id}_slider', min=0, max=1, value=0, marks={}, step=None)]
        )
        children.append(slider_component)

    if table:
        table_component = html.Div(
            id=f'{graph_id}_table_parent', style={'width': '50%', 'padding': '25px'},
            children=[
                html.H4("Edit Weight:"),
                dash_table.DataTable(
                    id=f'{graph_id}_table',
                    columns=(
                        [{'id': 'Parent', 'name': 'Parent'}, {'id': 'Child', 'name': 'Child'},
                         {'id': 'Weight', 'name': 'Weight'}]
                    ),
                    data=[dict(Parent='', Child='', Weight='')],
                    editable=True,
                    style_table={'overflowX': 'auto', 'width': '50%'},
                    style_cell={
                        # all three widths are needed
                        'minWidth': '120px', 'width': '120px', 'maxWidth': '120px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    }
                )
            ]
        )
        children.append(table_component)

    return dca.Card(
        id=f'{graph_id}_card',
        title=graph_name,
        info=graph_info,
        actions=[{'displayName': 'Download CSV', 'actionPropName': 'download'},
                 {'displayName': 'Download Excel', 'actionPropName': 'download_excel'}],
        children=children)
