from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh2_src.kh2_utils as utils


@callback(
    Output("CTabsDiv", "children"),
    Input("CTabs", "value"),
    Input("StatTabs", "value"),
)
def ctab_switch(id, tab):
    kh2 = utils.kh2
    c = kh2.characters[int(id)]
    if tab == "Stats":
        return __create_stats(c)
    if tab == "Equipment":
        return __create_equipment(c)
    if tab == "Abilities":
        return __create_abilities(c)
    if tab == "Customize":
        return __create_customize(c)

def __create_stats(c):
    kh2 = utils.kh2
    level = dcc.Input(
        id={"type": "Level", "index": c.name},
        type="number",
        value=c.level.value,
        min=1,
        max=99,
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
    apboost = dcc.Input(
        id={"type": "AP Boost", "index": c.name},
        type="number",
        value=c.apboost.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    strengthboost = dcc.Input(
        id={"type": "Strength Boost", "index": c.name},
        type="number",
        value=c.strengthboost.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    magicboost = dcc.Input(
        id={"type": "Magic Boost", "index": c.name},
        type="number",
        value=c.magicboost.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    defenseboost = dcc.Input(
        id={"type": "Defense Boost", "index": c.name},
        type="number",
        value=c.defenseboost.value,
        min=0,
        max=255,
        step=1,
        style={"width": 50},
    )
    return html.Div([
        html.Div([
            html.Div([dcc.Markdown("Level:"), level]),
            html.Div([dcc.Markdown("HP:"), hp]),
            html.Div([dcc.Markdown("MP:"), mp]),
            html.Div([dcc.Markdown("AP Boosts:"), apboost]),
            html.Div([dcc.Markdown("Strength Boosts:"), strengthboost]),
            html.Div([dcc.Markdown("Magic Boosts:"), magicboost]),
            html.Div([dcc.Markdown("Defense Boosts:"), defenseboost]),
        ]),
    ],
        style={"display": "flex"},
    )

def __create_equipment(c):
    kh2 = utils.kh2
    weapon = dcc.Dropdown(
        options=[
            {"label": k, "value": kh2.item_dict[k]}\
            for k in kh2.weapon_dict[c.name if c.name in kh2.weapon_dict else "Guest"]
        ],
        value=c.weapon.value,
        id={"type": "Weapon", "index": c.name},
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    armorslots = dcc.Input(
        id={"type": "Armor Slots", "index": c.name},
        type="number",
        value=c.armorslots.value,
        min=0,
        max=8,
        step=1,
        style={"width": 50},
    )
    armors = html.Div([
        dcc.Dropdown(
            options=[
                {"label": k, "value": kh2.item_dict[k]} for k in kh2.armor_list
            ],
            value=c.armors[i],
            id={"type": "Armor", "index": c.name + ":" + str(i)},
            searchable=False,
            clearable=False,
            style={"width": 200},
        ) for i in range(8)
    ])
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
                {"label": k, "value": kh2.item_dict[k]} for k in kh2.accessory_list
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
                {"label": k, "value": v} for k, v in kh2.item_dict.items() if v < 0x08
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
        html.Div([dcc.Markdown("Armor Slots:"), armorslots]),
        html.Div([dcc.Markdown("Armors:"), armors]),
        html.Div([dcc.Markdown("Accessory Slots:"), accessoryslots]),
        html.Div([dcc.Markdown("Accessories:"), accessories]),
        html.Div([dcc.Markdown("Item Slots:"), itemslots]),
        html.Div([dcc.Markdown("Items:"), items]),
    ])

def __create_abilities(c):
    kh2 = utils.kh2
    return html.Div([
        html.Div([
            dcc.Checklist(
                options=[{"label": "", "value": (1 << 15)}],
                value=[c.abilities[i] & (1 << 15)],
                id={"type": "AbilityCheck", "index": c.name + ":" + str(i)},
            ),
            dcc.Dropdown(
                options=[
                    {"label": k, "value": kh2.item_dict[k]}
                    for k in kh2.ability_list
                ],
                value=c.abilities[i] & ~(1 << 15),
                id={"type": "Ability", "index": c.name + ":" + str(i)},
                searchable=False,
                clearable=False,
                style={"width": 200},
            ),
        ],
            style={"display": "flex", "alignItems": "center"},
        ) for i in range(len(c.abilities)-2)
    ])

def __create_customize_sora(c):
    kh2 = utils.kh2
    circle = dcc.Dropdown(
        options=[
            {"label": k, "value": kh2.command_dict[k]}\
            for k in kh2.shortcut_list if kh2.version == 2 or k != "Limit Form"
        ],
        value=kh2.shortcuts[0],
        id="Circle Shortcut",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    triangle = dcc.Dropdown(
        options=[
            {"label": k, "value": kh2.command_dict[k]}\
            for k in kh2.shortcut_list if kh2.version == 2 or k != "Limit Form"
        ],
        value=kh2.shortcuts[1],
        id="Triangle Shortcut",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    square = dcc.Dropdown(
        options=[
            {"label": k, "value": kh2.command_dict[k]}\
            for k in kh2.shortcut_list if kh2.version == 2 or k != "Limit Form"
        ],
        value=kh2.shortcuts[2],
        id="Square Shortcut",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    cross = dcc.Dropdown(
        options=[
            {"label": k, "value": kh2.command_dict[k]}\
            for k in kh2.shortcut_list if kh2.version == 2 or k != "Limit Form"
        ],
        value=kh2.shortcuts[3],
        id="Cross Shortcut",
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    return html.Div([
        html.Div([html.H3("Shortcuts:")]),
        html.Div([dcc.Markdown("Circle:"), circle]),
        html.Div([dcc.Markdown("Triangle:"), triangle]),
        html.Div([dcc.Markdown("Square:"), square]),
        html.Div([dcc.Markdown("Cross:"), cross]),
    ])

def __create_customize(c):
    kh2 = utils.kh2
    autoreload = html.Div([
        dcc.Dropdown(
            options=[
                {"label": k, "value": v} for k, v in kh2.item_dict.items() if v < 0x08
            ],
            value=c.autoreload[i],
            id={"type": "AutoReload", "index": c.name + ":" + str(i)},
            searchable=False,
            clearable=False,
            style={"width": 200},
        ) for i in range(8)
    ])
    battlestyle = html.Div([
        dcc.Dropdown(
            options=[
                {"label": "Technic Attack", "value": 0x00},
                {"label": "Target Attack", "value": 0x01},
                {"label": "Huddle Attack", "value": 0x02},
                {"label": "Party Attack", "value": 0x03},
                {"label": "Sora Attack", "value": 0x04},
                {"label": "Relentless Attack", "value": 0x05},
            ],
            value=c.battlestyle.value,
            id={"type": "BattleStyle", "index": c.name},
            searchable=False,
            clearable=False,
            style={"width": 200},
        )
    ])
    abilitystyles = html.Div([
        dcc.Dropdown(
            options=[
                {"label": "Free", "value": 0x00},
                {"label": "Well-Balanced", "value": 0x01},
                {"label": "Rare", "value": 0x02},
            ],
            value=c.abilitystyles[i],
            id={"type": "AbilityStyle", "index": c.name + ":" + str(i)},
            searchable=False,
            clearable=False,
            style={"width": 200},
        ) for i in range(4)
    ])
    return html.Div([
        html.Div([dcc.Markdown("Auto-Reload:"), autoreload]),
        html.Div([
            html.Div([dcc.Markdown("Battle Style:"), battlestyle]),
            html.Div([dcc.Markdown("Ability Styles:"), abilitystyles]),
        ])  if c.name != "Sora" else None,
        __create_customize_sora(c) if c.name == "Sora" else None,
    ])

def create_characters():
    kh2 = utils.kh2
    ctabs = dcc.Tabs(id="CTabs", value="0")
    ctabs.children = [
        dcc.Tab(label=kh2.characters[i].name, value=f"{i}")\
        for i in range(len(kh2.characters))
    ]
    stattabs = dcc.Tabs(id="StatTabs", value="Stats")
    stattabs.children = [
        dcc.Tab(label="Stats", value="Stats"),
        dcc.Tab(label="Equipment", value="Equipment"),
        dcc.Tab(label="Abilities", value="Abilities"),
        dcc.Tab(label="Customize", value="Customize"),
    ]
    return html.Div([
        ctabs,
        stattabs,
        html.Div(id="CTabsDiv", style={"margin-top": 20})
    ])

@callback(
    Input({"type": "Level", "index": ALL}, "value"),
    Input({"type": "HP", "index": ALL}, "value"),
    Input({"type": "Max HP", "index": ALL}, "value"),
    Input({"type": "MP", "index": ALL}, "value"),
    Input({"type": "Max MP", "index": ALL}, "value"),
    Input({"type": "AP Boost", "index": ALL}, "value"),
    Input({"type": "Strength Boost", "index": ALL}, "value"),
    Input({"type": "Magic Boost", "index": ALL}, "value"),
    Input({"type": "Defense Boost", "index": ALL}, "value"),
    State({"type": "Level", "index": ALL}, "id"),
)
def stats_callback(
    level,
    hp, maxhp,
    mp, maxmp,
    apboost, strengthboost,
    magicboost, defenseboost,
    ids
):
    kh2 = utils.kh2
    id = kh2.character_dict[ids[0]["index"]]
    try:
        kh2.characters[id].level.value = level[0]
        kh2.characters[id].hp.value = hp[0]
        kh2.characters[id].maxhp.value = maxhp[0]
        kh2.characters[id].mp.value = mp[0]
        kh2.characters[id].maxmp.value = maxmp[0]
        kh2.characters[id].apboost.value = apboost[0]
        kh2.characters[id].strengthboost.value = strengthboost[0]
        kh2.characters[id].magicboost.value = magicboost[0]
        kh2.characters[id].defenseboost.value = defenseboost[0]
    except:
        pass

@callback(
    Input({"type": "Weapon", "index": ALL}, "value"),
    Input({"type": "Armor Slots", "index": ALL}, "value"),
    Input({"type": "Armors", "index": ALL}, "value"),
    Input({"type": "Accessory Slots", "index": ALL}, "value"),
    Input({"type": "Accessory", "index": ALL}, "value"),
    Input({"type": "Item Slots", "index": ALL}, "value"),
    Input({"type": "Item", "index": ALL}, "value"),
    State({"type": "Weapon", "index": ALL}, "id"),
)
def equipment_callback(weapon, armorslots, armors, accessoryslots, accessories, itemslots, items, ids):
    kh2 = utils.kh2
    id = kh2.character_dict[ids[0]["index"]]
    try:
        kh2.characters[id].weapon.value = weapon[0]
        kh2.characters[id].armorslots.value = armorslots[0]
        kh2.characters[id].accessoryslots.value = accessoryslots[0]
        kh2.characters[id].itemslots.value = itemslots[0]
        for i in range(8):
            kh2.characters[id].armors[i] = armors[i]
            kh2.characters[id].accessories[i] = accessories[i]
            kh2.characters[id].items[i] = items[i]
    except:
        pass

@callback(
    Input({"type": "AbilityCheck", "index": ALL}, "value"),
    Input({"type": "Ability", "index": ALL}, "value"),
    State({"type": "AbilityCheck", "index": ALL}, "id"),
)
def ability_callback(checks, abilities, ids):
    kh2 = utils.kh2
    id = kh2.character_dict[ids[0]["index"].split(":")[0]]
    for i in range(len(abilities)):
        check = (1 << 15) if (1 << 15) in checks[i] else 0
        kh2.characters[id].abilities[i] = check + abilities[i]

@callback(
    Input("Circle Shortcut", "value"),
    Input("Triangle Shortcut", "value"),
    Input("Square Shortcut", "value"),
    Input("Cross Shortcut", "value"),
)
def customize_sora_callback(circle, triangle, square, cross):
    kh2 = utils.kh2
    kh2.shortcuts[0] = circle
    kh2.shortcuts[1] = triangle
    kh2.shortcuts[2] = square
    kh2.shortcuts[3] = cross
