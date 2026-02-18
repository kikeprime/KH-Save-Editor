from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


@callback(
    Output("MiscDiv", "children"),
    Input("MiscTabs", "value"),
    Input("Encoding", "value"),
)
def __create_misc(tab, encoding):
    kh1 = utils.kh1
    if tab == "Misc Stuff":
        return __create_misc_stuff(encoding)

def __create_misc_stuff(encoding):
    kh1 = utils.kh1
    codec = "kh1us" if encoding == "International" else "kh1jp"
    return html.Div([
        html.Div([
            html.Label("The raft's name:"),
            dcc.Input(
                id="Raft",
                type="text",
                value=kh1.raft.decode(codec),
                style={"width": 100, "margin": 10},
            ),
            html.Button(
                "Validate", id="RaftValid", n_clicks=0, style={"width": 80},
            ),
        ]),
        html.Div([
            dcc.Markdown("Backed up keychain:"),
            dcc.Dropdown(
                options=[{"label": k, "value": v} for k, v in kh1.weapon_dict.items()],
                value=kh1.weapon_backup.value,
                id="WeaponBackup",
                style={"width": 200},
                searchable=False,
                clearable=False,
            ),
        ]),
        html.Div([
            dcc.Checklist(
                options=[{"label": "Xemnas beaten", "value": 1}],
                value=[kh1.xemnas.value],
                id="Xemnas",
                style={"margin-top": 20},
            ),
        ]) if kh1.fm else None,
    ])

def create_misc():
    kh1 = utils.kh1
    mtabs = dcc.Tabs(id="MiscTabs", value="Misc Stuff")
    mtabs.children = [
        dcc.Tab(label="Misc Stuff", value="Misc Stuff"),
    ]
    return html.Div([
        mtabs,
        html.Div(id="MiscDiv", style={"margin-top": 20}),
    ])

@callback(
    Output("Raft", "value"),
    Input("RaftValid", "n_clicks"),
    State("Raft", "value"),
    State("Encoding", "value"),
)
def raft_callback(n_clicks, raft, encoding):
    kh1 = utils.kh1
    codec = "kh1us" if encoding == "International" else "kh1jp"
    if n_clicks > 0:
        new_raft = bytearray(raft, codec)
        l = len(new_raft)
        kh1.raft[:min(l, 10)] = new_raft[:min(l, 10)]
        return kh1.raft.decode(codec)
    return raft

@callback(
    Input("WeaponBackup", "value"),
)
def misc_callback(weapon_backup):
    kh1 = utils.kh1
    kh1.weapon_backup.value = weapon_backup

@callback(
    Input("Xemnas", "value"),
)
def misc_callback(xemnas):
    kh1 = utils.kh1
    kh1.xemnas.value = 1 if 1 in xemnas else 0
