from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh2_src.kh2_utils as utils


@callback(
    Output("WorldsDiv", "children"),
    Input("WorldsTabs", "value"),
)
def __create_worlds(w):
    kh2 = utils.kh2
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
