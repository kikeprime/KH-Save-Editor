from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


@callback(
    Output("MiscDiv", "children"),
    Input("MiscTabs", "value"),
    Input("Encoding", "value"),
)
def __create_misc(tab, encoding):
    kh1 = utils.kh1

def create_misc():
    kh1 = utils.kh1
    mtabs = dcc.Tabs(id="MiscTabs", value="Misc")
    mtabs.children = [
        dcc.Tab(label="Misc", value="Misc"),
    ]
    return html.Div([
        mtabs,
        html.Div(id="MiscDiv"),
    ])
