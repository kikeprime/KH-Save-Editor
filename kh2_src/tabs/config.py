from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh2_src.kh2_utils as utils


def create_config(encoding):
    kh2 = utils.kh2
    difficulty = dcc.Dropdown(
        options=[
            {"label": "Beginner", "value": 0},
            {"label": "Standard", "value": 1},
            {"label": "Proud", "value": 2},
        ] if kh2.version < 2 else [
            {"label": "Beginner", "value": 0},
            {"label": "Standard", "value": 1},
            {"label": "Proud", "value": 2},
            {"label": "Critical", "value": 3},
        ],
        value=kh2.difficulty.value,
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
    kh2 = utils.kh2
    kh2.difficulty.value = difficulty
