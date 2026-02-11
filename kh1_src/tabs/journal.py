from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


@callback(
    Output("JournalDiv", "children"),
    Input("JournalTabs", "value"),
)
def __create_journal(tab):
    if tab == "Ansem's Report":
        return __create_reports()
    if tab == "Characters":
        return __create_journal_characters()
    if tab == "101 Dalmatians":
        return __create_dalmatians()

def __create_reports():
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
        html.H3("Characters 1:"),
        chars1,
        html.H3("Characters 2:"),
        chars2,
        html.H3("Heartless Bosses:"),
        bosses,
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
    return html.Div([html.H3("Heartless Kill Counts:"), heartless])

def __create_journal_characters():
    jctabs = dcc.Tabs(id="JournalCharactersTabs", value="Characters 1 & 2")
    jctabs.children = [
        dcc.Tab(label="Characters 1 & 2", value="Characters 1 & 2"),
        dcc.Tab(label="The Heartless", value="The Heartless"),
    ]
    return html.Div([
        jctabs,
        html.Div(id="JournalCharactersDiv"),
    ])

def __create_dalmatians():
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

def create_journal():
    jtabs = dcc.Tabs(id="JournalTabs", value="Journal Flags")
    jtabs.children = [
        dcc.Tab(label="Journal Flags", value="Journal Flags"),
        dcc.Tab(label="Chronicles", value="Chronicles"),
        dcc.Tab(label="Ansem's Report", value="Ansem's Report"),
        dcc.Tab(label="Characters", value="Characters"),
        dcc.Tab(label="101 Dalmatians", value="101 Dalmatians"),
        dcc.Tab(label="Trinity List", value="Trinity List"),
        dcc.Tab(label="Mini Games", value="Mini Games"),
        dcc.Tab(label="Treasures", value="Treasures"),
    ]
    return html.Div([
        jtabs,
        html.Div(id="JournalDiv"),
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
    Input({"type": "Report", "index": ALL}, "value"),
)
def reports_callback(values):
    kh1 = utils.kh1
    for i in range(len(kh1.reports)):
        kh1.reports[i] = sum(values[i])

@callback(
    Input({"type": "Journal Character Entry", "index": ALL}, "value"),
    Input({"type": "Journal Character Entry", "index": ALL}, "id"),
)
def journal_characters_callback(values, ids):
    kh1 = utils.kh1
    l = [[] for i in range(23)]
    i = 0
    for id in ids:
        idx = id["index"] // 16
        if len(values[i]) > 0:
            l[idx].append(values[i][-1])
        i += 1
    for i in list(range(16)) + [19, 20, 21, 22]: # Skipping unknown bytes
        kh1.journal_chars[i] = sum(l[i]) if len(l[i]) > 0 else 0

@callback(
    Input({"type": "Dalmatian", "index": ALL}, "value"),
)
def dalmatians_callback(values):
    kh1 = utils.kh1
    for i in range(len(kh1.dalmatians)):
        kh1.dalmatians[i] = sum(values[i])
