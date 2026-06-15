from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import khbbs_src.khbbs_utils as utils

from khbbs_src.tabs.commands_tabs import *


def create_commands():
    khbbs = utils.khbbs
    return html.Div([
        dcc.Markdown("Tab:"),
        dcc.Dropdown(
            options=[
                # {"label": "Decks", "value": "Decks"},
                {"label": "Command List", "value": "Command List"},
                {"label": "Finishers", "value": "Finishers"},
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
        return create_command_list()
    if tab == "Finishers":
        return create_finishers()
    if tab == "Abilities":
        return create_abilities()
    if tab == "D-Links":
        return create_dlinks()
