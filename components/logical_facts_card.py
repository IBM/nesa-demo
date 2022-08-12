import dash_carbon_components as dca
import dash_html_components as html


def logical_facts_card(facts=None, height: int = 250):
    children = [
        html.Ul(
            children=None,
            id='logical_facts',
            style={'padding-top': '.5rem',
                   'font-size': 'large'}
        ),
    ]

    return dca.Card(
        id='logical_facts_card',
        title='Current state fact visualizer',
        children=children)
