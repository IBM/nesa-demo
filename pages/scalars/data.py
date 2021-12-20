import os
from .functions.data_processing import *

home_dir = './'

network = load_network(os.path.join(home_dir, 'static', 'data', 'network1.json'))
scalars = create_loss_data(load_scalars(os.path.join(home_dir, 'static', 'data', 'scalars_example.json')))
roots_names, nodes, edges = create_network(network_dict=network)
slider_dict = create_slider_dict(network['epochs'])
options_loss_checklist = np.concatenate([[{"label": group + ": " + x, "value": group + ": " + x}
                                          for x in scalars[scalars['group'] == group]['loss_type'].unique()]
                                         for group in scalars['group'].unique()])
value_loss_checklist = np.concatenate([[group + ": " + x
                                        for x in scalars[scalars['group'] == group]['loss_type'].unique()]
                                       for group in scalars['group'].unique()])
