from dash import Dash
from dash.dependencies import Output, Input

from pages.home.layout import layout as home_layout
from pages.scalars.layout import layout as scalars_layout
from pages.graphs.layout import layout as graphs_layout
from pages.interact.layout import layout as interact_layout

pages = {
    '/': home_layout,
    '/scalars': scalars_layout,
    '/graphs': graphs_layout,
    '/interact': interact_layout,
}


def register_router(app: Dash):
    # Router callback
    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname'),
    )
    def display_page(pathname):
        return pages[pathname]
