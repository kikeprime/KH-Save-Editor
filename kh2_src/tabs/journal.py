from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh2_src.kh2_utils as utils

from kh2_src.tabs.journal_tabs import *


@callback(
    Output("JournalDiv", "children"),
    Input("JournalTabs", "value"),
)
def __create_journal(tab):
    if tab == "Ansem Reports":
        return create_reports()
    if tab == "Character Files":
        return create_character_files()
    if tab == "Bestiary":
        return create_bestiary()

def create_journal():
    jtabs = dcc.Tabs(id="JournalTabs", value="Journal Flags")
    jtabs.children = [
        dcc.Tab(label="Journal Flags", value="Journal Flags"),
        dcc.Tab(label="Ansem Reports", value="Ansem's Reports"),
        dcc.Tab(label="Character Files", value="Character Files"),
        dcc.Tab(label="Bestiary", value="Bestiary"),
        dcc.Tab(label="Treasures", value="Treasures"),
        dcc.Tab(label="Puzzle Pieces", value="Puzzle Pieces"),
        dcc.Tab(label="Maps", value="Maps"),
        dcc.Tab(label="Missions", value="Missions"),
        dcc.Tab(label="Minigames", value="Minigames"),
        dcc.Tab(label="Synthesis Notes", value="Synthesis Notes"),
    ]
    return html.Div([
        jtabs,
        html.Div(id="JournalDiv"),
    ])
