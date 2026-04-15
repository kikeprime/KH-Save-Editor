from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


def create_synthesis():
    kh1 = utils.kh1
    synthesis = html.Div([
        html.H3("Synthesized Items:"),
        html.Div([
            html.Div([
                dcc.Checklist(
                    options=[{"label": k, "value": (1 << v % 16)}],
                    value=[kh1.synth_flags[v//16] & (1 << v % 16)],
                    id={"type": "Synth Flag", "index": v},
                    style={"margin-top": 10},
                )
            ])\
            for k, v in kh1.synth_dict.items()
        ])
    ])
    return html.Div([
        synthesis,
    ])
