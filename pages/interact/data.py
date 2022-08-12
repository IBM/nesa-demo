import os
import sys

from .. import (DL_AGENT, EASY_LEVEL, HARD_LEVEL, LEVELS, LOA_AGENT,
                MEDIUM_LEVEL)
from .functions.data_processing import (create_loss_data, create_network,
                                        create_slider_dict, load_network,
                                        load_scalars)

if True:
    os.environ['DDLNN_HOME'] = 'third_party/loa/third_party/dd_lnn/'
    os.environ['TWC_HOME'] = 'static/games/twc/'

    sys_path_backup = sys.path
    sys.path.append('third_party/commonsense_rl/')
    from .twc_agent import get_twc_agent, kg_graphs
    sys.path = sys.path[:-1]

    sys.path.append('third_party/loa/')
    from third_party.loa.amr_parser import AMRSemParser
    from third_party.loa.loa_agent import LOAAgent, LogicalTWCQuantifier
    from third_party.loa.logical_twc import Action2Literal


network = \
    load_network(os.path.join('static', 'data', 'network1.json'))
scalars = \
    create_loss_data(load_scalars(os.path.join(
        'static', 'data', 'scalars_lnn_wts_N4_pos1_neg2.npz')))

roots_names, nodes, edges = create_network(network_dict=network)
slider_dict = create_slider_dict(network['epochs'])
options_loss_checklist = [{"label": x, "value": x}
                          for x in scalars['loss_type'].unique()]
value_loss_checklist = [x for x in scalars['loss_type'].unique()]


options_game_level = [{"label": x, "value": x} for x in LEVELS]
value_game_level = [EASY_LEVEL]
options_game = [{"label": x, "value": x}
                for x in ['One', 'Two', 'Three', 'Four', 'Five']]
value_game = ['One']

f = open(os.path.join('static', 'data', 'textworld_logo.txt'),
         'r', encoding='UTF-8')
textworld_logo = f.read()
f.close()

game_no = 0
easy_env = LogicalTWCQuantifier('easy',
                                split='test',
                                max_episode_steps=50,
                                batch_size=None,
                                game_number=game_no)

medium_env = LogicalTWCQuantifier('medium',
                                  split='test',
                                  max_episode_steps=50,
                                  batch_size=None,
                                  game_number=game_no)

hard_env = LogicalTWCQuantifier('hard',
                                split='test',
                                max_episode_steps=50,
                                batch_size=None,
                                game_number=game_no)

all_commonsense = dict()
for env in [easy_env, medium_env, hard_env]:
    _, facts = env.reset()
    for k, vs in env.commonsense_kb.items():
        k = k.replace('atlocation', 'at_location')
        lis = list()
        for v in vs:
            li = list()
            for e in v:
                found = False
                for entity in facts['entities']:
                    if (e + ' ') in (entity + ' '):
                        li.append(entity)
                        found = True
                if not found:
                    li.append(e)
            lis.append(li)
        if k in all_commonsense:
            all_commonsense[k].extend(lis)
        else:
            all_commonsense[k] = lis

env_dict = \
    {EASY_LEVEL: easy_env, MEDIUM_LEVEL: medium_env, HARD_LEVEL: hard_env}

difficulty_level = 'easy'
loa_pkl_filepath = 'results/loa-twc-dleasy-np2-nt15-ps1-ks6-spboth.pkl'
sem_parser_mode = 'both'
admissible_verbs = {'take': 1, 'put': 2, 'open': 1, 'insert': 2}

amr_server_ip = os.environ.get('AMR_SERVER_IP', 'localhost')
amr_server_port_str = os.environ.get('AMR_SERVER_PORT', '')
try:
    amr_server_port = int(amr_server_port_str)
except ValueError:
    amr_server_port = None

if LOA_AGENT:
    loa_agent = LOAAgent(difficulty_level=difficulty_level,
                         admissible_verbs=admissible_verbs,
                         amr_server_ip=amr_server_ip,
                         amr_server_port=amr_server_port,
                         sem_parser_mode=sem_parser_mode)

    loa_agent.load_pickel(loa_pkl_filepath)
    rest_amr = AMRSemParser(amr_server_ip=amr_server_ip,
                            amr_server_port=amr_server_port,
                            cache_folder='cache/')
    adm_verbs = loa_agent.admissible_verbs
    loa_agent.pi.eval()
    loa_rules = loa_agent.extract_rules()
else:
    loa_agent = None
    rest_amr = None
    loa_rules = None

if DL_AGENT:
    twc_agent, twc_agent_goal_graphs, \
        twc_agent_manual_world_graphs = get_twc_agent()
else:
    twc_agent = None
    twc_agent_goal_graphs = None
    twc_agent_manual_world_graphs = None

scored_action_history = [[] for _ in range(1)]

action2literal = Action2Literal()
color_default = 'black'
color1 = '#0f62fe'
color2 = 'green'
color_select = '#da1e28'
fired_color_name = 'color1'
text_margin_bottom = '.2rem'

default_network_name = 'lnn_twc_wo_empty'
ADD_NODE_FUNCTION = False

# default_network_name = 'lnn_twc_with_empty'
# ADD_NODE_FUNCTION = False

# default_network_name = 'lnn_twc_init'
# ADD_NODE_FUNCTION = True
