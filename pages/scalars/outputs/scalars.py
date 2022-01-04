import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from decorators.graph_output import graph_output


@graph_output('scalars')
def scalars(data: pd.DataFrame) -> go.Figure:
    return px.line(data, x="epoch", y="loss", color='loss_type')
