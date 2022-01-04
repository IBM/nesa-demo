import dash_cytoscape as cyto
# Load extra layouts
cyto.load_extra_layouts()


def network_editor(edges, nodes, roots_names, cytolayout='dagre'):
    return cyto.Cytoscape(
        id='network_editor_graph',
        elements=nodes + edges[-1],
        layout={'name': cytolayout, 'roots': roots_names},
        style={'width': '100%', 'height': '100%'},
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
