from dash import Dash, html, dcc, callback, Input, Output, State, ALL

from kh2_src.kh2 import *
from kh2_src.tabs import *
import kh2_src.kh2_utils as utils


kh2 = None
app = Dash("KH2 Save Editor", suppress_callback_exceptions=True)

app.title = "KH2 Save Editor"

icon = html.Img(src="assets/favicon.ico", height=30, disable_n_clicks=True)

app_title = html.H1(
    ["Kingdom Hearts 2 Save Editor    ", icon],
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
        html.Label("Version:"),
        html.Div([
            dcc.Dropdown(
                [
                    {"label": "Vanilla JP", "value": 0},
                    {"label": "Vanilla USA", "value": 1},
                    {"label": "Final Mix", "value": 2},
                ],
                value=1,
                id="Version",
                style={"margin-left": 5, "width": 200},
                searchable=False,
                clearable=False,
            ),
        ],
            style={"display": "inline-block", "height": 25},
        )
    ],
        style={"display": "inline-block", "margin-top": 10, "margin-bottom": 10},
    ),
    html.Div([
        html.Label("Encoding:"),
        html.Div([
            dcc.Dropdown(
                ["Japanese", "International"],
                "International",
                id="Encoding",
                style={"margin-left": 5, "width": 200},
                searchable=False,
                clearable=False,
            ),
        ],
            style={"display": "inline-block", "height": 25},
        ),
    ]),
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
forms = dcc.Tab(label="Drive Forms", value="Drive Forms")
inventory = dcc.Tab(label="Inventory", value="Inventory")
journal = dcc.Tab(label="Jiminy's Journal", value="Journal")
config = dcc.Tab(label="Config", value="Config")
misc = dcc.Tab(label="Misc", value="Misc")
gummi = dcc.Tab(label="Gummi Ships", value="Gummi Ships")
tabs.children = [
    general,
    characters,
    forms,
    inventory,
    journal,
    config,
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
    State("Version", "value"),
)
def load_file(n_clicks, slot, version):
    if n_clicks > 0:
        global kh2
        kh2 = KH2(slot, version)
        utils.kh2 = kh2
        return "General"

@callback(
    Input("Save", "n_clicks"),
)
def save_file(n_clicks):
    global kh2
    if kh2 is not None and n_clicks > 0:
        kh2.save()

@callback(
    Output("TabsDiv", "children"),
    Input("Tabs", "value"),
    Input("Encoding", "value"),
)
def tab_switch(tab, encoding):
    global kh2
    if kh2 is not None:
        if tab == "General":
            return create_general()
        if tab == "Characters":
            return create_characters()
        if tab == "Drive Forms":
            return create_forms()
        if tab == "Inventory":
            return create_inventory()
        if tab == "Journal":
            return create_journal()
        if tab == "Config":
            return create_config(encoding)
        if tab == "Gummi Ships":
            return create_gummi()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)

