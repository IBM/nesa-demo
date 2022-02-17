import os
from .functions.data_processing import *

home_dir = './'

network = load_network(os.path.join(home_dir, 'static', 'data', 'network1.json'))
scalars = create_loss_data(load_scalars(os.path.join(home_dir, 'static', 'data', 'scalars_lnn_wts_N4_pos1_neg2.npz')))
roots_names, nodes, edges = create_network(network_dict=network)
slider_dict = create_slider_dict(network['epochs'])
options_loss_checklist = [{"label": x, "value": x} for x in scalars['loss_type'].unique()]
value_loss_checklist = [x for x in scalars['loss_type'].unique()]