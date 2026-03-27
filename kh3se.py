import mimetypes

from dash import Dash, html, dcc, callback, Input, Output, State, ALL

from kh3_src.kh3 import *
from kh3_src.tabs import *
import kh3_src.kh3_utils as utils


# Windows fix
if "text/css" not in mimetypes.guess_type("style.css"):
    mimetypes.add_type("text/css", ".css")

app = Dash("KH3 Save Editor", suppress_callback_exceptions=True)

app.title = "KH3 Save Editor"

icon = html.Img(src="assets/favicon.ico", height=30, disable_n_clicks=True)

app_title = html.H1(
    ["Kingdom Hearts 3 Save Editor    ", icon],
    style={"text_align": "center", "color": "#0088CE", "fontSize": 30},
)

# Load parameter widgets
menu = html.Div([
    html.Div([
        html.Button(
            "Load", id="Load", n_clicks=0, style={"width": 100}
        ),
    ],
        style={"display": "inline-block"},
    ),
    html.Div([
        html.Label("Slot: "),
        dcc.Input(
            id="Slot",
            type="number",
            value=1,
            min=1,
            max=99,
            step=1,
            style={"width": 50},
        ),
    ],
        style={"display": "inline-block", "margin-left": 5},
    ),
    html.Div([
        html.Label("Account ID: "),
        dcc.Input(
            id="Account ID",
            type="text",
            value="",
            style={"width": 200},
        ),
    ],
        style={"margin-top": 10},
    ),
    html.Div([
        html.Button("Save", id="Save", n_clicks=0, style={"width": 100})
    ],
        style={"display": "inline-block", "margin-top": 10},
    ),
],
    style={"margin-bottom": 20},
)

tabs = dcc.Tabs(id="Tabs", value="General")
general = dcc.Tab(label="General", value="General")
characters = dcc.Tab(label="Characters", value="Characters")
inventory = dcc.Tab(label="Inventory", value="Inventory")
journal = dcc.Tab(label="Gummiphone", value="Journal")
config = dcc.Tab(label="Config", value="Config")
worlds = dcc.Tab(label="Worlds", value="Worlds")
misc = dcc.Tab(label="Misc", value="Misc")
gummi = dcc.Tab(label="Gummi Ships", value="Gummi Ships")
tabs.children = [
    general,
    characters,
    inventory,
    journal,
    config,
    worlds,
    misc,
    gummi,
]

app.layout = [
    app_title,
    menu,
    tabs,
    html.Div(id="TabsDiv", style={"margin-bottom": 120}),
]

@callback(
    Output("Tabs", "value"),
    Input("Load", "n_clicks"),
    State("Slot", "value"),
    State("Account ID", "value"),
)
def load_file(n_clicks, slot, account):
    if n_clicks > 0:
        utils.kh3 = KH3(slot, account)
        return "General"

@callback(
    Input("Save", "n_clicks"),
)
def save_file(n_clicks):
    kh3 = utils.kh3
    if kh3 is not None and n_clicks > 0:
        kh3.save()

@callback(
    Output("TabsDiv", "children"),
    Input("Tabs", "value"),
)
def tab_switch(tab):
    kh3 = utils.kh3
    if kh3 is not None:
        if tab == "General":
            return create_general()
    """
        if tab == "Characters":
            return create_characters()
        if tab == "Inventory":
            return create_inventory()
        if tab == "Journal":
            return create_journal()
        if tab == "Config":
            return create_config()
        if tab == "Worlds":
            return create_worlds()
        if tab == "Misc":
            return create_misc()
        if tab == "Gummi Ships":
            return create_gummi()"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
