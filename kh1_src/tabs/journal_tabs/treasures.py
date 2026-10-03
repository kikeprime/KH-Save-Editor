from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


@callback(
    Output("TreasuresDiv", "children"),
    Input("TreasuresTabs", "value"),
)
def __create_treasures(tab):
    kh1 = utils.kh1
    treasures = html.Div([
        html.H3("Treasure Chests:"),
        html.Div([
            html.Div([
                dcc.Checklist(
                    options=[{"label": k, "value": (1 << v % 16)}],
                    value=[kh1.treasures[v//16] & (1 << v % 16)],
                    id={"type": "Treasure", "index": v},
                    style={"margin-top": 10},
                )
            ])\
            for k, v in kh1.treasure_dicts[tab].items()
        ])
    ])
    unique = __create_treasures_unique(tab)
    return html.Div([
        treasures,
        unique,
    ])

def __create_treasures_unique(tab):
    kh1 = utils.kh1
    unique = None
    if tab == "Traverse Town":
        unique = html.Div([
            html.H3("Postcards"),
            dcc.Checklist(
                options=[{"label": "1st District Safe", "value": 1}],
                value=[kh1.safe_postcard.value],
                id="Safe Postcard",
                style={"margin-top": 10},
            ),
            dcc.Checklist(
                options=[
                    {"label": "Gizmo Shop 1", "value": (1 << 5)},
                    {"label": "Gizmo Shop 2", "value": (1 << 6)},
                ],
                value=[kh1.gizmo_postcards.value & (1 << i) for i in [5, 6]],
                id="Gizmo Postcards",
                style={"margin-top": 10},
                labelStyle={"margin-top": 10},
            ),
            dcc.Checklist(
                options=[
                    {"label": "Geppetto's House Shelf", "value": (1 << 3)},
                    {"label": "Item Workshop Poster", "value": (1 << 4)},
                    {"label": "1st District Balcony Barrel (vanilla JP only)", "value": (1 << 5)},
                    {"label": "3rd District Balcony", "value": (1 << 6)},
                    {"label": "Item Shop Fan", "value": (1 << 7)},
                ],
                value=[kh1.misc_postcards.value & (1 << i) for i in range(8)],
                id="Misc Postcards",
                style={"margin-top": 10},
                labelStyle={"margin-top": 10},
            ),
            dcc.Checklist(
                options=[
                    {"label": "Gizmo Shop switches are activated", "value": (1 << 0)},
                    {"label": "Gizmo Shop Postcards are ready", "value": (1 << 1)},
                ],
                value=[kh1.gizmo_switches.value & (1 << i) for i in range(8)],
                id="Gizmo Switches",
                style={"margin-top": 10},
                labelStyle={"margin-top": 10},
            ),
            dcc.Markdown("Postcards Mailed:"),
            dcc.Input(
                id="Postcards Mailed",
                type="number",
                value=kh1.postcards_mailed.value,
                min=0,
                max=10,
                step=1,
            ),
        ])
    if tab == "Atlantica":
        clams = html.Div([
            html.Div([
                dcc.Checklist(
                    options=[{"label": k, "value": (1 << v % 16)}],
                    value=[kh1.clams[v//16] & (1 << v % 16)],
                    id={"type": "Clam", "index": v},
                    style={"margin-top": 10},
                )
            ])\
            for k, v in kh1.clam_dict.items()
        ])
        unique = html.Div([
            html.H3("Clams:"),
            clams,
        ])
    if tab == "Neverland":
        doors = html.Div([
            html.Div([
                dcc.Checklist(
                    options=[{"label": k, "value": (1 << v % 16)}],
                    value=[kh1.bigben[v//16] & (1 << v % 16)],
                    id={"type": "Big Ben Door", "index": v},
                    style={"margin-top": 10},
                )
            ])\
            for k, v in kh1.bigben_dict.items()
        ])
        unique = html.Div([
            dcc.Checklist(
                options=[{"label": "Ship: Hold Aero Chest", "value": (1 << 1)}],
                value=[kh1.bigben[1] & (1 << 1)],
                id={"type": "Big Ben Door", "index": 0x11},
                style={"margin-top": 10},
            ),
            html.H3("Big Ben Doors:"),
            doors,
        ])
    return unique

def create_treasures():
    kh1 = utils.kh1
    tabs = dcc.Dropdown(
        options=[
            {"label": k, "value": k} for v, k in kh1.world_dict.items() if k in kh1.treasure_dicts
        ],
        value=kh1.world_dict[1],
        id="TreasuresTabs",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    return html.Div([
        html.Div([html.H3("World:"), tabs]),
        html.Div(id="TreasuresDiv", style={"margin-top": 20}),
    ])

@callback(
    Input({"type": "Treasure", "index": ALL}, "value"),
    State({"type": "Treasure", "index": ALL}, "id"),
)
def journal_treasures_callback(values, ids):
    kh1 = utils.kh1
    for i in range(len(values)):
        v = ids[i]["index"]
        if (1 << v % 16) in values[i]:
            kh1.treasures[v // 16] |= (1 << v % 16)
        else:
            kh1.treasures[v // 16] &= ~(1 << v % 16)

@callback(
    Input("Safe Postcard", "value"),
    Input("Gizmo Postcards", "value"),
    Input("Misc Postcards", "value"),
    Input("Gizmo Switches", "value"),
    Input("Postcards Mailed", "value"),
)
def postcards_callback(
    safe_postcard,
    gizmo_postcards,
    misc_postcards,
    gizmo_switches,
    postcards_mailed,
):
    kh1 = utils.kh1
    if 1 in safe_postcard:
        kh1.safe_postcard.value = 1
    else:
        kh1.safe_postcard.value = 0
    for i in range(8):
        if (1 << i) in gizmo_postcards:
            kh1.gizmo_postcards.value |= (1 << i)
        elif i in [5, 6]:
            kh1.gizmo_postcards.value &= ~(1 << i)
        if (1 << i) in misc_postcards:
            kh1.misc_postcards.value |= (1 << i)
        else:
            kh1.misc_postcards.value &= ~(1 << i)
        if (1 << i) in gizmo_switches:
            kh1.gizmo_switches.value |= (1 << i)
        else:
            kh1.gizmo_switches.value &= ~(1 << i)
    try:
        kh1.postcards_mailed.value = postcards_mailed
    except:
        pass

@callback(
    Input({"type": "Clam", "index": ALL}, "value"),
    State({"type": "Clam", "index": ALL}, "id"),
)
def journal_treasures_clams_callback(values, ids):
    kh1 = utils.kh1
    for i in range(len(values)):
        v = ids[i]["index"]
        if (1 << v % 16) in values[i]:
            kh1.clams[v // 16] |= (1 << v % 16)
        else:
            kh1.clams[v // 16] &= ~(1 << v % 16)

@callback(
    Input({"type": "Big Ben Door", "index": ALL}, "value"),
    State({"type": "Big Ben Door", "index": ALL}, "id"),
)
def journal_treasures_bigben_callback(values, ids):
    kh1 = utils.kh1
    for i in range(len(values)):
        v = ids[i]["index"]
        if (1 << v % 16) in values[i]:
            kh1.bigben[v // 16] |= (1 << v % 16)
        else:
            kh1.bigben[v // 16] &= ~(1 << v % 16)
