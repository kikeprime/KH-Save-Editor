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
            case "Traverse Town": {
                kh1jtrdiv.innerHTML += `
                <h2>Postcards</h2>
                <div id="safe_postcard">
                    <label style="display: flex; align-items: center">
                        <input
                            type="checkbox"
                            value=${(1 << 0)}
                            ${window.kh1.safe_postcard.value & (1 << 0) ? "checked" : ""}
                        >
                        1st District Safe
                    </label>
                </div>
                <div id="gizmo_postcards">
                    <label style="display: flex; align-items: center">
                        <input
                            type="checkbox"
                            value=${(1 << 5)}
                            ${window.kh1.gizmo_postcards.value & (1 << 5) ? "checked" : ""}
                        >
                        Gizmo Shop 1
                    </label>
                    <label style="display: flex; align-items: center">
                        <input
                            type="checkbox"
                            value=${(1 << 6)}
                            ${window.kh1.gizmo_postcards.value & (1 << 6) ? "checked" : ""}
                        >
                        Gizmo Shop 2
                    </label>
                </div>
                <div id="misc_postcards">
                    <label style="display: flex; align-items: center">
                        <input
                            type="checkbox"
                            value=${(1 << 3)}
                            ${window.kh1.misc_postcards.value & (1 << 3) ? "checked" : ""}
                        >
                        Geppeto's House Shelf
                    </label>
                    <label style="display: flex; align-items: center">
                        <input
                            type="checkbox"
                            value=${(1 << 4)}
                            ${window.kh1.misc_postcards.value & (1 << 4) ? "checked" : ""}
                        >
                        Item Workshop Poster
                    </label>
                    <label style="display: flex; align-items: center">
                        <input
                            type="checkbox"
                            value=${(1 << 5)}
                            ${window.kh1.misc_postcards.value & (1 << 5) ? "checked" : ""}
                        >
                        1st District Balcony Barrel (vanilla JP only)
                    </label>
                    <label style="display: flex; align-items: center">
                        <input
                            type="checkbox"
                            value=${(1 << 6)}
                            ${window.kh1.misc_postcards.value & (1 << 6) ? "checked" : ""}
                        >
                        3rd District Balcony
                    </label>
                    <label style="display: flex; align-items: center">
                        <input
                            type="checkbox"
                            value=${(1 << 7)}
                            ${window.kh1.misc_postcards.value & (1 << 7) ? "checked" : ""}
                        >
                        Item Shop Fan
                    </label>
                </div>
                <div id="gizmo_switches">
                    <label style="display: flex; align-items: center">
                        <input
                            type="checkbox"
                            value=${(1 << 0)}
                            ${window.kh1.gizmo_switches.value & (1 << 0) ? "checked" : ""}
                        >
                        Gizmo Shop switches are activated
                    </label>
                    <label style="display: flex; align-items: center">
                        <input
                            type="checkbox"
                            value=${(1 << 1)}
                            ${window.kh1.gizmo_switches.value & (1 << 1) ? "checked" : ""}
                        >
                        Gizmo Shop Postcards are ready
                    </label>
                </div>
                <div>
                    <label style="display: flex; align-items: center; gap: 10px">
                        Postcards Mailed:
                        <input
                            id="postcards_mailed"
                            type="number"
                            value=${window.kh1.postcards_mailed.value}
                            min=0
                            max=10
                            step=1
                        >
                    </label>
                </div>`;
                postcard_callbacks();
                break;
            }
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

function postcard_callbacks() {
    const safe_postcard = document.getElementById("safe_postcard");
    safe_postcard.addEventListener("change", (e) => {
        if (e.target.checked)
            window.kh1.safe_postcard.value |= e.target.value;
        else
            window.kh1.safe_postcard.value &= ~e.target.value;
    });
    const gizmo_postcards = document.getElementById("gizmo_postcards");
    gizmo_postcards.addEventListener("change", (e) => {
        if (e.target.checked)
            window.kh1.gizmo_postcards.value |= e.target.value;
        else
            window.kh1.gizmo_postcards.value &= ~e.target.value;
    });
    const misc_postcards = document.getElementById("misc_postcards");
    misc_postcards.addEventListener("change", (e) => {
        if (e.target.checked)
            window.kh1.misc_postcards.value |= e.target.value;
        else
            window.kh1.misc_postcards.value &= ~e.target.value;
    });
    const gizmo_switches = document.getElementById("gizmo_switches");
    gizmo_switches.addEventListener("change", (e) => {
        if (e.target.checked)
            window.kh1.gizmo_switches.value |= e.target.value;
        else
            window.kh1.gizmo_switches.value &= ~e.target.value;
    });
    const postcards_mailed = document.getElementById("postcards_mailed");
    postcards_mailed.addEventListener("change", () => {
        if (postcards_mailed.validity.valid)
            window.kh1.postcards_mailed.value = postcards_mailed.value;
        postcards_mailed.value = window.kh1.postcards_mailed.value;
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
