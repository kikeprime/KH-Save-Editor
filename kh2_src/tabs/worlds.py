from dash import Dash, html, dcc, callback, Input, Output, State, ALL, MATCH
import kh2_src.kh2_utils as utils
from .general import get_playtime, calculate_playtime


@callback(
    Output("WorldsDiv", "children"),
    Input("WorldsTabs", "value"),
)
def __create_worlds(w):
    kh2 = utils.kh2
    w_idx = {w: idx for idx, w in kh2.world_dict.items()}[w]
    hours, minutes, seconds, fraction = get_playtime(kh2.playtimes[w_idx+2])
    playtime = html.Div([
        dcc.Markdown("Playtime:"),
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
    return html.Div([
        playtime,
        progress,
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
    return html.Div([
        dcc.Markdown("World:"),
        wtabs,
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
