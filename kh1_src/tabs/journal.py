from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils

from kh1_src.tabs.journal_tabs import *


@callback(
    Output("JournalDiv", "children"),
    Input("JournalTabs", "value"),
)
def __create_journal(tab):
    if tab == "Chronicles":
        return create_chronicles()
    if tab == "Ansem's Report":
        return create_reports()
    if tab == "Characters":
        return create_journal_characters()
    if tab == "101 Dalmatians":
        return create_dalmatians()
    if tab == "Trinity List":
        return create_trinity()

def create_journal():
    jtabs = dcc.Tabs(id="JournalTabs", value="Journal Flags")
    jtabs.children = [
        dcc.Tab(label="Journal Flags", value="Journal Flags"),
        dcc.Tab(label="Chronicles", value="Chronicles"),
        dcc.Tab(label="Ansem's Report", value="Ansem's Report"),
        dcc.Tab(label="Characters", value="Characters"),
        dcc.Tab(label="101 Dalmatians", value="101 Dalmatians"),
        dcc.Tab(label="Trinity List", value="Trinity List"),
        dcc.Tab(label="Mini Games", value="Mini Games"),
        dcc.Tab(label="Treasures", value="Treasures"),
    ]
    return html.Div([
        jtabs,
        html.Div(id="JournalDiv"),
    ])
