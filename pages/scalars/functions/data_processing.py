import json
import numpy as np
import pandas as pd


def load_network(network_json_path):
    with open(network_json_path, 'r') as f:
        return json.load(f)


def load_scalars(scalars_npz_path):
    with open(scalars_npz_path, 'r') as f:
        obj = json.load(f)
    return obj


def create_network(network_dict):
    # generate roots string
    roots = network_dict['input']
    roots_names = ', '.join(['[id = "{}"]'.format(x) for x in roots])

    # generate nodes list
    node_ids = network_dict['input'] + list(network_dict['network'].keys())  # + ['output']
    node_labels = network_dict['input'] + [x['gate_type'] for _, x in network_dict['network'].items()]  # + ['y']
    nodes = [{'data': {'id': x, 'label': y}} for x, y in zip(node_ids, node_labels)]

    # generate edges by epoch lists
    edges = []
    for epoch in range(network_dict['epochs']):
        epoch_edges = []
        for k, v in network_dict['network'].items():
            for parent, weight in zip(v['parents'], v['weights'][epoch]):
                epoch_edges += [{'data': {'source': parent, 'target': k, 'weight': weight}}]
        edges += [epoch_edges]

    return roots_names, nodes, edges


def create_slider_dict(num_epochs):
    if num_epochs <= 10:
        return {i: str(i) for i in range(num_epochs)}
    elif num_epochs <= 50:
        return {i * 5: str(i * 5) for i in range(num_epochs // 5)}
    elif num_epochs <= 100:
        return {i * 10: str(2 ** i) for i in range(num_epochs // 10)}
    else:
        return {i * 50: str(2 ** i) for i in range(num_epochs)}


def create_loss_data(scalars_dict):
    group_col = []
    epoch_col = []
    loss_col = []
    loss_type_col = []

    for group, group_dict in scalars_dict.items():

        for i in range(len(group_dict['values'])):
            epoch_col += group_dict['epoch']

        for k, v in group_dict['values'].items():
            loss_col += v
            loss_type_col += [k] * len(v)
            group_col += [group] * len(v)

    return pd.DataFrame({'group': group_col, 'epoch': epoch_col, 'loss': loss_col, 'loss_type': loss_type_col})

