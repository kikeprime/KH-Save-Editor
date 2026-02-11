from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


@callback(
    Output("InventoryDiv", "children"),
    Input("InventoryTabs", "value"),
)
def __create_inventory(tab):
    kh1 = utils.kh1
    inventory = None
    if tab == "Consumables":
        interval = lambda x: x in range(0x01, 0x09) or x in range(0x8E, 0x91) or x in range(0x98, 0x9B)
    if tab == "Synthesis Materials":
        interval = lambda x: x in range(0x09, 0x11) or x in range(0x9B, 0x9E) or x > 0xE8
    if tab == "Accessories":
        interval = lambda x: x in kh1.accessory_dict.values() and x > 0
    if tab == "Weapons":
        interval = lambda x: x in kh1.weapon_dict.values() and x > 0
    if tab == "Key Items":
        interval = lambda x: x in range(0x95, 0x98) or x in range(0x9E, 0xE8)
    inventory = html.Div([
        html.Div([
            html.Label(k + ": "),
            dcc.Input(
                id={"type": "Inventory", "index": v},
                type="number",
                value=kh1.inventory[v],
                min=0,
                max=99,
                step=1,
                style={"width": 50},
            ),
        ],
            style={"margin-top": 20, "gap": 10},
        ) for k, v in kh1.item_dict.items()\
        if ("Unused" not in k and interval(v)\
        if tab != "Unused" else "Unused" in k)
    ])
    return inventory

def create_inventory():
    kh1 = utils.kh1
    itabs = dcc.Tabs(id="InventoryTabs", value="Consumables")
    itabs.children = [
        dcc.Tab(label="Consumables", value="Consumables"),
        dcc.Tab(label="Synthesis Materials", value="Synthesis Materials"),
        dcc.Tab(label="Accessories", value="Accessories"),
        dcc.Tab(label="Weapons", value="Weapons"),
        dcc.Tab(label="Key Items", value="Key Items"),
        dcc.Tab(label="Unused", value="Unused"),
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
    kh1 = utils.kh1
    try:
        i = 0
        for id in ids:
            idx = id["index"]
            kh1.inventory[idx] = values[i]
            i += 1
    except:
        pass
