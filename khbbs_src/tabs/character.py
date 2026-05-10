from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import khbbs_src.khbbs_utils as utils


def create_character():
    khbbs = utils.khbbs
    weapon = dcc.Dropdown(
        options=[
            {"label": k, "value": v} for k, v in khbbs.weapon_dict.items()
        ],
        value=khbbs.character.weapon.value,
        id="Weapon",
        searchable=False,
        clearable=False,
        style={"width": 300},
    )
    exp = dcc.Input(
        id="EXP",
        type="number",
        value=khbbs.character.exp.value,
        min=0,
        max=999999,
        step=1,
        style={"width": 60},
    )
    level = dcc.Input(
        id="Level",
        type="number",
        value=khbbs.character.level.value,
        min=1,
        max=99,
        step=1,
        style={"width": 50},
    )
    hp = html.Div([
        dcc.Input(
            id="HP",
            type="number",
            value=khbbs.character.hp.value,
            min=0,
            max=255,
            step=1,
            style={"width": 50},
        ),
        html.Label(" / "),
        dcc.Input(
            id="Max HP",
            type="number",
            value=khbbs.character.maxhp.value,
            min=0,
            max=255,
            step=1,
            style={"width": 50},
        ),
    ],
        style={"display": "inline-block"},
    )
    strength = dcc.Input(
        id="Strength",
        type="number",
        value=khbbs.character.strength.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    magic = dcc.Input(
        id="Magic",
        type="number",
        value=khbbs.character.magic.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    defense = dcc.Input(
        id="Defense",
        type="number",
        value=khbbs.character.defense.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    medals = dcc.Input(
        id="Medals",
        type="number",
        value=khbbs.character.medals.value,
        min=0,
        max=0xFFFF,
        step=1,
        style={"width": 50},
    )
    arenalevel = dcc.Input(
        id="Arena Level",
        type="number",
        value=khbbs.character.arenalevel.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    resistances = html.Div([
        html.Div([
            dcc.Markdown("Fire:"),
            dcc.Input(
                id="Fire Resistance",
                type="number",
                value=100 - khbbs.character.fire_resistance.value,
                min=-100,
                max=100,
                step=1,
                style={"width": 50},
            ),
            html.Label(" %"),
        ]),
        html.Div([
            dcc.Markdown("Thunder:"),
            dcc.Input(
                id="Thunder Resistance",
                type="number",
                value=100 - khbbs.character.thunder_resistance.value,
                min=-100,
                max=100,
                step=1,
                style={"width": 50},
            ),
            html.Label(" %"),
        ]),
        html.Div([
            dcc.Markdown("Blizzard:"),
            dcc.Input(
                id="Blizzard Resistance",
                type="number",
                value=100 - khbbs.character.blizzard_resistance.value,
                min=-100,
                max=100,
                step=1,
                style={"width": 50},
            ),
            html.Label(" %"),
        ]),
        html.Div([
            dcc.Markdown("Dark:"),
            dcc.Input(
                id="Dark Resistance",
                type="number",
                value=100 - khbbs.character.dark_resistance.value,
                min=-100,
                max=100,
                step=1,
                style={"width": 50},
            ),
            html.Label(" %"),
        ]),
    ])
    return html.Div([
        html.Div([
            html.Div([dcc.Markdown("Weapon:"), weapon]),
            html.Div([
                html.Div([dcc.Markdown("EXP:"), exp]),
                html.Div([dcc.Markdown("Level:"), level]),
            ],
                style={"display": "flex", "gap": 20},
            ),
            html.Div([dcc.Markdown("HP:"), hp]),
            html.Div([
                html.Div([dcc.Markdown("Strength:"), strength]),
                html.Div([dcc.Markdown("Magic:"), magic]),
                html.Div([dcc.Markdown("Defense:"), defense]),
            ],
                style={"display": "flex", "gap": 20},
            ),
            html.Div([
                html.Div([dcc.Markdown("Medals:"), medals]),
                html.Div([dcc.Markdown("Arena Level:"), arenalevel]),
            ],
                style={"display": "flex", "gap": 20},
            ),
            html.Div([html.H3("Resistances:"), resistances]),
        ]),
    ],
        style={"display": "flex"},
    )

@callback(
    Input("Weapon", "value"),
    Input("EXP", "value"),
    Input("Level", "value"),
    Input("HP", "value"),
    Input("Max HP", "value"),
    Input("Strength", "value"),
    Input("Magic", "value"),
    Input("Defense", "value"),
    Input("Medals", "value"),
    Input("Arena Level", "value"),
    Input("Fire Resistance", "value"),
    Input("Thunder Resistance", "value"),
    Input("Blizzard Resistance", "value"),
    Input("Dark Resistance", "value"),
)
def character_callback(
    weapon,
    exp,
    level,
    hp,
    maxhp,
    strength,
    magic,
    defense,
    medals,
    arenalevel,
    fire_resistance,
    thunder_resistance,
    blizzard_resistance,
    dark_resistance,
):
    khbbs = utils.khbbs
    try:
        khbbs.character.weapon.value = weapon
        khbbs.character.exp.value = exp
        khbbs.character.level.value = level
        khbbs.character.hp.value = hp
        khbbs.character.maxhp.value = maxhp
        khbbs.character.strength.value = strength
        khbbs.character.magic.value = magic
        khbbs.character.defense.value = defense
        khbbs.character.medals.value = medals
        khbbs.character.arenalevel.value = arenalevel
        khbbs.character.fire_resistance.value = 100 - fire_resistance
        khbbs.character.thunder_resistance.value = 100 - thunder_resistance
        khbbs.character.blizzard_resistance.value = 100 - blizzard_resistance
        khbbs.character.dark_resistance.value = 100 - dark_resistance
    except:
        pass
