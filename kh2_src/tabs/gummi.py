from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh2_src.kh2_utils as utils


def __create_gummi_inventory():
    kh2 = utils.kh2
    inventory = html.Div([])
    return inventory

@callback(
    Output("GummiInventoryDiv", "children"),
    Input("GummiInventoryTabs", "value"),
)
def __create_gummi(tab):
    if tab == "Gummi Inventory":
        return __create_gummi_inventory()

def create_gummi():
    gtabs = dcc.Tabs(id="GummiInventoryTabs", value="Gummi Inventory")
    gtabs.children = [
        dcc.Tab(label="Gummi Inventory", value="Gummi Inventory"),
    ]
    return html.Div([
        gtabs,
        html.Div(id="GummiInventoryDiv"),
    ])
