import json
from collections import deque
from json import JSONEncoder
from lib2to3.pgen2 import grammar
from operator import itemgetter

import dash
import dash_html_components as html
from dash import Dash
from dash.dependencies import ALL, Input, Output, State
from dash.exceptions import PreventUpdate

from components import commonsense_card, dialog_row, next_actions_row

from .. import MESSAGE_FOR_BEFORE_DONE, MESSAGE_FOR_DONE
from . import outputs
from .data import (ADD_NODE_FUNCTION, action2literal, admissible_verbs,
                   all_commonsense, color1, color2, color_default,
                   color_select, default_network_name, edges, env_dict,
                   fired_color_name, kg_graphs, loa_agent, loa_rules, nodes,
                   roots_names, scored_action_history, text_margin_bottom,
                   twc_agent, twc_agent_goal_graphs,
                   twc_agent_manual_world_graphs)
from .functions import get_agent_actions

LOGICAL_SYMBOLS = ['AND', 'OR', 'IMPLY', 'NOT']
BTN_STYLE_IN_NETWORK_VIEWER = \
    {'float': 'right',
     'display': 'block',
     'padding-right': '0px',
     'width': '130px',
     'margin-left': '16px',
     'height': '40px'}
HIDDEN_STYLE = \
    {'visibility': 'hidden',
     'width': '0px'}
DROPDOWN_STYLE_IN_NETWORK_VIEW = \
    {'float': 'right',
     'display': 'block',
     'height': '30px',
     'width': '200px',
     'padding-right': '0px'}


class DequeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, deque):
            return list(obj)
        return JSONEncoder.default(self, obj)


def register(app: Dash):
    # Function to register the select_all callbacks,

    @app.callback(
        Output('game_level_selection', 'value'),
        [
            Input('game_level_selection', 'value')
        ]
    )
    def game_level_selection(game_level_value):
        # receive the checkbox id and the dropdown id.
        values = game_level_value
        return values

    @app.callback(Output('fired_rules_agent_1', 'children'),
                  Input('ui-shell', 'name'))
    def edit_network_graph(input):
        return outputs.fired_rules(edges, nodes, roots_names,
                                   cytolayout='dagre',
                                   id='fired_rules_agent_1_graph')

    @app.callback(Output('working_memory_agent_1', 'children'),
                  Input('ui-shell', 'name'))
    def edit_network_graph(input):
        return outputs.fired_rules(edges, nodes, roots_names,
                                   cytolayout='dagre',
                                   id='working_memory_agent_1_graph')

    @app.callback(
        [Output('interactive_agent_chat', 'children'),
         Output('interactive_agent_chat_inspect', 'children'),
         Output('next_action_row', 'children'),
         Output('game_score', 'children'),
         Output('message_for_top_of_action_selector', 'children'),
         Output('lnn_state', 'data')],
        [Input('agent_1_actions_pie_chart', 'clickData'),
         Input('agent_2_actions_pie_chart', 'clickData'),
         Input('submit_action', 'n_clicks'),
         Input('reset_environment', 'n_clicks'),
         Input('configuration_interact_games_apply', 'n_clicks'),
         Input('configuration_interact_games_reset', 'n_clicks')],
        [State('interactive_agent_chat', 'children'),
         State('game_level_selection', 'value'),
         State('all_actions_dropdown', 'value'),
         State('lnn_state', 'data')]
    )
    def add_dialog_row(agent_1_click_data,
                       agent_2_click_data,
                       submit_action_n_action,
                       reset_environment_n_clicks,
                       configuration_interact_games_apply_n_clicks,
                       configuration_interact_games_reset_n_clicks,
                       interactive_agent_chat_children,
                       game_level,
                       all_actions_dropdown,
                       lnn_state):

        env = env_dict[game_level]
        if twc_agent is not None:
            twc_agent.kg_graph = kg_graphs[game_level]
        ctx = dash.callback_context

        if not ctx.triggered:
            button_id = 'No clicks yet'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # print(button_id)
        generate_cytoscape()

        if (button_id != 'agent_1_actions_pie_chart' and
            button_id != 'agent_2_actions_pie_chart' and
            button_id != 'submit_action' and
            reset_environment_n_clicks is None) \
                or button_id == 'reset_environment' \
                or button_id == 'configuration_interact_games_reset' \
                or button_id == 'configuration_interact_games_apply':
            obs, info = env.reset()
            if twc_agent is not None:
                twc_agent.start_episode(1)
            new_interactive_chat_children = \
                [dialog_row(is_agent=False,
                            text='Objective: ' + info['objective']),
                 dialog_row(is_agent=False,
                            text=info['description'].replace('\n\n', '\n')
                            .replace('\n\n', '\n')
                            .replace('\n', '<br>')),
                 dialog_row(is_agent=False, text=info['inventory'])
                 ]
            all_actions, ns_agent_actions, dl_agent_actions, \
                facts, commonsense, selected_facts_commonsense = \
                get_agent_actions(env, obs, [0], [False], info,
                                  '', scored_action_history,
                                  loa_agent=loa_agent,
                                  dl_agent=[twc_agent,
                                            twc_agent_goal_graphs,
                                            twc_agent_manual_world_graphs])

            new_action_row = next_actions_row(
                all_actions=info['admissible_commands'],
                agent_1_actions=ns_agent_actions,
                agent_1_rules=loa_rules,
                agent_1_facts=selected_facts_commonsense,
                agent_2_actions=dl_agent_actions,
                done=False
            )

            score_str = 'Score: %d/%d' % (0, info['max_score'])

            lnn_state = {
                'actions': info['admissible_commands'],
                'facts': facts,
                'commonsense': commonsense,
                'recommended_action': sorted(ns_agent_actions,
                                             key=itemgetter(1),
                                             reverse=True)[0][0],
            }

            return \
                list(reversed(new_interactive_chat_children)), \
                list(reversed(new_interactive_chat_children)), \
                new_action_row, \
                score_str, \
                MESSAGE_FOR_BEFORE_DONE, \
                json.dumps(lnn_state)

        elif (button_id.find('pie') != -1 or
              (button_id == 'submit_action'
               and all_actions_dropdown != 'NONE')):

            # recreate old interactions
            new_interactive_chat_children = []
            for row in interactive_agent_chat_children[::-1]:
                img = \
                    row['props']['children'][0]['props']['children'][0][
                        'props']['children'][0]['props']['src']
                is_agent = True if img.find('robot') > -1 else False
                text = \
                    row['props']['children'][0]['props']['children'][0][
                        'props']['children'][1]['props']['children']
                new_interactive_chat_children.extend(
                    [dialog_row(is_agent=is_agent, text=text)])

            if button_id == 'agent_1_actions_pie_chart':
                action = agent_1_click_data['points'][0]['label']
            elif button_id == 'agent_2_actions_pie_chart':
                action = agent_2_click_data['points'][0]['label']
            elif button_id == 'submit_action':
                action = all_actions_dropdown

            obs, score, done, info = env.step(action)
            environment_response = obs

            score_str = 'Score: %d/%d' % (score, info['max_score'])

            # add new interactions
            new_interactive_chat_children.extend(
                [dialog_row(is_agent=True, text=action),
                 dialog_row(is_agent=False,
                            text=environment_response.replace('\n\n', '\n')
                            .replace('\n\n', '\n').replace('\n', '<br>'))])

            all_actions, ns_agent_actions, dl_agent_actions, \
                facts, commonsense, selected_facts_commonsense = \
                get_agent_actions(env, obs, [0], [False], info,
                                  action, scored_action_history,
                                  loa_agent=loa_agent,
                                  dl_agent=[
                                      twc_agent,
                                      twc_agent_goal_graphs,
                                      twc_agent_manual_world_graphs
                ])
            new_action_row = next_actions_row(
                all_actions=info['admissible_commands'],
                agent_1_actions=ns_agent_actions,
                agent_1_rules=loa_rules,
                agent_1_facts=selected_facts_commonsense,
                agent_2_actions=dl_agent_actions,
                done=done
            )

            lnn_state = {
                'actions': info['admissible_commands'],
                'facts': facts,
                'commonsense': commonsense,
                'recommended_action': sorted(ns_agent_actions,
                                             key=itemgetter(1),
                                             reverse=True)[0][0],
            }

            return \
                list(reversed(new_interactive_chat_children)), \
                list(reversed(new_interactive_chat_children)), \
                new_action_row, \
                score_str, \
                MESSAGE_FOR_DONE if done else MESSAGE_FOR_BEFORE_DONE, \
                json.dumps(lnn_state)
        else:
            raise PreventUpdate

    @app.callback(
        [Output('admissible_actions', 'children'),
         Output('inspect_action_dropdown', 'label'),
         Output('inspect_action_dropdown', 'options'),
         Output('inspect_action_dropdown', 'value'),
         Output('logical_facts', 'children'),
         Output('commonsense', 'children'),
         Output('graph_elements', 'data'),
         Output('graph_elements_history', 'data'),
         Output('add_node_dropdown', 'label'),
         Output('add_node_dropdown', 'options'),
         Output('add_node_dropdown', 'value'),
         Output('add_node_dropdown', 'style'),
         Output('add_node_button', 'style'),
         Output('execute_test_graph_element', 'children'),
         ],
        [Input('lnn_state', 'data'),
         Input('inspector_state', 'data'),
         Input('use_recommendation', 'data'),
         Input('delete_graph_element', 'n_clicks'),
         Input('undo_graph_element', 'n_clicks'),
         Input('add_node_button', 'n_clicks'),
         ],
        [State('selected_graph_element_id', 'data'),
         State('graph_elements', 'data'),
         State('graph_elements', 'modified_timestamp'),
         State('graph_elements_history', 'data'),
         State('add_node_dropdown', 'value'),
         ]
    )
    def update_inspection_view(
            lnn_state,
            inspected_action,
            use_recommendation,
            delete_graph_element_n_clicks,
            undo_graph_element_n_clicks,
            add_node_button_n_clicks,
            selected_element,
            current_graph,
            graph_ts,
            graph_stack,
            add_node_dropdown_value):
        current_state = json.loads(lnn_state)
        ctx = dash.callback_context

        graph_elements_history = deque()
        actions = current_state['actions']
        facts = current_state['facts']
        # commonsense = current_state['commonsense']
        recommended_action = current_state['recommended_action']

        triggered_by = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_by == 'lnn_state' or triggered_by == 'undo_graph_element':
            inspected_action = None

        if triggered_by == 'use_recommendation' and use_recommendation:
            inspected_action = recommended_action

        if inspected_action is not None:
            verb, obj1, obj2 = action2literal(inspected_action)
            objs = [obj1, obj2]
        else:
            objs = [None, None]

        graph_data = []
        execute_name = 'Execute test'

        if not current_graph:
            graph_data = generate_cytoscape()
            graph_data = clear_highlights_from_graph(graph_data)
        elif triggered_by == 'lnn_state':
            graph_data = generate_cytoscape()
            graph_data = clear_highlights_from_graph(graph_data)
        elif triggered_by == 'undo_graph_element':
            graph_elements_history = deque(json.loads(graph_stack))
            graph_data = graph_elements_history.pop()
            graph_data = clear_highlights_from_graph(graph_data)
        elif triggered_by == 'delete_graph_element':
            graph_data = json.loads(current_graph)
            graph_elements_history = deque(json.loads(graph_stack))
            graph_elements_history.append(graph_data)
            graph_data = delete_graph_element(graph_data, selected_element)
        elif triggered_by == 'add_node_button':
            graph_data = json.loads(current_graph)
            graph_elements_history = deque(json.loads(graph_stack))
            graph_elements_history.append(graph_data)

            and_name = 'and1'
            new_node = \
                {'data':
                 {'id': add_node_dropdown_value,
                  'label': add_node_dropdown_value,
                  'is_input': True},
                 'classes': ''}
            new_edge = \
                {'data':
                 {'source': add_node_dropdown_value,
                  'target': and_name,
                  'id': add_node_dropdown_value + ' → ' + and_name,
                  'label': add_node_dropdown_value + ' → ' + and_name,
                  'weight': 1.0},
                 'classes': ''}
            graph_data.append(new_node)
            graph_data.append(new_edge)
            execute_name = 'Execute train'

        elif (triggered_by == 'inspector_state' or
              triggered_by == 'use_recommendation') and current_graph:
            graph_data = json.loads(current_graph)
            graph_elements_history = deque(json.loads(graph_stack))
            graph_data = clear_highlights_from_graph(graph_data)

        input_nodes = [d['data']['label'].split('(')[0]
                       for d in graph_data if d['data'].get('is_input', False)]

        actions_list = \
            generate_admissible_actions_list(actions, inspected_action, objs)

        (dropdown_value, dropdown_options) = \
            generate_admissible_actions_dropdown(actions, inspected_action)

        facts_list, lf_keys = \
            generate_logical_facts_list(facts, objs, input_nodes)
        commonsense_list, cs_keys = \
            generate_commonsense_list(all_commonsense, objs, input_nodes)

        add_node_dropdown_value = ''
        add_node_dropdown_options = list()
        add_node_dropdown_style = HIDDEN_STYLE
        add_node_button_style = HIDDEN_STYLE

        if (triggered_by == 'inspector_state' or
                triggered_by == 'use_recommendation') and current_graph:
            if verb in get_verb_list(1):
                sub_graph, input_nodes = \
                    get_sub_graph(verb + '(x)', graph_data)
                for o in sub_graph:
                    idx = graph_data.index(o)
                    graph_data[idx]['classes'] += f' {fired_color_name}'

            if verb in get_verb_list(2):
                add_classes_from_keys_highlighted(lf_keys, graph_data)
                add_classes_from_keys_highlighted(cs_keys, graph_data)

                sub_graph, input_nodes = \
                    get_sub_graph(verb + '(x,y)', graph_data)
                all_fired = True if len(input_nodes) > 0 else False
                for n in input_nodes:
                    if fired_color_name not in n['classes']:
                        all_fired = False
                if all_fired:
                    for o in sub_graph:
                        idx = graph_data.index(o)
                        graph_data[idx]['classes'] += f' {fired_color_name}'

            if ADD_NODE_FUNCTION and \
                    (verb in get_verb_list(1) or
                     verb in get_verb_list(2)) and \
                    len(input_nodes) == 0:
                add_node_dropdown_options = [
                    {
                        'label': 'Select',
                        'value': 'ALL'
                    }
                ]

                add_node_dropdown_value = \
                    add_node_dropdown_options[0]['value']

                name_cs = \
                    list(set(
                        [f.to_plotly_json()['props'][
                            'children'][0].split(':')[0]
                         for f in commonsense_list]))

                name_facts = \
                    list(set([
                        f.to_plotly_json()['props'][
                            'children'][0].split(':')[0]
                        for f in facts_list]))

                for n in name_cs:
                    add_node_dropdown_options.append(
                        {'label': n + '(x,y)', 'value': n + '(x,y)'})

                for n in name_facts:
                    add_node_dropdown_options.append(
                        {'label': n + '(x)', 'value': n + '(x)'})
                    add_node_dropdown_options.append(
                        {'label': n + '(y)', 'value': n + '(y)'})

                add_node_dropdown_style = DROPDOWN_STYLE_IN_NETWORK_VIEW
                add_node_button_style = BTN_STYLE_IN_NETWORK_VIEWER
                add_node_button_style['margin-left'] = '0px'

        return \
            actions_list, \
            dropdown_value, dropdown_options, dropdown_value, \
            facts_list, commonsense_list, \
            json.dumps(graph_data), \
            json.dumps(graph_elements_history, cls=DequeEncoder), \
            add_node_dropdown_value, add_node_dropdown_options, \
            add_node_dropdown_value, \
            add_node_dropdown_style, add_node_button_style, \
            execute_name

    def get_sub_graph(target_id, graph_data):
        sub_graph = list()
        input_nodes = list()
        ns = list(filter(lambda li:
                         li['data']['id'] == target_id, graph_data))
        while len(ns) > 0:
            sub_graph += ns
            new_ns = list()
            for n in ns:
                es = list(filter(lambda li:
                                 li['data'].get('target', '') ==
                                 n['data']['id'], graph_data))
                for e in es:
                    new_ns += \
                        list(filter(lambda li:
                                    li['data']['id'] ==
                                    e['data'].get('source', ''), graph_data))
                sub_graph += es
            ns = list()
            for n in new_ns:
                if n['data']['label'] in LOGICAL_SYMBOLS:
                    ns += [n]
                else:
                    sub_graph += [n]
                    input_nodes += [n]
        return sub_graph, input_nodes

    def clear_highlights_from_graph(graph):
        for item in graph:
            if 'classes' in item:
                item['classes'] = \
                    item['classes'].replace('color1', '').\
                    replace('color2', '').strip()

        return graph

    def add_classes_from_keys_highlighted(keys_highlighted, graph_data):
        for key, color_class in keys_highlighted.items():
            obj = list(filter(lambda li: key in li['data']['id'] and
                              not ('weight' in li['data']),
                              graph_data))
            for o in obj:
                idx = graph_data.index(o)
                graph_data[idx]['classes'] += f' {color_class}'
        return graph_data

    def get_color(word, objs):
        if objs[0] is not None and (word + ' ') in objs[0] + ' ':
            color = color1
            x_or_y = 'x'
        elif objs[1] is not None and (word + ' ') in objs[1] + ' ':
            color = color2
            x_or_y = 'y'
        else:
            color = color_default
            x_or_y = None

        return color, x_or_y

    def get_verb_list(arity):
        verb_list = list()
        for k, v in admissible_verbs.items():
            if v == arity:
                verb_list.append(k)
        return verb_list

    def generate_admissible_actions_list(actions, selection, objs):

        if actions is None:
            return None

        items = list()

        for a in actions:
            if a == selection:
                li = list()
                ws = a.split(' ')
                for w in ws:
                    sp = ' ' if w != ws[-1] else ''
                    color = get_color(w, objs)[0]
                    li.append(
                        html.B(f"{w}{sp}",
                               style={'font-weight': '700',
                                      'color': color,
                                      'margin-bottom': text_margin_bottom}))
                items.append(html.Li(li))
            else:
                items.append(
                    html.Li(a, style={'margin-bottom': text_margin_bottom}))

        return items

    def generate_admissible_actions_dropdown(actions, selection):
        if actions is None:
            return (None, None)

        first_selection = 'Choose an action'
        dropdown_options = [
            {
                'label': first_selection,
                'value': 'ALL'
            }
        ]

        selected = dropdown_options[0]['value']

        if selection:
            selected = selection

        for a in actions:
            dropdown_options.append({'label': a, 'value': a})

        return selected, dropdown_options

    def generate_logical_facts_list(facts, objs, input_nodes):

        if facts is None:
            return None, None, None

        items = list()
        highlighted_items = list()

        sorted_facts = sorted(facts.items())
        keys_highlighted = {}

        for k, f in sorted_facts:
            highlighted = False
            fired = False

            li = [f"{k.lower()}: ["]

            # check if nested list
            # otherwise it will unpack strings
            if not isinstance(f[0], str):
                flat_facts = [item for sublist in f for item in sublist]
            else:
                flat_facts = f

            for ff in flat_facts:
                comma = ", "
                if ff == flat_facts[-1]:
                    comma = ""

                color, x_or_y = get_color(ff, objs)

                if color != color_default:
                    li.append(html.B(f"{ff}",
                                     style={'color': color,
                                            'font-weight': '700'}))
                    li.append(f"{comma}")

                    highlighted = True
                    if k in input_nodes:
                        fired = True

                    if k.lower() in keys_highlighted:
                        keys_highlighted[k.lower() + '(' + x_or_y + ')'] += \
                            ' ' + fired_color_name
                    else:
                        keys_highlighted[k.lower() +
                                         '(' + x_or_y + ')'] = fired_color_name
                else:
                    li.append(f"{ff}{comma}")

            li.append(']')
            if highlighted:
                if fired:
                    highlighted_items.append(
                        html.Li(li,
                                style={'margin-bottom': text_margin_bottom,
                                       'font-weight': '700',
                                       'text-decoration': 'underline'}))
                else:
                    highlighted_items.append(
                        html.Li(li,
                                style={'margin-bottom': text_margin_bottom}))
            else:
                items.append(
                    html.Li(li, style={'margin-bottom': text_margin_bottom}))

        return highlighted_items + items, keys_highlighted

    def generate_commonsense_list(commonsense, objs, input_nodes):

        if commonsense is None:
            return None, None, None

        items = []
        highlighted_items = []
        keys_highlighted = {}

        for k, fs in commonsense.items():
            for f in fs:
                highlighted = 0
                fired = False

                li = [f"{k}: ["]

                if not isinstance(f[0], str):
                    flat_commonsense = \
                        [item for sublist in f for item in sublist]
                else:
                    flat_commonsense = f

                for fc in flat_commonsense:
                    comma = ", "
                    if fc == flat_commonsense[-1]:
                        comma = ""
                    color, _ = get_color(fc, objs)

                    if color != color_default:
                        li.append(html.B(f"{fc}",
                                         style={'color': color,
                                                'font-weight': '700'}))
                        li.append(f"{comma}")
                        highlighted += 1
                    else:
                        li.append(f"{fc}{comma}")

                li.append(']')

                style = {}
                if highlighted > 0:
                    if highlighted == 2 and k in input_nodes:
                        keys_highlighted[k + '(x,y)'] = fired_color_name
                        style = {'font-weight': '700',
                                 'text-decoration': 'underline'}
                    style.update({'margin-bottom': text_margin_bottom})
                    highlighted_items.append(html.Li(li, style=style))
                else:
                    items.append(html.Li(li, style=style))

        return highlighted_items + items, keys_highlighted

    def generate_cytoscape(network_name=default_network_name):
        if network_name == 'lnn_twc_with_empty':
            network = \
                {"epochs": 1,
                 "input": ["carry(x)", "empty(y)",
                           "at_location(x,y)", "true"],
                 "network": {
                     "and1": {"gate_type": "AND",
                              "parents": ["carry(x)", "empty(y)",
                                           "at_location(x,y)"],
                              "weights": [[1.0, 1.0, 1.0]]},
                     "and2": {"gate_type": "AND",
                              "parents": ["carry(x)", "empty(y)",
                                           "at_location(x,y)"],
                              "weights": [[1.0, 1.0, 1.0]]},
                     "imply1": {"gate_type": "IMPLY",
                                "parents": ["and1"], "weights": [[1.0]]},
                     "imply2": {"gate_type": "IMPLY",
                                "parents": ["and2"], "weights": [[1.0]]},
                     "imply3": {"gate_type": "IMPLY",
                                "parents": ["true"], "weights": [[1.0]]},
                     "insert(x,y)": {"gate_type": "NODE",
                                     "parents": ["imply1"],
                                     "weights": [[1.0]]},
                     "put(x,y)": {"gate_type": "NODE",
                                  "parents": ["imply2"],
                                  "weights": [[1.0]]},
                     "take(x)": {"gate_type": "NODE",
                                 "parents": ["imply3"],
                                 "weights": [[1.0]]}}}

        elif network_name == 'lnn_twc_wo_empty':
            network = \
                {"epochs": 1,
                 "input": ["carry(x)", "at_location(x,y)", "true"],
                 "network": {
                     "and1": {"gate_type": "AND",
                              "parents": ["carry(x)", "at_location(x,y)"],
                              "weights": [[1.0, 1.0]]},
                     "and2": {"gate_type": "AND",
                              "parents": ["carry(x)", "at_location(x,y)"],
                              "weights": [[1.0, 1.0]]},
                     "imply1": {"gate_type": "IMPLY",
                                "parents": ["and1"], "weights": [[1.0]]},
                     "imply2": {"gate_type": "IMPLY",
                                "parents": ["and2"], "weights": [[1.0]]},
                     "imply3": {"gate_type": "IMPLY",
                                "parents": ["true"], "weights": [[1.0]]},
                     "insert(x,y)": {"gate_type": "NODE",
                                     "parents": ["imply1"],
                                     "weights": [[1.0]]},
                     "put(x,y)": {"gate_type": "NODE",
                                  "parents": ["imply2"],
                                  "weights": [[1.0]]},
                     "take(x)": {"gate_type": "NODE",
                                 "parents": ["imply3"],
                                 "weights": [[1.0]]}}}

        elif network_name == 'lnn_twc_init':
            network = \
                {"epochs": 1,
                 "input": [],
                 "network": {
                     "and1": {"gate_type": "AND",
                              "parents": [],
                              "weights": []},
                     "imply1": {"gate_type": "IMPLY",
                                "parents": ["and1"], "weights": [[1.0]]},
                     "insert(x,y)": {"gate_type": "NODE",
                                     "parents": ["imply1"],
                                     "weights": [[1.0]]}}}

        nodes = []

        for i in network['input']:
            nodes.append(i)

        for ops in network['network'].keys():
            nodes.append(ops)

        cyto_el = []

        for n in nodes:
            label = n
            css_classes = ''

            if 'and' in n:
                label = 'AND'
                css_classes = 'logicGate and'
            if 'or' in n:
                label = 'OR'
                css_classes = 'logicGate or'
            if 'not' in n:
                label = 'NOT'
                css_classes = 'logicGate not'
            if 'imply' in n:
                label = 'IMPLY'
                css_classes = 'logicGate imply'
            if 'true' in n:
                label = 'TRUE'
                css_classes = 'logicGate true'

            cyto_el.append({'data': {'id': n, 'label': label,
                                     'is_input': label in network['input']},
                            'classes': css_classes})

        css_classes = ''
        for ops_id, ops in network['network'].items():
            for idx, p in enumerate(ops['parents']):
                weight = ops['weights'][-1][idx]
                gate_type = ops["gate_type"]
                if gate_type == 'NODE':
                    gate_type = '→'
                cyto_el.append(
                    {'data': {'source': p,
                              'target': ops_id,
                              'id': f'{p} {gate_type} {ops_id}',
                              'label': f'{p} {gate_type} {ops_id}',
                              'weight': weight},
                     'classes': css_classes})

        return cyto_el

    @app.callback(
        Output('inspector_state', 'data'),
        Input('submit_inspect_action', 'n_clicks'),
        State('inspect_action_dropdown', 'value')
    )
    def inspect_action(n_clicks, selected):
        return selected

    @app.callback(
        Output('use_recommendation', 'data'),
        Input('select_recommendation_action', 'n_clicks')
    )
    def inspect_recommendation_action(n_clicks):
        return False if n_clicks is None else True

    @app.callback(
        Output('interact_tabs', 'value'),
        Input('agent_1_details_button', 'n_clicks')
    )
    def inspect_recommendation_action(n_clicks):
        return 'interact_tab' if n_clicks is None else 'inspect_tab'

    @app.callback(
        [Output('fired_rules_agent_1_graph', 'elements'),
         Output('fired_rules_agent_1_graph', 'layout'),
         Output('fired_rules_agent_1_graph', 'stylesheet'),
         Output('fired_rules_agent_1_graph', 'style'),
         Output('fired_rules_agent_1_graph', 'responsive'),
         ],
        Input('graph_elements', 'modified_timestamp'),
        State('graph_elements', 'data')
    )
    def update_graph_elements(ts, data):

        layout = {'name': 'dagre', 'rankDir': 'LR', 'nodeSep': '25'}
        style = {'height': '450px', 'width': '90%'}
        stylesheet = [
            {
                'selector': 'node',
                'style': {
                    'content': 'data(label)',
                    'color': '#000',
                    'text-outline-color': '#fff',
                    'text-outline-width': '2px'
                }
            },
            {
                'selector': 'node:selected',
                'style': {
                    'content': 'data(label)',
                    'background-color': color_select,
                    'border-color': color_select,
                    'border-width': '3px'
                }
            },
            {
                'selector': 'edge:selected',
                'style': {
                    'line-color': color_select
                }
            },
            {
                'selector': '.color1',
                'style': {
                    'background-color': color1,
                    'line-color': color1
                }
            },
            {
                'selector': '.color2',
                'style': {
                    'background-color': color2,
                    'line-color': color2
                }
            },
            {
                'selector': '.logicGate',
                'style': {
                    'color': '#fff',
                    'text-halign': 'center',
                    'text-valign': 'center',
                    'text-outline-width': '0px',
                    'font-weight': 700
                }
            },
            {
                'selector': '.logicGate.and',
                'style': {
                    'content': '∧'
                }
            },
            {
                'selector': '.logicGate.or',
                'style': {
                    'content': '∨'
                }
            },
            {
                'selector': '.logicGate.not',
                'style': {
                    'content': '¬'
                }
            },
            {
                'selector': '.logicGate.imply',
                'style': {
                    'content': '→'
                }
            },
            {
                'selector': '.logicGate.true',
                'style': {
                    'content': 'true',
                    'font-weight': 'normal'
                    # 'content': '⊤'
                }
            }
        ]

        elements = []

        # ts is -1 when initialized
        # See
        # https://dash.plotly.com/dash-core-components/store#retrieving-the-initial-store-data

        ts != -1 or ts

        if data:
            elements = json.loads(data)

        return elements, layout, stylesheet, style, True

    @app.callback(
        [Output('selected_graph_element', 'children'),
         Output('delete_graph_element', 'children'),
         Output('delete_graph_element', 'style'),
         Output('selected_graph_element_id', 'data'),
         ],
        [Input('fired_rules_agent_1_graph', 'tapNodeData'),
         Input('fired_rules_agent_1_graph', 'tapEdgeData'),
         Input('delete_graph_element', 'n_clicks'),
         Input('undo_graph_element', 'n_clicks')
         ]
    )
    def select_graph_element(node, edge, delete_n_clicks, undo_n_clicks):
        ctx = dash.callback_context
        triggered_by = ctx.triggered[0]['prop_id'].split('.')[1]

        if triggered_by == 'n_clicks':
            return 'Select a node or edge', 'Delete element', \
                   HIDDEN_STYLE, ''

        if node is not None and triggered_by == 'tapNodeData':
            if node['label'] == node['id']:
                html_el = [
                    html.B('SELECTED NODE:', style={'font-weight': '700'}),
                    html.Span(f' {node["label"]}')
                ]
                return html_el, 'Delete node', \
                    BTN_STYLE_IN_NETWORK_VIEWER, node['id']

        if triggered_by == 'tapEdgeData':
            html_el = [
                html.B('SELECTED EDGE:', style={'font-weight': '700'}),
                html.Span(f' {edge["label"]} - Weight: {edge["weight"]}')
            ]
            return html_el, 'Delete edge', \
                BTN_STYLE_IN_NETWORK_VIEWER, edge['id']

        return 'Select a node or edge', 'Delete element', \
               HIDDEN_STYLE, ''

    def delete_graph_element(graph, el):
        nodes_deleted = list(filter(lambda n: n['data']['id'] != el, graph))
        res = list(filter(lambda e:
                          not (el in e['data']['label']), nodes_deleted))
        return res

    @app.callback(
        [
            Output('execute_test_graph_element', 'style'),
            Output('undo_graph_element', 'style'),
        ],
        Input('graph_elements_history', 'modified_timestamp'),
        State('graph_elements_history', 'data')
    )
    def change_button_visibility(graph_stack_ts, graph_stack):
        if graph_stack_ts != -1 and graph_stack:
            undo_count = len(json.loads(graph_stack))
        else:
            undo_count = 0

        if undo_count > 0:
            return BTN_STYLE_IN_NETWORK_VIEWER, BTN_STYLE_IN_NETWORK_VIEWER
        else:
            return HIDDEN_STYLE, HIDDEN_STYLE
