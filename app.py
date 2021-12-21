import os
import argparse

import dash
import dash_html_components as html

from components import ui_shell
from decorators.graph_output import function_map
from router import register_router
from utils_demo.callbacks import reset_page_callback, download_callback

from pages.home.layout import layout as home_layout
from pages.home.callbacks import register as register_home

from pages.scalars.layout import layout as scalars_layout
from pages.scalars.callbacks import register as register_scalars

from pages.graphs.layout import layout as graphs_layout
from pages.graphs.callbacks import register as register_graphs

from pages.interact.layout import layout as interact_layout
from pages.interact.callbacks import register as register_interact

# Dash App instantiation
app = dash.Dash(__name__)
server = app.server
app.title = 'NeSA Demo'

app.layout = ui_shell(
    app.title,
    header=[
        {'name': 'Home', 'url': '/'},
        {'name': 'Interact', 'url': '/interact'},
        # {'name': 'Scalars', 'url': '/scalars'},
        # {'name': 'Graphs', 'url': '/graphs'},
    ],
    sidebar=[]
)
app.validation_layout = html.Div([
    app.layout,
    home_layout,
    scalars_layout,
    graphs_layout,
    interact_layout,
])


register_router(app)

# OPENID CONNECT SSO
enable_sso = os.getenv('DASH_ENABLE_OIDC', 'false')
if enable_sso.lower() == 'true':
    raise NotImplemented

# Callback to reset the page when the user press the reset button
reset_page_callback(app)

# Automatically register the download callbacks of all graphs
# in the application that using the graph_output decorator
for graph_id in function_map.keys():
    download_callback(app, graph_id + '_card', graph_id,
                      graph_id + '_download')

# Pages callbacks
register_home(app)
register_scalars(app)
register_graphs(app)
# register_comparison(app)
register_interact(app)

# Load static files
html.Img(src=app.get_asset_url('globe-icon.png'))
html.Img(src=app.get_asset_url('robot-icon.png'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8050)
    parser.add_argument('--release', action='store_true')
    args = parser.parse_args()

    app.run_server(debug=not args.release, host='0.0.0.0', port=args.port)
