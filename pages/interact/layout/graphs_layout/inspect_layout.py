import dash_carbon_components as dca
import dash_core_components as dcc

from components import (admissible_actions_card, commonsense_card,
                        fired_rule_card, logical_facts_card)

inspect_layout = dca.Grid(
    style={'padding': '16px',
           'height': 'calc(100% - 40px)',
           'overflow': 'auto'},
    className='bx--grid--narrow bx--grid--full-width',
    children=[
        dca.Row(
            children=[
                dca.Column(columnSizes=['sm-4'], children=[
                    dca.Card(
                        id='interactive_agent_chat_inspect',
                        title='Interaction with environment',
                        children=[
                        ],
                        style={
                            'overflow': 'auto',
                            'display': 'flex',
                            'flex-direction': 'column-reverse',
                            'height': '400px',
                        }
                    )
                ], style={'padding-left': '16px'})
            ],
        ),
        dca.Row(children=[
            dca.Column(columnSizes=['sm-4'], children=[
                dca.Row(children=[
                    dca.Column(columnSizes=['sm-2'], children=[
                        admissible_actions_card()
                    ]),
                    dca.Column(columnSizes=['sm-2'], children=[
                        commonsense_card()
                    ]),
                    dca.Column(columnSizes=['sm-2'], children=[
                        logical_facts_card()
                    ], style={'margin-top': '16px'}),
                    dca.Column(columnSizes=['sm-2'],
                               className='hide-scroll',
                               children=[
                        fired_rule_card(
                            graph_id='fired_rules_agent_1',
                            graph_name='Trained rules analyzer (LNN Network)',
                            height=550,
                        )
                    ], style={'margin-top': '16px'})
                ], style={'margin-left': '16px', 'margin-top': '16px'}),
            ]),
        ]),
        dcc.Store(id='graph_elements'),
        dcc.Store(id='graph_elements_history'),
        dcc.Store(id='selected_graph_element_id'),
    ]
)
