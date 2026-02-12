from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


@callback(
    Output("TrinityDiv", "children"),
    Input("TrinityDD", "value"),
)
def __create_trinity_tabs(tab):
    if tab == "Trinity Jump":
        return __create_trinity_jump()

def __create_trinity_jump():
    kh1 = utils.kh1
    count = dcc.Input(
        id={"type": "Trinity Count", "index": "Jump"},
        type="number",
        value=kh1.trinity_count[0],
        min=0,
        max=0xFF,
        step=1,
        disabled=True,
        style={"width": 50},
    )
    return html.Div([
        html.Div([
            html.Label("Count:"), count
        ],
            style={"display": "flex", "margin-top": 20, "gap": 10},
        ),
        html.H4("Traverse Town:"),
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
        id="TrinityUnlock",
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
