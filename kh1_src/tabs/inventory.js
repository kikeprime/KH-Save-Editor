export function create_inventory() {
    const kh1div = document.getElementById("kh1div");
    kh1div.innerHTML = `
    <div>
        <div>
            <h3>Category:</h3>
            <select id="kh1invtabs">
                <option value="Consumables">Consumables</option>
                <option value="Synthesis Materials">Synthesis Materials</option>
                <option value="Accessories">Accessories</option>
                <option value="Weapons">Weapons</option>
                <option value="Key Items">Key Items</option>
                <option value="Unused">Unused</option>
            </select>
        </div>
        <div id="kh1invdiv"></div>
    </div>`;
    const kh1invtabs = document.getElementById("kh1invtabs");
    function tab_sel() {
        __create_inventory(kh1invtabs.value);
    }
    kh1invtabs.addEventListener("change", tab_sel);
    __create_inventory("Consumables");
}

function __create_inventory(tab) {
    const kh1invdiv = document.getElementById("kh1invdiv");
    let items = null;
    switch (tab) {
        case "Consumables": {
            items = Object.fromEntries(Object.entries(window.kh1.item_dict)
                .filter(([label, value]) => {
                    return !label.includes("Unused") && (
                        (value >= 0x01 && value < 0x09) ||
                        (value >= 0x8E && value < 0x91) ||
                        (value >= 0x98 && value < 0x9B)
                    );
                }));
            break;
        }
        case "Synthesis Materials": {
            items = Object.fromEntries(Object.entries(window.kh1.item_dict)
                .filter(([label, value]) => {
                    return !label.includes("Unused") && (
                        (value >= 0x09 && value < 0x11) ||
                        (value >= 0x9B && value < 0x9E) ||
                        (value >= 0xE9 && value < 0x100)
                    );
                }));
            break;
        }
        case "Accessories": {
            items = Object.fromEntries(Object.entries(window.kh1.accessory_dict)
                .filter(([label, value]) => {
                    return !label.includes("Unused") && value > 0;
                }));
            break;
        }
        case "Weapons": {
            items = Object.fromEntries(Object.entries(window.kh1.weapon_dict)
                .filter(([label, value]) => {
                    return !label.includes("Unused") && value > 0;
                }));
            break;
        }
        case "Key Items": {
            items = Object.fromEntries(Object.entries(window.kh1.item_dict)
                .filter(([label, value]) => {
                    return !label.includes("Unused") && (
                        (value >= 0x95 && value < 0x98) ||
                        (value >= 0x9E && value < 0xE8)
                    );
                }));
            break;
        }
        case "Unused": {
            items = Object.fromEntries(Object.entries(window.kh1.item_dict)
                .filter(([label, value]) => {
                    return label.includes("Unused");
                })
                .sort());
            break;
        }
    };
    const inventory = Object.entries(items)
        .map(([label, value]) => `
        <label style="display: flex; gap: 10px; align-items: center">
            ${label}: 
            <input
                type="number"
                min=0
                max=99
                step=1
                value=${window.kh1.inventory[value]}
                name=${value}
            >
        </label>`)
        .join("");
    kh1invdiv.innerHTML = `
    <div id="inventory">
        <h3>Inventory:</h3>
        ${inventory}
    </div>`;
    inventory_callbacks();
}

function inventory_callbacks() {
    const inventory = document.getElementById("inventory");
    inventory.addEventListener("change", (e) => {
        if (e.target.validity.valid)
            window.kh1.inventory[e.target.name] = e.target.value;
        e.target.value = window.kh1.inventory[e.target.name];
    });
}
