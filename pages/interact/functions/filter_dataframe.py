from pandas import DataFrame
from typing import List


def filter_dataframe(data: DataFrame, years: List[str], countries: List[str]):
    criteria = (data['year'].isin(years)) & \
               (data['country'].isin(countries))
    return data[criteria]
