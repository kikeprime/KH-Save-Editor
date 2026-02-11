from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh1_src.kh1_utils as utils


@callback(
    Output("CTabsDiv", "children"),
    Input("CTabs", "value"),
    Input("StatTabs", "value"),
)
def ctab_switch(id, tab):
    kh1 = utils.kh1
    c = kh1.characters[int(id)]
    if tab == "Stats":
        return __create_stats(c)
    if tab == "Equipment":
        return __create_equipment(c)
    if tab == "Abilities":
        return __create_abilities(c)
    if tab == "Customize":
        return __create_customize(c)
    if tab == "Shared Abilities":
        return __create_shared_abilities()

def __create_stats(c):
    kh1 = utils.kh1
    exp = dcc.Input(
        id={"type": "EXP", "index": c.name},
        type="number",
        value=c.exp.value,
        min=0,
        max=999999,
        step=1,
        style={"width": 60},
    )
    level = dcc.Input(
        id={"type": "Level", "index": c.name},
        type="number",
        value=c.level.value,
        min=1,
        max=100,
        step=1,
        style={"width": 50},
    )
    hp = html.Div([
        dcc.Input(
            id={"type": "HP", "index": c.name},
            type="number",
            value=c.hp.value,
            min=0,
            max=255,
            step=1,
            style={"width": 50},
        ),
        html.Label(" / "),
        dcc.Input(
            id={"type": "Max HP", "index": c.name},
            type="number",
            value=c.maxhp.value,
            min=0,
            max=255,
            step=1,
            style={"width": 50},
        ),
    ],
        style={"display": "inline-block"},
    )
    mp = html.Div([
        dcc.Input(
            id={"type": "MP", "index": c.name},
            type="number",
            value=c.mp.value,
            min=0,
            max=255,
            step=1,
            style={"width": 50},
        ),
        html.Label(" / "),
        dcc.Input(
            id={"type": "Max MP", "index": c.name},
            type="number",
            value=c.maxmp.value,
            min=0,
            max=255,
            step=1,
            style={"width": 50},
        ),
    ],
        style={"display": "inline-block"},
    )
    submp = html.Div([
        dcc.Input(
            id={"type": "Sub MP 1", "index": c.name},
            type="number",
            value=c.submp.value // 30,
            min=0,
            max=c.mp.value,
            step=1,
            style={"width": 50},
        ),
        html.Label(" : "),
        dcc.Input(
            id={"type": "Sub MP 2", "index": c.name},
            type="number",
            value=c.submp.value % 30,
            min=0,
            max=29,
            step=1,
            style={"width": 50},
        ),
    ],
        style={"display": "inline-block"},
    )
    maxap = dcc.Input(
        id={"type": "Max AP", "index": c.name},
        type="number",
        value=c.maxap.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    strength = dcc.Input(
        id={"type": "Strength", "index": c.name},
        type="number",
        value=c.strength.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    defense = dcc.Input(
        id={"type": "Defense", "index": c.name},
        type="number",
        value=c.defense.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    magic = dcc.Checklist(
        [{"label": kh1.magicnames[i], "value": (1 << i)} for i in range(7)],
        [(1 << i) for i in range(7) if c.magic.value & (1 << i)],
        id={"type": "Magic", "index": c.name},
        style={"margin-bottom": 10},
    )
    return html.Div([
        html.Div([
            html.Div([
                html.Div([dcc.Markdown("EXP:"), exp]),
                html.Div([dcc.Markdown("Level:"), level]),
            ], style={"display": "flex", "gap": 20},
            ),
            html.Div([dcc.Markdown("HP:"), hp]),
            html.Div([dcc.Markdown("MP:"), mp]),
            html.Div([dcc.Markdown("Sub MP:"), submp]),
            html.Div([dcc.Markdown("Max AP:"), maxap]),
            html.Div([
                html.Div([dcc.Markdown("Strength:"), strength]),
                html.Div([dcc.Markdown("Defense:"), defense]),
            ], style={"display": "flex", "gap": 20},
            )
        ]),
        html.Div([dcc.Markdown("Spells:"), magic], style={"margin-left": 50}),
    ],
        style={"display": "flex"},
    )

def __create_equipment(c):
    kh1 = utils.kh1
    weapon = dcc.Dropdown(
        options=[
            {"label": k, "value": v} for k, v in kh1.weapon_dict.items()
        ],
        value=c.weapon.value,
        id={"type": "Weapon", "index": c.name},
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    accessoryslots = dcc.Input(
        id={"type": "Accessory Slots", "index": c.name},
        type="number",
        value=c.accessoryslots.value,
        min=0,
        max=8,
        step=1,
        style={"width": 50},
    )
    accessories = html.Div([
        dcc.Dropdown(
            options=[
                {"label": k, "value": v} for k, v in kh1.accessory_dict.items()
            ],
            value=c.accessories[i],
            id={"type": "Accessory", "index": c.name + ":" + str(i)},
            searchable=False,
            clearable=False,
            style={"width": 200},
        ) for i in range(8)
    ])
    itemslots = dcc.Input(
        id={"type": "Item Slots", "index": c.name},
        type="number",
        value=c.itemslots.value,
        min=0,
        max=8,
        step=1,
        style={"width": 50},
    )
    items = html.Div([
        dcc.Dropdown(
            options=[
                {"label": k, "value": v} for k, v in kh1.item_dict.items() if v < 0x09
            ],
            value=c.items[i],
            id={"type": "Item", "index": c.name + ":" + str(i)},
            searchable=False,
            clearable=False,
            style={"width": 200},
        ) for i in range(8)
    ])
    return html.Div([
        html.Div([dcc.Markdown("Weapon:"), weapon]),
        html.Div([dcc.Markdown("Accessory Slots:"), accessoryslots]),
        html.Div([dcc.Markdown("Accessories:"), accessories]),
        html.Div([dcc.Markdown("Item Slots:"), itemslots]),
        html.Div([dcc.Markdown("Items:"), items]),
    ])

def __create_abilities(c):
    kh1 = utils.kh1
    return html.Div([
        html.Div([
            dcc.Checklist(
                options=[{"label": "", "value": 0}],
                value=[c.abilities[i] & (1 << 7)],
                id={"type": "AbilityCheck", "index": c.name + ":" + str(i)},
            ),
            dcc.Dropdown(
                options=[
                    {"label": k, "value": v}
                    for k, v in kh1.ability_dict.items()
                ],
                value=c.abilities[i] & ~(1 << 7),
                id={"type": "Ability", "index": c.name + ":" + str(i)},
                searchable=False,
                clearable=False,
                style={"width": 200},
            ),
        ],
            style={"display": "flex", "alignItems": "center"},
        ) for i in range(48)
    ])

def __create_customize_sora(c):
    kh1 = utils.kh1
    circle = dcc.Dropdown(
        options=[{"label": kh1.magicnames[i], "value": i} for i in range(7)]\
        + [{"label": "Empty", "value": 0xFF}],
        value=kh1.shortcuts[0],
        id="Circle Shortcut",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    triangle = dcc.Dropdown(
        options=[{"label": kh1.magicnames[i], "value": i} for i in range(7)]\
        + [{"label": "Empty", "value": 0xFF}],
        value=kh1.shortcuts[1],
        id="Triangle Shortcut",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    square = dcc.Dropdown(
        options=[{"label": kh1.magicnames[i], "value": i} for i in range(7)]\
        + [{"label": "Empty", "value": 0xFF}],
        value=kh1.shortcuts[2],
        id="Square Shortcut",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    magiclevels = html.Div([
        dcc.Dropdown(
            options=[
                {"label": kh1.magicnames[i], "value": 1},
                {"label": kh1.magicnames2[i], "value": 2},
                {"label": kh1.magicnames3[i], "value": 3},
            ],
            value=kh1.magiclevels[i],
            id={"type": "Magic Level", "index": i},
            searchable=False,
            clearable=False,
            style={"width": 200},
        ) for i in range(7)
    ])
    summons = html.Div([
        dcc.Dropdown(
            options=[
                {"label": k, "value": v} for k, v in kh1.summon_dict.items()
            ],
            value=kh1.summons[i],
            id={"type": "Summon", "index": i},
            searchable=False,
            clearable=False,
            style={"width": 200},
        ) for i in range(7)
    ])
    return html.Div([
        html.Div([dcc.Markdown("Shortcuts:")]),
        html.Div([dcc.Markdown("Circle / Triangle:"), circle]),
        html.Div([dcc.Markdown("Triangle / Square:"), triangle]),
        html.Div([dcc.Markdown("Square / Cross:"), square]),
        html.Div([dcc.Markdown("Magic Levels:"), magiclevels]),
        html.Div([dcc.Markdown("Summons:"), summons]),
    ])

def __create_customize(c):
    if c.name == "Sora":
        return __create_customize_sora(c)
    else:
        pass

def __create_shared_abilities():
    kh1 = utils.kh1
    return html.Div([
        html.Div([
            dcc.Checklist(
                options=[{"label": "", "value": 0}],
                value=[kh1.shared_abilities[i] & (1 << 7)],
                id={"type": "SharedAbilityCheck", "index": i},
            ),
            dcc.Dropdown(
                options=[
                    {"label": k, "value": v}
                    for k, v in kh1.ability_dict.items()
                ],
                value=kh1.shared_abilities[i] & ~(1 << 7),
                id={"type": "SharedAbility", "index": i},
                searchable=False,
                clearable=False,
                style={"width": 200},
            )
        ],
            style={"display": "flex", "alignItems": "center"},
        ) for i in range(48)
    ])

def create_characters():
    kh1 = utils.kh1
    ctabs = dcc.Tabs(id="CTabs", value="0")
    ctabs.children = [
        dcc.Tab(label=kh1.characters[i].name, value=f"{i}")
        for i in range(len(kh1.characters))
        if kh1.characters[i].name != "Winnie the Pooh"
    ]
    stattabs = dcc.Tabs(id="StatTabs", value="Stats")
    stattabs.children = [
        dcc.Tab(label="Stats", value="Stats"),
        dcc.Tab(label="Equipment", value="Equipment"),
        dcc.Tab(label="Abilities", value="Abilities"),
        dcc.Tab(label="Customize", value="Customize"),
        dcc.Tab(label="Shared Abilities", value="Shared Abilities"),
    ]
    return html.Div([
        ctabs,
        stattabs,
        html.Div(id="CTabsDiv", style={"margin-top": 20})
    ])

@callback(
    Input({"type": "EXP", "index": ALL}, "value"),
    Input({"type": "Level", "index": ALL}, "value"),
    Input({"type": "HP", "index": ALL}, "value"),
    Input({"type": "Max HP", "index": ALL}, "value"),
    Input({"type": "MP", "index": ALL}, "value"),
    Input({"type": "Max MP", "index": ALL}, "value"),
    Input({"type": "Sub MP 1", "index": ALL}, "value"),
    Input({"type": "Sub MP 2", "index": ALL}, "value"),
    Input({"type": "Max AP", "index": ALL}, "value"),
    Input({"type": "Strength", "index": ALL}, "value"),
    Input({"type": "Defense", "index": ALL}, "value"),
    Input({"type": "Magic", "index": ALL}, "value"),
    State({"type": "EXP", "index": ALL}, "id"),
)
def stats_callback(
    exp, level,
    hp, maxhp,
    mp, maxmp,
    submp1, submp2,
    maxap,
    strength, defense,
    magic,
    ids
):
    kh1 = utils.kh1
    id = kh1.character_dict[ids[0]["index"]]
    try:
        kh1.characters[id].exp.value = exp[0]
        kh1.characters[id].level.value = level[0]
        kh1.characters[id].hp.value = hp[0]
        kh1.characters[id].maxhp.value = maxhp[0]
        kh1.characters[id].mp.value = mp[0]
        kh1.characters[id].maxmp.value = maxmp[0]
        kh1.characters[id].submp.value = submp1[0] * 30 + submp2[0]
        kh1.characters[id].maxap.value = maxap[0]
        kh1.characters[id].strength.value = strength[0]
        kh1.characters[id].defense.value = defense[0]
        kh1.characters[id].magic.value = sum(magic[0]) if len(magic[0]) > 0 else 0
    except:
        pass

@callback(
    Input({"type": "Weapon", "index": ALL}, "value"),
    Input({"type": "Accessory Slots", "index": ALL}, "value"),
    Input({"type": "Accessory", "index": ALL}, "value"),
    Input({"type": "Item Slots", "index": ALL}, "value"),
    Input({"type": "Item", "index": ALL}, "value"),
    State({"type": "Weapon", "index": ALL}, "id"),
)
def equipment_callback(weapon, accessoryslots, accessories, itemslots, items, ids):
    kh1 = utils.kh1
    id = kh1.character_dict[ids[0]["index"]]
    try:
        kh1.characters[id].weapon.value = weapon[0]
        kh1.characters[id].accessoryslots.value = accessoryslots[0]
        kh1.characters[id].itemslots.value = itemslots[0]
        for i in range(8):
            kh1.characters[id].accessories[i] = accessories[i]
            kh1.characters[id].items[i] = items[i]
    except:
        pass

@callback(
    Input({"type": "AbilityCheck", "index": ALL}, "value"),
    Input({"type": "Ability", "index": ALL}, "value"),
    State({"type": "AbilityCheck", "index": ALL}, "id"),
)
def ability_callback(checks, abilities, ids):
    kh1 = utils.kh1
    id = kh1.character_dict[ids[0]["index"].split(":")[0]]
    for i in range(48):
        check = 0
        if (len(checks[i]) == 0 or checks[i][-1] == 128):
            check = 128
        kh1.characters[id].abilities[i] = check + abilities[i]

@callback(
    Input("Circle Shortcut", "value"),
    Input("Triangle Shortcut", "value"),
    Input("Square Shortcut", "value"),
    Input({"type": "Magic Level", "index": ALL}, "value"),
    Input({"type": "Summon", "index": ALL}, "value"),
)
def customize_sora_callback(circle, triangle, square, magiclevels, summons):
    kh1 = utils.kh1
    kh1.shortcuts[0] = circle
    kh1.shortcuts[1] = triangle
    kh1.shortcuts[2] = square
    for i in range(7):
        kh1.magiclevels[i] = magiclevels[i]
        kh1.summons[i] = summons[i]

@callback(
    Input({"type": "SharedAbilityCheck", "index": ALL}, "value"),
    Input({"type": "SharedAbility", "index": ALL}, "value"),
)
def shared_ability_callback(checks, abilities):
    kh1 = utils.kh1
    for i in range(48):
        check = 0
        if (len(checks[i]) == 0 or checks[i][-1] == 128):
            check = 128
        kh1.shared_abilities[i] = check + abilities[i]
