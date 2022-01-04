import dash_carbon_components as dca
import dash_html_components as html
from pages.interact import data

filters_layout = [
    html.Div(children=[
        dca.Dropdown(
            id='game_level_selection',
            options=data.options_game_level,
            value='Easy',
            label='Select Game Level'
        ),
    ]),
]
