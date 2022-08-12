import dash_carbon_components as dca
import dash_html_components as html

from components import dialog_row, fired_rule_card, next_actions_row

interact_layout = dca.Grid(
    style={'padding': '16px',
           'height': 'calc(100% - 40px)',
           'overflow': 'auto'},
    className='bx--grid--narrow bx--grid--full-width',
    children=[
        dca.Row(
            children=[
                dca.Column(columnSizes=['sm-5'], children=[
                    dca.Card(
                        id='interactive_agent_chat',
                        title='Interaction with environment',
                        children=[
                        ],
                        style={
                            'overflow': 'auto',
                            'display': 'flex',
                            'flex-direction': 'column-reverse',
                            'height': '400px',
                            'width': '100%'
                        }
                    )
                ], style={'padding-left': '16px',
                          'padding-right': '16px'})
            ],
        ),
        dca.Row(
            children=[
                dca.Column(columnSizes=['sm-5'], children=[
                    # dca.Column(columnSizes=['sm-3'], children=[
                    dca.Card(
                        id='select_next_action_card',
                        title='Action selector to perform',
                        children=[
                            html.P('',
                                   id='message_for_top_of_action_selector',
                                   style={
                                       'padding-bottom': '16px',
                                       'padding-left': '10px'
                                   }),

                            html.Div(
                                id='next_action_row',
                                children=[
                                    next_actions_row(
                                        [''],
                                        agent_1_actions=[['', 0]],
                                        agent_1_rules=None,
                                        agent_1_facts=None,
                                        agent_2_actions=[['', 0]],
                                        done=False
                                    ),
                                ]
                            ),
                        ],
                        style={
                            'margin-top': '16px',
                            'margin-bottom': '16px',
                            'height': 'calc(100% - 50px)'
                        }
                    ),
                ], style={'margin-left': '16px',
                          'margin-top': '16px',
                          'padding-right': '16px',
                          'width': '100%'}),
                dca.Column(columnSizes=['sm-1'], children=[
                    dca.Card(
                        id='apply_next_action_card',
                        children=[
                            html.Div(
                                children=[
                                    dca.Button(
                                        id='reset_environment',
                                        size='sm',
                                        children='Reset Environment',
                                        kind='primary',
                                        style={'margin-top': '10%'}
                                    )
                                ],
                                style={'text-align': 'center'}
                            ),
                            html.P(
                                id='game_score', children='',
                                style={
                                    'text-align': 'center',
                                    'margin-top': '16px',
                                    'margin-bottom': '16px'
                                }
                            ),
                        ],
                        style={
                            'margin-top': '16px',
                            'margin-bottom': '0px',
                            'height': '0px',
                            # 'height': 'calc(100% - 50px)',
                        }
                    ),
                ], style={'flex': '0 0 24%',
                          'visibility': 'hidden',
                          'height': '0px'}),
            ],
        ),
    ])
