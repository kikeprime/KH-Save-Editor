from dash import Dash, html, dcc, callback, Input, Output, State, ALL, MATCH, ctx
import kh2_src.kh2_utils as utils


def create_treasures():
    kh2 = utils.kh2
    treasures = html.Div([
        html.Div([
            html.H3(w),
            html.Label(
                "Click on a checkbox to see the content!",
                id={"type": "Treasure Chest Viewer", "world": w},
                style={"margin-bottom": 10},
            ),
            html.Table([
                html.Tr([
                    html.Td([
                        dcc.Checklist(
                            options=[{"label": "", "value": (1 << v % 16)}],
                            value=[kh2.treasures[v//16] & (1 << v % 16)],
                            id={"type": "Treasure Chest", "world": w, "index": v},
                            style={"margin-bottom": 10, "margin-right": 10},
                        ),
                    ]) for v in row
                ]) for row in t
            ]),
        ]) for w, t in kh2.treasure_dict.items()
    ])
    return html.Div([
        treasures,
    ])

@callback(
    Output({"type": "Treasure Chest Viewer", "world": MATCH}, "children"),
    Input({"type": "Treasure Chest", "world": MATCH, "index": ALL}, "value"),
    State({"type": "Treasure Chest", "world": MATCH, "index": ALL}, "id"),
)
def treasures_callbacks(chests, ids):
    kh2 = utils.kh2
    for chest, id in zip(chests, ids):
        idx = id["index"]
        if (1 << idx % 16) in chest:
            kh2.treasures[idx//16] |= (1 << idx % 16)
        else:
            kh2.treasures[idx//16] &= ~(1 << idx % 16)
    chest = ctx.triggered_id
    if chest is not None:
        w = chest["world"]
        idx = chest["index"]
        return kh2.treasure_zip[w][idx]
    else:
        return "Click on a checkbox to see the content!"
