import dash_cytoscape as cyto


def create_edit_network_graph(edges, nodes, roots_names, cytolayout='dagre'):
    return cyto.Cytoscape(
        id='nn',
        elements=nodes + edges[-1],
        layout={'name': cytolayout, 'roots': roots_names},
        style={'width': '400px', 'height': '500px'},
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'opacity': 'data(weight)'
                }
            },
        ]
    )


def create_network_training_inspector_graph(edges, nodes, roots_names, cytolayout='dagre'):
    return cyto.Cytoscape(
        id='nn-slider',
        elements=nodes + edges[0],
        layout={'name': cytolayout, 'roots': roots_names},
        style={'width': '400px', 'height': '500px'},
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'opacity': 'data(weight)'
                }
            },
        ]
    )