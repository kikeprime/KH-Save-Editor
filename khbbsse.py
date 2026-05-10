import mimetypes

from dash import Dash, html, dcc, callback, Input, Output, State, ALL

from khbbs_src.khbbs import *
from khbbs_src.tabs import *
import khbbs_src.khbbs_utils as utils


# Windows fix
if "text/css" not in mimetypes.guess_type("style.css"):
    mimetypes.add_type("text/css", ".css")

app = Dash("KHBBS Save Editor", suppress_callback_exceptions=True)

app.title = "KHBBS Save Editor"

icon = html.Img(src="assets/favicon.ico", height=30, disable_n_clicks=True)

app_title = html.H1(
    ["Kingdom Hearts Birth by Sleep Save Editor    ", icon],
    style={"text_align": "center", "color": "#0088CE", "fontSize": 30},
)

# Load parameter widgets
menu = html.Div([
    html.Div([
        html.Button(
            "Load", id="Load", n_clicks=0, style={"width": 100}
        ),
        html.Div([
            html.Label("Slot: "),
            dcc.Input(
                id="Slot",
                type="number",
                value=1,
                min=0,
                max=99,
                step=1,
                style={"width": 50},
            ),
        ],
            style={"margin-left": 10},
        ),
    ],
        style={"display": "flex", "margin-bottom": 10},
    ),
    html.Div([
        html.Label("Version:", style={"margin-top": 8}),
        dcc.Dropdown(
            options=[
                {"label": "Vanilla JP", "value": 0},
                {"label": "Vanilla USA", "value": 1},
                {"label": "Final Mix", "value": 2},
            ],
            value=2,
            id="Version",
            style={"margin-left": 5, "width": 200},
            searchable=False,
            clearable=False,
        ),
    ],
        style={"display": "flex", "margin-bottom": 10},
    ),
    html.Div([
        html.Label("Encoding:", style={"margin-top": 8}),
        html.Div([
            dcc.Dropdown(
                ["Japanese", "International"],
                "International",
                id="Encoding",
                style={"margin-left": 5, "width": 200},
                searchable=False,
                clearable=False,
            ),
        ]),
    ],
        style={"display": "flex", "margin-bottom": 10},
    ),
    html.Div([
        html.Button("Save", id="Save", n_clicks=0, style={"width": 100})
    ]),
],
    style={"margin-bottom": 20},
)

tabs = dcc.Tabs(id="Tabs", value="General")
general = dcc.Tab(label="General", value="General")
character = dcc.Tab(label="Character", value="Character")
inventory = dcc.Tab(label="Inventory", value="Inventory")
journal = dcc.Tab(label="Reports", value="Journal")
config = dcc.Tab(label="Config", value="Config")
worlds = dcc.Tab(label="Worlds", value="Worlds")
misc = dcc.Tab(label="Misc", value="Misc")
tabs.children = [
    general,
    character,
    inventory,
    journal,
    config,
    worlds,
    misc,
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
    State("Version", "value"),
)
def load_file(n_clicks, slot, version):
    if n_clicks > 0:
        utils.khbbs = KHBBS(slot, version, slot == 0)
        return "General"

@callback(
    Input("Save", "n_clicks"),
)
def save_file(n_clicks):
    khbbs = utils.khbbs
    if khbbs is not None and n_clicks > 0:
        khbbs.save()

@callback(
    Output("TabsDiv", "children"),
    Input("Tabs", "value"),
    Input("Encoding", "value"),
)
def tab_switch(tab, encoding):
    khbbs = utils.khbbs
    if khbbs is not None:
        if tab == "General":
            return create_general()
        if tab == "Character":
            return create_character()
        """if tab == "Inventory":
            return create_inventory()
        if tab == "Journal":
            return create_journal()
        if tab == "Config":
            return create_config()
        if tab == "Worlds":
            return create_worlds()
        if tab == "Misc":
            return create_misc()"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
