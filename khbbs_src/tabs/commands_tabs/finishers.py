from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import khbbs_src.khbbs_utils as utils


def create_finishers():
    khbbs = utils.khbbs
    return html.Div([
        html.Div([
            html.H3(f"Finisher {finisher.idx+1}"),
            html.Div([
                dcc.Markdown("Finisher:"),
                dcc.Dropdown(
                    options=[
                        {"label": k, "value": v} for k, v\
                        in khbbs.finisher_dict.items()
                    ],
                    value=finisher.id,
                    id={"type": "Finisher ID", "index": finisher.idx},
                    style={"width": 200},
                    searchable=False,
                    clearable=False,
                ),
            ]),
            html.Div([
                dcc.Markdown("State:"),
                dcc.Dropdown(
                    options=[
                        {"label": "Empty", "value": 0},
                        {"label": "Locked", "value": 1},
                        {"label": "Unlocked", "value": 2},
                    ],
                    value=finisher.state,
                    id={"type": "Finisher State", "index": finisher.idx},
                    style={"width": 200},
                    searchable=False,
                    clearable=False,
                ),
            ]),
            html.Div([
                dcc.Markdown("EXP:"),
                dcc.Input(
                    id={"type": "Finisher EXP", "index": finisher.idx},
                    type="number",
                    value=finisher.exp,
                    min=0,
                    max=0xFFFF,
                    step=1,
                    style={"width": 50},
                ),
            ]),
            html.Div([
                dcc.Markdown("Name:"),
                dcc.Input(
                    id={"type": "Finisher Name", "index": finisher.idx},
                    type="text",
                    value=khbbs.finisher_names[finisher.idx].decode("Shift-JIS").strip("\0"),
                    style={"width": 200},
                ),
            ]),
        ]) for finisher in khbbs.finishers
    ])

@callback(
    Input({"type": "Finisher ID", "index": ALL}, "value"),
    Input({"type": "Finisher State", "index": ALL}, "value"),
    Input({"type": "Finisher EXP", "index": ALL}, "value"),
    State({"type": "Finisher ID", "index": ALL}, "id"),
)
def finisher_callback(
    ids,
    states,
    exps,
    idxs,
):
    khbbs = utils.khbbs
    for id, state, exp, idx in zip(ids, states, exps, idxs):
        finisher = khbbs.finishers[idx["index"]]
        finisher.id = id
        finisher.state = state
        try:
            finisher.exp = exp
        except:
            pass

@callback(
    Output({"type": "Finisher Name", "index": ALL}, "value"),
    Input({"type": "Finisher Name", "index": ALL}, "value"),
)
def finisher_name_callback(
    names,
):
    khbbs = utils.khbbs
    char_limit = 0x14 if khbbs.version == 0 else 0x26
    l = []
    for i in range(len(names)):
        name = bytearray(names[i], "Shift-JIS")
        limit = min(len(name), char_limit-1)
        khbbs.finisher_names[i] = name[:limit] + bytearray(char_limit - limit)
        l.append(khbbs.finisher_names[i].decode("Shift-JIS").strip("\0"))
    return l if len(l) > 0 else names
