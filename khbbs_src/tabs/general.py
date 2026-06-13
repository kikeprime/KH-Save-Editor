from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import khbbs_src.khbbs_utils as utils


def get_playtime(playtime):
    hours = playtime // 3600
    minutes = (playtime % 3600) // 60
    seconds = (playtime % 3600) % 60
    return hours, minutes, seconds

def calculate_playtime(hours, minutes, seconds):
    return hours * 3600 + minutes * 60 + seconds

def create_general():
    khbbs = utils.khbbs
    hours, minutes, seconds = get_playtime(khbbs.playtime.value)
    playtime = html.Div([
        dcc.Input(
            id="Hours",
            type="number",
            value=hours,
            min=0,
            max=399,
            step=1,
            style={"width": 50},
        ),
        html.Label(" : "),
        dcc.Input(
            id="Minutes",
            type="number",
            value=minutes,
            min=0,
            max=59,
            step=1,
            style={"width": 50},
        ),
        html.Label(" : "),
        dcc.Input(
            id="Seconds",
            type="number",
            value=seconds,
            min=0,
            max=59,
            step=1,
            style={"width": 50},
        ),
    ])
    character_type = dcc.Dropdown(
        options=[
            {"label": k, "value": v} for k, v in khbbs.character_dict.items()
        ],
        value=khbbs.character_type.value,
        id="CharacterType",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    world = dcc.Dropdown(
        options=[
            {"label": v, "value": k} for k, v in khbbs.world_dict.items()
        ],
        value=khbbs.world.value,
        id="World",
        searchable=False,
        clearable=False,
        style={"width": 250},
    )
    room = dcc.Input(
        id="Room",
        type="number",
        value=khbbs.room.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    flag = dcc.Input(
        id="Flag",
        type="number",
        value=khbbs.flag.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    munny = dcc.Input(
        id="Munny",
        type="number",
        value=khbbs.character.munny,
        min=0,
        max=0xFFFFFFFF,
        step=1,
        style={"width": 100},
    )
    return html.Div([
        html.Div([dcc.Markdown("Playtime:"), playtime]),
        html.Div([dcc.Markdown("Character:"), character_type]),
        html.Div([dcc.Markdown("World:"), world]),
        html.Div([
            html.Div([dcc.Markdown("Room:"), room]),
            html.Div([dcc.Markdown("Flag:"), flag]),
        ],
            style={"display": "flex", "gap": 20},
        ),
        html.Div([dcc.Markdown("Munny:"), munny]),
    ])

@callback(
    Input("Hours", "value"),
    Input("Minutes", "value"),
    Input("Seconds", "value"),
)
def playtime_callback(
    hours,
    minutes,
    seconds
):
    khbbs = utils.khbbs
    try:
        khbbs.playtime.value = calculate_playtime(hours, minutes, seconds)
    except:
        pass

@callback(
    Output("CharacterTab", "label"),
    Input("CharacterType", "value"),
    Input("World", "value"),
    Input("Room", "value"),
    Input("Flag", "value"),
    Input("Munny", "value"),
)
def general_callbacks(
    character_type,
    world,
    room,
    flag,
    munny,
):
    khbbs = utils.khbbs
    try:
        khbbs.character_type.value = character_type
        khbbs.world.value = world
        khbbs.room.value = room
        khbbs.flag.value = flag
        khbbs.character.munny = munny
        return khbbs.name
    except:
        return "Character"
