export function create_inventory() {
    const kh2div = document.getElementById("kh2div");
    kh2div.innerHTML = `
    <div>
        <div>
            <h3>Category:</h3>
            <select id="kh2invtabs">
                ${
                    Object.keys(window.kh2.stock_dict)
                    .map((k) => `<option value="${k}">${k}</option>`)
                    .join("")
                }
            </select>
        </div>
        <div id="kh2invdiv"></div>
    </div>`;
    const kh2invtabs = document.getElementById("kh2invtabs");
    function tab_sel() {
        __create_inventory(kh2invtabs.value);
    }
    kh2invtabs.addEventListener("change", tab_sel);
    __create_inventory("Consumables");
}

function __create_inventory(tab) {
    const kh2invdiv = document.getElementById("kh2invdiv");
    const items = window.kh2.stock_dict[tab]
        .filter((label) => window.kh2.inventory_dict[label] < window.kh2.inventory.length);
    const inventory = items
        .map((label) => `
        <label style="display: flex; gap: 10px; align-items: center">
            ${label}: 
            <input
                type="number"
                min=0
                max=99
                step=1
                value=${window.kh2.inventory[window.kh2.inventory_dict[label]]}
                name=${window.kh2.inventory_dict[label]}
            >
        </label>`)
        .join("");
    kh2invdiv.innerHTML = `
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
            window.kh2.inventory[e.target.name] = e.target.value;
        e.target.value = window.kh2.inventory[e.target.name];
    });
}
