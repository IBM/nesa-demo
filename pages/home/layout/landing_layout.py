import dash_carbon_components as dca
import dash_html_components as html

from ... import LOA_REPO_URL, REPO_URL

landing_layout = dca.Grid(
    style={
        'padding': '16px',
        'height': 'calc(100% - 75px)',
        'overflow': 'auto',
        'width': '75%'
    },
    className='bx--grid--narrow bx--grid--full-width',
    children=[
        dca.Row(children=[
            dca.Column(columnSizes=['sm-4'], children=[
                dca.Card(
                    id='landing_card',
                    children=[
                        html.H1("NeSA Demo",
                                style={
                                    'padding-top': '10px',
                                    'padding-bottom': '10px',
                                }),
                        html.P(
                            "Welcome to Neuro-Sybmolic Agent (NeSA) Demo, "
                            "where you can explore, understand and interact "
                            "with NeSA which is Logical Optimal Action (LOA).",
                            className="lead",
                            style={
                                'padding-top': '10px',
                                'padding-bottom': '10px',
                            }
                        ),
                        html.Hr(className="my-2"),
                        html.P(
                            "Click the buttons below to find for each code "
                            "of NeSA Demo and LOA.",
                            style={
                                'padding-top': '10px',
                                'padding-bottom': '10px',
                            }
                        ),
                        dca.Button(
                            id='learn_more_button',
                            size='sm',
                            children='NeSA Demo Repo',
                            kind='primary',
                            href=REPO_URL,
                            style={
                                'padding': '10px',
                                'right': '10px',
                                'left': '0px',
                            }
                        ),
                        dca.Button(
                            id='learn_more_button',
                            size='sm',
                            children='LOA Repo',
                            kind='primary',
                            href=LOA_REPO_URL,
                            style={
                                'padding': '10px',
                                'right': '0px',
                                'left': '10px',
                            }
                        ),
                    ]
                ),
            ]),
        ]),
    ])
