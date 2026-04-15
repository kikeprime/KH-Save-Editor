from dash import Dash, html, dcc, callback, Input, Output, State, ALL, MATCH
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
        html.H3("Ship:"),
        gshtabs,
        html.Div(id="ShipDiv", style={"margin-bottom": 20}),
        viewerb,
        html.Div(id="ViewerDiv", style={"margin-bottom": 20}),
    ])

@callback(
    Output("ShipDiv", "children"),
    Input("ShipTabs", "value"),
    Input("Encoding", "value"),
)
def __create_ships(idx, encoding):
    kh1 = utils.kh1
    ship = kh1.gummiships[idx]
    blockcount = dcc.Input(
        id={"type": "Block Count", "index": idx},
        type="number",
        value=ship.blockcount.value,
        min=0,
        max=200,
        step=1,
        style={"width": 50},
    )
    area = html.Div([
        html.Label("X: "),
        dcc.Input(
            id={"type": "Assembly Area X", "index": idx},
            type="number",
            value=ship.x.value,
            min=0,
            max=10,
            step=1,
            style={"width": 50},
        ),
        html.Label(" Y: "),
        dcc.Input(
            id={"type": "Assembly Area Y", "index": idx},
            type="number",
            value=ship.y.value,
            min=0,
            max=10,
            step=1,
            style={"width": 50},
        ),
        html.Label(" Z: "),
        dcc.Input(
            id={"type": "Assembly Area Z", "index": idx},
            type="number",
            value=ship.z.value,
            min=0,
            max=10,
            step=1,
            style={"width": 50},
        ),
    ])
    codec = "kh1us" if encoding == "International" else "kh1jp"
    transformpair = dcc.Dropdown(
        options=[
            {"label": "No Pair", "value": 0}
        ] + [
            {"label": kh1.gummiships[i].name.decode(codec), "value": i+1} for i in range(len(kh1.gummiships))
        ],
        value=ship.transformpair.value,
        id={"type": "Transform Pair", "index": idx},
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    name = html.Div([
        dcc.Input(
            id={"type": "Ship Name", "index": idx},
            type="text",
            value=ship.name.decode(codec),
            style={"width": 120},
        ),
        html.Button(
            "Validate", id={"type": "Ship Name Validate", "index": idx}, n_clicks=0, style={"width": 80, "margin-left": 10},
        ),
    ])
    blocktabs = dcc.Dropdown(
        options=[{"label": f"Block {i+1}", "value": i} for i in range(len(ship.blocks))],
        value=0,
        id="BlockTabs",
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    return html.Div([
        dcc.Markdown("Block Count:"),
        blockcount,
        dcc.Markdown("Assembly Area:"),
        area,
        dcc.Markdown("Transform Pair:"),
        transformpair,
        dcc.Markdown("Name:"),
        name,
        html.H3("Blocks:"),
        blocktabs,
        html.Div(id="BlockDiv"),
    ])

@callback(
    Output("BlockDiv", "children"),
    Input("BlockTabs", "value"),
    State("ShipTabs", "value"),
)
def __create_gummi_ship_blocks(idx, ship_idx):
    kh1 = utils.kh1
    ship = kh1.gummiships[ship_idx]
    block_type = dcc.Dropdown(
        options=[{"label": k, "value": v} for v, k in kh1.gummi_block_dict.items()],
        value=ship.blocks[idx].id.value,
        id={"type": "Gummi Block Type", "ship": ship_idx, "index": idx},
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    coordinates = html.Div([
        html.Label("X: "),
        dcc.Input(
            id={"type": "Gummi Block X", "ship": ship_idx, "index": idx},
            type="number",
            value=ship.blocks[idx].x.value,
            min=0,
            max=9,
            step=1,
            style={"width": 50},
        ),
        html.Label(" Y: "),
        dcc.Input(
            id={"type": "Gummi Block Y", "ship": ship_idx, "index": idx},
            type="number",
            value=ship.blocks[idx].y.value,
            min=0,
            max=255,
            step=1,
            style={"width": 50},
        ),
        html.Label(" Z: "),
        dcc.Input(
            id={"type": "Gummi Block Z", "ship": ship_idx, "index": idx},
            type="number",
            value=ship.blocks[idx].z.value,
            min=0,
            max=9,
            step=1,
            style={"width": 50},
        ),
    ])
    rotation_options = [
        {"label": "Normal", "value": 0x0420},
        {"label": "Left", "value": 0x0124},
        {"label": "Right", "value": 0x0025},
        {"label": "Back", "value": 0x0521},
        {"label": "Up", "value": 0x0250},
        {"label": "Down", "value": 0x0340},
        {"label": "Up Up or Down Down", "value": 0x0530},
        {"label": "Tilt Left", "value": 0x0412},
        {"label": "Tilt Right", "value": 0x0403},
        {"label": "Upside Down", "value": 0x0431},
        {"label": "Left then Up", "value": 0x0204},
        {"label": "Left then Down", "value": 0x0314},
        {"label": "Left then Up Up", "value": 0x0034},
        {"label": "Left then Tilt Left", "value": 0x0252},
        {"label": "Left then Tilt Right", "value": 0x0143},
        {"label": "Right then Up", "value": 0x0215},
        {"label": "Right then Down", "value": 0x0305},
        {"label": "Right then Up Up", "value": 0x0135},
        {"label": "Right then Tilt Left", "value": 0x0042},
        {"label": "Right then Tilt Right", "value": 0x0053},
        {"label": "Back then Up", "value": 0x0241},
        {"label": "Back then Down", "value": 0x0351},
        {"label": "Back then Tilt Left", "value": 0x0502},
        {"label": "Back then Tilt Right", "value": 0x0513},
        {"label": "None-G", "value": 0x0000},
    ]
    rotation = dcc.Dropdown(
        options=rotation_options,
        value=ship.blocks[idx].r.value & ~0x1000,
        id={"type": "Gummi Block Rotation", "ship": ship_idx, "index": idx},
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    color = dcc.Input(
        id={"type": "Gummi Block Color", "ship": ship_idx, "index": idx},
        type="number",
        value=ship.blocks[idx].color.value,
        min=0,
        max=63,
        step=1,
        style={"width": 50},
    )
    return html.Div([
        dcc.Markdown("Block Type:"),
        block_type,
        dcc.Markdown("Block Coordinates:"),
        coordinates,
        dcc.Markdown("Orientation:"),
        rotation,
        dcc.Markdown("Color:"),
        color,
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

def __create_gummi_config():
    kh1 = utils.kh1
    config_options = [
        {"label": "Circle", "value": 0x20},
        {"label": "Triangle", "value": 0x10},
        {"label": "Square", "value": 0x80},
        {"label": "Cross", "value": 0x40},
        {"label": "L1", "value": 4},
        {"label": "L2", "value": 1},
        {"label": "R1", "value": 8},
        {"label": "R2", "value": 2},
    ]
    decelerate = dcc.Dropdown(
        options=config_options,
        value=kh1.gummi_decelerate.value,
        id="Ship Decelerate",
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    accelerate = dcc.Dropdown(
        options=config_options,
        value=kh1.gummi_accelerate.value,
        id="Ship Accelerate",
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    transform = dcc.Dropdown(
        options=config_options,
        value=kh1.gummi_transform.value,
        id="Ship Transform",
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    scannon = dcc.Dropdown(
        options=config_options,
        value=kh1.gummi_scannon.value,
        id="Ship Small Cannon",
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    mcannon = dcc.Dropdown(
        options=config_options,
        value=kh1.gummi_mcannon.value,
        id="Ship Mid Cannon",
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    lcannon = dcc.Dropdown(
        options=config_options,
        value=kh1.gummi_lcannon.value,
        id="Ship Large Cannon",
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    slaser = dcc.Dropdown(
        options=config_options,
        value=kh1.gummi_slaser.value,
        id="Ship Small Laser",
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    mlaser = dcc.Dropdown(
        options=config_options,
        value=kh1.gummi_mlaser.value,
        id="Ship Mid Laser",
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    llaser = dcc.Dropdown(
        options=config_options,
        value=kh1.gummi_llaser.value,
        id="Ship Large Laser",
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    return html.Div([
        dcc.Markdown("Decelerate:"),
        decelerate,
        dcc.Markdown("Accelerate:"),
        accelerate,
        dcc.Markdown("Transform:"),
        transform,
        dcc.Markdown("Small Cannon:"),
        scannon,
        dcc.Markdown("Mid Cannon:"),
        mcannon,
        dcc.Markdown("Large Cannon:"),
        lcannon,
        dcc.Markdown("Small Laser:"),
        slaser,
        dcc.Markdown("Mid Laser:"),
        mlaser,
        dcc.Markdown("Large Laser:"),
        llaser,
    ])

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
    if tab == "Control Config":
        return __create_gummi_config()

def create_gummi():
    gtabs = dcc.Tabs(id="GummiTabs", value="Ships")
    gtabs.children = [
        dcc.Tab(label="Ships", value="Ships"),
        dcc.Tab(label="Gummi Inventory", value="Gummi Inventory"),
        dcc.Tab(label="Control Config", value="Control Config"),
    ]
    return html.Div([
        gtabs,
        html.Div(id="GummiDiv"),
    ])

@callback(
    Input({"type": "Block Count", "index": ALL}, "value"),
    Input({"type": "Assembly Area X", "index": ALL}, "value"),
    Input({"type": "Assembly Area Y", "index": ALL}, "value"),
    Input({"type": "Assembly Area Z", "index": ALL}, "value"),
    Input({"type": "Transform Pair", "index": ALL}, "value"),
    State({"type": "Block Count", "index": ALL}, "id"),
)
def ship_callback(blockcount, x, y, z, transformpair, id):
    kh1 = utils.kh1
    idx = id[0]["index"]
    ship = kh1.gummiships[idx]
    try:
        ship.blockcount.value = blockcount[0]
        ship.x.value = x[0]
        ship.y.value = y[0]
        ship.z.value = z[0]
        ship.transformpair.value = transformpair[0]
    except:
        pass

@callback(
    Output({"type": "Ship Name", "index": MATCH}, "value"),
    Input({"type": "Ship Name Validate", "index": MATCH}, "n_clicks"),
    State({"type": "Ship Name", "index": MATCH}, "value"),
    State({"type": "Ship Name", "index": MATCH}, "id"),
    State("Encoding", "value"),
)
def ship_name_callback(n_clicks, name, id, encoding):
    kh1 = utils.kh1
    codec = "kh1us" if encoding == "International" else "kh1jp"
    idx = id["index"]
    if n_clicks > 0:
        new_name = bytearray(name, codec)
        l = len(new_name)
        kh1.gummiships[idx].name[:min(l, 10)] = new_name[:min(l, 10)]
        return kh1.gummiships[idx].name.decode(codec)
    return name

@callback(
    Input({"type": "Gummi Block Type", "ship": ALL, "index": ALL}, "value"),
    Input({"type": "Gummi Block X", "ship": ALL, "index": ALL}, "value"),
    Input({"type": "Gummi Block Y", "ship": ALL, "index": ALL}, "value"),
    Input({"type": "Gummi Block Z", "ship": ALL, "index": ALL}, "value"),
    Input({"type": "Gummi Block Rotation", "ship": ALL, "index": ALL}, "value"),
    Input({"type": "Gummi Block Color", "ship": ALL, "index": ALL}, "value"),
    State({"type": "Gummi Block Type", "ship": ALL, "index": ALL}, "id"),
)
def gummi_block_callback(t, x, y, z, r, c, id):
    kh1 = utils.kh1
    ship = id[0]["ship"]
    idx = id[0]["index"]
    block = kh1.gummiships[ship].blocks[idx]
    try:
        block.id.value = t[0]
        block.x.value = x[0]
        block.y.value = y[0]
        block.z.value = z[0]
        block.r.value = r[0]
        block.color.value = c[0]
    except:
        pass

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

@callback(
    Input("Ship Decelerate", "value"),
    Input("Ship Accelerate", "value"),
    Input("Ship Transform", "value"),
    Input("Ship Small Cannon", "value"),
    Input("Ship Mid Cannon", "value"),
    Input("Ship Large Cannon", "value"),
    Input("Ship Small Laser", "value"),
    Input("Ship Mid Laser", "value"),
    Input("Ship Large Laser", "value"),
)
def gummi_control_config_callback(
    decelerate,
    accelerate,
    transform,
    scannon,
    mcannon,
    lcannon,
    slaser,
    mlaser,
    llaser
):
    kh1 = utils.kh1
    kh1.gummi_decelerate.value = decelerate
    kh1.gummi_accelerate.value = accelerate
    kh1.gummi_transform.value = transform
    kh1.gummi_scannon.value = scannon
    kh1.gummi_mcannon.value = mcannon
    kh1.gummi_lcannon.value = lcannon
    kh1.gummi_slaser.value = slaser
    kh1.gummi_mlaser.value = mlaser
    kh1.gummi_llaser.value = llaser
