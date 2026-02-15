from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


def __create_worlds():
    kh1 = utils.kh1
    return html.Div([
        html.Div([
            html.H3(w),
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
        ]) for w, lp in kh1.landingpoints_dict.items()
    ])

@callback(
    Output("MiscDiv", "children"),
    Input("MiscTabs", "value"),
    Input("Encoding", "value"),
)
def __create_misc(tab, encoding):
    kh1 = utils.kh1
    if tab == "Worlds":
        return __create_worlds()

def create_misc():
    kh1 = utils.kh1
    mtabs = dcc.Tabs(id="MiscTabs", value="Worlds")
    mtabs.children = [
        dcc.Tab(label="Worlds", value="Worlds"),
    ]
    return html.Div([
        mtabs,
        html.Div(id="MiscDiv"),
    ])

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
