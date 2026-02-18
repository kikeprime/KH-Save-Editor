from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


@callback(
    Output("WorldsDiv", "children"),
    Input("WorldsTabs", "value"),
)
def __create_worlds(w):
    kh1 = utils.kh1
    wm_status = None
    progress = None
    tw2_progress = None
    if w in kh1.landingpoints_dict.keys():
        lp = kh1.landingpoints_dict[w]
        wm_status = html.Div([
            html.Div([
                dcc.Markdown("World Status:"),
                dcc.Dropdown(
                    options=[{"label": k, "value": v} for k, v in kh1.world_status_dict.items()],
                    value=kh1.world_statuses[lp[0]],
                    id={"type": "World Status", "index": lp[0]},
                    style={"margin-bottom": 10, "width": 200},
                    searchable=False,
                    clearable=False,
                ),
                dcc.Markdown("Landing Points:") if len(lp) > 1 else None,
                dcc.Checklist(
                    options=[{"label": lp[i+1], "value": (1 << i)} for i in range(len(lp)-1)],
                    value=[kh1.landingpoints[lp[0]] & (1 << i) for i in range(8)],
                    id={"type": "Landing Points", "index": lp[0]},
                )
            ])
        ])
    if w in kh1.world_progress_dict.keys():
        idx = kh1.world_progress_dict[w]["index"]
        progress = html.Div([
            dcc.Markdown("Progress:"),
            dcc.Dropdown(
                options=[{"label": k, "value": v} for k, v in kh1.world_progress_dict[w].items() if k != "index"],
                value=kh1.world_progresses[idx],
                id={"type": "World Progress", "index": idx},
                style={"margin-bottom": 10, "width": 300},
                searchable=False,
                clearable=False,
            ),
        ])
    if w == "Traverse Town":
        idx = kh1.world_progress_dict[w+" 2"]["index"]
        tw2_progress = html.Div([
            dcc.Markdown("2nd visit progress:"),
            dcc.Dropdown(
                options=[{"label": k, "value": v} for k, v in kh1.world_progress_dict[w+" 2"].items() if k != "index"],
                value=kh1.world_progresses[idx],
                id={"type": "World Progress", "index": idx},
                style={"margin-bottom": 10, "width": 300},
                searchable=False,
                clearable=False,
            ),
        ])
    return html.Div([
        wm_status,
        progress,
        tw2_progress,
    ])

def create_worlds():
    kh1 = utils.kh1
    world_list = list(kh1.world_dict.values())
    world_list += [k for k in kh1.landingpoints_dict.keys() if k not in world_list]
    wtabs = dcc.Dropdown(
        options=[{"label": k, "value": k} for k in world_list],
        value="Dive to the Heart",
        id="WorldsTabs",
        style={"margin-bottom": 10, "width": 200},
        searchable=False,
        clearable=False,
    )
    return html.Div([
        dcc.Markdown("World:"),
        wtabs,
        html.Div(id="WorldsDiv"),
    ])

@callback(
    Input({"type": "World Progress", "index": ALL}, "value"),
    Input({"type": "World Progress", "index": ALL}, "id"),
)
def world_progresses_callback(progresses, ids):
    kh1 = utils.kh1
    for progress, id in zip(progresses, ids):
        idx = id["index"]
        if progress is not None:
            kh1.world_progresses[idx] = progress

@callback(
    Input({"type": "World Status", "index": ALL}, "value"),
    Input({"type": "Landing Points", "index": ALL}, "value"),
    Input({"type": "World Status", "index": ALL}, "id"),
)
def worlds_callback(statuses, lps, ids):
    kh1 = utils.kh1
    for i in range(len(statuses)):
        idx = ids[i]["index"]
        kh1.world_statuses[idx] = statuses[i]
        kh1.landingpoints[idx] = sum(lps[i])
