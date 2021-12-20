from pandas import DataFrame
from typing import List
import pandas as pd


def filter_dataframe(data: DataFrame, loss_type: List[str]):
    dfs = []
    for l in loss_type:
        group, metric = l.split(": ")
        dfs += [data[(data['group'] == group) & (data['loss_type'] == metric)]]

    return pd.concat(dfs)
