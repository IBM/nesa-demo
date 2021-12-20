import dash_carbon_components as dca
import dash_html_components as html
from pages.scalars import data

filters_layout = [
    html.Div(children=[
        dca.MultiSelect(
            id="loss_type_selection",
            options=data.options_loss_checklist,
            value=data.value_loss_checklist,
            label="Select Metrics"
        )
    ]),
]
