from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


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
