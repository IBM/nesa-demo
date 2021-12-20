import dash
from components import dialog_row, next_actions_row
from dash import Dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_html_components.P import P

from .. import MESSAGE_FOR_DONE, MESSAGE_FOR_SELECT_NEXT_ACTION
from . import outputs
from .data import (edges, env_dict, kg_graphs, loa_agent, loa_rules, nodes,
                   roots_names, scored_action_history, twc_agent,
                   twc_agent_goal_graphs, twc_agent_manual_world_graphs)
from .functions import get_agent_actions


def register(app: Dash):
    # Function to register the select_all callbacks,
    # receive the checkbox id and the dropdown id.

    @app.callback(
        Output('game_level_selection', 'value'),
        [
            Input('game_level_selection', 'value')
        ]
    )
    def game_level_selection(game_level_value):
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
         Output('next_action_row', 'children'),
         Output('game_score', 'children'),
         Output('message_for_top_of_action_selector', 'children')],
        [Input('agent_1_actions_pie_chart', 'clickData'),
         Input('agent_2_actions_pie_chart', 'clickData'),
         Input('submit_action', 'n_clicks'),
         Input('reset_environment', 'n_clicks'),
         Input('configuration_interact_games_apply', 'n_clicks'),
         Input('configuration_interact_games_reset', 'n_clicks')],
        [State('interactive_agent_chat', 'children'),
         State('game_level_selection', 'value'),
         State('all_actions_dropdown', 'value')]
    )
    def add_dialog_row(agent_1_click_data,
                       agent_2_click_data,
                       submit_action_n_action,
                       reset_environment_n_clicks,
                       configuration_interact_games_apply_n_clicks,
                       configuration_interact_games_reset_n_clicks,
                       interactive_agent_chat_children,
                       game_level,
                       all_actions_dropdown):

        env = env_dict[game_level]
        if twc_agent is not None:
            twc_agent.kg_graph = kg_graphs[game_level]
        ctx = dash.callback_context

        if not ctx.triggered:
            button_id = 'No clicks yet'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        print(button_id)

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
                            .replace('\n', '<br>')),
                 dialog_row(is_agent=False, text=info['inventory'])
                 ]
            all_actions, ns_agent_actions, dl_agent_actions, loa_facts = \
                get_agent_actions(env, obs, [0], [False], info,
                                  '', scored_action_history,
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
                agent_1_facts=loa_facts,
                agent_2_actions=dl_agent_actions,
                done=False
            )

            score_str = 'Score: %d/%d' % (0, info['max_score'])

            return \
                list(reversed(new_interactive_chat_children)), \
                new_action_row, \
                score_str, \
                MESSAGE_FOR_SELECT_NEXT_ACTION

        elif (button_id.find('pie') != -1 or
              (button_id == 'submit_action'
               and all_actions_dropdown != 'NONE')):

            print(all_actions_dropdown)

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

            if (button_id == 'agent_1_actions_pie_chart'):
                action = agent_1_click_data['points'][0]['label']
            elif (button_id == 'agent_2_actions_pie_chart'):
                action = agent_2_click_data['points'][0]['label']
            elif (button_id == 'submit_action'):
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

            all_actions, ns_agent_actions, dl_agent_actions, loa_facts = \
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
                agent_1_facts=loa_facts,
                agent_2_actions=dl_agent_actions,
                done=done
            )

            return \
                list(reversed(new_interactive_chat_children)), \
                new_action_row, \
                score_str, \
                MESSAGE_FOR_DONE if done else MESSAGE_FOR_SELECT_NEXT_ACTION
        else:
            raise PreventUpdate
