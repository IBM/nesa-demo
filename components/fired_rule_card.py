import dash_carbon_components as dca
import dash_cytoscape as cyto
import dash_html_components as html

cyto.load_extra_layouts()


def fired_rule_card(graph_id: str, graph_name: str,
                    graph_info: str = '', height: int = 500) -> dca.Card:

    cytoscape = cyto.Cytoscape(
        id='fired_rules_agent_1_graph',
        layout={},
        elements=[],
        style={},
        stylesheet=[],
        responsive=True
    )

    children = [
        html.Div(id='fired_rules_agent_1_action_bar',
                 style={'height': '50px', 'width': '100%'},
                 children=[
                    html.Div(
                        'Select a node or edge',
                        id='selected_graph_element',
                        style={'float': 'left', 'padding-top': '0.4rem'}
                    ),
                     dca.Button(
                        'Delete element',
                        id='delete_graph_element',
                        kind='danger',
                        size='sm',
                        style={'visibility': 'hidden',
                               'width': '0px'}
                    ),
                     dca.Button(
                         'Execute test',
                         id='execute_test_graph_element',
                         kind='primary',
                         size='sm',
                         style={'visibility': 'hidden',
                                'width': '0px'}
                    ),
                     dca.Button(
                         'Undo change',
                         id='undo_graph_element',
                         kind='secondary',
                         size='sm',
                         style={'visibility': 'hidden',
                                'width': '0px'}
                    ),
                     dca.Button(
                         'Add node',
                         id='add_node_button',
                         kind='primary',
                         size='sm',
                         style={'visibility': 'hidden',
                                'width': '0px'}
                    ),
                     dca.Dropdown(
                         id='add_node_dropdown',
                         label=None,
                         options=None,
                         value=None,
                         style={'visibility': 'hidden',
                                'width': '0px'}
                    ),
                 ]),

        html.Div(id=f'{graph_id}',
                    style={'height': f'{height-50}px', 'width': '100%'},
                    children=[
                        cytoscape
                    ]
                 )
    ]

    return dca.Card(
        id=f'{graph_id}_card',
        title=graph_name,
        # actions=[{'displayName': 'Download CSV',
        #           'actionPropName': 'download'},
        #          {'displayName': 'Download Excel',
        #          'actionPropName': 'download_excel'}],
        style={'height': f'{height-50}px'},
        children=children)
