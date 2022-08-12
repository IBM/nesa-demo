import dash_carbon_components as dca
import dash_html_components as html


def commonsense_card(commonsense=None, height: int = 250):
    children = [
        html.P('Commonsense knowledge from ConceptNet',
               style={'text-align': 'left',
                      'font-weight': 'bold',
                      'padding-top': '.5rem'}),
        html.Ul(children=None,
                id='commonsense',
                style={'padding-left': '2rem',
                       'padding-top': '.75rem',
                       'font-size': 'large'})
    ]

    return dca.Card(
        id='commonsense_card',
        title='Contrastive external knowledge visualizer',
        children=children)
