from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import khbbs_src.khbbs_utils as utils


def create_dlinks():
    khbbs = utils.khbbs
    return html.Div([
        html.Div([
            html.H3(f"D-Link {dlink.idx+1}"),
            html.Div([
                dcc.Markdown("D-Link:"),
                dcc.Dropdown(
                    options=[
                        {"label": k, "value": v} for k, v\
                        in khbbs.dlink_dict.items()
                    ],
                    value=dlink.id,
                    id={"type": "D-Link ID", "index": dlink.idx},
                    style={"width": 200},
                    searchable=False,
                    clearable=False,
                ),
            ]),
            html.Div([
                dcc.Markdown("Equipped:"),
                dcc.Dropdown(
                    options=[
                        {"label": "On", "value": True},
                        {"label": "Off", "value": False},
                    ],
                    value=dlink.on,
                    id={"type": "D-Link On", "index": dlink.idx},
                    style={"width": 200},
                    searchable=False,
                    clearable=False,
                ),
            ]),
            html.Div([
                dcc.Markdown("Ability 1:"),
                dcc.Dropdown(
                    options=[
                        {"label": "Got", "value": True},
                        {"label": "Not Got", "value": False},
                    ],
                    value=dlink.ability_1,
                    id={"type": "D-Link Ability 1", "index": dlink.idx},
                    style={"width": 200},
                    searchable=False,
                    clearable=False,
                ),
            ]),
            html.Div([
                dcc.Markdown("Ability 2:"),
                dcc.Dropdown(
                    options=[
                        {"label": "Got", "value": True},
                        {"label": "Not Got", "value": False},
                    ],
                    value=dlink.ability_2,
                    id={"type": "D-Link Ability 2", "index": dlink.idx},
                    style={"width": 200},
                    searchable=False,
                    clearable=False,
                ),
            ]),
        ]) for dlink in khbbs.dlinks
    ])

@callback(
    Input({"type": "D-Link ID", "index": ALL}, "value"),
    Input({"type": "D-Link On", "index": ALL}, "value"),
    Input({"type": "D-Link Ability 1", "index": ALL}, "value"),
    Input({"type": "D-Link Ability 2", "index": ALL}, "value"),
    State({"type": "D-Link ID", "index": ALL}, "id"),
)
def dlink_callback(
    ids,
    ons,
    ability_1s,
    ability_2s,
    idxs,
):
    khbbs = utils.khbbs
    for id, on, ability_1, ability_2, idx in zip(ids, ons, ability_1s, ability_2s, idxs):
        dlink = khbbs.dlinks[idx["index"]]
        dlink.id = id
        dlink.on = on
        dlink.ability_1 = ability_1
        dlink.ability_2 = ability_2
