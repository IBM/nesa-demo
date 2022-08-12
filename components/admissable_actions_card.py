import dash_carbon_components as dca
import dash_html_components as html


def admissible_actions_card(actions=None, height: int = 250):

    action_ul = html.Ul(
        children=None,
        id='admissible_actions',
        style={'height': f'{height}px',
               'width': '100%'},
    )

    inspect_action_dropdown = html.Div(
        id='dropdown_wrapper',
        children=[dca.Dropdown(
            id='inspect_action_dropdown',
            label=None,
            options=None,
            value=None,
            style={
                'height': '40px',
                'padding-right': '0px'
            }
        )]
    )

    inspect_action_submit = dca.Button(
        'Select',
        id='submit_inspect_action',
        kind='primary',
        style={
            'height': '40px',
            'width': '50px'
        },
        size='small'
    )

    loa_action_submit = dca.Button(
        'Select NeSA recommendation',
        id='select_recommendation_action',
        kind='primary',
        style={
            'height': '40px',
            'width': '100%',
            'padding-right': '0px'
        },
        size='small'
    )

    row = dca.Row(
        children=[
            dca.Column(loa_action_submit, columnSizes=['md-3'],
                       style={'margin-right': '22px',
                              'padding-right': '0px'}),
            html.Div('or',
                     style={'padding-right': '22px',
                            'height': '40px',
                            'padding-top': '12px'}),
            dca.Column(inspect_action_dropdown, columnSizes=['md-4'],
                       style={'height': '1.5em',
                              'max-width': '300px',
                              'padding-right': '0px'}),
            dca.Column(inspect_action_submit, columnSizes=['md-2'],
                       style={'max-width': '30px',
                              'padding-right': '0px',
                              'margin-right': '0px',
                              'padding-left': '0px'})
        ],
        style={
            'width': '100%',
            'margin-bottom': '10pt',
            'padding-left': '15px'
        }
    )

    return dca.Card(
        id='admissible_actions_card',
        title='Action selector for checking inside of the model',
        children=[
            row,
            action_ul
        ])
