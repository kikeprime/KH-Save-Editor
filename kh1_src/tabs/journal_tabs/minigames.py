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
        minigame = html.Div([
            html.Div([
                html.H3(k + ":"),
                html.Div([
                    # TODO: Buttons to set them to -1.
                    html.Div([
                        dcc.Markdown(p + ":"),
                        html.Div([
                            # Hours aren't needed
                            dcc.Input(
                                id={"type": "Minutes OC", "index": t},
                                type="number",
                                value=get_playtime(c_uint(kh1.oc_minigames[t//4]))[1],
                                min=0,
                                max=59,
                                step=1,
                                style={"width": 50},
                            ),
                            html.Label(" : "),
                            dcc.Input(
                                id={"type": "Seconds OC", "index": t},
                                type="number",
                                value=get_playtime(c_uint(kh1.oc_minigames[t//4]))[2],
                                min=0,
                                max=59,
                                step=1,
                                style={"width": 50},
                            ),
                            html.Label(" : "),
                            dcc.Input(
                                id={"type": "Fraction OC", "index": t},
                                type="number",
                                value=get_playtime(c_uint(kh1.oc_minigames[t//4]))[3],
                                min=0,
                                max=59,
                                step=1,
                                style={"width": 50},
                            ),
                            html.Label(" 100th: "),
                            dcc.Input(
                                id={"type": "100th OC", "index": t},
                                type="number",
                                value=get_playtime(c_uint(kh1.oc_minigames[t//4]))[3] * 100 // 60,
                                min=0,
                                max=99,
                                step=1,
                                disabled=True,
                                style={"width": 50},
                            ),
                        ]) if kh1.oc_minigames[t//4] >= 0 else\
                        html.Div([
                            # TODO: Initializer buttons to set them to 0.
                        ])
                    ],
                        style={"margin-top": 20, "gap": 10},
                    )\
                    for p, t in v.items()
                ])
            ])\
            for k, v in kh1.oc_minigame_dict.items()
        ])
    elif tab in kh1.minigames_with_sub:
        minigame = html.Div([
            html.Div([
                html.H3(k + ":"),
                html.Div([
                    # TODO: Buttons to set them to -1.
                    html.Div([
                        dcc.Markdown(p + ":"),
                        html.Div([
                            # Hours aren't needed
                            dcc.Input(
                                id={"type": "Minutes", "index": t},
                                type="number",
                                value=get_playtime(c_uint(kh1.minigames[t//4]))[1],
                                min=0,
                                max=59,
                                step=1,
                                style={"width": 50},
                            ),
                            html.Label(" : "),
                            dcc.Input(
                                id={"type": "Seconds", "index": t},
                                type="number",
                                value=get_playtime(c_uint(kh1.minigames[t//4]))[2],
                                min=0,
                                max=59,
                                step=1,
                                style={"width": 50},
                            ),
                            html.Label(" : "),
                            dcc.Input(
                                id={"type": "Fraction", "index": t},
                                type="number",
                                value=get_playtime(c_uint(kh1.minigames[t//4]))[3],
                                min=0,
                                max=59,
                                step=1,
                                style={"width": 50},
                            ),
                            html.Label(" 100th: "),
                            dcc.Input(
                                id={"type": "100th", "index": t},
                                type="number",
                                value=get_playtime(c_uint(kh1.minigames[t//4]))[3] * 100 // 60,
                                min=0,
                                max=99,
                                step=1,
                                disabled=True,
                                style={"width": 50},
                            ),
                        ]) if kh1.minigames[t//4] >= 0 else\
                        html.Div([
                            # TODO: Initializer buttons to set them to 0.
                        ])
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
                    # TODO: Buttons to set them to -1.
                    html.Div([
                        dcc.Markdown(p + ":"),
                        html.Div([
                            # Hours aren't needed
                            dcc.Input(
                                id={"type": "Minutes", "index": t},
                                type="number",
                                value=get_playtime(c_uint(kh1.minigames[t//4]))[1],
                                min=0,
                                max=59,
                                step=1,
                                style={"width": 50},
                            ),
                            html.Label(" : "),
                            dcc.Input(
                                id={"type": "Seconds", "index": t},
                                type="number",
                                value=get_playtime(c_uint(kh1.minigames[t//4]))[2],
                                min=0,
                                max=59,
                                step=1,
                                style={"width": 50},
                            ),
                            html.Label(" : "),
                            dcc.Input(
                                id={"type": "Fraction", "index": t},
                                type="number",
                                value=get_playtime(c_uint(kh1.minigames[t//4]))[3],
                                min=0,
                                max=59,
                                step=1,
                                style={"width": 50},
                            ),
                            html.Label(" 100th: "),
                            dcc.Input(
                                id={"type": "100th", "index": t},
                                type="number",
                                value=get_playtime(c_uint(kh1.minigames[t//4]))[3] * 100 // 60,
                                min=0,
                                max=99,
                                step=1,
                                disabled=True,
                                style={"width": 50},
                            ),
                        ]) if kh1.minigames[t//4] >= 0 else\
                        html.Div([
                            # TODO: Initializer buttons to set them to 0.
                        ])
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

def create_minigames():
    kh1 = utils.kh1
    mgtabs = dcc.Tabs(id="MiniGamesTabs", value="Jungle Slider")
    mgtabs.children = [
        dcc.Tab(label=k, value=k)\
        for k in kh1.minigame_dict.keys()
    ] + [
        dcc.Tab(label="Olympus Coliseum", value="Olympus Coliseum"),
    ]
    return html.Div([
        mgtabs,
        html.Div(id="MiniGamesDiv"),
    ])

@callback(
    Input({"type": "Score", "index": ALL}, "value"),
    Input({"type": "Score", "index": ALL}, "id"),
)
def minigame_score_callback(scores, ids):
    kh1 = utils.kh1
    try:
        for score, id in zip(scores, ids):
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
    try:
        l = []
        for minute, second, fraction, id in zip(minutes, seconds, fractions, ids):
            idx = id["index"] // 4
            kh1.minigames[idx] = calculate_playtime(0, minute, second, fraction)
            l.append(fraction * 100 // 60)
        return l
    except:
        return [0 for i in range(len(minutes))]

@callback(
    Output({"type": "100th OC", "index": ALL}, "value"),
    Input({"type": "Minutes OC", "index": ALL}, "value"),
    Input({"type": "Seconds OC", "index": ALL}, "value"),
    Input({"type": "Fraction OC", "index": ALL}, "value"),
    Input({"type": "Minutes OC", "index": ALL}, "id"),
)
def minigame_oc_callback(minutes, seconds, fractions, ids):
    kh1 = utils.kh1
    try:
        l = []
        for minute, second, fraction, id in zip(minutes, seconds, fractions, ids):
            idx = id["index"] // 4
            kh1.oc_minigames[idx] = calculate_playtime(0, minute, second, fraction)
            l.append(fraction * 100 // 60)
        return l
    except:
        return [0 for i in range(len(minutes))]
