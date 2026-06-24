from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils

def create_dalmatians():
    kh1 = utils.kh1
    dalmatians_flags = html.Div([
        html.H3("Event Flags"),
        dcc.Checklist(
            options=[
                {"label": "Watched all puppies event", "value": 1},
            ],
            value=[kh1.dalmatian_event.value],
            id="Dalmatian Event",
        ),
        dcc.Checklist(
            options=[
                {"label": "Pongo & Perdita has a gift for you", "value": 1},
            ],
            value=[kh1.dalmatian_gift_ready.value],
            id="Dalmatian Gift Ready",
        ),
        html.H3("Gift Flags"),
        dcc.Checklist(
            options=[
                {"label": "Curaga-G", "value": 0},
                {"label": "Firaga-G", "value": 1},
                {"label": "Thundara-G", "value": 2},
                {"label": "Mythril Shard", "value": 3},
                {"label": "Torn Page & Mythril", "value": 4},
                {"label": "Megalixir", "value": 5},
                {"label": "Orichalcum", "value": 6},
                {"label": "Ultima-G", "value": 7},
                {"label": "Tech Boost" if kh1.fm else "Ribbon", "value": 8},
                {"label": "Gummi Set & Aero Upgrade", "value": 9},
            ],
            value=[i for i in range(10) if kh1.dalmatian_gifts[i] == 1],
            id="Dalmatian Gifts",
        ),
    ])
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
    return html.Div([
        dalmatians_flags,
        html.H3("Puppy Flags"),
        html.Div(dalmatians, style={"margin-top": 20}),
    ])

@callback(
    Input("Dalmatian Event", "value"),
    Input("Dalmatian Gifts", "value"),
    Input("Dalmatian Gift Ready", "value"),
    Input({"type": "Dalmatian", "index": ALL}, "value"),
)
def dalmatians_callback(event, gifts, ready, puppies):
    kh1 = utils.kh1
    kh1.dalmatian_event.value = 1 if 1 in event else 0
    kh1.dalmatian_gift_ready.value = 1 if 1 in ready else 0
    for i in range(10):
        if i in gifts:
            kh1.dalmatian_gifts[i] = 1
        else:
            kh1.dalmatian_gifts[i] = 0
    for i in range(len(kh1.dalmatians)):
        kh1.dalmatians[i] = sum(puppies[i])
