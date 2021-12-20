import dash_carbon_components as dca
import dash_html_components as html
from components import dialog_row, fired_rule_card, next_actions_row

inspect_layout = dca.Grid(
    style={'padding': '16px',
           'height': 'calc(100% - 40px)',
           'overflow': 'auto'},
    className='bx--grid--narrow bx--grid--full-width',
    children=[
        dca.Row(children=[
            dca.Column(columnSizes=['sm-4'], children=[
                dca.Row(children=[
                    dca.Column(columnSizes=['sm-2'], children=[
                        fired_rule_card(
                            graph_id='working_memory_agent_1',
                            graph_name='Working Memory Agent 1',
                            graph_info='Working Memory for Agent 1',
                            height=250,
                        ),
                    ]),
                    dca.Column(columnSizes=['sm-2'], children=[
                        fired_rule_card(
                            graph_id='fired_rules_agent_1',
                            graph_name='Fired Rules for Agent 1',
                            graph_info='Fired Rules for Agent 1',
                            height=250,
                        ),
                    ]),
                ], style={'marginLeft': '0px'})
            ]),
        ]),
    ])
