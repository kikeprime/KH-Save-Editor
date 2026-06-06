from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import khbbs_src.khbbs_utils as utils


def create_commands():
    khbbs = utils.khbbs
    return html.Div([
        dcc.Markdown("Tab:"),
        dcc.Dropdown(
            options=[
                {"label": "Command List", "value": "Command List"},
                # {"label": "Decks", "value": "Decks"},
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
