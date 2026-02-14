from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils

@callback(
    Output("JournalCharactersDiv", "children"),
    Input("JournalCharactersTabs", "value"),
)
def __create_journal_characters_tabs(tab):
    if tab == "Characters 1":
        return __create_characters_1()
    if tab == "Characters 2":
        return __create_characters_2()
    if tab == "The Heartless":
        return __create_the_heartless()

def __create_characters_1():
    kh1 = utils.kh1
    chars1 = html.Div([
        dcc.Checklist(
            options=[
                {"label": k, "value": (1 << v % 16)}
            ],
            value=[kh1.journal_chars[v // 16] & (1 << v % 16)],
            id={"type": "Journal Character Entry", "index": v},
        ) for k, v in kh1.journal_chars_1_dict.items()
    ],
        style={"margin-top": 20},
    )
    return chars1

def __create_characters_2():
    kh1 = utils.kh1
    chars2 = html.Div([
        dcc.Checklist(
            options=[
                {"label": k, "value": (1 << v % 16)}
            ],
            value=[kh1.journal_chars[v // 16] & (1 << v % 16)],
            id={"type": "Journal Character Entry", "index": v},
        ) for k, v in kh1.journal_chars_2_dict.items()
    ],
        style={"margin-top": 20},
    )
    return chars2

def __create_the_heartless():
    kh1 = utils.kh1
    heartless_dict = kh1.heartless_fm_dict if kh1.fm else kh1.heartless_dict
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
        ) for k, v in heartless_dict.items()
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
    jctabs = dcc.Tabs(id="JournalCharactersTabs", value="Characters 1")
    jctabs.children = [
        dcc.Tab(label="Characters 1", value="Characters 1"),
        dcc.Tab(label="Characters 2", value="Characters 2"),
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
    
