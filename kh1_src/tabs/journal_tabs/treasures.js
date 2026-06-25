export function create_treasures() {
    const kh1jdiv = document.getElementById("kh1jdiv");
    kh1jdiv.innerHTML = `
    <div>
        <div>
            <h3>World:</h3>
            <select id="kh1jtrtabs">
                ${
                    Object.entries(window.kh1.world_dict)
                        .filter(([value, label]) => { return label != "Disney Castle"; })
                        .map(([value, label]) => `<option value="${label}">${label}</option>`)
                        .join("")
                }
            </select>
        </div>
        <div id="kh1jtrdiv"></div>
    </div>`;
    const kh1jtrtabs = document.getElementById("kh1jtrtabs");
    const kh1jtrdiv = document.getElementById("kh1jtrdiv");
    function tab_sel() {
        kh1jtrdiv.innerHTML = `
        <div id=treasures>
            <h3>Treasures Chests:</h3>
            ${
                Object.entries(window.kh1.treasure_dicts[kh1jtrtabs.value])
                    .map(([label, value]) => {
                        const idx = Math.floor(value / 16);
                        const bit = value % 16;
                        return `
                        <label style="display: flex; align-items: center">
                            <input
                                type="checkbox"
                                value=${value}
                                ${window.kh1.treasures[idx] & (1 << bit) ? "checked" : ""}
                            >
                            ${label}
                        </label>`;
                    })
                    .join("")
            }
        </div>`;
        switch (kh1jtrtabs.value) {
            case "Atlantica": {
                kh1jtrdiv.innerHTML += `
                <div id=clams>
                    <h3>Atlantica Clams:</h3>
                    ${
                        Object.entries(window.kh1.clam_dict)
                            .map(([label, value]) => {
                                const idx = Math.floor(value / 16);
                                const bit = value % 16;
                                return `
                                <label style="display: flex; align-items: center">
                                    <input
                                        type="checkbox"
                                        value=${value}
                                        ${window.kh1.clams[idx] & (1 << bit) ? "checked" : ""}
                                    >
                                    ${label}
                                </label>`;
                            })
                            .join("")
                    }
                </div>`;
                clams_callbacks();
                break;
            }
            case "Neverland": {
                kh1jtrdiv.innerHTML += `
                <div id=bigben>
                    <label style="display: flex; align-items: center">
                        <input
                            type="checkbox"
                            value=${0x11}
                            ${window.kh1.bigben[1] & (1 << 1) ? "checked" : ""}
                        >
                        Ship: Hold Aero Chest
                    </label>
                    <h3>Big Ben Doors:</h3>
                    ${
                        Object.entries(window.kh1.bigben_dict)
                            .map(([label, value]) => {
                                const idx = Math.floor(value / 16);
                                const bit = value % 16;
                                return `
                                <label style="display: flex; align-items: center">
                                    <input
                                        type="checkbox"
                                        value=${value}
                                        ${window.kh1.bigben[idx] & (1 << bit) ? "checked" : ""}
                                    >
                                    ${label}
                                </label>`;
                            })
                            .join("")
                    }
                </div>`;
                bigben_callbacks();
                break;
            }
            default: {
                break;
            }
        }
        treasures_callbacks();
    }
    kh1jtrtabs.addEventListener("change", tab_sel);
    kh1jtrtabs.value = "Traverse Town";
    tab_sel();
}

function treasures_callbacks() {
    const treasures = document.getElementById("treasures");
    treasures.addEventListener("change", (e) => {
        const idx = Math.floor(e.target.value / 16);
        const bit = e.target.value % 16;
        if (e.target.checked)
            window.kh1.treasures[idx] |= (1 << bit);
        else
            window.kh1.treasures[idx] &= ~(1 << bit);
    });
}

function clams_callbacks() {
    const clams = document.getElementById("clams");
    clams.addEventListener("change", (e) => {
        const idx = Math.floor(e.target.value / 16);
        const bit = e.target.value % 16;
        if (e.target.checked)
            window.kh1.clams[idx] |= (1 << bit);
        else
            window.kh1.clams[idx] &= ~(1 << bit);
    });
}

function bigben_callbacks() {
    const bigben = document.getElementById("bigben");
    bigben.addEventListener("change", (e) => {
        const idx = Math.floor(e.target.value / 16);
        const bit = e.target.value % 16;
        if (e.target.checked)
            window.kh1.bigben[idx] |= (1 << bit);
        else
            window.kh1.bigben[idx] &= ~(1 << bit);
    });
}
