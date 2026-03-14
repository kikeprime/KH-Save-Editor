from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils
from kh1_src.kh1_gummi_viewer import *


def __create_gummi_ships(encoding):
    kh1 = utils.kh1
    codec = "kh1us" if encoding == "International" else "kh1jp"
    selected = dcc.Dropdown(
        options=[{"label": f"Gummi Ship {i+1}", "value": i} for i in range(len(kh1.gummiships))],
        value=kh1.selectedship.value,
        id="SelectedShip",
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    gshtabs = dcc.Dropdown(
        options=[{"label": kh1.gummiships[i].name.decode(codec), "value": i} for i in range(len(kh1.gummiships))],
        value=0,
        id="ShipTabs",
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    viewerb = html.Button(
        "Gummi Ship Viewer",
        id="ViewerButton",
        n_clicks=0,
        style={"margin": 20, "width": 200},
    )
    return html.Div([
        dcc.Markdown("Selected Gummi Ship:"),
        selected,
        dcc.Markdown("Ship:"),
        gshtabs,
        html.Div(id="ShipDiv", style={"margin-bottom": 20}),
        viewerb,
        html.Div(id="ViewerDiv", style={"margin-bottom": 20}),
    ])

@callback(
    Output("ViewerDiv", "children"),
    Input("ViewerButton", "n_clicks"),
    Input("ShipTabs", "value")
)
def viewerb_callback(n_clicks, idx):
    if n_clicks % 2 == 1:
        return create_gummi_ship_viewer(idx)

def __create_gummi_inventory():
    kh1 = utils.kh1
    cockpits = html.Div([
        html.Div([
            html.Label(k + ": "),
            dcc.Input(
                id={"type": "Gummi Block", "index": v},
                type="number",
                value=kh1.gummiblocks[v],
                min=0,
                max=kh1.gummi_max_list[v],
                step=1,
                style={"width": 50},
            ),
        ],
            style={"margin-top": 20, "gap": 10},
        ) for k, v in kh1.gummi_block_cockpit_dict.items()
    ])
    engines = html.Div([
        html.Div([
            html.Label(k + ": "),
            dcc.Input(
                id={"type": "Gummi Block", "index": v},
                type="number",
                value=kh1.gummiblocks[v],
                min=0,
                max=kh1.gummi_max_list[v],
                step=1,
                style={"width": 50},
            ),
        ],
            style={"margin-top": 20, "gap": 10},
        ) for k, v in kh1.gummi_block_engine_dict.items()
    ])
    armors = html.Div([
        html.Div([
            html.Label(k + ": "),
            dcc.Input(
                id={"type": "Gummi Block", "index": v},
                type="number",
                value=kh1.gummiblocks[v],
                min=0,
                max=kh1.gummi_max_list[v],
                step=1,
                style={"width": 50},
            ),
        ],
            style={"margin-top": 20, "gap": 10},
        ) for k, v in kh1.gummi_block_armor_dict.items()
    ])
    wings = html.Div([
        html.Div([
            html.Label(k + ": "),
            dcc.Input(
                id={"type": "Gummi Block", "index": v},
                type="number",
                value=kh1.gummiblocks[v],
                min=0,
                max=kh1.gummi_max_list[v],
                step=1,
                style={"width": 50},
            ),
        ],
            style={"margin-top": 20, "gap": 10},
        ) for k, v in kh1.gummi_block_wing_dict.items()
    ])
    specials = html.Div([
        html.Div([
            html.Label(k + ": "),
            dcc.Input(
                id={"type": "Gummi Block", "index": v},
                type="number",
                value=kh1.gummiblocks[v],
                min=0,
                max=kh1.gummi_max_list[v],
                step=1,
                style={"width": 50},
            ),
        ],
            style={"margin-top": 20, "gap": 10},
        ) for k, v in kh1.gummi_block_special_dict.items()
    ])
    weapons = html.Div([
        html.Div([
            html.Label(k + ": "),
            dcc.Input(
                id={"type": "Gummi Block", "index": v},
                type="number",
                value=kh1.gummiblocks[v],
                min=0,
                max=kh1.gummi_max_list[v],
                step=1,
                style={"width": 50},
            ),
        ],
            style={"margin-top": 20, "gap": 10},
        ) for k, v in kh1.gummi_block_weapon_dict.items()
    ])
    upgrades = html.Div([
        html.Div([
            html.Label(k + ": "),
            dcc.Input(
                id={"type": "Gummi Block", "index": v},
                type="number",
                value=kh1.gummiblocks[v],
                min=0,
                max=kh1.gummi_max_list[v],
                step=1,
                style={"width": 50},
            ),
        ],
            style={"margin-top": 20, "gap": 10},
        ) for k, v in kh1.gummi_block_upgrade_dict.items()
    ])
    blueprints = html.Div([
        html.Div([
            html.Label(k + ": "),
            dcc.Input(
                id={"type": "Gummi Block", "index": v},
                type="number",
                value=kh1.gummiblocks[v],
                min=0,
                max=1,
                step=1,
                style={"width": 50},
            ),
        ],
            style={"margin-top": 20, "gap": 10},
        ) for k, v in kh1.gummi_blueprint_dict.items()
    ])
    if kh1.fm:
        blueprints_fm = html.Div([
            html.Div([
                html.Label(k + ": "),
                dcc.Input(
                    id={"type": "Gummi Block", "index": v},
                    type="number",
                    value=kh1.gummiblocks[v],
                    min=0,
                    max=1,
                    step=1,
                    style={"width": 50},
                ),
            ],
                style={"margin-top": 20, "gap": 10},
            ) for k, v in kh1.gummi_blueprint_fm_dict.items()
        ])
        designs = html.Div([
            html.Div([
                html.Label(k + ": "),
                dcc.Input(
                    id={"type": "Gummi Block", "index": v},
                    type="number",
                    value=kh1.gummiblocks[v],
                    min=0,
                    max=99, # needs research
                    step=1,
                    style={"width": 50},
                ),
            ],
                style={"margin-top": 20, "gap": 10},
            ) for k, v in kh1.gummi_block_design_dict.items()
        ])
    inventory = html.Div([
        html.H3("Cockpits:"),
        cockpits,
        html.H3("Engines:"),
        engines,
        html.H3("Armors:"),
        armors,
        html.H3("Wings:"),
        wings,
        html.H3("Specials:"),
        specials,
        html.H3("Weapons:"),
        weapons,
        html.H3("Upgrades:"),
        upgrades,
        html.H3("Blueprints:"),
        blueprints,
    ])
    if kh1.fm:
        inventory.children += [
            html.H3("Final Mix Blueprints:"),
            blueprints_fm,
            html.H3("Design Gummies:"),
            designs,
        ]
    return inventory

@callback(
    Output("GummiDiv", "children"),
    Input("GummiTabs", "value"),
    Input("Encoding", "value"),
)
def __create_gummi(tab, encoding):
    if tab == "Ships":
        return __create_gummi_ships(encoding)
    if tab == "Gummi Inventory":
        return __create_gummi_inventory()

def create_gummi():
    gtabs = dcc.Tabs(id="GummiTabs", value="Ships")
    gtabs.children = [
        dcc.Tab(label="Ships", value="Ships"),
        dcc.Tab(label="Gummi Inventory", value="Gummi Inventory"),
    ]
    return html.Div([
        gtabs,
        html.Div(id="GummiDiv"),
    ])

@callback(
    Input({"type": "Gummi Block", "index": ALL}, "value"),
    State({"type": "Gummi Block", "index": ALL}, "id"),
)
def inventory_gummi_callback(values, ids):
    kh1 = utils.kh1
    try:
        i = 0
        for id in ids:
            idx = id["index"]
            kh1.gummiblocks[idx] = values[i]
            i += 1
    except:
        pass
