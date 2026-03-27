from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh3_src.kh3_utils as utils


def get_playtime(playtime):
    hours = playtime // 3600
    minutes = (playtime % 3600) // 60
    seconds = (playtime % 3600) % 60
    return hours, minutes, seconds

def calculate_playtime(hours, minutes, seconds):
    return hours * 3600 + minutes * 60 + seconds

def create_general():
    kh3 = utils.kh3
    hours, minutes, seconds = get_playtime(kh3.playtime.value)
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
    desire = dcc.Dropdown(
        options=[
            {"label": "Vitality", "value": 0},
            {"label": "Wisdom", "value": 1},
            {"label": "Balance", "value": 2},
        ],
        value=kh3.desire.value,
        id="Desire",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    power = dcc.Dropdown(
        options=[
            {"label": "Warrior", "value": 0},
            {"label": "Mystic", "value": 1},
            {"label": "Guardian", "value": 2},
        ],
        value=kh3.power.value,
        id="Power",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    """
    world = dcc.Dropdown(
        options=[
            {"label": v, "value": k} for k, v in kh3.world_dict.items()
        ],
        value=kh3.world.value,
        id="World",
        searchable=False,
        clearable=False,
        style={"width": 250},
    )
    room = dcc.Input(
        id="Room",
        type="number",
        value=kh3.room.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    flag = dcc.Input(
        id="Flag",
        type="number",
        value=kh3.flag.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )"""
    leader = dcc.Dropdown(
        options=[
            {"label": k, "value": v} for k, v in kh3.character_dict.items()
        ],
        value=kh3.party[0],
        id="Leader",
        disabled=False,
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    friend1 = dcc.Dropdown(
        options=[
            {"label": k, "value": v} for k, v in kh3.character_dict.items()
        ],
        value=kh3.party[1],
        id="Friend1",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    friend2 = dcc.Dropdown(
        options=[
            {"label": k, "value": v} for k, v in kh3.character_dict.items()
        ],
        value=kh3.party[2],
        id="Friend2",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    friend3 = dcc.Dropdown(
        options=[
            {"label": k, "value": v} for k, v in kh3.character_dict.items()
        ],
        value=kh3.party[3],
        id="Friend3",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    friend4 = dcc.Dropdown(
        options=[
            {"label": k, "value": v} for k, v in kh3.character_dict.items()
        ],
        value=kh3.party[4],
        id="Friend4",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    munny = dcc.Input(
        id="Munny",
        type="number",
        value=kh3.munny.value,
        min=0,
        max=0xFFFFFFFF,
        step=1,
        style={"width": 100},
    )
    exp = dcc.Input(
        id="EXP",
        type="number",
        value=kh3.exp.value,
        min=0,
        max=0xFFFFFFFF,
        step=1,
        style={"width": 100},
    )
    difficulty = dcc.Dropdown(
        options=[
            {"label": "Beginner", "value": 0},
            {"label": "Standard", "value": 1},
            {"label": "Proud", "value": 2},
            {"label": "Critical", "value": 3},
        ],
        value=kh3.difficulty.value,
        id="Difficulty",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    return html.Div([
        html.Div([dcc.Markdown("Playtime:"), playtime]),
        html.Div([dcc.Markdown("Desire:"), desire]),
        html.Div([dcc.Markdown("Power:"), power]),
        #html.Div([dcc.Markdown("World:"), world]),
        #html.Div([
        #    html.Div([dcc.Markdown("Room:"), room]),
        #    html.Div([dcc.Markdown("Flag:"), flag]),
        #],
        #    style={"display": "flex", "gap": 20},
        #),
        html.Div([dcc.Markdown("Party:"), leader, friend1, friend2, friend3, friend4]),
        html.Div([dcc.Markdown("Munny:"), munny]),
        html.Div([dcc.Markdown("EXP:"), exp]),
        html.Div([dcc.Markdown("Difficulty:"), difficulty]),
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
    kh3 = utils.kh3
    try:
        kh3.playtime.value = calculate_playtime(hours, minutes, seconds)
    except:
        pass

@callback(
    Input("Desire", "value"),
    Input("Power", "value"),
    #Input("World", "value"),
    #Input("Room", "value"),
    #Input("Flag", "value"),
    Input("Leader", "value"),
    Input("Friend1", "value"),
    Input("Friend2", "value"),
    Input("Friend3", "value"),
    Input("Friend4", "value"),
    Input("Munny", "value"),
    Input("EXP", "value"),
    Input("Difficulty", "value"),
)
def general_callback(
    desire,
    power,
    #world,
    #room,
    #flag,
    leader,
    friend1,
    friend2,
    friend3,
    friend4,
    munny,
    exp,
    difficulty,
):
    kh3 = utils.kh3
    try:
        kh3.desire.value = desire
        kh3.power.value = power
        #kh3.world.value = world
        #kh3.room.value = room
        #kh3.flag.value = flag
        kh3.party[0] = leader
        kh3.party[1] = friend1
        kh3.party[2] = friend2
        kh3.party[3] = friend3
        kh3.party[4] = friend4
        kh3.munny.value = munny
        kh3.exp.value = exp
        kh3.difficulty.value = difficulty
    except:
        pass
