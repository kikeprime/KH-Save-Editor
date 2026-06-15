from ctypes import *
from dash import Dash, html, dcc, callback, Input, Output, State, ALL, MATCH
import khbbs_src.khbbs_utils as utils


def create_decks():
    khbbs = utils.khbbs
    return html.Div([
        html.Div([
                dcc.Markdown("Equipped Deck:"),
                    dcc.Dropdown(
                        options=[
                            {"label": f"Deck {i+1}", "value": i} for i\
                            in range(3)
                        ],
                        value=khbbs.deck.value,
                        id="Deck",
                        style={"width": 200},
                        searchable=False,
                        clearable=False,
                    ),
            ]),
        html.Div([
            html.Div([
                html.H3(f"Deck {deck.idx+1}"),
                html.Div([
                    dcc.Markdown("Name:"),
                    dcc.Input(
                        id={"type": "Deck Name", "index": deck.idx},
                        type="text",
                        value=bytearray(deck.name).decode("Shift-JIS").strip("\0"),
                        style={"width": 200},
                    ),
                ]),
                html.H4("Battle Commands:"),
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            options=[
                                {"label": "Empty", "value": -1},
                            ] + [
                                {"label": f"Command {i+1}", "value": i} for i\
                                in range(len(khbbs.commands))
                            ],
                            value=deck.battle_commands[i].id,
                            id={"type": "Battle Command", "deck": deck.idx, "index": i},
                            style={"width": 200},
                            searchable=False,
                            clearable=False,
                        ),
                        dcc.Markdown(
                            str(khbbs.commands[deck.battle_commands[i].id]),
                            id={"type": "Battle Command text", "deck": deck.idx, "index": i},
                            style={"whiteSpace": "pre-wrap"},
                        ),
                    ]) for i in range(8)
                ]),
                html.H4("Action Commands:"),
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            options=[
                                {"label": "Empty", "value": -1},
                            ] + [
                                {"label": f"Command {i+1}", "value": i} for i\
                                in range(len(khbbs.commands))
                            ],
                            value=deck.action_commands[i].id,
                            id={"type": "Action Command", "deck": deck.idx, "index": i},
                            style={"width": 200},
                            searchable=False,
                            clearable=False,
                        ),
                        dcc.Markdown(
                            str(khbbs.commands[deck.action_commands[i].id]),
                            id={"type": "Action Command text", "deck": deck.idx, "index": i},
                            style={"whiteSpace": "pre-wrap"},
                        ),
                    ]) for i in range(10)
                ]),
                html.H4("Shotlock:"),
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            options=[
                                {"label": "Empty", "value": -1},
                            ] + [
                                {"label": f"Command {i+1}", "value": i} for i\
                                in range(len(khbbs.commands))
                            ],
                            value=deck.shotlock.id,
                            id={"type": "Shotlock", "deck": deck.idx},
                            style={"width": 200},
                            searchable=False,
                            clearable=False,
                        ),
                        dcc.Markdown(
                            str(khbbs.commands[deck.shotlock.id]),
                            id={"type": "Shotlock text", "deck": deck.idx},
                            style={"whiteSpace": "pre-wrap"},
                        ),
                    ])
                ]),
            ]) for deck in khbbs.decks
        ]),
    ])

@callback(
    Input("Deck", "value"),
)
def deck_callback(deck):
    khbbs = utils.khbbs
    khbbs.deck.value = deck

@callback(
    Output({"type": "Battle Command text", "deck": MATCH, "index": ALL}, "children"),
    Input({"type": "Battle Command", "deck": MATCH, "index": ALL}, "value"),
    State({"type": "Battle Command", "deck": MATCH, "index": 0}, "id"),
)
def battle_commands_callback(
    battle_commands,
    id,
):
    khbbs = utils.khbbs
    deck = khbbs.decks[id["deck"]]
    l = []
    for i in range(8):
        deck.battle_commands[i].id = battle_commands[i]
        l.append(str(khbbs.commands[deck.battle_commands[i].id]))
    return l

@callback(
    Output({"type": "Action Command text", "deck": MATCH, "index": ALL}, "children"),
    Input({"type": "Action Command", "deck": MATCH, "index": ALL}, "value"),
    State({"type": "Action Command", "deck": MATCH, "index": 0}, "id"),
)
def action_commands_callback(
    action_commands,
    id,
):
    khbbs = utils.khbbs
    deck = khbbs.decks[id["deck"]]
    l = []
    for i in range(10):
        deck.action_commands[i].id = action_commands[i]
        l.append(str(khbbs.commands[deck.action_commands[i].id]))
    return l

@callback(
    Output({"type": "Shotlock text", "deck": MATCH}, "children"),
    Input({"type": "Shotlock", "deck": MATCH}, "value"),
    State({"type": "Shotlock", "deck": MATCH}, "id"),
)
def shotlock_callback(
    shotlock,
    id,
):
    khbbs = utils.khbbs
    deck = khbbs.decks[id["deck"]]
    deck.shotlock.id = shotlock
    return str(khbbs.commands[deck.shotlock.id])

@callback(
    Output({"type": "Deck Name", "index": ALL}, "value"),
    Input({"type": "Deck Name", "index": ALL}, "value"),
)
def deck_name_callback(
    names,
):
    khbbs = utils.khbbs
    char_limit = 0x10
    l = []
    for i in range(len(names)):
        name = bytearray(names[i], "Shift-JIS")
        limit = min(len(name), char_limit-1)
        khbbs.decks[i].name = (c_ubyte*char_limit)(*(name[:limit] + bytearray(char_limit - limit)))
        l.append(bytearray(khbbs.decks[i].name).decode("Shift-JIS").strip("\0"))
    return l if len(l) > 0 else names
