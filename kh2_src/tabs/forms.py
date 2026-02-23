from dash import Dash, html, dcc, callback, Input, Output, State, ALL
import kh2_src.kh2_utils as utils


@callback(
    Output("FTabsDiv", "children"),
    Input("FTabs", "value"),
    Input("FStatTabs", "value"),
)
def ftab_switch(id, tab):
    kh2 = utils.kh2
    c = kh2.forms[int(id)]
    if tab == "Stats":
        return __create_stats(c)
    if tab == "Abilities":
        return __create_abilities(c)

def __create_stats(c):
    kh2 = utils.kh2
    level = dcc.Input(
        id={"type": "Form Level", "index": c.name},
        type="number",
        value=c.level.value,
        min=1,
        max=99,
        step=1,
        style={"width": 50},
    )
    abilitylevel = dcc.Input(
        id={"type": "Form Ability Level", "index": c.name},
        type="number",
        value=c.abilitylevel.value,
        min=1,
        max=3,
        step=1,
        style={"width": 50},
    )
    exp = dcc.Input(
        id={"type": "Form EXP", "index": c.name},
        type="number",
        value=c.exp.value,
        min=0,
        max=0xFFFFFFFF,
        step=1,
        style={"width": 50},
    )
    weapon = dcc.Dropdown(
        options=[
            {"label": k, "value": kh2.item_dict[k]}\
            for k in kh2.weapon_dict["Sora"]
        ],
        value=c.weapon.value,
        id={"type": "Form Weapon", "index": c.name},
        searchable=False,
        clearable=False,
        style={"width": 200},
    )
    return html.Div([
        html.Div([
            html.Div([dcc.Markdown("Level:"), level]),
            html.Div([dcc.Markdown("Ability Level:"), abilitylevel]),
        ],
            style={"display": "flex", "gap": 20},
        ),
        html.Div([dcc.Markdown("EXP:"), exp]),
        html.Div([dcc.Markdown("Weapon:"), weapon]),
    ])

def __create_abilities(c):
    kh2 = utils.kh2
    return html.Div([
        html.Div([
            dcc.Checklist(
                options=[{"label": "", "value": (1 << 15)}],
                value=[c.abilities[i] & (1 << 15)],
                id={"type": "FormAbilityCheck", "index": c.name + ":" + str(i)},
            ),
            dcc.Dropdown(
                options=[
                    {"label": k, "value": kh2.item_dict[k]}
                    for k in kh2.ability_list
                ],
                value=c.abilities[i] & ~(1 << 15),
                id={"type": "FormAbility", "index": c.name + ":" + str(i)},
                searchable=False,
                clearable=False,
                style={"width": 200},
            ),
        ],
            style={"display": "flex", "alignItems": "center"},
        ) for i in range(len(c.abilities))
    ])

def create_forms():
    kh2 = utils.kh2
    ftabs = dcc.Tabs(id="FTabs", value="0")
    ftabs.children = [
        dcc.Tab(label=kh2.forms[i].name, value=f"{i}")\
        for i in range(len(kh2.forms)) if "Unused" not in kh2.forms[i].name
    ]
    stattabs = dcc.Tabs(id="FStatTabs", value="Stats")
    stattabs.children = [
        dcc.Tab(label="Stats", value="Stats"),
        dcc.Tab(label="Abilities", value="Abilities"),
    ]
    return html.Div([
        ftabs,
        stattabs,
        html.Div(id="FTabsDiv", style={"margin-top": 20})
    ])

@callback(
    Input({"type": "Form Level", "index": ALL}, "value"),
    Input({"type": "Form Ability Level", "index": ALL}, "value"),
    Input({"type": "Form EXP", "index": ALL}, "value"),
    Input({"type": "Form Weapon", "index": ALL}, "value"),
    State({"type": "Form Level", "index": ALL}, "id"),
)
def fstats_callback(
    level,
    abilitylevel,
    exp,
    weapon,
    ids,
):
    kh2 = utils.kh2
    id = kh2.drive_form_dict[ids[0]["index"]] if kh2.version < 2\
    else kh2.drive_form_fm_dict[ids[0]["index"]]
    try:
        kh2.forms[id].level.value = level[0]
        kh2.forms[id].abilitylevel.value = abilitylevel[0]
        kh2.forms[id].exp.value = exp[0]
        kh2.forms[id].weapon.value = weapon[0]
    except:
        pass

@callback(
    Input({"type": "FormAbilityCheck", "index": ALL}, "value"),
    Input({"type": "FormAbility", "index": ALL}, "value"),
    State({"type": "FormAbilityCheck", "index": ALL}, "id"),
)
def fability_callback(checks, abilities, ids):
    kh2 = utils.kh2
    id = kh2.drive_form_dict[ids[0]["index"].split(":")[0]] if kh2.version < 2\
    else kh2.drive_form_fm_dict[ids[0]["index"].split(":")[0]]
    for i in range(len(abilities)):
        check = (1 << 15) if (1 << 15) in checks[i] else 0
        kh2.forms[id].abilities[i] = check + abilities[i]
