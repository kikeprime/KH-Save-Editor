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
