from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh2_src.kh2_utils as utils
from kh2_src.tabs.general import get_playtime


@callback(
    Output({"type": "Minigame Div", "index": ALL}, "children"),
    Input({"type": "Minigame Type", "index": ALL}, "value"),
    Input({"type": "Minigame Type", "index": ALL}, "id"),
)
def __create_minigame(mg_types, ids):
    kh2 = utils.kh2
    mgs = []
    for t, id in zip(mg_types, ids):
        idx = kh2.minigame_list.index(id["index"])
        if t == 4:
            mgs.append(
                html.Div([
                    # Hours aren't needed
                    dcc.Input(
                        id={"type": "MG Minutes", "index": idx},
                        type="number",
                        value=get_playtime(kh2.minigames[idx].score.value)[1],
                        min=0,
                        max=59,
                        step=1,
                        style={"width": 30},
                    ),
                    html.Label(" : "),
                    dcc.Input(
                        id={"type": "MG Seconds", "index": idx},
                        type="number",
                        value=get_playtime(kh2.minigames[idx].score.value)[2],
                        min=0,
                        max=59,
                        step=1,
                        style={"width": 30},
                    ),
                    html.Label(" : "),
                    dcc.Input(
                        id={"type": "MG Fraction", "index": idx},
                        type="number",
                        value=get_playtime(kh2.minigames[idx].score.value)[3],
                        min=0,
                        max=59,
                        step=1,
                        style={"width": 30},
                    ),
                    html.Label(" : "),
                    dcc.Input(
                        id={"type": "MG 100th", "index": idx},
                        type="number",
                        value=get_playtime(kh2.minigames[idx].score.value)[3] * 100 // 60,
                        min=0,
                        max=99,
                        step=1,
                        disabled=True,
                        style={"width": 30},
                    ),
                ], style={"margin": 5})
            )
        else:
            mgs.append(
                html.Div([
                    dcc.Input(
                        id={"type": "Minigame", "index": idx},
                        type="number",
                        value=kh2.minigames[idx].score.value,
                        min=0,
                        max=0xFFFFFFFF,
                        step=1,
                        style={"width": 100, "margin": 5},
                    ),
                ])
            )
            kh2.minigames[idx].type.value = t
    return mgs

def create_minigames():
    kh2 = utils.kh2
    return html.Div([
        html.Div([
            html.H3(w),
            html.Div([
                html.Div([
                    html.Div(id={"type": "Minigame Div", "index": mg}),
                    dcc.Dropdown(
                        options=[
                            {"label": v, "value": k}\
                            for k, v in kh2.minigame_type_dict.items()
                        ],
                        value=kh2.minigames[kh2.minigame_list.index(mg)].type.value,
                        id={"type": "Minigame Type", "index": mg},
                        searchable=False,
                        clearable=False,
                        style={"width": 150},
                    ),
                ], style={"display": "flex", "margin-bottom": 20})\
                for mg in mgs if kh2.minigame_list.index(mg) < len(kh2.minigames)
            ]),
        ])\
        for w, mgs in kh2.minigame_list_dict.items()
    ])
