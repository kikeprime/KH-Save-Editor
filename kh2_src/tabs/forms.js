export function create_forms() {
    const kh2div = document.getElementById("kh2div");
    const form_options = Object.entries(window.kh2.fm ? window.kh2.drive_form_fm_dict : window.kh2.drive_form_dict)
        .map(([label, value]) => `\n\t<option value=${value}>${label}</option>`)
        .join("");
    kh2div.innerHTML = `
    <div>
        <div style="display: flex; gap: 20px">
            <select id="kh2formtabs">
                ${form_options}
            </select>
            <select id="kh2formsubtabs">
                <option value="Stats">Stats</option>
                <option value="Abilities">Abilities</option>
            </select>
        </div>
        <div id="kh2formdiv"></div>
    </div>`;
    const kh2formtabs = document.getElementById("kh2formtabs");
    const kh2formsubtabs = document.getElementById("kh2formsubtabs");
    function tab_sel() {
        create_form(kh2formtabs.value, kh2formsubtabs.value);
    }
    kh2formtabs.addEventListener("change", tab_sel);
    kh2formsubtabs.addEventListener("change", tab_sel);
    tab_sel();
}

function create_form(id, tab) {
    switch (tab) {
        case "Stats": {
            create_stats(id);
            break;
        }
        case "Abilities": {
            create_abilities(id);
            break;
        }
        default: {
            const kh2formdiv = document.getElementById("kh2formdiv");
            kh2formdiv.innerHTML = "";
            break;
        }
    }
}

function create_stats(id) {
    const kh2formdiv = document.getElementById("kh2formdiv");
    const c = window.kh2.forms[id];
    const level = `
    <div>
        <h3>Form Level:</h3>
        <input
            type="number"
            id="level"
            min=1
            max=99
            step=1
            value=${c.level.value}
        >
    </div>`;
    const abilitylevel = `
    <div>
        <h3>Form Ability Level:</h3>
        <input
            type="number"
            id="abilitylevel"
            min=1
            max=3
            step=1
            value=${c.abilitylevel.value}
        >
    </div>`;
    const exp = `
    <div>
        <h3>${c.name != "Antiform" ? "EXP" : "Antipoints"}:</h3>
        <input
            type="number"
            id="exp"
            min=0
            max=${0xFFFFFFFF}
            step=1
            value=${c.exp.value}
        >
    </div>`;
    const weapon_options = window.kh2.weapon_dict["Sora"]
        .map((label) => `\n\t<option value=${window.kh2.item_dict[label]}>${label}</option>`)
        .join("");
    const weapon = `
    <div>
        <h3>Weapon:</h3>
        <select id="weapon">
            ${weapon_options}
        </select>
    </div>`;
    kh2formdiv.innerHTML = `
    <div>
        <div style="display: flex; gap: 20px">
            ${level}
            ${abilitylevel}
            ${exp}
        </div>
        ${weapon}
    </div>`;
    stats_callbacks(id);
}

function stats_callbacks(id) {
    const c = window.kh2.forms[id];
    const level = document.getElementById("level");
    level.addEventListener("change", () => {
        if (level.validity.valid)
            c.level.value = level.value;
        level.value = c.level.value;
    });
    const abilitylevel = document.getElementById("abilitylevel");
    abilitylevel.addEventListener("change", () => {
        if (abilitylevel.validity.valid)
            c.abilitylevel.value = abilitylevel.value;
        abilitylevel.value = c.abilitylevel.value;
    });
    const exp = document.getElementById("exp");
    exp.addEventListener("change", () => {
        if (exp.validity.valid)
            c.exp.value = exp.value;
        exp.value = c.exp.value;
    });
    const weapon = document.getElementById("weapon");
    weapon.value = c.weapon.value;
    weapon.addEventListener("change", () => {
        c.weapon.value = weapon.value;
    });
}

function equipment_callbacks(id) {
    const c = window.kh2.characters[id];
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
    const c = window.kh2.forms[id];
    const kh2formdiv = document.getElementById("kh2formdiv");
    const ability_options = window.kh2.ability_list
        .map((label) => `\n\t<option value=${window.kh2.item_dict[label]}>${label}</option>`)
        .join("");
    let abilities = "";
    for (let i = 0; i < c.abilities.length; i++) {
        const checked = c.abilities[i] & (1 << 15) ? "checked" : "";
        abilities += `
        <div style="display: flex; align-items: center">
            <input type="checkbox" value=${i} ${checked}>
            <select name=${i}>
                ${ability_options}
            </select>
        </div>`
    }
    kh2formdiv.innerHTML = `
    <div id="abilities">
        <h3>Abilities:</h3>
        ${abilities}
    </div>`;
    ability_callbacks(id);
}

function ability_callbacks(id) {
    const c = window.kh2.forms[id];
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
