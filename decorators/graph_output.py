import plotly.graph_objs as go

function_map = {}


# Decorator to handle empty filtered_df and apply the graph application layout
def graph_output(graph_id: str):
    def decorator(func):
        def wrapper(*args, **kw):
            filtered_df = args[0]
            if filtered_df is None:
                filtered_df = kw['filtered_df']
            if filtered_df.empty:
                return go.Figure(layout=go.Layout(
                    xaxis={"visible": False},
                    yaxis={"visible": False},
                    paper_bgcolor='#fff',
                    plot_bgcolor='#fff',
                    annotations=[
                        {
                            "text": "No matching data found. Please change the filters.",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {
                                "size": 16
                            }
                        }
                    ]
                ))
            fig = func(*args, **kw)
            fig.update_xaxes(showgrid=False, showticklabels=True, zeroline=True, color='#B2B2B2',
                             tickcolor='#B2B2B2')
            fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
            fig.layout.update(
                paper_bgcolor='#fff',
                plot_bgcolor='#fff',
                legend=go.layout.Legend(
                    x=.175,
                    y=2.00,
                    traceorder="normal",
                    orientation='h',
                    font=dict(
                        family="sans-serif",
                        size=14,
                        color="#B2B2B2"
                    )
                ),
                margin=dict(t=20, b=75),
            )
            return fig

        function_map[graph_id] = wrapper
        return wrapper

    return decorator
