from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import khbbs_src.khbbs_utils as utils


def create_commands():
    khbbs = utils.khbbs
    return html.Div([
        dcc.Markdown("Tab:"),
        dcc.Dropdown(
            options=[
                # {"label": "Decks", "value": "Decks"},
                {"label": "Command List", "value": "Command List"},
                {"label": "Abilities", "value": "Abilities"},
                {"label": "D-Links", "value": "D-Links"},
            ],
            value="Command List",
            id="CommandsTabs",
            style={"width": 200},
            searchable=False,
            clearable=False,
        ),
        html.Div(id="CommandsDiv"),
    ])

@callback(
    Output("CommandsDiv", "children"),
    Input("CommandsTabs", "value"),
)
def __create_commands(tab):
    khbbs = utils.khbbs
    if tab == "Command List":
        return __create_command_list()
    if tab == "Abilities":
        return __create_abilities()
    if tab == "D-Links":
        return __create_dlinks()

def __create_command_list():
    khbbs = utils.khbbs
    return html.Div([
        html.Div([
            dcc.Markdown("Command:"),
            dcc.Dropdown(
                options=[
                    {"label": f"Command {i+1}", "value": i} for i\
                    in range(len(khbbs.commands))
                ],
                value=0,
                id="CommandListTab",
                style={"width": 200},
                searchable=False,
                clearable=False,
            ),
        ]),
        html.Div(id="CommandListDiv"),
    ])

@callback(
    Output("CommandListDiv", "children"),
    Input("CommandListTab", "value"),
)
def __create_command(idx):
    khbbs = utils.khbbs
    command = khbbs.commands[idx]
    return html.Div([
        dcc.Markdown("Type:"),
        dcc.Dropdown(
            options=[
                {"label": k, "value": v} for k, v\
                in khbbs.command_dict.items()
            ],
            value=command.id.value,
            id={"type": "Command Type", "index": command.idx},
            style={"width": 300},
            searchable=False,
            clearable=False,
        ),
        dcc.Markdown("Ability:"),
        dcc.Dropdown(
            options=[
                {"label": k, "value": v} for k, v\
                in khbbs.ability_dict.items()
            ],
            value=command.ability.value,
            id={"type": "Command Ability", "index": command.idx},
            style={"width": 200},
            searchable=False,
            clearable=False,
        ),
        dcc.Markdown("Level:"),
        dcc.Input(
            id={"type": "Command Level", "index": command.idx},
            type="number",
            value=command.level.value,
            min=0,
            max=99,
            step=1,
            style={"width": 50},
        ),
        dcc.Markdown("CP:"),
        dcc.Input(
            id={"type": "Command CP", "index": command.idx},
            type="number",
            value=command.cp.value,
            min=0,
            max=0xFFFF,
            step=1,
            style={"width": 50},
        ),
        dcc.Markdown("State:"),
        dcc.Input(
            id={"type": "Command State", "index": command.idx},
            type="number",
            value=command.state.value,
            min=0,
            max=0xFFFF,
            step=1,
            style={"width": 50},
        ),
    ])

def __create_abilities():
    khbbs = utils.khbbs
    return html.Div([
        html.Div([
            html.H3(name),
            html.Div([
                html.Label("Installations Active: "),
                dcc.Input(
                    id={"type": "Ability Num On", "index": name},
                    type="number",
                    value=ability.num_on,
                    min=0,
                    max=5,
                    step=1,
                    disabled=True,
                    style={"width": 50},
                ),
            ],
                style={"margin-bottom": 10},
            ),
            html.Div([
                html.Label("Installations Unlocked: "),
                dcc.Input(
                    id={"type": "Ability Num Unlocked", "index": name},
                    type="number",
                    value=ability.num_unlocked,
                    min=0,
                    max=5,
                    step=1,
                    style={"width": 50},
                ),
            ],
                style={"margin-bottom": 10},
            ),
            html.Div([
                dcc.Checklist(
                    options=[
                        {"label": f"Installation {i}", "value": i} for i in range(1, 6)
                    ],
                    value=[i for i in range(1, 6) if ability.active(i)],
                    id={"type": "Ability Active", "index": name},
                ),
            ]),
            html.Div([
                dcc.Markdown("Unlocked & Unread:"),
                dcc.Dropdown(
                    options=[
                        {"label": "True", "value": True},
                        {"label": "False", "value": False},
                    ],
                    value=ability.unread,
                    id={"type": "Ability Unread", "index": name},
                    style={"width": 100},
                    searchable=False,
                    clearable=False,
                ),
            ]),
            html.Div([
                dcc.Markdown("Unlocked & Read:"),
                dcc.Dropdown(
                    options=[
                        {"label": "True", "value": True},
                        {"label": "False", "value": False},
                    ],
                    value=ability.read,
                    id={"type": "Ability Read", "index": name},
                    style={"width": 100},
                    searchable=False,
                    clearable=False,
                ),
            ]),
            html.Div([
                dcc.Markdown("Display Message:"),
                dcc.Dropdown(
                    options=[
                        {"label": "True", "value": True},
                        {"label": "False", "value": False},
                    ],
                    value=ability.mastered_message,
                    id={"type": "Ability Mastered Message", "index": name},
                    style={"width": 100},
                    searchable=False,
                    clearable=False,
                ),
            ]),
        ]) for name, ability in khbbs.abilities.items()
    ])

def __create_dlinks():
    khbbs = utils.khbbs
    return html.Div([
        html.Div([
            html.H3(f"D-Link {dlink.idx+1}"),
            html.Div([
                dcc.Markdown("D-Link:"),
                dcc.Dropdown(
                    options=[
                        {"label": k, "value": v} for k, v\
                        in khbbs.dlink_dict.items()
                    ],
                    value=dlink.id.value,
                    id={"type": "D-Link ID", "index": dlink.idx},
                    style={"width": 200},
                    searchable=False,
                    clearable=False,
                ),
            ]),
            html.Div([
                dcc.Markdown("Equipped:"),
                dcc.Dropdown(
                    options=[
                        {"label": "On", "value": True},
                        {"label": "Off", "value": False},
                    ],
                    value=dlink.on,
                    id={"type": "D-Link On", "index": dlink.idx},
                    style={"width": 200},
                    searchable=False,
                    clearable=False,
                ),
            ]),
            html.Div([
                dcc.Markdown("Ability 1:"),
                dcc.Dropdown(
                    options=[
                        {"label": "Got", "value": True},
                        {"label": "Not Got", "value": False},
                    ],
                    value=dlink.ability_1,
                    id={"type": "D-Link Ability 1", "index": dlink.idx},
                    style={"width": 200},
                    searchable=False,
                    clearable=False,
                ),
            ]),
            html.Div([
                dcc.Markdown("Ability 2:"),
                dcc.Dropdown(
                    options=[
                        {"label": "Got", "value": True},
                        {"label": "Not Got", "value": False},
                    ],
                    value=dlink.ability_2,
                    id={"type": "D-Link Ability 2", "index": dlink.idx},
                    style={"width": 200},
                    searchable=False,
                    clearable=False,
                ),
            ]),
        ]) for dlink in khbbs.dlinks
    ])

@callback(
    Input({"type": "Command Type", "index": ALL}, "value"),
    Input({"type": "Command Ability", "index": ALL}, "value"),
    Input({"type": "Command Level", "index": ALL}, "value"),
    Input({"type": "Command CP", "index": ALL}, "value"),
    Input({"type": "Command State", "index": ALL}, "value"),
    State({"type": "Command Type", "index": ALL}, "id"),
)
def command_list_callback(id, ability, level, cp, state, idx):
    khbbs = utils.khbbs
    idx = idx[0]["index"]
    khbbs.commands[idx].id.value = id[0]
    khbbs.commands[idx].ability.value = ability[0]
    try:
        khbbs.commands[idx].level.value = level[0]
        khbbs.commands[idx].cp.value = cp[0]
        khbbs.commands[idx].state.value = state[0]
    except:
        pass

@callback(
    Output({"type": "Ability Num On", "index": ALL}, "value"),
    Input({"type": "Ability Num Unlocked", "index": ALL}, "value"),
    Input({"type": "Ability Active", "index": ALL}, "value"),
    Input({"type": "Ability Unread", "index": ALL}, "value"),
    Input({"type": "Ability Read", "index": ALL}, "value"),
    Input({"type": "Ability Mastered Message", "index": ALL}, "value"),
    State({"type": "Ability Num Unlocked", "index": ALL}, "id"),
)
def ability_callback(
    num_unlockeds,
    actives,
    unreads,
    reads,
    mastered_messages,
    ids,
):
    khbbs = utils.khbbs
    num_on = []
    for num_unlocked, active, unread, read, mastered_message, id in zip(num_unlockeds, actives, unreads, reads, mastered_messages, ids):
        ability = khbbs.abilities[id["index"]]
        ability.unread = unread
        ability.read = read
        ability.mastered_message = mastered_message
        for i in range(1, 6):
            if i in active:
                ability.set_active(i, True)
            else:
                ability.set_active(i, False)
        try:
            ability.num_unlocked = num_unlocked
            ability.num_on = min(num_unlocked, len(active))
        except:
            pass
        num_on.append(ability.num_on)
    return num_on

@callback(
    Input({"type": "D-Link ID", "index": ALL}, "value"),
    Input({"type": "D-Link On", "index": ALL}, "value"),
    Input({"type": "D-Link Ability 1", "index": ALL}, "value"),
    Input({"type": "D-Link Ability 2", "index": ALL}, "value"),
    State({"type": "D-Link ID", "index": ALL}, "id"),
)
def dlink_callback(
    ids,
    ons,
    ability_1s,
    ability_2s,
    idxs,
):
    khbbs = utils.khbbs
    for id, on, ability_1, ability_2, idx in zip(ids, ons, ability_1s, ability_2s, idxs):
        dlink = khbbs.dlinks[idx["index"]]
        dlink.id.value = id
        dlink.on = on
        dlink.ability_1 = ability_1
        dlink.ability_2 = ability_2
