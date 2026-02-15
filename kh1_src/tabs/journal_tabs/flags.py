from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


def create_flags():
    kh1 = utils.kh1
    unlocked = html.Div([
        dcc.Checklist(
            options=[
                {"label": "Jiminy's Journal unlocked", "value": (1 << 3)}
            ],
            value=[kh1.journal_unlock.value & (1 << 3)],
            id="Journal Unlock",
        ),
    ],
        style={"margin-top": 20},
    )
    return html.Div([
        unlocked,
    ])

@callback(
    Input("Journal Unlock", "value"),
)
def journal_unlock_callback(value):
    kh1 = utils.kh1
    if (1 << 3) in value:
        kh1.journal_unlock.value |= (1 << 3)
    else:
        kh1.journal_unlock.value &= ~(1 << 3)
