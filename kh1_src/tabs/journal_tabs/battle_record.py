from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


def create_battle_record():
    kh1 = utils.kh1
    heartless_killed = html.Div([
        html.Label("Heartless defeated: "),
        dcc.Input(
            id="HeartlessDefeated",
            type="number",
            value=kh1.heartless_killed.value,
            min=0,
            max=0xFFFF,
            step=1,
            style={"width": 50},
        ),
    ],
        style={"margin-top": 20},
    )
    deaths = html.Div([
        html.Label("Times defeated: "),
        dcc.Input(
            id="TimesDefeated",
            type="number",
            value=kh1.deaths.value,
            min=0,
            max=0xFFFF,
            step=1,
            style={"width": 50},
        ),
    ],
        style={"margin-top": 20},
    )
    deflected = html.Div([
        html.Label("Attacks deflected: "),
        dcc.Input(
            id="AttacksDeflected",
            type="number",
            value=kh1.deflected.value,
            min=0,
            max=0xFFFF,
            step=1,
            style={"width": 50},
        ),
    ],
        style={"margin-top": 20},
    )
    hits = html.Div([
        html.Label("Times hit by an enemy: "),
        dcc.Input(
            id="Hits",
            type="number",
            value=kh1.hits.value,
            min=0,
            max=0xFFFF,
            step=1,
            style={"width": 50},
        ),
    ],
        style={"margin-top": 20},
    )
    item_usage = html.Div([
        html.Label("Total item usage: "),
        dcc.Input(
            id="ItemUsage",
            type="number",
            value=kh1.item_usage.value,
            min=0,
            max=0xFFFF,
            step=1,
            style={"width": 50},
        ),
    ],
        style={"margin-top": 20},
    )
    friend_ko = html.Div([
        html.Label("Party member knockouts: "),
        dcc.Input(
            id="FriendKO",
            type="number",
            value=kh1.friend_ko.value,
            min=0,
            max=0xFFFF,
            step=1,
            style={"width": 50},
        ),
    ],
        style={"margin-top": 20},
    )
    cure_on_friends = html.Div([
        html.Label("Curative spells cast on friend: "),
        dcc.Input(
            id="CureOnFriends",
            type="number",
            value=kh1.cure_on_friends.value,
            min=0,
            max=0xFFFF,
            step=1,
            style={"width": 50},
        ),
    ],
        style={"margin-top": 20},
    )
    return html.Div([
        heartless_killed,
        deaths,
        deflected,
        hits,
        item_usage,
        friend_ko,
        cure_on_friends
    ])

@callback(
    Input("HeartlessDefeated", "value"),
    Input("TimesDefeated", "value"),
    Input("AttacksDeflected", "value"),
    Input("Hits", "value"),
    Input("ItemUsage", "value"),
    Input("FriendKO", "value"),
    Input("CureOnFriends", "value"),
)
def journal_battle_record_callback(
    heartless_killed,
    deaths,
    deflected,
    hits,
    item_usage,
    friend_ko,
    cure_on_friends
):
    kh1 = utils.kh1
    try:
        kh1.heartless_killed.value = heartless_killed
        kh1.deaths.value = deaths
        kh1.deflected.value = deflected
        kh1.hits.value = hits
        kh1.item_usage.value = item_usage
        kh1.friend_ko.value = friend_ko
        kh1.cure_on_friends.value = cure_on_friends
    except:
        pass
