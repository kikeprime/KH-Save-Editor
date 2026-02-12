from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


def create_reports():
    kh1 = utils.kh1
    reports = [
        dcc.Checklist(
            options=[
                {"label": f"Ansem's Report {i*8+j+1}", "value": (1 << 7 - j)}\
                for j in range(8) if i*8+j+1 < 14
            ],
            value=[kh1.reports[i] & (1 << j) for j in range(8)],
            id={"type": "Report", "index": i},
        ) for i in range(len(kh1.reports))
    ]
    return html.Div(reports, style={"margin-top": 20})

@callback(
    Input({"type": "Report", "index": ALL}, "value"),
)
def reports_callback(values):
    kh1 = utils.kh1
    for i in range(len(kh1.reports)):
        kh1.reports[i] = sum(values[i])
