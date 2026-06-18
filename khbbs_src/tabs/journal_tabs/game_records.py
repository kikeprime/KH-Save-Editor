from dash import Dash, html, dcc, callback, Input, Output, State, ALL, MATCH
import khbbs_src.khbbs_utils as utils


def create_game_records():
    khbbs = utils.khbbs
    return html.Div([
        dcc.Markdown("Tab:"),
        dcc.Dropdown(
            options=[
                {"label": "Arena Missions", "value": "Arena Missions"},
                {"label": "Mini-games", "value": "Mini-games"},
                {"label": "Hit Counts", "value": "Hit Counts"},
                {"label": "Unversed Missions", "value": "Unversed Missions"},
            ],
            value="Arena Missions",
            id="GameRecordsTabs",
            style={"width": 200},
            searchable=False,
            clearable=False,
        ),
        html.Div(id="GameRecordsDiv"),
    ])

@callback(
    Output("GameRecordsDiv", "children"),
    Input("GameRecordsTabs", "value"),
)
def __create_game_records(tab):
    if tab == "Arena Missions":
        return create_arena_missions()

def create_arena_missions():
    khbbs = utils.khbbs
    return html.Div([
        html.Div([
            html.H3("Arena Missions"),
            html.Div([
                dcc.Checklist(
                    options=[
                        {"label": k, "value": (1 << v % 16)}
                    ],
                    value=[khbbs.arena_missions[v//16] & (1 << v % 16)],
                    id={"type": "Arena Mission", "index": v},
                    style={"margin-top": 10, "whiteSpace": "pre-wrap"},
                ) for k, v in khbbs.arena_missions_dict.items()
            ]),
        ]),
        html.Div([
            html.H3("Command Board Counter"),
            dcc.Input(
                id="Command Board Counter",
                type="number",
                value=khbbs.commandboard_counter.value,
                min=0,
                max=0xFFFF,
                step=1,
                style={"width": 60},
            ),
        ]) if khbbs.fm else None,
    ])

@callback(
    Input({"type": "Arena Mission", "index": ALL}, "value"),
    State({"type": "Arena Mission", "index": ALL}, "id"),
)
def arena_missions_callback(
    arena_missions,
    ids,
):
    khbbs = utils.khbbs
    for arena_mission, id in zip(arena_missions, ids):
        v = id["index"]
        if (1 << v % 16) in arena_mission:
            khbbs.arena_missions[v//16] |= (1 << v % 16)
        else:
            khbbs.arena_missions[v//16] &= ~(1 << v % 16)

@callback(
    Input("Command Board Counter", "value"),
)
def commandboard_counter_callback(
    commandboard_counter,
):
    try:
        khbbs.commandboard_counter.value = commandboard_counter
    except:
        pass
