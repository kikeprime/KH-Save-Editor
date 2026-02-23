from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh2_src.kh2_utils as utils


@callback(
    Output("JournalBestiaryDiv", "children"),
    Input("JournalBestiaryTabs", "value"),
)
def __create_journal_characters_tabs(tab):
    if tab == "The Heartless":
        return __create_the_heartless()
    if tab == "The Nobodies":
        return __create_nobodies()
    if tab == "Reaction Commands":
        return __create_rcs()
    if tab == "Limits":
        return __create_limits()

def __create_the_heartless():
    kh2 = utils.kh2
    heartless = html.Div([
        html.Div([
            html.Label(k + ": "),
            dcc.Input(
                id={"type": "Heartless Kill Count", "index": kh2.heartless_dict[k]},
                type="number",
                value=kh2.heartless[kh2.heartless_dict[k]],
                min=0,
                max=0xFFFFFFFF,
                step=1,
                style={"width": 100},
            ),
        ],
            style={"margin-top": 20, "gap": 10},
        ) for k in kh2.heartless_list if kh2.heartless_dict[k] < len(kh2.heartless)
    ])
    return html.Div([
        heartless,
    ])

def __create_nobodies():
    kh2 = utils.kh2
    nobodies = html.Div([
        html.Div([
            html.Label(k + ": "),
            dcc.Input(
                id={"type": "Nobody Kill Count", "index": kh2.nobody_dict[k]},
                type="number",
                value=kh2.nobodies[kh2.nobody_dict[k]],
                min=0,
                max=0xFFFFFFFF,
                step=1,
                style={"width": 100},
            ),
        ],
            style={"margin-top": 20, "gap": 10},
        ) for k in kh2.nobody_list
    ])
    return html.Div([
        nobodies,
    ])

def __create_rcs():
    kh2 = utils.kh2
    rcs = html.Div([
        html.Div([
            html.H3(k + ":"),
            html.Div([
                html.Div([
                    html.Label(rc + ": "),
                    dcc.Input(
                        id={"type": "RC Count", "index": kh2.rc_dict[rc]},
                        type="number",
                        value=kh2.rc_usage[kh2.rc_dict[rc]],
                        min=0,
                        max=0xFFFFFFFF,
                        step=1,
                        style={"width": 100},
                    )
                ],
                    style={"margin-top": 20, "gap": 10},
                ) for rc in v
            ]),
        ]) for k, v in kh2.rc_list_dict.items()
    ])
    return html.Div([
        rcs,
    ])

def __create_limits():
    kh2 = utils.kh2
    limits = html.Div([
        html.Div([
            html.Label(k + ": "),
            dcc.Input(
                id={"type": "Limit Count", "index": kh2.limit_dict[k]},
                type="number",
                value=kh2.limit_usage[kh2.limit_dict[k]],
                min=0,
                max=0xFFFFFFFF,
                step=1,
                style={"width": 100},
            ),
        ],
            style={"margin-top": 20, "gap": 10},
        ) for k in kh2.limit_list
    ])
    return html.Div([
        limits,
    ])


def create_bestiary():
    kh2 = utils.kh2
    jbtabs = dcc.Tabs(id="JournalBestiaryTabs", value="The Heartless")
    jbtabs.children = [
        dcc.Tab(label="The Heartless", value="The Heartless"),
        dcc.Tab(label="The Nobodies", value="The Nobodies"),
        dcc.Tab(label="Reaction Commands", value="Reaction Commands"),
        dcc.Tab(label="Combo Attacks" if not kh2.fm else "Limits", value="Limits"),
    ]
    return html.Div([
        jbtabs,
        html.Div(id="JournalBestiaryDiv"),
    ])

@callback(
    Input({"type": "Heartless Kill Count", "index": ALL}, "value"),
    State({"type": "Heartless Kill Count", "index": ALL}, "id"),
)
def the_heartless_callback(values, ids):
    kh2 = utils.kh2
    i = 0
    for id in ids:
        idx = id["index"]
        if values[i] is not None:
            kh2.heartless[idx] = values[i]
        i += 1

@callback(
    Input({"type": "Nobody Kill Count", "index": ALL}, "value"),
    State({"type": "Nobody Kill Count", "index": ALL}, "id"),
)
def the_nobodies_callback(values, ids):
    kh2 = utils.kh2
    i = 0
    for id in ids:
        idx = id["index"]
        if values[i] is not None:
            kh2.nobodies[idx] = values[i]
        i += 1

@callback(
    Input({"type": "RC Count", "index": ALL}, "value"),
    State({"type": "RC Count", "index": ALL}, "id"),
)
def rcs_callback(values, ids):
    kh2 = utils.kh2
    i = 0
    for id in ids:
        idx = id["index"]
        if values[i] is not None:
            kh2.rc_usage[idx] = values[i]
        i += 1

@callback(
    Input({"type": "Limit Count", "index": ALL}, "value"),
    State({"type": "Limit Count", "index": ALL}, "id"),
)
def limits_callback(values, ids):
    kh2 = utils.kh2
    i = 0
    for id in ids:
        idx = id["index"]
        if values[i] is not None:
            kh2.limit_usage[idx] = values[i]
        i += 1
