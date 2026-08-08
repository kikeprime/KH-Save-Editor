from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


def create_flags():
    kh1 = utils.kh1
    unlocked = html.Div([
        dcc.Checklist(
            options=[
                {"label": "Jiminy's Journal unlocked", "value": (1 << 3)},
                {"label": "Heartless are powered up", "value": (1 << 0)},
                {"label": "Gummi Ship Save Point option is usable", "value": (1 << 1)},
            ],
            value=[kh1.journal_unlock.value & (1 << i) for i in range(8)],
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
    for i in range(8):
        if (1 << i) in value:
            kh1.journal_unlock.value |= (1 << i)
        else:
            kh1.journal_unlock.value &= ~(1 << i)
