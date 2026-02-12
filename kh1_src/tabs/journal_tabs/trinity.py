from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


@callback(
    Output("TrinityDiv", "children"),
    Input("TrinityDD", "value"),
)
def __create_trinity_tabs(tab):
    if tab == "Trinity Jump":
        return __create_trinity(0)
    if tab == "Trinity Charge":
        return __create_trinity(1)
    if tab == "Trinity Ladder":
        return __create_trinity(2)
    if tab == "Trinity Push":
        return __create_trinity(3)
    if tab == "Trinity Detect":
        return __create_trinity(4)

def __create_trinity(i):
    kh1 = utils.kh1
    count = dcc.Input(
        id={"type": "Trinity Count", "index": i + 1 if i > 0 else i},
        type="number",
        value=kh1.trinity_count[i + 1 if i > 0 else i],
        min=0,
        max=0xFF,
        step=1,
        disabled=True,
        style={"width": 50},
    )
    flags = html.Div([
        dcc.Checklist(
            options=[
                {"label": k, "value": (1 << v % 16)}
            ],
            value=[kh1.trinity_flags[v // 16] & (1 << v % 16)],
            id={"type": "Trinity", "index": v},
        ) for k, v in kh1.trinity_dict_list[i].items()
    ])
    return html.Div([
        html.Div([
            html.Label("Count:"),
            count,
        ],
            style={"display": "flex", "margin-top": 20, "gap": 10},
        ),
        html.H4("Unlocked Trinities:"),
        flags,
    ])

def create_trinity():
    kh1 = utils.kh1
    trinity_unlock = dcc.Checklist(
        options=[
            {"label": kh1.trinity_names[i], "value": (1 << i)}\
            for i in range(len(kh1.trinity_names))
        ],
        value=[
            kh1.trinity_unlock.value & (1 << i)\
            for i in range(len(kh1.trinity_names))
        ],
        id="Trinity Unlock",
    )
    trinity_dd = dcc.Dropdown(
        options=[
            {"label": n, "value": n} for n in kh1.trinity_names
        ],
        value=kh1.trinity_names[0],
        id="TrinityDD",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    return html.Div([
        html.Div([html.H3("Trinity Unlock Flags:"), trinity_unlock]),
        html.Div([html.H3("Trinity Type:"), trinity_dd]),
        html.Div(id="TrinityDiv"),
    ])

@callback(
    Input("Trinity Unlock", "value")
)
def trinity_unlock_callback(value):
    kh1 = utils.kh1
    kh1.trinity_unlock.value = sum(value)

@callback(
    Input({"type": "Trinity Count", "index": ALL}, "value"),
    Input({"type": "Trinity Count", "index": ALL}, "id"),
)
def trinity_count_callback(values, ids):
    kh1 = utils.kh1
    kh1.trinity_count[ids[0]["index"]] = values[0]

@callback(
    Output({"type": "Trinity Count", "index": ALL}, "value"),
    Input({"type": "Trinity", "index": ALL}, "value"),
    Input({"type": "Trinity", "index": ALL}, "id"),
)
def trinity_callback(values, ids):
    kh1 = utils.kh1
    count = 0
    for i in range(len(values)):
        v = ids[i]["index"]
        if (1 << v % 16) in values[i]:
            kh1.trinity_flags[v // 16] |= (1 << v % 16)
            count += 1
        else:
            kh1.trinity_flags[v // 16] &= ~(1 << v % 16)
    return [count]
