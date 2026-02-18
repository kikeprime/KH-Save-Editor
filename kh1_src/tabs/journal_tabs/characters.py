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
        html.Div([
            dcc.Checklist(
                options=[
                    {"label": k, "value": (1 << v % 16)}
                ],
                value=[kh1.journal_chars[v // 16] & (1 << v % 16)],
                id={"type": "Journal Character Entry", "index": v},
                style={"margin-top": 15},
            )
        ]) if type(v) == int else\
        html.Div([
            dcc.Markdown(k+":"),
            dcc.RadioItems(
                options=[
                    # This works because multipart entries always on different bits.
                    {"label": l, "value": (1 << p % 16)}\
                    for l, p in v.items()
                ],
                value=sum([kh1.journal_chars[p // 16] & (1 << p % 16) for p in v.values()]),
                id={"type": "Journal Character Multi Entry", "index": k},
            ),
        ])\
        for k, v in kh1.journal_chars_1_dict.items()
    ],
        style={"margin-top": 20},
    )
    return chars1

def __create_characters_2():
    kh1 = utils.kh1
    chars2 = html.Div([
        html.Div([
            dcc.Checklist(
                options=[
                    {"label": k, "value": (1 << v % 16)}
                ],
                value=[kh1.journal_chars[v // 16] & (1 << v % 16)],
                id={"type": "Journal Character Entry", "index": v},
                style={"margin-top": 15},
            )
        ]) if type(v) == int else\
        html.Div([
            dcc.Markdown(k+":"),
            dcc.RadioItems(
                options=[
                    # This works because multipart entries always on different bits.
                    {"label": l, "value": (1 << p % 16)}\
                    for l, p in v.items()
                ],
                value=sum([kh1.journal_chars[p // 16] & (1 << p % 16) for p in v.values()]),
                id={"type": "Journal Character Multi Entry", "index": k},
            ),
        ])\
        for k, v in kh1.journal_chars_2_dict.items()
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
    State({"type": "Journal Character Entry", "index": ALL}, "id"),
)
def journal_characters_callback(values, ids):
    kh1 = utils.kh1
    for i in range(len(values)):
        v = ids[i]["index"]
        if (1 << v % 16) in values[i]:
            kh1.journal_chars[v // 16] |= (1 << v % 16)
        else:
            kh1.journal_chars[v // 16] &= ~(1 << v % 16)

@callback(
    Input({"type": "Journal Character Multi Entry", "index": ALL}, "value"),
    State({"type": "Journal Character Multi Entry", "index": ALL}, "id"),
)
def journal_characters_callback(values, ids):
    kh1 = utils.kh1
    for value, id in zip(values, ids):
        name = id["index"]
        if name in kh1.journal_chars_1_dict:
            for v in kh1.journal_chars_1_dict[name].values():
                if (1 << v % 16) == value:
                    kh1.journal_chars[v // 16] |= (1 << v % 16)
                else:
                    kh1.journal_chars[v // 16] &= ~(1 << v % 16)
        if name in kh1.journal_chars_2_dict:
            for v in kh1.journal_chars_2_dict[name].values():
                if (1 << v % 16) == value:
                    kh1.journal_chars[v // 16] |= (1 << v % 16)
                else:
                    kh1.journal_chars[v // 16] &= ~(1 << v % 16)
