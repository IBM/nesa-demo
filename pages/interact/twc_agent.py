from typing import Any, Mapping

import numpy as np

import torch

from .. import EASY_LEVEL, HARD_LEVEL, LEVELS, MEDIUM_LEVEL

if True:
    from third_party.commonsense_rl import agent
    from third_party.commonsense_rl.games import dataset
    from third_party.commonsense_rl.utils_twc import extractor
    from third_party.commonsense_rl.utils_twc.kg \
        import (RelationExtractor, construct_kg, load_manual_graphs)
    from third_party.commonsense_rl.utils_twc.nlp import Tokenizer
    from third_party.commonsense_rl.utils_twc.textworld_utils \
        import get_goal_graph
    from third_party.commonsense_rl.utils_twc.generic import max_len, to_tensor

    kg_graphs = dict()


class TestKnowledgeAwareAgent(agent.KnowledgeAwareAgent):
    def act(self, obs: str, score: int,
            done: bool, infos: Mapping[str, Any],
            scored_commands: list, random_action=False):
        batch_size = len(obs)
        if not self._episode_has_started:
            self.start_episode(batch_size)

        just_finished = [done[b] != self.last_done[b]
                         for b in range(batch_size)]
        sel_rand_action_idx = \
            [np.random.choice(len(infos["admissible_commands"][b]))
             for b in range(batch_size)]
        if random_action:
            return \
                [infos["admissible_commands"][b][sel_rand_action_idx[b]]
                 for b in range(batch_size)]

        torch.autograd.set_detect_anomaly(True)
        input_t = []
        # Build agent's observation: feedback + look + inventory.
        state = ["{}\n{}\n{}\n{}".format(obs[b],
                                         infos["description"][b],
                                         infos["inventory"][b],
                                         ' \n'.join(scored_commands[b]))
                 for b in range(batch_size)]
        # Tokenize and pad the input and the commands to chose from.
        state_tensor = self._process(state, self.word2id)

        command_list = []
        for b in range(batch_size):
            cmd_b = self._process(infos["admissible_commands"][b],
                                  self.word2id)
            command_list.append(cmd_b)
        max_num_candidate = \
            max_len(infos["admissible_commands"])
        max_num_word = max([cmd.size(1) for cmd in command_list])
        commands_tensor = \
            to_tensor(np.zeros((batch_size, max_num_candidate, max_num_word)),
                      self.device)
        for b in range(batch_size):
            commands_tensor[b, :command_list[b].size(0),
                            :command_list[b].size(1)] = command_list[b]

        localkg_tensor = torch.FloatTensor()
        localkg_adj_tensor = torch.FloatTensor()
        worldkg_tensor = torch.FloatTensor()
        worldkg_adj_tensor = torch.FloatTensor()
        localkg_hint_tensor = torch.FloatTensor()
        worldkg_hint_tensor = torch.FloatTensor()
        if self.graph_emb_type is not None and \
                ('local' in self.graph_type or 'world' in self.graph_type):

            # prepare Local graph and world graph ....
            # Extra empty node (sentinel node) for no attention option
            #  (Xiong et al ICLR 2017 and https://arxiv.org/pdf/1612.01887.pdf)
            if 'world' in self.graph_type:
                world_entities = []
                for b in range(batch_size):
                    world_entities.extend(self.world_graph[b].nodes())
                world_entities = set(world_entities)
                wentities2id = dict(
                    zip(world_entities, range(len(world_entities))))
                max_num_nodes = \
                    len(wentities2id) + \
                    1 if self.sentinel_node else len(wentities2id)
                worldkg_tensor = \
                    self._process(wentities2id, self.node2id,
                                  sentinel=self.sentinel_node)
                world_adj_matrix = \
                    np.zeros((batch_size, max_num_nodes, max_num_nodes),
                             dtype="float32")
                for b in range(batch_size):
                    # get adjacentry matrix for each batch based on the
                    # all_entities
                    triplets = [list(edges)
                                for edges
                                in self.world_graph[b].edges.data('relation')]
                    for [e1, e2, r] in triplets:
                        e1 = wentities2id[e1]
                        e2 = wentities2id[e2]
                        world_adj_matrix[b][e1][e2] = 1.0
                        world_adj_matrix[b][e2][e1] = 1.0  # reverse relation
                    for e1 in list(self.world_graph[b].nodes):
                        e1 = wentities2id[e1]
                        world_adj_matrix[b][e1][e1] = 1.0
                    if self.sentinel_node:  # Fully connected sentinel
                        world_adj_matrix[b][-1, :] = \
                            np.ones((max_num_nodes), dtype="float32")
                        world_adj_matrix[b][:, -1] = \
                            np.ones((max_num_nodes), dtype="float32")
                worldkg_adj_tensor = \
                    to_tensor(world_adj_matrix, self.device, type="float")

            if 'local' in self.graph_type:
                local_entities = []
                for b in range(batch_size):
                    local_entities.extend(self.local_graph[b].nodes())
                local_entities = set(local_entities)
                lentities2id = dict(
                    zip(local_entities, range(len(local_entities))))
                max_num_nodes = \
                    len(lentities2id) + \
                    1 if self.sentinel_node else len(lentities2id)
                localkg_tensor = \
                    self._process(lentities2id, self.word2id,
                                  sentinel=self.sentinel_node)
                local_adj_matrix = np.zeros(
                    (batch_size, max_num_nodes, max_num_nodes),
                    dtype="float32")
                for b in range(batch_size):
                    # get adjacentry matrix for each batch based on the
                    # all_entities
                    triplets = [list(edges)
                                for edges
                                in self.local_graph[b].edges.data('relation')]
                    for [e1, e2, r] in triplets:
                        e1 = lentities2id[e1]
                        e2 = lentities2id[e2]
                        local_adj_matrix[b][e1][e2] = 1.0
                        local_adj_matrix[b][e2][e1] = 1.0
                    for e1 in list(self.local_graph[b].nodes):
                        e1 = lentities2id[e1]
                        local_adj_matrix[b][e1][e1] = 1.0
                    if self.sentinel_node:
                        local_adj_matrix[b][-1, :] = np.ones((max_num_nodes),
                                                             dtype="float32")
                        local_adj_matrix[b][:, -1] = np.ones((max_num_nodes),
                                                             dtype="float32")
                localkg_adj_tensor = to_tensor(local_adj_matrix, self.device,
                                               type="float")

            if len(scored_commands) > 0:
                # Get the scored commands as one string
                hint_str = \
                    [' \n'.join(scored_commands[b][-self.hist_scmds_size:])
                     for b in range(batch_size)]
            else:
                hint_str = [obs[b] + ' \n' + infos["inventory"][b]
                            for b in range(batch_size)]
            localkg_hint_tensor = self._process(hint_str, self.word2id)
            worldkg_hint_tensor = self._process(hint_str, self.node2id)

        input_t.append(state_tensor)
        input_t.append(commands_tensor)
        input_t.append(localkg_tensor)
        input_t.append(localkg_hint_tensor)
        input_t.append(localkg_adj_tensor)
        input_t.append(worldkg_tensor)
        input_t.append(worldkg_hint_tensor)
        input_t.append(worldkg_adj_tensor)

        outputs, indexes, values = self.model(*input_t)
        outputs, indexes, values = \
            outputs, indexes.view(batch_size), values.view(batch_size)
        sel_action_idx = [indexes[b] for b in range(batch_size)]
        action = \
            [infos["admissible_commands"][b][sel_action_idx[b]]
             for b in range(batch_size)]

        if any(done):
            for b in range(batch_size):
                if done[b]:
                    self.model.reset_hidden_per_batch(b)
                    action[b] = 'look'

        assert self.mode == "test"
        return action, outputs


class myDict(dict):
    def __init__(self, **arg):
        super(myDict, self).__init__(**arg)

    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)


def get_twc_agent():
    opt = myDict()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    opt.difficulty_level = 'easy'
    opt.graph_type = 'world'
    opt.graph_mode = 'evolve'
    opt.mode = 'test'
    opt.eval_max_step_per_episode = 50
    opt.local_evolve_type = 'direct'
    opt.hidden_size = 300
    opt.world_evolve_type = 'manual'
    opt.egreedy_epsilon = 0.0
    opt.emb_loc = 'embeddings/'
    opt.word_emb_type = 'glove'
    opt.graph_emb_type = 'glove'
    opt.hist_scmds_size = 3
    opt.batch_size = 1
    opt.no_eval_episodes = 5
    opt.verbose = False

    opt.pretrained_model = \
        'results/' \
        'knowledgeaware_twc_evolve_world_glove_glove-1runs_' \
        '100episodes_3hsize_0.0eps_easy_direct_manual_0runId.pt'

    tk_extractor = extractor.get_extractor("max")

    graph = None

    print("Testing ...")
    tokenizer = Tokenizer(noun_only_tokens=False,
                          use_stopword=False,
                          ngram=3,
                          extractor=tk_extractor)
    rel_extractor = RelationExtractor(tokenizer,
                                      openie_url='http://localhost:9000/')
    agent = \
        TestKnowledgeAwareAgent(graph, opt, tokenizer, rel_extractor, device)
    agent.type = "knowledgeaware"

    print('Loading Pretrained Model ...', end='')
    agent.model.load_state_dict(
        torch.load(opt.pretrained_model, map_location=device))
    print('DONE')

    agent.test(opt.batch_size)
    opt.nepisodes = opt.no_eval_episodes  # for testing
    opt.max_step_per_episode = opt.eval_max_step_per_episode
    print("RUN")

    infos_to_request = agent.infos_to_request
    infos_to_request.max_score = True

    print("Loading Graph ... ", end='')
    manual_world_graphs = dict()
    goal_graphs = {}
    lower_level_str = {EASY_LEVEL: 'easy',
                       MEDIUM_LEVEL: 'medium', HARD_LEVEL: 'hard'}
    for level in LEVELS:
        game_path = 'static/games/twc/%s/test/' % lower_level_str[level]

        agent.kg_graph, _, _ = \
            construct_kg(game_path + '/conceptnet_subgraph.txt')
        kg_graphs[level] = agent.kg_graph

        manual_world_graph = \
            load_manual_graphs(game_path + '/manual_subgraph_brief')
        manual_world_graphs.update(manual_world_graph)

        game_path = game_path + '/*.ulx'

        env, game_file_names = \
            dataset.get_game_env(game_path, infos_to_request,
                                 opt.max_step_per_episode, opt.batch_size,
                                 mode='test', verbose=False)

        for game_file in env.gamefiles:
            goal_graph = get_goal_graph(game_file)
            if goal_graph:
                game_id = game_file.split('-')[-1].split('.')[0]
                goal_graphs[game_id] = goal_graph
    print(' DONE')

    return agent, goal_graphs, manual_world_graphs
