import dash_carbon_components as dca
import dash_html_components as html


def dialog_row(is_agent: bool, text: str):
    """

    :param is_agent: bool, is the agent otherwise the environment
    :param text: text to display
    """
    if is_agent:
        img = 'assets/robot-icon.jpeg'
        float_dir = 'right'
        margins = {'margin-left': 'calc(100% - 40px)'}
    else:
        img = 'assets/globe-icon.png'
        float_dir = 'left'
        margins = {}

    if isinstance(text, str):
        texts = [t for t in text.split('<br>')]
        text = list()
        for t in texts:
            text.append(t)
            text.append(html.Br())
        text = text[:-1]

    return dca.Row(children=[
        dca.Column(
            columnSizes=['sm-4'],
            children=[
                html.Div(
                    children=[
                        html.Img(src=img,
                                 style={'height': '50px',
                                        'width': '50px',
                                        'float': float_dir,
                                        'margin-right': '20px',
                                        'margin-left': '20px'}),
                        html.P(text,
                               style={
                                   'float': float_dir,
                                   'maxWidth': '70%'
                               }),
                    ],
                    style={'display': 'inline-block'}.update(margins))
            ],
        ),
    ])
