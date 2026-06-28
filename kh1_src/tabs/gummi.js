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
    let ship_options = "";
    for (let i = 0; i < 10; i++) {
        ship_options += `<option value=${i}>Gummi Ship ${i + 1}</option>`;
    }
    kh1gdiv.innerHTML = `
    <div>
        <h3>Selected Gummi Ship:</h3>
        <select id="selectedship">
            ${ship_options}
        </select>
        <h3>Ship:</h3>
        <select id="kh1gshtabs">
            ${ship_options}
        </select>
        <div id="kh1gshdiv"></div>
    </div>`;
    const kh1gshtabs = document.getElementById("kh1gshtabs");
    function tab_sel() {
        create_ship(kh1gshtabs.value);
    }
    kh1gshtabs.addEventListener("change", tab_sel);
    tab_sel();
    
    const selectedship = document.getElementById("selectedship");
    selectedship.value = window.kh1.selectedship.value;
    selectedship.addEventListener("change", () => {
        window.kh1.selectedship.value = selectedship.value;
    });
}

function create_ship(idx) {
    const kh1gshdiv = document.getElementById("kh1gshdiv");
    const ship = window.kh1.gummiships[idx];
    const blockcount = `
    <div>
        <h3>Block Count:</h3>
        <input
            type="number"
            id="blockcount"
            min=0
            max=200
            step=1
            value=${ship.blockcount.value}
        >
    </div>`;
    const area = `
    <h3>Assembly Area:</h3>
    <div id="assemblyarea" style="display: flex; align-items: center; gap: 10px">
        <h4>X:</h4>
        <input
            type="number"
            name=x
            min=0
            max=10
            step=1
            value=${ship.x.value}
        >
        <h4>Y:</h4>
        <input
            type="number"
            name=y
            min=0
            max=10
            step=1
            value=${ship.y.value}
        >
        <h4>Z:</h4>
        <input
            type="number"
            name=z
            min=0
            max=10
            step=1
            value=${ship.z.value}
        >
    </div>`;
    let ship_options = "<option value=0>No Pair</option>";
    for (let i = 0; i < 10; i++) {
        ship_options += `<option value=${i + 1}>Gummi Ship ${i + 1}</option>`;
    }
    const transformpair = `
    <div>
        <h3>Transform Pair:</h3>
        <select id="transformpair">
            ${ship_options}
        </select>
    </div>`;
    const name = `
    <div>
        <h3>Name:</h3>
        <input
            type="text"
            id="ship_name"
            value="${ship.name.decode()}"
        >
    </div>`;
    let block_options = "";
    for (let i = 0; i < 200; i++) {
        block_options += `<option value=${i}>Block ${i + 1}</option>`;
    }
    kh1gshdiv.innerHTML = `
    <div>
        ${blockcount}
        ${area}
        ${transformpair}
        ${name}
        <h3>Gummi Block:</h3>
        <select id="kh1gbtabs">
            ${block_options}
        </select>
        <div id="kh1gbdiv"></div>
    </div>`;
    gummi_ship_callbacks(ship);
    const kh1gbtabs = document.getElementById("kh1gbtabs");
    function tab_sel() {
        create_block(ship, kh1gbtabs.value);
    }
    kh1gbtabs.addEventListener("change", tab_sel);
    tab_sel();
}

function create_block(ship, idx) {
    const kh1gbdiv = document.getElementById("kh1gbdiv");
    const block = ship.blocks[idx];
    const block_type_options = Object.entries(window.kh1.gummi_block_dict)
        .map(([value, label]) => `<option value=${value}>${label}</option>`)
        .join("");
    const block_type = `
    <h3>Block Type:</h3>
    <select id="block_type">
        ${block_type_options}
    </select>`;
    const block_coordinates = `
    <h3>Coordinates:</h3>
    <div id="block_coordinates" style="display: flex; align-items: center; gap: 10px">
        <h4>X:</h4>
        <input
            type="number"
            name=x
            min=0
            max=9
            step=1
            value=${block.x}
        >
        <h4>Y:</h4>
        <input
            type="number"
            name=y
            min=0
            max=255
            step=1
            value=${block.y.value}
        >
        <h4>Z:</h4>
        <input
            type="number"
            name=z
            min=0
            max=9
            step=1
            value=${block.z}
        >
    </div>`;
    const rotation_dict = {
        "Normal": 0x0420,
        "Left": 0x0124,
        "Right": 0x0025,
        "Back": 0x0521,
        "Up": 0x0250,
        "Down": 0x0340,
        "Up Up or Down Down": 0x0530,
        "Tilt Left": 0x0412,
        "Tilt Right": 0x0403,
        "Upside Down": 0x0431,
        "Left then Up": 0x0204,
        "Left then Down": 0x0314,
        "Left then Up Up": 0x0034,
        "Left then Tilt Left": 0x0252,
        "Left then Tilt Right": 0x0143,
        "Right then Up": 0x0215,
        "Right then Down": 0x0305,
        "Right then Up Up": 0x0135,
        "Right then Tilt Left": 0x0042,
        "Right then Tilt Right": 0x0053,
        "Back then Up": 0x0241,
        "Back then Down": 0x0351,
        "Back then Tilt Left": 0x0502,
        "Back then Tilt Right": 0x0513,
        "None-G": 0x0000,
    };
    const rotation_options = Object.entries(rotation_dict)
        .map(([label, value]) => `<option value=${value}>${label}</option>`)
        .join("");
    const rotation = `
    <h3>Orientation:</h3>
    <select id="block_r">
        ${rotation_options}
    </select>`;
    const color = `
    <h3>Color:</h3>
    <input
        type="number"
        id="block_color"
        min=0
        max=63
        step=1
        value=${block.color.value}
    >`;
    kh1gbdiv.innerHTML = `
    <div>
        ${block_type}
        ${block_coordinates}
        ${rotation}
        ${color}
    </div>`;
    gummi_block_callbacks(block);
}

function gummi_ship_callbacks(ship) {
    const blockcount = document.getElementById("blockcount");
    blockcount.addEventListener("change", () => {
        if (blockcount.validity.valid)
            ship.blockcount.value = blockcount.value;
        blockcount.value = ship.blockcount.value;
    });
    const assemblyarea = document.getElementById("assemblyarea");
    assemblyarea.addEventListener("change", (e) => {
        if (e.target.validity.valid)
            ship[e.target.name].value = e.target.value;
        e.target.value = ship[e.target.name].value;
    });
    const transformpair = document.getElementById("transformpair");
    transformpair.value = ship.transformpair.value;
    transformpair.addEventListener("change", () => {
        ship.transformpair.value = transformpair.value;
    });
    const name = document.getElementById("ship_name");
    name.addEventListener("change", () => {
        ship.name.encode(name.value);
        name.value = ship.name.decode();
    });
}

function gummi_block_callbacks(block) {
    const block_type = document.getElementById("block_type");
    block_type.value = block.id.value;
    block_type.addEventListener("change", () => {
        block.id.value = block_type.value;
    });
    const block_coordinates = document.getElementById("block_coordinates");
    block_coordinates.addEventListener("change", (e) => {
        if (e.target.name == "y") {
            if (e.target.validity.valid)
                block.y.value = e.target.value;
            e.target.value = block.y.value;
        }
        else {
            if (e.target.validity.valid)
                block[e.target.name] = e.target.value;
            e.target.value = block[e.target.name];
        }
    });
    const rotation = document.getElementById("block_r");
    rotation.value = block.r.value & ~0x1000;
    rotation.addEventListener("change", () => {
        block.r.value = rotation.value | (block.r.value & 0x1000);
    });
    const color = document.getElementById("block_color");
    color.addEventListener("change", () => {
        if (color.validity.valid)
            block.color.value = color.value;
        color.value = block.color.value;
    });
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
