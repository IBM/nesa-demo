import copy
import glob
import os
import random
import sys

import gym
import textworld
import textworld.gym
import torch
from textworld import EnvInfos

if True:
    sys.path.append(os.path.join(os.path.dirname(__file__) + '/../../../'))

    from third_party.loa.amr_parser import get_formatted_obs_text
    from third_party.loa.logical_twc import Action2Literal
    from third_party.loa.utils import obtain_predicates_logic_vector


home_dir = './'

request_infos = \
    EnvInfos(verbs=True, moves=True, inventory=True, description=True,
             objective=True, intermediate_reward=True,
             policy_commands=True, max_score=True, admissible_commands=True,
             last_action=True, game=True, facts=True, entities=True,
             won=True, lost=True, location=True)


def load_twc_game(level_str, type_str, index):
    game_file_names = sorted(glob.glob(
        os.path.join(home_dir, 'static', 'games', 'twc', '%s', '%s', '*.ulx') %
        (level_str, type_str)))
    game_file_name = [game_file_names[index]]
    env_id = \
        textworld.gym.register_games(game_file_name, request_infos,
                                     max_episode_steps=50,
                                     name='twc-%s-%s-%d' %
                                          (level_str, type_str, index),
                                     batch_size=None)
    env = gym.make(env_id)

    return env


def info2infos(info):
    return {k: [v] for k, v in info.items()}


def convert_instance_for_commonsense(cs_raw, is_instance_raw):
    cs_list = list()
    for cs in cs_raw:
        li = list()
        for o in cs:
            found = False
            for ins in is_instance_raw:
                if o == ins[1]:
                    li.append(ins[0])
                    found = True
                    break
            if not found:
                li.append(o)
        cs_list.append(li)
    return cs_list


def get_agent_actions(env, obs, score, done, info,
                      action, scored_action_history,
                      loa_agent=None, dl_agent=None):
    from ..data import rest_amr

    action2literal = Action2Literal()
    all_actions = info['admissible_commands']
    if loa_agent is None:
        ns_agent_actions_list = \
            [a for a in all_actions if not a.startswith('examine')]
        ns_agent_actions = \
            [[a, random.random()] for a in ns_agent_actions_list]
    else:
        ns_agent_actions = list()

        env_facts = env.get_logical_state(info)
        obs_text = get_formatted_obs_text(info)
        commonsense = dict()

        try:
            facts, _ = rest_amr.obs2facts(obs_text, mode='propbank')
            rest_amr.save_cache()

            facts_cs = copy.deepcopy(facts)
            facts_cs['atlocation'] = env_facts['atlocation']
            facts_cs['is_instance'] = env_facts['is_instance']

            commonsense['at_location'] = \
                convert_instance_for_commonsense(env_facts['atlocation'],
                                                 env_facts['is_instance'])

            selected_facts_commonsense = \
                {
                    'at_location': commonsense['at_location'],
                    'carry': facts['carry'] if 'carry' in facts else []
                }

            for adm_comm in all_actions:
                rule, x, y = action2literal(adm_comm)
                if rule in loa_agent.admissible_verbs:
                    rule_arity = loa_agent.admissible_verbs[rule]

                    logic_vector, all_preds = \
                        obtain_predicates_logic_vector(
                            rule_arity, x, y,
                            facts=facts_cs,
                            template=loa_agent.arity_predicate_templates)
                    logic_vector = logic_vector.unsqueeze(0)
                    yhat = loa_agent.pi.forward_eval(logic_vector,
                                                     lnn_model_name=rule)
                    # print("{} : {:.2f}".format(adm_comm, yhat.item()))
                    ns_agent_actions.append([adm_comm, float(yhat.item())])
                else:
                    ns_agent_actions.append([adm_comm, 0])

        except Exception:
            selected_facts_commonsense = None
            for adm_comm in all_actions:
                ns_agent_actions.append([adm_comm, 0])

    if dl_agent is None or dl_agent[0] is None:
        dl_agent_actions_list = \
            [a for a in all_actions if a.startswith('examine')]
        dl_agent_actions = \
            [[a, random.random()] for a in dl_agent_actions_list]
    else:
        dl_agent_actions = list()

        twc_agent, twc_agent_goal_graphs, twc_agent_manual_world_graphs = \
            dl_agent

        infos = info2infos(info)

        game_goal_graphs = [None] * 1
        game_manual_world_graph = [None] * 1

        for b, game in enumerate(infos["game"]):
            if "uuid" in game.metadata:
                game_id = game.metadata["uuid"].split("-")[-1]
                game_goal_graphs[b] = twc_agent_goal_graphs[game_id]
                game_manual_world_graph[b] = \
                    twc_agent_manual_world_graphs[game_id]

        infos['goal_graph'] = game_goal_graphs
        infos['manual_world_graph'] = game_manual_world_graph

        if twc_agent.graph_emb_type and \
                ('local' in twc_agent.graph_type or
                 'world' in twc_agent.graph_type):
            twc_agent.update_current_graph([obs], [action],
                                           scored_action_history,
                                           infos,
                                           'evolve')

        action, commands_values = \
            twc_agent.act([obs], [score], [done], infos,
                          scored_action_history, random_action=False)

        values = torch.nn.functional.softmax(commands_values)[0].tolist()

        for i, a in enumerate(all_actions):
            dl_agent_actions.append([a, values[i]])

    return all_actions, ns_agent_actions, dl_agent_actions, \
        facts, commonsense, selected_facts_commonsense
