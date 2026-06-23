export function create_gummi() {
    const kh1div = document.getElementById("kh1div");
    kh1div.innerHTML = `
    <div>
        <div>
            <h3>Subtab:</h3>
            <select id="kh1gtabs">
                <option value="Ships">Ships</option>
                <option value="Gummi Inventory">Gummi Inventory</option>
                <option value="Control Config">Control Config</option>
            </select>
        </div>
        <div id="kh1gdiv"></div>
    </div>`;
    const kh1gtabs = document.getElementById("kh1gtabs");
    function tab_sel() {
        switch (kh1gtabs.value) {
            case "Ships": {
                create_gummi_ships();
                break;
            }
            case "Gummi Inventory": {
                create_gummi_inventory();
                break;
            }
            case "Control Config": {
                create_gummi_config();
                break;
            }
        }
    }
    kh1gtabs.addEventListener("change", tab_sel);
    tab_sel();
}

function create_gummi_ships() {
    const kh1gdiv = document.getElementById("kh1gdiv");
    kh1gdiv.innerHTML = "<h2>Coming Soon!</h2>The other 2 subtabs work.";
}

function create_gummi_inventory() {
    const kh1gdiv = document.getElementById("kh1gdiv");
    const cockpits = Object.entries(window.kh1.gummi_block_cockpit_dict)
        .map(([label, value]) => `
        <label style="display: flex; gap: 10px; align-items: center">
            ${label}: 
            <input
                type="number"
                min=0
                max=${window.kh1.gummi_max_list[value]}
                step=1
                value=${window.kh1.gummiblocks[value]}
                name=${value}
            >
        </label>`)
        .join("");
    const engines = Object.entries(window.kh1.gummi_block_engine_dict)
        .map(([label, value]) => `
        <label style="display: flex; gap: 10px; align-items: center">
            ${label}: 
            <input
                type="number"
                min=0
                max=${window.kh1.gummi_max_list[value]}
                step=1
                value=${window.kh1.gummiblocks[value]}
                name=${value}
            >
        </label>`)
        .join("");
    const armors = Object.entries(window.kh1.gummi_block_armor_dict)
        .map(([label, value]) => `
        <label style="display: flex; gap: 10px; align-items: center">
            ${label}: 
            <input
                type="number"
                min=0
                max=${window.kh1.gummi_max_list[value]}
                step=1
                value=${window.kh1.gummiblocks[value]}
                name=${value}
            >
        </label>`)
        .join("");
    const wings = Object.entries(window.kh1.gummi_block_wing_dict)
        .map(([label, value]) => `
        <label style="display: flex; gap: 10px; align-items: center">
            ${label}: 
            <input
                type="number"
                min=0
                max=${window.kh1.gummi_max_list[value]}
                step=1
                value=${window.kh1.gummiblocks[value]}
                name=${value}
            >
        </label>`)
        .join("");
    const specials = Object.entries(window.kh1.gummi_block_special_dict)
        .map(([label, value]) => `
        <label style="display: flex; gap: 10px; align-items: center">
            ${label}: 
            <input
                type="number"
                min=0
                max=${window.kh1.gummi_max_list[value]}
                step=1
                value=${window.kh1.gummiblocks[value]}
                name=${value}
            >
        </label>`)
        .join("");
    const weapons = Object.entries(window.kh1.gummi_block_weapon_dict)
        .map(([label, value]) => `
        <label style="display: flex; gap: 10px; align-items: center">
            ${label}: 
            <input
                type="number"
                min=0
                max=${window.kh1.gummi_max_list[value]}
                step=1
                value=${window.kh1.gummiblocks[value]}
                name=${value}
            >
        </label>`)
        .join("");
    const upgrades = Object.entries(window.kh1.gummi_block_upgrade_dict)
        .map(([label, value]) => `
        <label style="display: flex; gap: 10px; align-items: center">
            ${label}: 
            <input
                type="number"
                min=0
                max=${window.kh1.gummi_max_list[value]}
                step=1
                value=${window.kh1.gummiblocks[value]}
                name=${value}
            >
        </label>`)
        .join("");
    const blueprints = Object.entries(window.kh1.gummi_blueprint_dict)
        .map(([label, value]) => `
        <label style="display: flex; gap: 10px; align-items: center">
            ${label}: 
            <input
                type="number"
                min=0
                max=1
                step=1
                value=${window.kh1.gummiblocks[value]}
                name=${value}
            >
        </label>`)
        .join("");
    const blueprints_fm = !window.kh1.fm ? "" : Object.entries(window.kh1.gummi_blueprint_fm_dict)
        .map(([label, value]) => `
        <label style="display: flex; gap: 10px; align-items: center">
            ${label}: 
            <input
                type="number"
                min=0
                max=1
                step=1
                value=${window.kh1.gummiblocks[value]}
                name=${value}
            >
        </label>`)
        .join("");
    const designs = !window.kh1.fm ? "" : Object.entries(window.kh1.gummi_block_design_dict)
        .map(([label, value]) => `
        <label style="display: flex; gap: 10px; align-items: center">
            ${label}: 
            <input
                type="number"
                min=0
                max=99
                step=1
                value=${window.kh1.gummiblocks[value]}
                name=${value}
            >
        </label>`)
        .join("");
    const gummiblocks_fm = `
    <div>
        <h3>Final Mix Blueprints:</h3>
            ${blueprints_fm}
        <h3>Design Gummies:</h3>
            ${designs}
    </div>`;
    kh1gdiv.innerHTML = `
    <div id="gummiblocks">
        <h3>Cockpits:</h3>
            ${cockpits}
        <h3>Engines:</h3>
            ${engines}
        <h3>Armors:</h3>
            ${armors}
        <h3>Wings:</h3>
            ${wings}
        <h3>Specials:</h3>
            ${specials}
        <h3>Weapons:</h3>
            ${weapons}
        <h3>Upgrades:</h3>
            ${upgrades}
        <h3>Blueprints:</h3>
            ${blueprints}
        ${window.kh1.fm ? gummiblocks_fm : ""}
    </div>`;
    gummi_inventory_callbacks();
}

function gummi_inventory_callbacks() {
    const gummiblocks = document.getElementById("gummiblocks");
    gummiblocks.addEventListener("change", (e) => {
        if (e.target.validity.valid)
            kh1.gummiblocks[e.target.name] = e.target.value;
        e.target.value = kh1.gummiblocks[e.target.name];
    });
}

function create_gummi_config() {
    const kh1gdiv = document.getElementById("kh1gdiv");
    const config_options = {
        "Circle": 0x20,
        "Triangle": 0x10,
        "Square": 0x80,
        "Cross": 0x40,
        "L1": 4,
        "L2": 1,
        "R1": 8,
        "R2": 2,
    }
    const options = Object.entries(config_options)
        .map(([label, value]) => `\n\t<option value=${value}>${label}</option>`)
        .join("");
    const decelerate = `
    <select id="decelerate">
        ${options}
    </select>`;
    const accelerate = `
    <select id="accelerate">
        ${options}
    </select>`;
    const transform = `
    <select id="transform">
        ${options}
    </select>`;
    const scannon = `
    <select id="scannon">
        ${options}
    </select>`;
    const mcannon = `
    <select id="mcannon">
        ${options}
    </select>`;
    const lcannon = `
    <select id="lcannon">
        ${options}
    </select>`;
    const slaser = `
    <select id="slaser">
        ${options}
    </select>`;
    const mlaser = `
    <select id="mlaser">
        ${options}
    </select>`;
    const llaser = `
    <select id="llaser">
        ${options}
    </select>`;
    kh1gdiv.innerHTML = `
    <div>
        <h3>Decelerate:</h3>
            ${decelerate}
        <h3>Accelerate:</h3>
            ${accelerate}
        <h3>Transform:</h3>
            ${transform}
        <h3>Small Cannon:</h3>
            ${scannon}
        <h3>Mid Cannon:</h3>
            ${mcannon}
        <h3>Large Cannon:</h3>
            ${lcannon}
        <h3>Small Laser:</h3>
            ${slaser}
        <h3>Mid Laser:</h3>
            ${mlaser}
        <h3>Large Laser:</h3>
            ${llaser}
    </div>`;
    gummi_config_callbacks();
}

function gummi_config_callbacks() {
    const decelerate = document.getElementById("decelerate");
    decelerate.value = window.kh1.gummi_decelerate.value;
    decelerate.addEventListener("change", () => {
        window.kh1.gummi_decelerate.value = decelerate.value;
    });
    const accelerate = document.getElementById("accelerate");
    accelerate.value = window.kh1.gummi_accelerate.value;
    accelerate.addEventListener("change", () => {
        window.kh1.gummi_accelerate.value = accelerate.value;
    });
    const transform = document.getElementById("transform");
    transform.value = window.kh1.gummi_transform.value;
    transform.addEventListener("change", () => {
        window.kh1.gummi_transform.value = transform.value;
    });
    const scannon = document.getElementById("scannon");
    scannon.value = window.kh1.gummi_scannon.value;
    scannon.addEventListener("change", () => {
        window.kh1.gummi_scannon.value = scannon.value;
    });
    const mcannon = document.getElementById("mcannon");
    mcannon.value = window.kh1.gummi_mcannon.value;
    mcannon.addEventListener("change", () => {
        window.kh1.gummi_mcannon.value = mcannon.value;
    });
    const lcannon = document.getElementById("lcannon");
    lcannon.value = window.kh1.gummi_lcannon.value;
    lcannon.addEventListener("change", () => {
        window.kh1.gummi_lcannon.value = lcannon.value;
    });
    const slaser = document.getElementById("slaser");
    slaser.value = window.kh1.gummi_slaser.value;
    slaser.addEventListener("change", () => {
        window.kh1.gummi_slaser.value = slaser.value;
    });
    const mlaser = document.getElementById("mlaser");
    mlaser.value = window.kh1.gummi_mlaser.value;
    mlaser.addEventListener("change", () => {
        window.kh1.gummi_mlaser.value = mlaser.value;
    });
    const llaser = document.getElementById("llaser");
    llaser.value = window.kh1.gummi_llaser.value;
    llaser.addEventListener("change", () => {
        window.kh1.gummi_llaser.value = llaser.value;
    });
}
