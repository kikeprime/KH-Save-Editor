from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


@callback(
    Output("TreasuresDiv", "children"),
    Input("TreasuresTabs", "value"),
)
def __create_treasures(tab):
    kh1 = utils.kh1
    treasures = html.Div([
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
    unique = None
    return html.Div([
        treasures,
        unique,
    ])

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
