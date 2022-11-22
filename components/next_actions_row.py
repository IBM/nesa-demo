from colorsys import hls_to_rgb

import dash_carbon_components as dca
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from numpy import tile, zeros

NEXT_ACTION_MIN_CONFIDENCE = 0.05
BUTTON_TITLE_FOR_GO_INSPECTION = 'Check inside of the model'


def next_actions_row(all_actions: list,
                     agent_1_actions: dict,
                     agent_1_rules: dict,
                     agent_1_facts: dict,
                     agent_2_actions: dict,
                     done: bool):

    hex_array = []
    step = 360 // len(all_actions)
    for angle in range(0, 360, step):
        rgb = hls_to_rgb(angle / 360, .7, .7)
        hex = \
            '#%02x%02x%02x' % \
            (round(rgb[0] * 255), round(rgb[1] * 255), round(rgb[2] * 255))
        hex_array.append(hex)
    colors = {'colors': hex_array}

    all_actions_list = []
    for idx, action in enumerate(sorted(all_actions)):
        all_actions_list += [html.Li(
            children=[
                html.Span(
                    style={
                        'width': '12px',
                        'height': '12px',
                        'background': colors['colors'][idx],
                        'display':'inline-block',
                        'margin-right':'6px'
                    }
                ),
                html.Span(action),
                html.Br()
            ]
        )]

    first_selection = 'Select an action'
    dropdown_options = [
        {
            'label': first_selection,
            'value': 'NONE'
        }
    ]

    for idx, action in enumerate(sorted(all_actions)):
        dropdown_options.append({'label': action, 'value': action})

    actions_dropdown = dca.Dropdown(
        id='all_actions_dropdown',
        label=first_selection,
        options=dropdown_options,
        value=dropdown_options[0]['value'],
        style={
            'height': '40px',
        }
    )

    action_submit = dca.Button(
        'Perform this action',
        id='submit_action',
        kind='primary',
        style={
            'height': '40px',
        },
        size='small'
    )

    all_actions_card = dca.Card(
        id='all_actions_card',
        title='All possible actions',
        children=[
            html.Ul(
                children=all_actions_list,
                className='lead',
                style={
                    'padding-top': '10px',
                    'padding-bottom': '10px',
                    'listStyleType': 'none'
                }
            ),
            html.Br(),
            dca.Column(actions_dropdown, columnSizes=['md-9']),
            dca.Column(action_submit, columnSizes=['md-9'])
        ],
        style={
            'width': '100%',
            'height': 'calc(100% - 50px)',
        }
    )

    # Agent 1 Actions Card
    agent_1_labels_list = []
    agent_1_values_list = []
    agent_1_text_pos_list = []

    for action, confidence in agent_1_actions:
        agent_1_labels_list.append(action)
        agent_1_values_list.append(confidence)

        if confidence > NEXT_ACTION_MIN_CONFIDENCE:
            agent_1_text_pos_list.append('outside')
        else:
            agent_1_text_pos_list.append('none')

    agent_1_max_idx = agent_1_values_list.index(max(agent_1_values_list))
    agent_1_pull = zeros(len(agent_1_values_list))
    agent_1_pull[agent_1_max_idx] = 0.3

    agent_layout = \
        go.Layout(title='Click to perform a recommended action',
                  hovermode='closest',
                  height=330)

    agent_1_rules_children = list()
    if agent_1_rules is not None:
        for k, v in agent_1_rules.items():
            if v != '':
                agent_1_rules_children.append(
                    v.replace('atlocation', 'at_location') + ' → ' + k)
                agent_1_rules_children.append(html.Br())
        agent_1_rules_children = agent_1_rules_children[:-1]

    agent_1_logical_facts_children = list()
    if agent_1_facts is not None:
        for k, v in agent_1_facts.items():
            if v != []:
                for i in v:
                    if isinstance(i, list):
                        agent_1_logical_facts_children.append(
                            k + '(' + ', '.join(i) + ')')
                    else:
                        agent_1_logical_facts_children.append(k + '(%s)' % i)
                    agent_1_logical_facts_children.append(', ')
                agent_1_logical_facts_children = \
                    agent_1_logical_facts_children[:-1]
                agent_1_logical_facts_children.append(html.Br())
        agent_1_logical_facts_children = agent_1_logical_facts_children[:-1]
    else:
        agent_1_logical_facts_children.append('AMR does not work')

    agent_1_actions_card = dca.Card(
        id='agent_1_actions_card',
        title='Neuro-symbolic agent',
        children=[
            dcc.Graph(
                id='agent_1_actions_pie_chart',
                figure=go.Figure(
                    data=[go.Pie(
                        name="",
                        labels=agent_1_labels_list,
                        values=agent_1_values_list,
                        sort=False,
                        marker=dict(colors,
                                    line=dict(color='#efefef', width=1)),
                        pull=agent_1_pull,
                        textposition=agent_1_text_pos_list,
                        showlegend=False,
                        hovertemplate="%{label}<br>%{percent}",
                    )],
                    layout=agent_layout
                )),

            html.P('Current logical facts & commonsense: ',
                   style={'text-align': 'left', 'font-weight': 'bold'}),
            html.P(
                id='logical_facts_p',
                children=agent_1_logical_facts_children,
                style={'text-align': 'center'}),
            html.Br(),
            html.P('Trained rules: ',
                   style={'text-align': 'left', 'font-weight': 'bold'}),
            html.P(
                id='loa_rule_p',
                children=agent_1_rules_children,
                style={'text-align': 'center'}),
            html.Br(),
            html.Br(),
            dca.Button(id='agent_1_details_button',
                       size='sm', children=BUTTON_TITLE_FOR_GO_INSPECTION,
                       kind='primary',
                       style={'margin-left': 'auto',
                              'margin-right': 'auto',
                              'display': 'block',
                              'height': '40px'}),

        ],
        style={'width': '100%'}
    )

    # Agent 2 Actions Card
    agent_2_labels_list = []
    agent_2_values_list = []
    agent_2_text_pos_list = []

    for action, confidence in agent_2_actions:
        agent_2_labels_list.append(action)
        agent_2_values_list.append(confidence)

        if confidence > NEXT_ACTION_MIN_CONFIDENCE:
            agent_2_text_pos_list.append('outside')
        else:
            agent_2_text_pos_list.append('none')

    agent_2_max_idx = agent_2_values_list.index(max(agent_2_values_list))
    agent_2_pull = zeros(len(agent_2_values_list))
    agent_2_pull[agent_2_max_idx] = 0.3

    agent_2_actions_card = dca.Card(
        id='agent_2_actions_card',
        title='Deep learning agent',
        children=[
            dcc.Graph(
                id='agent_2_actions_pie_chart',
                figure=go.Figure(
                    data=[go.Pie(
                        name="",
                        labels=agent_2_labels_list,
                        values=agent_2_values_list,
                        sort=False,
                        marker=dict(colors,
                                    line=dict(color='#efefef', width=1)),
                        pull=agent_2_pull,
                        textposition=agent_2_text_pos_list,
                        showlegend=False,
                        hovertemplate="%{label}<br>%{percent}",
                    )],
                    layout=agent_layout
                )),
            html.Br(),
            html.Br(),
            dca.Button(id='agent_2_details_button',
                       size='sm', children=BUTTON_TITLE_FOR_GO_INSPECTION,
                       kind='primary',
                       disabled=True,
                       style={'margin-left': 'auto',
                              'margin-right': 'auto',
                              'display': 'block',
                              'height': '40px'}),
        ],
        style={'width': '100%'}
    )

    final_row = dca.Row(
        children=[
            dca.Row(
                children=[
                    dca.Column(all_actions_card, columnSizes=['md-2'],
                               style={'width': '450px'}),
                    dca.Column(agent_1_actions_card, columnSizes=['md-3'],
                               style={'width': '450px'}),
                    dca.Column(agent_2_actions_card, columnSizes=['md-3'],
                               style={'width': '450px'})
                ],
                style={
                }
            )
        ],
        style={'padding-left': '2em'}
    ) if not done else dca.Row(children=[])

    return final_row
