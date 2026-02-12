from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils

def create_dalmatians():
    kh1 = utils.kh1
    dalmatians = [
        dcc.Checklist(
            options=[
                {"label": f"Puppy {i*8+j+1}", "value": (1 << 7 - j)}\
                for j in range(8) if i*8+j+1 < 100
            ],
            value=[kh1.dalmatians[i] & (1 << j) for j in range(8)],
            id={"type": "Dalmatian", "index": i},
        ) for i in range(len(kh1.dalmatians))
    ]
    return html.Div(dalmatians, style={"margin-top": 20})

@callback(
    Input({"type": "Dalmatian", "index": ALL}, "value"),
)
def dalmatians_callback(values):
    kh1 = utils.kh1
    for i in range(len(kh1.dalmatians)):
        kh1.dalmatians[i] = sum(values[i])
