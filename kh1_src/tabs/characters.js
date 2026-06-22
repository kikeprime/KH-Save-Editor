export function create_characters() {
    const kh1div = document.getElementById("kh1div");
    const ignored = new Set(["Winnie the Pooh", "None"]);
    const char_options = Object.entries(window.kh1.character_dict)
        .filter(([label]) => !ignored.has(label))
        .map(([label, value]) => `\n\t<option value=${value}>${label}</option>`)
        .join("");
    kh1div.innerHTML = `
    <div>
        <div style="display: flex; gap: 20px">
            <select id="kh1chartabs">
                ${char_options}
            </select>
            <select id="kh1charsubtabs">
                <option value="Stats">Stats</option>
                <option value="Equipment">Equipment</option>
                <option value="Abilities">Abilities</option>
                <option value="Customize">Customize</option>
                <option value="Shared Abilities">Shared Abilities</option>
            </select>
        </div>
        <div id="kh1chardiv"></div>
    </div>`;
    const kh1chartabs = document.getElementById("kh1chartabs");
    const kh1charsubtabs = document.getElementById("kh1charsubtabs");
    function tab_sel() {
        create_character(kh1chartabs.value, kh1charsubtabs.value);
    }
    kh1chartabs.addEventListener("change", tab_sel);
    kh1charsubtabs.addEventListener("change", tab_sel);
    create_character(kh1chartabs.value, kh1charsubtabs.value);
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
        default: {
            const kh1chardiv = document.getElementById("kh1chardiv");
            kh1chardiv.innerHTML = "";
            break;
        }
    }
}

function create_stats(id) {
    const kh1chardiv = document.getElementById("kh1chardiv");
    const c = window.kh1.characters[id];
    const exp = `
    <div>
        <h3>EXP:</h3>
        <input
            type="number"
            id="exp"
            min=0
            max=999999
            step=1
            value=${c.exp.value}
        >
    </div>`;
    const level = `
    <div>
        <h3>Level:</h3>
        <input
            type="number"
            id="level"
            min=1
            max=100
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
    const maxap = `
    <div>
        <h3>Max AP:</h3>
        <input
            type="number"
            id="maxap"
            min=0
            max=255
            step=1
            value=${c.maxap.value}
        >
    </div>`;
    const strength = `
    <div>
        <h3>Strength:</h3>
        <input
            type="number"
            id="strength"
            min=0
            max=255
            step=1
            value=${c.strength.value}
        >
    </div>`;
    const defense = `
    <div>
        <h3>Defense:</h3>
        <input
            type="number"
            id="defense"
            min=0
            max=255
            step=1
            value=${c.defense.value}
        >
    </div>`;
    function magcheck(b) {
        return c.magic.value & (1 << b) ? "checked" : "";
    }
    let magbox = "";
    for (let i = 0; i < 7; i++) {
        magbox += `
        <label style="display: flex; align-items: center">
            <input type="checkbox" value=${1 << i} ${magcheck(i)}>
            ${window.kh1.magicnames[i]}
        </label>`
    }
    const magic = `
    <div id="magic">
        <h3>Spells:</h3>
        ${magbox}
    </div>`;
    const res = Object.entries(window.kh1.resistance_dict)
        .map(([label, value]) => `
        <label style="display: flex; gap: 10px; align-items: center">
            ${label}: 
            <input
                type="number"
                min=-100
                max=100
                step=1
                value=${100 - c.resistances[value]}
                name=${value}
            > %
        </label>`)
        .join("");
    const resistances = `
    <div id="resistances">
        <h3>Resistances:</h3>
        ${res}
    </div>`;
    kh1chardiv.innerHTML = `
    <div>
        <div style="display: flex; gap: 20px">
            ${exp}
            ${level}
        </div>
        <div style="display: flex; gap: 20px">
            ${hp}
            ${maxhp}
        </div>
        <div style="display: flex; gap: 20px">
            ${mp}
            ${maxmp}
        </div>
        ${maxap}
        <div style="display: flex; gap: 20px">
            ${strength}
            ${defense}
        </div>
        ${magic}
        ${resistances}
    </div>`;
    stats_callbacks(id);
}

function stats_callbacks(id) {
    const c = window.kh1.characters[id];
    const exp = document.getElementById("exp");
    exp.addEventListener("change", () => {
        if (exp.validity.valid)
            c.exp.value = exp.value;
        exp.value = c.exp.value;
    });
    const level = document.getElementById("level");
    level.addEventListener("change", () => {
        if (level.validity.valid)
            c.level.value = level.value;
        level.value = c.level.value;
    });
    const magic = document.getElementById("magic");
    magic.addEventListener("change", (e) => {
        if (e.target.type === "checkbox") {
            if (e.target.checked)
                c.magic.value |= e.target.value
            else
                c.magic.value &= ~e.target.value
        }
    });
    const resistances = document.getElementById("resistances");
    resistances.addEventListener("change", (e) => {
        if (e.target.type === "number") {
            if (e.target.validity.valid)
                c.resistances[e.target.name] = 100 - e.target.value
            e.target.value = 100 - c.resistances[e.target.name]
        }
    });
}

function create_equipment(id) {
    const c = window.kh1.characters[id];
    const kh1chardiv = document.getElementById("kh1chardiv");
    const weapon_options = Object.entries(window.kh1.weapon_dict)
        .map(([label, value]) => `\n\t<option value=${value}>${label}</option>`)
        .join("");
    const accessory_options = Object.entries(window.kh1.accessory_dict)
        .map(([label, value]) => `\n\t<option value=${value}>${label}</option>`)
        .join("");
    const item_options = Object.entries(window.kh1.item1_dict)
        .filter(([label, value]) => value < 0x09)
        .map(([label, value]) => `\n\t<option value=${value}>${label}</option>`)
        .join("");
    const weapon = `
    <div>
        <h3>Weapon:</h3>
        <select id="weapon">
            ${weapon_options}
        </select>
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
    let accessory = "";
    let item = "";
    for (let i = 0; i < 8; i++) {
        accessory += `
        <select name=${i}>
            ${accessory_options}
        </select>`
        item += `
        <select name=${i}>
            ${item_options}
        </select>`
    }
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
    kh1chardiv.innerHTML = `
    <div>
        ${weapon}
        ${accessoryslots}
        ${accessories}
        ${itemslots}
        ${items}
    </div>`;
    equipment_callbacks(id);
}

function equipment_callbacks(id) {
    const c = window.kh1.characters[id];
    const weapon = document.getElementById("weapon");
    weapon.value = c.weapon.value;
    weapon.addEventListener("change", () => {
        c.weapon.value = weapon.value;
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
