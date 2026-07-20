export function create_characters() {
    const kh2div = document.getElementById("kh2div");
    const char_options = Object.entries(window.kh2.character_dict)
        .map(([label, value]) => `\n\t<option value=${value}>${label}</option>`)
        .join("");
    kh2div.innerHTML = `
    <div>
        <div style="display: flex; gap: 20px">
            <select id="kh2chartabs">
                ${char_options}
            </select>
            <select id="kh2charsubtabs">
                <option value="Stats">Stats</option>
                <option value="Equipment">Equipment</option>
                <option value="Abilities">Abilities</option>
                <option value="Customize">Customize</option>
            </select>
        </div>
        <div id="kh2chardiv"></div>
    </div>`;
    const kh2chartabs = document.getElementById("kh2chartabs");
    const kh2charsubtabs = document.getElementById("kh2charsubtabs");
    function tab_sel() {
        create_character(kh2chartabs.value, kh2charsubtabs.value);
    }
    kh2chartabs.addEventListener("change", tab_sel);
    kh2charsubtabs.addEventListener("change", tab_sel);
    create_character(kh2chartabs.value, kh2charsubtabs.value);
}

function create_character(id, tab) {
    switch (tab) {
        case "Stats": {
            create_stats(id);
            break;
        }
        case "Equipment": {
            create_equipment(id);
            break;
        }
        case "Abilities": {
            create_abilities(id);
            break;
        }
        case "Customize": {
            create_customize(id);
            break;
        }
        default: {
            const kh2chardiv = document.getElementById("kh2chardiv");
            kh2chardiv.innerHTML = "";
            break;
        }
    }
}

function create_stats(id) {
    const kh2chardiv = document.getElementById("kh2chardiv");
    const c = window.kh2.characters[id];
    const level = `
    <div>
        <h3>Level:</h3>
        <input
            type="number"
            id="level"
            min=1
            max=99
            step=1
            value=${c.level.value}
        >
    </div>`;
    const hp = `
    <div>
        <h3>HP:</h3>
        <input
            type="number"
            id="hp"
            min=0
            max=255
            step=1
            value=${c.hp.value}
        >
    </div>`;
    const maxhp = `
    <div>
        <h3>Max HP:</h3>
        <input
            type="number"
            id="maxhp"
            min=0
            max=255
            step=1
            value=${c.maxhp.value}
        >
    </div>`;
    const mp = `
    <div>
        <h3>MP:</h3>
        <input
            type="number"
            id="mp"
            min=0
            max=255
            step=1
            value=${c.mp.value}
        >
    </div>`;
    const maxmp = `
    <div>
        <h3>Max MP:</h3>
        <input
            type="number"
            id="maxmp"
            min=0
            max=255
            step=1
            value=${c.maxmp.value}
        >
    </div>`;
    const apboost = `
    <div>
        <h3>AP Boosts:</h3>
        <input
            type="number"
            id="apboost"
            min=0
            max=255
            step=1
            value=${c.apboost.value}
        >
    </div>`;
    const strengthboost = `
    <div>
        <h3>Strength Boosts:</h3>
        <input
            type="number"
            id="strengthboost"
            min=0
            max=255
            step=1
            value=${c.strengthboost.value}
        >
    </div>`;
    const magicboost = `
    <div>
        <h3>Magic Boosts:</h3>
        <input
            type="number"
            id="magicboost"
            min=0
            max=255
            step=1
            value=${c.magicboost.value}
        >
    </div>`;
    const defenseboost = `
    <div>
        <h3>Defense Boosts:</h3>
        <input
            type="number"
            id="defenseboost"
            min=0
            max=255
            step=1
            value=${c.defenseboost.value}
        >
    </div>`;
    kh2chardiv.innerHTML = `
    <div>
        ${level}
        <div style="display: flex; gap: 20px">
            ${hp}
            ${maxhp}
        </div>
        <div style="display: flex; gap: 20px">
            ${mp}
            ${maxmp}
        </div>
        <div style="display: flex; gap: 20px">
            ${strengthboost}
            ${magicboost}
        </div>
        <div style="display: flex; gap: 20px">
            ${apboost}
            ${defenseboost}
        </div>
    </div>`;
    stats_callbacks(id);
}

function stats_callbacks(id) {
    const c = window.kh2.characters[id];
    const level = document.getElementById("level");
    level.addEventListener("change", () => {
        if (level.validity.valid)
            c.level.value = level.value;
        level.value = c.level.value;
    });
    const hp = document.getElementById("hp");
    hp.addEventListener("change", () => {
        if (hp.validity.valid)
            c.hp.value = hp.value;
        hp.value = c.hp.value;
    });
    const maxhp = document.getElementById("maxhp");
    maxhp.addEventListener("change", () => {
        if (maxhp.validity.valid)
            c.maxhp.value = maxhp.value;
        maxhp.value = c.maxhp.value;
    });
    const mp = document.getElementById("mp");
    mp.addEventListener("change", () => {
        if (mp.validity.valid)
            c.mp.value = mp.value;
        mp.value = c.mp.value;
    });
    const maxmp = document.getElementById("maxmp");
    maxmp.addEventListener("change", () => {
        if (maxmp.validity.valid)
            c.maxmp.value = maxmp.value;
        maxmp.value = c.maxmp.value;
    });
    const strengthboost = document.getElementById("strengthboost");
    strengthboost.addEventListener("change", () => {
        if (strengthboost.validity.valid)
            c.strengthboost.value = strengthboost.value;
        strengthboost.value = c.strengthboost.value;
    });
    const magicboost = document.getElementById("magicboost");
    magicboost.addEventListener("change", () => {
        if (magicboost.validity.valid)
            c.magicboost.value = magicboost.value;
        magicboost.value = c.magicboost.value;
    });
    const apboost = document.getElementById("apboost");
    apboost.addEventListener("change", () => {
        if (apboost.validity.valid)
            c.apboost.value = apboost.value;
        apboost.value = c.apboost.value;
    });
    const defenseboost = document.getElementById("defenseboost");
    defenseboost.addEventListener("change", () => {
        if (defenseboost.validity.valid)
            c.defenseboost.value = defenseboost.value;
        defenseboost.value = c.defenseboost.value;
    });
}

function create_equipment(id) {
    const c = window.kh2.characters[id];
    const kh2chardiv = document.getElementById("kh2chardiv");
    const weapon_options = window.kh2.weapon_dict[c.name]
        .map((label) => `\n\t<option value=${window.kh2.item_dict[label]}>${label}</option>`)
        .join("");
    const armor_options = window.kh2.armor_list
        .map((label) => `\n\t<option value=${window.kh2.item_dict[label]}>${label}</option>`)
        .join("");
    const accessory_options = window.kh2.accessory_list
        .map((label) => `\n\t<option value=${window.kh2.item_dict[label]}>${label}</option>`)
        .join("");
    const item_options = Object.entries(window.kh2.item_dict)
        .filter(([label, value]) => value < 0x08)
        .map(([label, value]) => `\n\t<option value=${value}>${label}</option>`)
        .join("");
    const weapon = `
    <div>
        <h3>Weapon:</h3>
        <select id="weapon">
            ${weapon_options}
        </select>
    </div>`;
    const armorslots = `
    <div>
        <h3>Armor Slots:</h3>
        <input
            type="number"
            id="armorslots"
            min=0
            max=8
            step=1
            value=${c.armorslots.value}
        >
    </div>`;
    let armor = "";
    let accessory = "";
    let item = "";
    for (let i = 0; i < 8; i++) {
        armor += `
        <select name=${i}>
            ${armor_options}
        </select>`;
        accessory += `
        <select name=${i}>
            ${accessory_options}
        </select>`;
        item += `
        <select name=${i}>
            ${item_options}
        </select>`;
    }
    const armors = `
    <div id="armors">
        <h3>Armors:</h3>
        ${armor}
    </div>`;
    const accessoryslots = `
    <div>
        <h3>Accessory Slots:</h3>
        <input
            type="number"
            id="accessoryslots"
            min=0
            max=8
            step=1
            value=${c.accessoryslots.value}
        >
    </div>`;
    const accessories = `
    <div id="accessories">
        <h3>Accessories:</h3>
        ${accessory}
    </div>`;
    const itemslots = `
    <div>
        <h3>Item Slots:</h3>
        <input
            type="number"
            id="itemslots"
            min=0
            max=8
            step=1
            value=${c.itemslots.value}
        >
    </div>`;
    const items = `
    <div id="items">
        <h3>Items:</h3>
        ${item}
    </div>`;
    kh2chardiv.innerHTML = `
    ${weapon}
    <div style="display: flex; gap: 20px">
        <div>
            ${armorslots}
            ${armors}
        </div>
        <div>
            ${accessoryslots}
            ${accessories}
        </div>
        <div>
            ${itemslots}
            ${items}
        </div>
    </div>`;
    equipment_callbacks(id);
}

function equipment_callbacks(id) {
    const c = window.kh2.characters[id];
    const weapon = document.getElementById("weapon");
    weapon.value = c.weapon.value;
    weapon.addEventListener("change", () => {
        c.weapon.value = weapon.value;
    });
    const armorslots = document.getElementById("armorslots");
    armorslots.addEventListener("change", () => {
        if (armorslots.validity.valid)
            c.armorslots.value = armorslots.value;
        armorslots.value = c.armorslots.value;
    });
    const armors = document.getElementById("armors");
    armors.querySelectorAll("select").forEach(select => {
        select.value = c.armors[select.name]; 
    });
    armors.addEventListener("change", (e) => {
        c.armors[e.target.name] = e.target.value
    });
    const accessoryslots = document.getElementById("accessoryslots");
    accessoryslots.addEventListener("change", () => {
        if (accessoryslots.validity.valid)
            c.accessoryslots.value = accessoryslots.value;
        accessoryslots.value = c.accessoryslots.value;
    });
    const accessories = document.getElementById("accessories");
    accessories.querySelectorAll("select").forEach(select => {
        select.value = c.accessories[select.name]; 
    });
    accessories.addEventListener("change", (e) => {
        c.accessories[e.target.name] = e.target.value
    });
    const itemslots = document.getElementById("itemslots");
    itemslots.addEventListener("change", () => {
        if (itemslots.validity.valid)
            c.itemslots.value = itemslots.value;
        itemslots.value = c.itemslots.value;
    });
    const items = document.getElementById("items");
    items.querySelectorAll("select").forEach(select => {
        select.value = c.items[select.name]; 
    });
    items.addEventListener("change", (e) => {
        c.items[e.target.name] = e.target.value
    });
}

function create_abilities(id) {
    const c = window.kh2.characters[id];
    const kh2chardiv = document.getElementById("kh2chardiv");
    const ability_options = window.kh2.ability_list
        .map((label) => `\n\t<option value=${window.kh2.item_dict[label]}>${label}</option>`)
        .join("");
    let abilities = "";
    for (let i = 0; i < c.abilities.length - 2; i++) {
        const checked = c.abilities[i] & (1 << 15) ? "checked" : "";
        abilities += `
        <div style="display: flex; align-items: center">
            <input type="checkbox" value=${i} ${checked}>
            <select name=${i}>
                ${ability_options}
            </select>
        </div>`
    }
    kh2chardiv.innerHTML = `
    <div id="abilities">
        <h3>Abilities:</h3>
        ${abilities}
    </div>`;
    ability_callbacks(id);
}

function ability_callbacks(id) {
    const c = window.kh2.characters[id];
    const abilities = document.getElementById("abilities");
    abilities.querySelectorAll("select").forEach(select => {
        select.value = c.abilities[select.name] & ~(1 << 15);
    });
    abilities.addEventListener("change", (e) => {
        if (e.target.type != "checkbox") {
            const checked = c.abilities[e.target.name] & (1 << 15);
            c.abilities[e.target.name] = e.target.value;
            if (checked)
                c.abilities[e.target.name] |= (1 << 15);
        }
        else {
            if (e.target.checked)
                c.abilities[e.target.value] |= (1 << 15);
            else
                c.abilities[e.target.value] &= ~(1 << 15);
        }
    });
}

function create_customize(id) {
    const c = window.kh2.characters[id];
    const kh2chardiv = document.getElementById("kh2chardiv");
    const item_options = Object.entries(window.kh2.item_dict)
        .filter(([label, value]) => value < 0x08)
        .map(([label, value]) => `\n\t<option value=${value}>${label}</option>`)
        .join("");
    let item = "";
    for (let i = 0; i < 8; i++) {
        item += `
        <select name=${i}>
            ${item_options}
        </select>`;
    }
    const autoreload = `
    <div id="autoreload">
        <h3>Auto-Reload:</h3>
        ${item}
    </div>`;
    let abilitystyle = "";
    for (let i = 0; i < 4; i++) {
        abilitystyle += `
        <select name=${i}>
            <option value=0>Free</option>
            <option value=1>Well-Balanced</option>
            <option value=2>Rare</option>
        </select>`;
    }
    const battlestyle = `
    <div>
        <h3>Battle Style:</h3>
        <select id="battlestyle">
            <option value=0>Technic Attack</option>
            <option value=1>Target Attack</option>
            <option value=2>Huddle Attack</option>
            <option value=3>Party Attack</option>
            <option value=4>Sora Attack</option>
            <option value=5>Relentless Attack</option>
        </select>
    </div>`;
    const abilitystyles = `
    <div id="abilitystyles">
        <h3>Ability Styles:</h3>
        ${abilitystyle}
    </div>`;
    const shortcut_options = window.kh2.shortcut_list
        .filter((label) => window.kh2.fm || label != "Limit Form")
        .map((label) => `\n\t<option value=${window.kh2.command_dict[label]}>${label}</option>`)
        .join("");
    const shortcuts = `
    <h3 style="margin-bottom: 0px">Shortcuts:</h3>
    <div id="shortcuts" style="display: flex; gap: 20px">
        <div>
            <h4>Circle:</h4>
            <select name=0>
                ${shortcut_options}
            </select>
        </div>
        <div>
            <h4>Triangle:</h4>
            <select name=1>
                ${shortcut_options}
            </select>
        </div>
        <div>
            <h4>Square:</h4>
            <select name=2>
                ${shortcut_options}
            </select>
        </div>
        <div>
            <h4>Cross:</h4>
            <select name=3>
                ${shortcut_options}
            </select>
        </div>
    </div>`;
    kh2chardiv.innerHTML = `
    <div>
        <div style="display: flex; gap: 20px">
            ${autoreload}
            <div>
                ${battlestyle}
                ${abilitystyles}
            </div>
        </div>
        ${id == 0 ? shortcuts : ""}
    </div>`;
    customize_callbacks(id);
    if (id == 0)
        customize_sora_callbacks();
}

function customize_callbacks(id) {
    const c = window.kh2.characters[id];
    const autoreload = document.getElementById("autoreload");
    autoreload.querySelectorAll("select").forEach(select => {
        select.value = c.autoreload[select.name]; 
    });
    autoreload.addEventListener("change", (e) => {
        c.autoreload[e.target.name] = e.target.value
    });
    const abilitystyles = document.getElementById("abilitystyles");
    abilitystyles.querySelectorAll("select").forEach(select => {
        select.value = c.abilitystyles[select.name]; 
    });
    abilitystyles.addEventListener("change", (e) => {
        c.abilitystyles[e.target.name] = e.target.value
    });
    const battlestyle = document.getElementById("battlestyle");
    battlestyle.value = c.battlestyle.value;
    battlestyle.addEventListener("change", () => {
        c.battlestyle.value = battlestyle.value
    });
}

function customize_sora_callbacks() {
    const shortcuts = document.getElementById("shortcuts");
    shortcuts.querySelectorAll("select").forEach(select => {
        select.value = window.kh2.shortcuts[select.name]; 
    });
    shortcuts.addEventListener("change", (e) => {
        window.kh2.shortcuts[e.target.name] = e.target.value
    });
}
