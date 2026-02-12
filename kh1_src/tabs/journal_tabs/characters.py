from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils

@callback(
    Output("JournalCharactersDiv", "children"),
    Input("JournalCharactersTabs", "value"),
)
def __create_journal_characters_tabs(tab):
    if tab == "Characters 1 & 2":
        return __create_characters_12()
    if tab == "The Heartless":
        return __create_the_heartless()

def __create_characters_12():
    kh1 = utils.kh1
    chars1 = html.Div([
        dcc.Checklist(
            options=[
                {"label": k, "value": (1 << v % 16)}
            ],
            value=[kh1.journal_chars[v // 16] & (1 << v % 16)],
            id={"type": "Journal Character Entry", "index": v},
        ) for k, v in kh1.journal_chars_1_dict.items()
    ])
    chars2 = html.Div([
        dcc.Checklist(
            options=[
                {"label": k, "value": (1 << v % 16)}
            ],
            value=[kh1.journal_chars[v // 16] & (1 << v % 16)],
            id={"type": "Journal Character Entry", "index": v},
        ) for k, v in kh1.journal_chars_2_dict.items()
    ])
    return html.Div([
        html.H3("Characters 1:"),
        chars1,
        html.H3("Characters 2:"),
        chars2,
    ])

def __create_the_heartless():
    kh1 = utils.kh1
    heartlessnames = kh1.fmheartlessnames if kh1.fm else kh1.heartlessnames
    heartless = html.Div([
        html.Div([
            html.Label(k + ": "),
            dcc.Input(
                id={"type": "Heartless Kill Count", "index": v},
                type="number",
                value=kh1.heartless[v],
                min=0,
                max=0xFFFF,
                step=1,
                style={"width": 50},
            ),
        ],
            style={"margin-top": 20, "gap": 10},
        ) for k, v in zip(heartlessnames, range(len(heartlessnames)))
    ])
    bosses = html.Div([
        dcc.Checklist(
            options=[
                {"label": k, "value": (1 << v % 16)}
            ],
            value=[kh1.journal_chars[v // 16] & (1 << v % 16)],
            id={"type": "Journal Character Entry", "index": v},
        ) for k, v in kh1.journal_boss_dict.items()
    ])
    return html.Div([
        html.H3("Heartless Kill Counts:"),
        heartless,
        html.H3("Heartless Bosses:"),
        bosses,
    ])

def create_journal_characters():
    jctabs = dcc.Tabs(id="JournalCharactersTabs", value="Characters 1 & 2")
    jctabs.children = [
        dcc.Tab(label="Characters 1 & 2", value="Characters 1 & 2"),
        dcc.Tab(label="The Heartless", value="The Heartless"),
    ]
    return html.Div([
        jctabs,
        html.Div(id="JournalCharactersDiv"),
    ])

@callback(
    Input({"type": "Heartless Kill Count", "index": ALL}, "value"),
    State({"type": "Heartless Kill Count", "index": ALL}, "id"),
)
def the_heartless_callback(values, ids):
    kh1 = utils.kh1
    try:
        i = 0
        for id in ids:
            idx = id["index"]
            kh1.heartless[idx] = values[i]
            i += 1
    except:
        pass

@callback(
    Input({"type": "Journal Character Entry", "index": ALL}, "value"),
    Input({"type": "Journal Character Entry", "index": ALL}, "id"),
)
def journal_characters_callback(values, ids):
    kh1 = utils.kh1
    for i in range(len(values)):
        v = ids[i]["index"]
        if (1 << v % 16) in values[i]:
            kh1.journal_chars[v // 16] |= (1 << v % 16)
        else:
            kh1.journal_chars[v // 16] &= ~(1 << v % 16)
