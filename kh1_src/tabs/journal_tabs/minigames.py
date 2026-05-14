from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils

from ctypes import *
from kh1_src.tabs.general import get_playtime, calculate_playtime


@callback(
    Output("MiniGamesDiv", "children"),
    Input("MiniGamesTabs", "value"),
)
def __create_minigames_tabs(tab):
    kh1 = utils.kh1
    if tab == "Olympus Coliseum":
        return __create_oc_minigames()
    if tab == "Destiny Islands":
        return __create_di_minigames()
    elif tab in kh1.minigames_with_sub:
        minigame = html.Div([
            html.Div([
                html.H3(k + ":"),
                html.Div([
                    html.Div([
                        dcc.Markdown(p + ":"),
                        html.Div(
                            __create_minigame(t),
                            id={"type": "Minigame Div", "index": t},
                        ),
                    ],
                        style={"margin-top": 20, "gap": 10},
                    )\
                    for p, t in v.items()
                ])
            ])\
            for k, v in kh1.minigame_dict[tab].items()
        ])
    else:
        minigame = html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Markdown(p + ":"),
                        html.Div(
                            __create_minigame(t),
                            id={"type": "Minigame Div", "index": t},
                        ),
                    ],
                        style={"margin-top": 20, "gap": 10},
                    ) if tab not in kh1.minigames_with_scores.keys() else\
                    html.Div([
                        dcc.Markdown(p + ":"),
                        html.Div([
                            dcc.Input(
                                id={"type": "Score", "index": t},
                                type="number",
                                value=kh1.minigames[t//4],
                                min=-1,
                                max=1000, # temporary
                                step=1,
                                style={"width": 50},
                            ),
                            html.Label(" " + kh1.minigames_with_scores[tab]),
                        ])
                    ],
                        style={"margin-top": 20, "gap": 10},
                    ),
                ])
            ])\
            for p, t in kh1.minigame_dict[tab].items()
        ])
    return minigame

def __create_minigame(t):
    kh1 = utils.kh1
    return html.Div([
        # Hours aren't needed
        dcc.Input(
            id={"type": "Minutes", "index": t},
            type="number",
            value=get_playtime(kh1.minigames[t//4])[1],
            min=0,
            max=59,
            step=1,
            style={"width": 50},
        ),
        html.Label(" : "),
        dcc.Input(
            id={"type": "Seconds", "index": t},
            type="number",
            value=get_playtime(kh1.minigames[t//4])[2],
            min=0,
            max=59,
            step=1,
            style={"width": 50},
        ),
        html.Label(" : "),
        dcc.Input(
            id={"type": "Fraction", "index": t},
            type="number",
            value=get_playtime(kh1.minigames[t//4])[3],
            min=0,
            max=59,
            step=1,
            style={"width": 50},
        ),
        html.Label(" 100th: "),
        dcc.Input(
            id={"type": "100th", "index": t},
            type="number",
            value=get_playtime(kh1.minigames[t//4])[3] * 100 // 60,
            min=0,
            max=99,
            step=1,
            disabled=True,
            style={"width": 50},
        ),
        html.Div([
            html.Button(
                "Unset",
                id={"type": "Uninitializer", "index": t},
                n_clicks=0,
                style={"width": 100},
            ),
        ],
            style={"margin-top": 15},
        ),
    ]) if kh1.minigames[t//4] >= 0 else\
    html.Div([
        html.Label("Unset record. "),
        html.Button(
            "Initialize",
            id={"type": "Initializer", "index": t},
            n_clicks=0,
            style={"width": 100},
        ),
    ]),

def __create_oc_minigames():
    kh1 = utils.kh1
    minigame = html.Div([
        html.Div([
            html.H3(k + ":"),
            html.Div([
                html.Div([
                    dcc.Markdown(p + ":"),
                    html.Div(
                        __create_oc_minigame(t),
                        id={"type": "OC Minigame Div", "index": t}
                    ),
                ],
                    style={"margin-top": 20, "gap": 10},
                )\
                for p, t in v.items()
            ])
        ])\
        for k, v in kh1.oc_minigame_dict.items()
    ])
    return minigame

def __create_oc_minigame(t):
    kh1 = utils.kh1
    return html.Div([
        # Hours aren't needed
        dcc.Input(
            id={"type": "Minutes OC", "index": t},
            type="number",
            value=get_playtime(kh1.oc_minigames[t//4])[1],
            min=0,
            max=59,
            step=1,
            style={"width": 50},
        ),
        html.Label(" : "),
        dcc.Input(
            id={"type": "Seconds OC", "index": t},
            type="number",
            value=get_playtime(kh1.oc_minigames[t//4])[2],
            min=0,
            max=59,
            step=1,
            style={"width": 50},
        ),
        html.Label(" : "),
        dcc.Input(
            id={"type": "Fraction OC", "index": t},
            type="number",
            value=get_playtime(kh1.oc_minigames[t//4])[3],
            min=0,
            max=59,
            step=1,
            style={"width": 50},
        ),
        html.Label(" 100th: "),
        dcc.Input(
            id={"type": "100th OC", "index": t},
            type="number",
            value=get_playtime(kh1.oc_minigames[t//4])[3] * 100 // 60,
            min=0,
            max=99,
            step=1,
            disabled=True,
            style={"width": 50},
        ),
        html.Div([
            html.Button(
                "Unset",
                id={"type": "Uninitializer OC", "index": t},
                n_clicks=0,
                style={"width": 100},
            ),
        ],
            style={"margin-top": 15},
        ),
    ]) if kh1.oc_minigames[t//4] >= 0 else\
    html.Div([
        html.Label("Unset record. "),
        html.Button(
            "Initialize",
            id={"type": "Initializer OC", "index": t},
            n_clicks=0,
            style={"width": 100},
        ),
    ]),

def __create_di_minigames():
    kh1 = utils.kh1
    return html.Div([
        html.H3("Sora vs. Riku"),
        html.Div([
            html.Div([
                html.Label("Sora: "),
                dcc.Input(
                    id="Sora Wins",
                    type="number",
                    value=kh1.sorawins.value,
                    min=0,
                    max=100,
                    step=1,
                    style={"width": 50},
                ),
            ]),
            html.Div([
                html.Label("Riku: "),
                dcc.Input(
                    id="Riku Wins",
                    type="number",
                    value=kh1.rikuwins.value,
                    min=0,
                    max=100,
                    step=1,
                    style={"width": 50},
                ),
            ]),
        ],
            style={"display": "flex", "gap": 10},
        ),
        html.H3("Sora vs. FF Trio"),
        html.Div([
            html.Div([
                html.Label("Tidus: "),
                dcc.Input(
                    id="Tidus Wins",
                    type="number",
                    value=kh1.tiduswins.value,
                    min=0,
                    max=255,
                    step=1,
                    style={"width": 50},
                ),
            ]),
            html.Div([
                html.Label("Wakka: "),
                dcc.Input(
                    id="Wakka Wins",
                    type="number",
                    value=kh1.wakkawins.value,
                    min=0,
                    max=255,
                    step=1,
                    style={"width": 50},
                ),
            ]),
            html.Div([
                html.Label("Selphie: "),
                dcc.Input(
                    id="Selphie Wins",
                    type="number",
                    value=kh1.selphiewins.value,
                    min=0,
                    max=255,
                    step=1,
                    style={"width": 50},
                ),
            ]),
        ],
            style={"display": "flex", "gap": 10},
        ),
    ])

def create_minigames():
    kh1 = utils.kh1
    mgtabs = dcc.Tabs(id="MiniGamesTabs", value="Jungle Slider")
    mgtabs.children = [
        dcc.Tab(label=k, value=k)\
        for k in kh1.minigame_dict.keys()
    ] + [
        dcc.Tab(label="Olympus Coliseum", value="Olympus Coliseum"),
        dcc.Tab(label="Destiny Islands", value="Destiny Islands"),
    ]
    return html.Div([
        mgtabs,
        html.Div(id="MiniGamesDiv"),
    ])

@callback(
    Output({"type": "OC Minigame Div", "index": ALL}, "children"),
    Input({"type": "Initializer OC", "index": ALL}, "n_clicks"),
    Input({"type": "Initializer OC", "index": ALL}, "id"),
    Input({"type": "Uninitializer OC", "index": ALL}, "n_clicks"),
    Input({"type": "Uninitializer OC", "index": ALL}, "id"),
    State({"type": "OC Minigame Div", "index": ALL}, "id"),
)
def initialize_oc_callback(n_clicks_oc, ids_oc, n_clicks_oc_u, ids_oc_u, divs):
    kh1 = utils.kh1
    if n_clicks_oc != []:
        for n_click, id in zip(n_clicks_oc, ids_oc):
            if n_click > 0:
                idx = id["index"] // 4
                kh1.oc_minigames[idx] = 0
    if n_clicks_oc_u != []:
        for n_click, id in zip(n_clicks_oc_u, ids_oc_u):
            if n_click > 0:
                idx = id["index"] // 4
                kh1.oc_minigames[idx] = -1
    return [__create_oc_minigame(div["index"]) for div in divs]

@callback(
    Output({"type": "Minigame Div", "index": ALL}, "children"),
    Input({"type": "Initializer", "index": ALL}, "n_clicks"),
    Input({"type": "Initializer", "index": ALL}, "id"),
    Input({"type": "Uninitializer", "index": ALL}, "n_clicks"),
    Input({"type": "Uninitializer", "index": ALL}, "id"),
    State({"type": "Minigame Div", "index": ALL}, "id"),
)
def initialize_callback(n_clicks, ids, n_clicks_u, ids_u, divs):
    kh1 = utils.kh1
    if n_clicks != []:
        for n_click, id in zip(n_clicks, ids):
            if n_click > 0:
                idx = id["index"] // 4
                kh1.minigames[idx] = 0
    if n_clicks_u != []:
        for n_click, id in zip(n_clicks_u, ids_u):
            if n_click > 0:
                idx = id["index"] // 4
                kh1.minigames[idx] = -1
    return [__create_minigame(div["index"]) for div in divs]

@callback(
    Input({"type": "Score", "index": ALL}, "value"),
    Input({"type": "Score", "index": ALL}, "id"),
)
def minigame_score_callback(scores, ids):
    kh1 = utils.kh1
    for score, id in zip(scores, ids):
        try:
            idx = id["index"] // 4
            kh1.minigames[idx] = score
        except:
            pass

@callback(
    Output({"type": "100th", "index": ALL}, "value"),
    Input({"type": "Minutes", "index": ALL}, "value"),
    Input({"type": "Seconds", "index": ALL}, "value"),
    Input({"type": "Fraction", "index": ALL}, "value"),
    Input({"type": "Minutes", "index": ALL}, "id"),
)
def minigame_time_callback(minutes, seconds, fractions, ids):
    kh1 = utils.kh1
    centis = []
    for minute, second, fraction, id in zip(minutes, seconds, fractions, ids):
        try:
            idx = id["index"] // 4
            kh1.minigames[idx] = calculate_playtime(0, minute, second, fraction)
            centis.append(fraction * 100 // 60)
        except:
            centis.append(0)
    return centis

@callback(
    Output({"type": "100th OC", "index": ALL}, "value"),
    Input({"type": "Minutes OC", "index": ALL}, "value"),
    Input({"type": "Seconds OC", "index": ALL}, "value"),
    Input({"type": "Fraction OC", "index": ALL}, "value"),
    Input({"type": "Minutes OC", "index": ALL}, "id"),
)
def minigame_oc_callback(minutes, seconds, fractions, ids):
    kh1 = utils.kh1
    centis = []
    for minute, second, fraction, id in zip(minutes, seconds, fractions, ids):
        try:
            idx = id["index"] // 4
            kh1.oc_minigames[idx] = calculate_playtime(0, minute, second, fraction)
            centis.append(fraction * 100 // 60)
        except:
            centis.append(0)
    return centis

@callback(
    Input("Sora Wins", "value"),
    Input("Riku Wins", "value"),
    Input("Tidus Wins", "value"),
    Input("Wakka Wins", "value"),
    Input("Selphie Wins", "value"),
)
def minigame_di_callback(
    sorawins, rikuwins,
    tiduswins, wakkawins, selphiewins,
):
    kh1 = utils.kh1
    try:
        kh1.sorawins.value = sorawins
        kh1.rikuwins.value = rikuwins
        kh1.tiduswins.value = tiduswins
        kh1.wakkawins.value = wakkawins
        kh1.selphiewins.value = selphiewins
    except:
        pass
