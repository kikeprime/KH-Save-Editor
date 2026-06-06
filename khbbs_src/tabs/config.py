from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import khbbs_src.khbbs_utils as utils

def create_config():
    khbbs = utils.khbbs
    difficulty = dcc.Dropdown(
        options=[
            {"label": "Beginner", "value": 0x08},
            {"label": "Standard", "value": 0x48},
            {"label": "Proud", "value": 0x88},
        ] if khbbs.version == 0 else [
            {"label": "Beginner", "value": 0x08},
            {"label": "Standard", "value": 0x48},
            {"label": "Proud", "value": 0x88},
            {"label": "Critical", "value": 0xC8},
        ],
        value=khbbs.difficulty.value,
        id="Difficulty",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    return html.Div([
        html.Div([dcc.Markdown("Difficulty:"), difficulty]),
    ])

@callback(
    Input("Difficulty", "value"),
)
def config_callback(
    difficulty,
):
    khbbs = utils.khbbs
    khbbs.difficulty.value = difficulty
