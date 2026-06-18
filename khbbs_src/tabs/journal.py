from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import khbbs_src.khbbs_utils as utils

from khbbs_src.tabs.journal_tabs import *


@callback(
    Output("JournalDiv", "children"),
    Input("JournalTabs", "value"),
)
def __create_journal(tab):
    if tab == "Game Records":
        return create_game_records()

def create_journal():
    jtabs = dcc.Tabs(id="JournalTabs", value="Game Records")
    jtabs.children = [
        dcc.Tab(label="Story", value="Story"),
        dcc.Tab(label="Secret Reports", value="Secret Reports"),
        dcc.Tab(label="Game Records", value="Game Records"),
        dcc.Tab(label="Event Records", value="Event Records"),
        dcc.Tab(label="Character Files", value="Character Files"),
        dcc.Tab(label="The Unversed", value="The Unversed"),
        dcc.Tab(label="Ice Cream Guide", value="Ice Cream Guide"),
        dcc.Tab(label="Command Collection", value="Command Collection"),
        dcc.Tab(label="Treasures", value="Treasures"),
        dcc.Tab(label="Sticker Album", value="Sticker Album"),
    ]
    return html.Div([
        jtabs,
        html.Div(id="JournalDiv"),
    ])
