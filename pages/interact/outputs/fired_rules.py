import dash_cytoscape as cyto
# Load extra layouts
cyto.load_extra_layouts()


def fired_rules(edges, nodes, roots_names, cytolayout='dagre', id='fired_rules_agent_1'):
    return cyto.Cytoscape(
        id=id,
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
