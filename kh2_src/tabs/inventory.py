from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh2_src.kh2_utils as utils


@callback(
    Output("InventoryDiv", "children"),
    Input("InventoryTabs", "value"),
)
def __create_inventory(tab):
    kh2 = utils.kh2
    inventory = html.Div([
        html.Div([
            html.Label(k + ": "),
            dcc.Input(
                id={"type": "Inventory", "index": kh2.inventory_dict[k]},
                type="number",
                value=kh2.inventory[kh2.inventory_dict[k]],
                min=0,
                max=99,
                step=1,
                style={"width": 50},
            ),
        ],
            style={"margin-top": 20, "gap": 10},
        ) for k in kh2.stock_dict[tab] if kh2.inventory_dict[k] < len(kh2.inventory)
    ])
    return inventory

def create_inventory():
    kh2 = utils.kh2
    itabs = dcc.Tabs(id="InventoryTabs", value="Consumables")
    itabs.children = [
        dcc.Tab(label=k, value=k) for k in kh2.stock_dict
    ]
    return html.Div([
        itabs,
        html.Div(id="InventoryDiv"),
    ])

@callback(
    Input({"type": "Inventory", "index": ALL}, "value"),
    State({"type": "Inventory", "index": ALL}, "id"),
)
def inventory_callback(values, ids):
    kh2 = utils.kh2
    try:
        i = 0
        for id in ids:
            idx = id["index"]
            kh2.inventory[idx] = values[i]
            i += 1
    except:
        pass
