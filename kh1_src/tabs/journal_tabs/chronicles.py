from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


def create_chronicles():
    kh1 = utils.kh1
    chronicles = [
        html.Div([
            dcc.Markdown(list(kh1.chronicles_dict.keys())[i]),
            dcc.Checklist(
                options=[
                    {"label": f"Part {j+1}", "value": (1 << 7 - j)}\
                    for j in range(list(kh1.chronicles_dict.values())[i])
                ],
                value=[kh1.chronicles[i] & (1 << j) for j in range(8)],
                id={"type": "Chronicle", "index": i},
            )
        ]) for i in range(len(kh1.chronicles))
    ]
    return html.Div(chronicles, style={"margin-top": 20})

@callback(
    Input({"type": "Chronicle", "index": ALL}, "value"),
)
def chronicles_callback(values):
    kh1 = utils.kh1
    for i in range(len(kh1.chronicles)):
        kh1.chronicles[i] = sum(values[i])
