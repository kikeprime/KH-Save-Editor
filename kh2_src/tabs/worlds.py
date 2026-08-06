from dash import Dash, html, dcc, callback, Input, Output, State, ALL, MATCH
import kh2_src.kh2_utils as utils
from .general import get_playtime, calculate_playtime


@callback(
    Output("WorldsDiv", "children"),
    Input("WorldsTabs", "value"),
    Input("WorldsSubTabs", "value"),
)
def __create_worlds(w, tab):
    kh2 = utils.kh2
    w_idx = {w: idx for idx, w in kh2.world_dict.items()}[w]
    hours, minutes, seconds, fraction = get_playtime(kh2.playtimes[w_idx+2])
    playtime = html.Div([
        html.H3("Playtime:"),
        html.Div([
            dcc.Input(
                id={"type": "Hours", "world": w},
                type="number",
                value=hours,
                min=0,
                max=399,
                step=1,
                style={"width": 50},
            ),
            html.Label(" : "),
            dcc.Input(
                id={"type": "Minutes", "world": w},
                type="number",
                value=minutes,
                min=0,
                max=59,
                step=1,
                style={"width": 50},
            ),
            html.Label(" : "),
            dcc.Input(
                id={"type": "Seconds", "world": w},
                type="number",
                value=seconds,
                min=0,
                max=59,
                step=1,
                style={"width": 50},
            ),
            html.Label(" : "),
            dcc.Input(
                id={"type": "Fraction", "world": w},
                type="number",
                value=fraction,
                min=0,
                max=59,
                step=1,
                style={"width": 50},
            ),
            html.Label(" : "),
            dcc.Input(
                id={"type": "100th", "world": w_idx},
                type="number",
                value=fraction * 100 // 60,
                min=0,
                max=99,
                step=1,
                disabled=True,
                style={"width": 50},
            ),
        ]),
    ])
    progress = None
    if (tab == "Progress Flags"):
        progress = html.Div([
            html.H3("Progress Flags:"),
            html.Div([
                dcc.Checklist(
                    options=[{"label": k, "value":(1 << v % 16)}],
                    value=[kh2.progress[w][v//16] & (1 << v % 16)],
                    id={"type": "Progress", "world": w, "index": v},
                    style={"margin-bottom": 10},
                ) for k, v in kh2.progress_dict[w].items()
            ]),
        ])
    placescripts = None
    if (tab == "Place Scripts"):
        placescripts = __create_placescripts(w)
    return html.Div([
        playtime,
        progress,
        placescripts,
    ])

def __create_placescripts(w):
    kh2 = utils.kh2
    if kh2.fm:
        return html.Div([
            html.H3("Place Scripts:"),
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Map", scope="col"),
                        html.Th("Map 2", scope="col"),
                        html.Th("Battle", scope="col"),
                        html.Th("Battle 2", scope="col"),
                        html.Th("Event", scope="col"),
                        html.Th("Event 2", scope="col"),
                    ]),
                ]),
                html.Tbody([
                    html.Tr([
                        html.Td([
                            dcc.Input(
                                id={"type": "Place Script Map", "world": w, "index": i},
                                type="number",
                                value=kh2.placescripts[w][i].map.value,
                                min=0,
                                max=255,
                                step=1,
                                style={"width": 50},
                            ),
                        ]),
                        html.Td([
                            dcc.Input(
                                id={"type": "Place Script Map 2", "world": w, "index": i},
                                type="number",
                                value=kh2.placescripts[w][i].map2.value,
                                min=0,
                                max=255,
                                step=1,
                                style={"width": 50},
                            ),
                        ]),
                        html.Td([
                            dcc.Input(
                                id={"type": "Place Script Battle", "world": w, "index": i},
                                type="number",
                                value=kh2.placescripts[w][i].battle.value,
                                min=0,
                                max=255,
                                step=1,
                                style={"width": 50},
                            ),
                        ]),
                        html.Td([
                            dcc.Input(
                                id={"type": "Place Script Battle 2", "world": w, "index": i},
                                type="number",
                                value=kh2.placescripts[w][i].battle2.value,
                                min=0,
                                max=255,
                                step=1,
                                style={"width": 50},
                            ),
                        ]),
                        html.Td([
                            dcc.Input(
                                id={"type": "Place Script Event", "world": w, "index": i},
                                type="number",
                                value=kh2.placescripts[w][i].event.value,
                                min=0,
                                max=255,
                                step=1,
                                style={"width": 50},
                            ),
                        ]),
                        html.Td([
                            dcc.Input(
                                id={"type": "Place Script Event 2", "world": w, "index": i},
                                type="number",
                                value=kh2.placescripts[w][i].event2.value,
                                min=0,
                                max=255,
                                step=1,
                                style={"width": 50},
                            ),
                        ]),
                    ]) for i in range(len(kh2.placescripts[w]))
                ]),
            ],
                style={
                    "border-collapse": "collapse",
                    "border": "2px solid",
                },
            ),
        ])
    else:
        return html.Div([
            html.H3("Place Scripts:"),
            html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Map", scope="col"),
                        html.Th("Battle", scope="col"),
                        html.Th("Event", scope="col"),
                    ]),
                ]),
                html.Tbody([
                    html.Tr([
                        html.Td([
                            dcc.Input(
                                id={"type": "Place Script Map", "world": w, "index": i},
                                type="number",
                                value=kh2.placescripts[w][i].map.value,
                                min=0,
                                max=255,
                                step=1,
                                style={"width": 50},
                            ),
                        ]),
                        html.Td([
                            dcc.Input(
                                id={"type": "Place Script Battle", "world": w, "index": i},
                                type="number",
                                value=kh2.placescripts[w][i].battle.value,
                                min=0,
                                max=255,
                                step=1,
                                style={"width": 50},
                            ),
                        ]),
                        html.Td([
                            dcc.Input(
                                id={"type": "Place Script Event", "world": w, "index": i},
                                type="number",
                                value=kh2.placescripts[w][i].event.value,
                                min=0,
                                max=255,
                                step=1,
                                style={"width": 50},
                            ),
                        ]),
                    ]) for i in range(len(kh2.placescripts[w]))
                ]),
            ],
                style={
                    "border-collapse": "collapse",
                    "border": "2px solid",
                },
            ),
        ])

def create_worlds():
    kh2 = utils.kh2
    wtabs = dcc.Dropdown(
        options=[{"label": w, "value": w} for w in kh2.world_dict.values()],
        value="Twilight Town",
        id="WorldsTabs",
        style={"margin-bottom": 10, "width": 240},
        searchable=False,
        clearable=False,
    )
    wstabs = dcc.Dropdown(
        options=[
            {"label": "Progress Flags", "value": "Progress Flags"},
            {"label": "Place Scripts", "value": "Place Scripts"},
        ],
        value="Progress Flags",
        id="WorldsSubTabs",
        style={"margin-bottom": 10, "width": 240},
        searchable=False,
        clearable=False,
    )
    return html.Div([
        dcc.Markdown("World:"),
        wtabs,
        dcc.Markdown("Tab:"),
        wstabs,
        html.Div(id="WorldsDiv"),
    ])

@callback(
    Input({"type": "Progress", "world": ALL, "index": ALL}, "value"),
    Input({"type": "Progress", "world": ALL, "index": ALL}, "id"),
)
def progress_callback(values, ids):
    kh2 = utils.kh2
    for v, id in zip(values, ids):
        w = id["world"]
        idx = id["index"]
        if (1 << idx % 16) in v:
            kh2.progress[w][idx//16] |= (1 << idx % 16)
        else:
            kh2.progress[w][idx//16] &= ~(1 << idx % 16)

@callback(
    Output({"type": "100th", "world": MATCH}, "value"),
    Input({"type": "Hours", "world": MATCH}, "value"),
    Input({"type": "Minutes", "world": MATCH}, "value"),
    Input({"type": "Seconds", "world": MATCH}, "value"),
    Input({"type": "Fraction", "world": MATCH}, "value"),
    State({"type": "100th", "world": MATCH}, "id"),
)
def playtime_callback(
    hours,
    minutes,
    seconds,
    fraction,
    idx
):
    kh2 = utils.kh2
    w_idx = idx["world"]
    try:
        kh2.playtimes[w_idx+2] = calculate_playtime(hours, minutes, seconds, fraction)
        return fraction * 100 // 60
    except:
        return 0

@callback(
    Input({"type": "Place Script Map", "world": ALL, "index": ALL}, "value"),
    Input({"type": "Place Script Battle", "world": ALL, "index": ALL}, "value"),
    Input({"type": "Place Script Event", "world": ALL, "index": ALL}, "value"),
    State("WorldsTabs", "value"),
    State({"type": "Place Script Map", "world": ALL, "index": ALL}, "id"),
)
def placescripts_callback(maps, battles, events, w, ids):
    kh2 = utils.kh2
    for map, battle, event, id in zip(maps, battles, events, ids):
        i = id["index"]
        try:
            kh2.placescripts[w][i].map.value = map
            kh2.placescripts[w][i].battle.value = battle
            kh2.placescripts[w][i].event.value = event
        except:
            pass

@callback(
    Input({"type": "Place Script Map 2", "world": ALL, "index": ALL}, "value"),
    Input({"type": "Place Script Battle 2", "world": ALL, "index": ALL}, "value"),
    Input({"type": "Place Script Event 2", "world": ALL, "index": ALL}, "value"),
    State("WorldsTabs", "value"),
    State({"type": "Place Script Map 2", "world": ALL, "index": ALL}, "id"),
)
def placescripts_fm_callback(maps, battles, events, w, ids):
    kh2 = utils.kh2
    for map, battle, event, id in zip(maps, battles, events, ids):
        i = id["index"]
        try:
            kh2.placescripts[w][i].map2.value = map
            kh2.placescripts[w][i].battle2.value = battle
            kh2.placescripts[w][i].event2.value = event
        except:
            pass
