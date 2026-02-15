from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


def get_playtime(playtime):
    time = playtime.value // 60
    hours = time // 3600
    minutes = (time % 3600) // 60
    seconds = (time % 3600) % 60
    fraction = playtime.value % 60
    return hours, minutes, seconds, fraction

def calculate_playtime(hours, minutes, seconds, fraction):
    return (hours * 3600 + minutes * 60 + seconds) * 60 + fraction

def create_general():
    kh1 = utils.kh1
    if kh1.sysdata is not None:
        hours, minutes, seconds, fraction = get_playtime(kh1.playtime)
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
            html.Label(" : "),
            dcc.Input(
                id="Fraction",
                type="number",
                value=fraction,
                min=0,
                max=59,
                step=1,
                style={"width": 50},
            ),
            html.Label(" 100th: "),
            dcc.Input(
                id="100th",
                type="number",
                value=fraction * 100 // 60,
                min=0,
                max=99,
                step=1,
                disabled=True,
                style={"width": 30},
            ),
        ])
    curve = dcc.Dropdown(
        options=[
            {"label": "Dawn", "value": 0},
            {"label": "Midday", "value": 1},
            {"label": "Dusk", "value": 2},
        ],
        value=kh1.curve.value,
        id="Curve",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    path = dcc.Dropdown(
        options=[
            {"label": "Warrior", "value": 0},
            {"label": "Guardian", "value": 1},
            {"label": "Mystic", "value": 2},
        ],
        value=kh1.path.value,
        id="Path",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    world = dcc.Dropdown(
        options=[
            {"label": v, "value": k} for k, v in kh1.world_dict.items()
        ],
        value=kh1.world.value,
        id="World",
        searchable=False,
        clearable=False,
        style={"display": "inline-block", "width": 200},
    )
    room = dcc.Input(
        id="Room",
        type="number",
        value=kh1.room.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    flag = dcc.Input(
        id="Flag",
        type="number",
        value=kh1.flag.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    leader = dcc.Dropdown(
        options=[
            {"label": k, "value": v} for k, v in kh1.character_dict.items()
        ],
        value=kh1.party[0],
        id="Leader",
        disabled=True,
        searchable=False,
        clearable=False,
        style={"display": "inline-block", "width": 200},
    )
    friend1 = dcc.Dropdown(
        options=[
            {"label": k, "value": v} for k, v in kh1.character_dict.items()
        ],
        value=kh1.party[1],
        id="Friend1",
        searchable=False,
        clearable=False,
        style={"display": "inline-block", "width": 200},
    )
    friend2 = dcc.Dropdown(
        options=[
            {"label": k, "value": v} for k, v in kh1.character_dict.items()
        ],
        value=kh1.party[2],
        id="Friend2",
        searchable=False,
        clearable=False,
        style={"display": "inline-block", "width": 200},
    )
    friend3 = dcc.Dropdown(
        options=[
            {"label": k, "value": v} for k, v in kh1.character_dict.items()
        ],
        value=kh1.party[3],
        id="Friend3",
        searchable=False,
        clearable=False,
        style={"display": "inline-block", "width": 200},
    )
    munny = dcc.Input(
        id="Munny",
        type="number",
        value=kh1.munny.value,
        min=0,
        max=0xFFFFFFFF,
        step=1,
        style={"width": 60},
    )
    return html.Div([
        html.Div([dcc.Markdown("Playtime:"), playtime]) if kh1.sysdata is not None else None,
        html.Div([dcc.Markdown("Leveling curve:"), curve]),
        html.Div([dcc.Markdown("Path:"), path]),
        html.Div([dcc.Markdown("World:"), world]),
        html.Div([
            html.Div([dcc.Markdown("Room:"), room]),
            html.Div([dcc.Markdown("Flag:"), flag]),
        ],
            style={"display": "flex", "gap": 20},
        ),
        html.Div([dcc.Markdown("Party:"), leader, friend1, friend2, friend3]),
        html.Div([dcc.Markdown("Munny:"), munny]),
    ])

@callback(
    Output("100th", "value"),
    Input("Hours", "value"),
    Input("Minutes", "value"),
    Input("Seconds", "value"),
    Input("Fraction", "value"),
)
def playtime_callback(
    hours,
    minutes,
    seconds,
    fraction
):
    kh1 = utils.kh1
    try:
        kh1.playtime.value = calculate_playtime(hours, minutes, seconds, fraction)
        return fraction * 100 // 60
    except:
        return 0

@callback(
    Input("Curve", "value"),
    Input("Path", "value"),
    Input("World", "value"),
    Input("Room", "value"),
    Input("Flag", "value"),
    Input("Leader", "value"),
    Input("Friend1", "value"),
    Input("Friend2", "value"),
    Input("Friend3", "value"),
    Input("Munny", "value"),
)
def general_callbacks(
    curve,
    path,
    world,
    room,
    flag,
    leader,
    friend1,
    friend2,
    friend3,
    munny
):
    kh1 = utils.kh1
    try:
        kh1.curve.value = curve
        kh1.path.value = path
        kh1.world.value = world
        kh1.room.value = room
        kh1.flag.value = flag
        kh1.party[0] = leader
        kh1.party[1] = friend1
        kh1.party[2] = friend2
        kh1.party[3] = friend3
        kh1.munny.value = munny
    except:
        pass
