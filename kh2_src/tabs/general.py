from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh2_src.kh2_utils as utils


def get_playtime(playtime):
    time = playtime // 60
    hours = time // 3600
    minutes = (time % 3600) // 60
    seconds = (time % 3600) % 60
    fraction = playtime % 60
    return hours, minutes, seconds, fraction

def calculate_playtime(hours, minutes, seconds, fraction):
    return (hours * 3600 + minutes * 60 + seconds) * 60 + fraction

def create_general():
    kh2 = utils.kh2
    hours, minutes, seconds, fraction = get_playtime(kh2.playtimes[0])
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
        html.Label(" : "),
        dcc.Input(
            id="100th",
            type="number",
            value=fraction * 100 // 60,
            min=0,
            max=99,
            step=1,
            disabled=True,
            style={"width": 50},
        ),
    ])
    path = dcc.Dropdown(
        options=[
            {"label": "Warrior", "value": 0},
            {"label": "Guardian", "value": 1},
            {"label": "Mystic", "value": 2},
        ],
        value=kh2.path.value,
        id="Path",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    world = dcc.Dropdown(
        options=[
            {"label": v, "value": k} for k, v in kh2.world_dict.items()
        ],
        value=kh2.world.value,
        id="World",
        searchable=False,
        clearable=False,
        style={"width": 250},
    )
    room = dcc.Input(
        id="Room",
        type="number",
        value=kh2.room.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    flag = dcc.Input(
        id="Flag",
        type="number",
        value=kh2.flag.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    munny = dcc.Input(
        id="Munny",
        type="number",
        value=kh2.munny.value,
        min=0,
        max=0xFFFFFFFF,
        step=1,
        style={"width": 100},
    )
    exp = dcc.Input(
        id="EXP",
        type="number",
        value=kh2.exp.value,
        min=0,
        max=0xFFFFFFFF,
        step=1,
        style={"width": 100},
    )
    form_dict = kh2.form_dict if kh2.version < 2 else kh2.form_fm_dict
    form = dcc.Dropdown(
        options=[
            {"label": k, "value": v} for k, v in form_dict.items()
        ],
        value=kh2.current_form.value,
        id="CurrentForm",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    summon = dcc.Dropdown(
        options=[
            {"label": k, "value": v} for k, v in kh2.summon_dict.items()
        ],
        value=kh2.current_summon.value,
        id="CurrentSummon",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    return html.Div([
        html.Div([dcc.Markdown("Playtime:"), playtime]),
        html.Div([dcc.Markdown("Path:"), path]),
        html.Div([dcc.Markdown("World:"), world]),
        html.Div([
            html.Div([dcc.Markdown("Room:"), room]),
            html.Div([dcc.Markdown("Flag:"), flag]),
        ],
            style={"display": "flex", "gap": 20},
        ),
        html.Div([dcc.Markdown("Munny:"), munny]),
        html.Div([dcc.Markdown("EXP:"), exp]),
        html.Div([dcc.Markdown("Current Form:"), form]),
        html.Div([dcc.Markdown("Current Summon:"), summon]),
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
    kh2 = utils.kh2
    try:
        kh2.playtimes[0] = calculate_playtime(hours, minutes, seconds, fraction)
        return fraction * 100 // 60
    except:
        return 0

@callback(
    Input("Path", "value"),
    Input("World", "value"),
    Input("Room", "value"),
    Input("Flag", "value"),
    Input("Munny", "value"),
    Input("EXP", "value"),
    Input("CurrentForm", "value"),
    Input("CurrentSummon", "value"),
)
def general_callbacks(
    path,
    world,
    room,
    flag,
    munny,
    exp,
    current_form,
    current_summon,
):
    kh2 = utils.kh2
    try:
        kh2.path.value = path
        kh2.world.value = world
        kh2.room.value = room
        kh2.flag.value = flag
        kh2.munny.value = munny
        kh2.exp.value = exp
        kh2.current_form.value = current_form
        kh2.current_summon.value = current_summon
    except:
        pass
