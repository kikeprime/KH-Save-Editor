from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import khbbs_src.khbbs_utils as utils


def create_abilities():
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
                    inputClassName="kh2-ability",
                    labelStyle={"display": "flex", "align-items": "center"},
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
