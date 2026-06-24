export function create_journal_characters() {
    const kh1jdiv = document.getElementById("kh1jdiv");
    kh1jdiv.innerHTML = `
    <div>
        <div>
            <h3>Entry:</h3>
            <select id="kh1jchartabs">
                <option value="Characters 1">Characters 1</option>
                <option value="Characters 2">Characters 2</option>
                <option value="The Heartless">The Heartless</option>
            </select>
        </div>
        <div id="kh1jchardiv"></div>
    </div>`;
    const kh1jchartabs = document.getElementById("kh1jchartabs");
    function tab_sel() {
        switch (kh1jchartabs.value) {
            case "Characters 1": {
                create_journal_chars_1();
                break;
            }
            case "Characters 2": {
                create_journal_chars_2();
                break;
            }
            case "The Heartless": {
                create_heartless();
                break;
            }
        }
    }
    kh1jchartabs.addEventListener("change", tab_sel);
    tab_sel();
}

function create_journal_chars_1() {
    const kh1jchardiv = document.getElementById("kh1jchardiv");
    let journal_chars_1 = `<div id="journal_chars_1">`;
    Object.entries(window.kh1.journal_chars_1_dict).forEach(([label, value]) => {
        if (typeof value == "number") {
            const idx = Math.floor(value / 16);
            const bit = value % 16;
            journal_chars_1 += `
            <label style="display: flex; align-items: center">
                <input
                    type="checkbox"
                    value=${value}
                    ${window.kh1.journal_chars[idx] & (1 << bit) ? "checked" : ""}
                >
                ${label}
            </label>`;
        }
        else {
            journal_chars_1 += `
            <h3>${label}</h3>
            <label style="display: flex; align-items: center">
                <input
                    type="radio"
                    name=${label}
                    value=0
                    checked
                >
                Locked
            </label>`;
            Object.entries(value).forEach(([k, v]) => {
                const idx = Math.floor(v / 16);
                const bit = v % 16;
                journal_chars_1 += `
                <label style="display: flex; align-items: center">
                    <input
                        type="radio"
                        name=${label}
                        value=${v}
                        ${window.kh1.journal_chars[idx] & (1 << bit) ? "checked" : ""}
                    >
                    ${k}
                </label>`;
            });
        }
    });
    journal_chars_1 += "</div>";
    kh1jchardiv.innerHTML = `
    <div>
        ${journal_chars_1}
    </div>`;
    journal_chars_1_callbacks();
}

function journal_chars_1_callbacks() {
    const journal_chars_1 = document.getElementById("journal_chars_1");
    journal_chars_1.addEventListener("change", (e) => {
        if (e.target.type == "checkbox") {
            const idx = Math.floor(e.target.value / 16);
            const bit = e.target.value % 16;
            if (e.target.checked)
                window.kh1.journal_chars[idx] |= (1 << bit);
            else
                window.kh1.journal_chars[idx] &= ~(1 << bit);
        }
        else {
            Object.entries(window.kh1.journal_chars_1_dict[e.target.name]).forEach(([label, value]) => {
                const idx = Math.floor(value / 16);
                const bit = value % 16;
                if (e.target.value == value)
                    window.kh1.journal_chars[idx] |= (1 << bit);
                else
                    window.kh1.journal_chars[idx] &= ~(1 << bit);
            });
        }
    });
}

function create_journal_chars_2() {
    const kh1jchardiv = document.getElementById("kh1jchardiv");
    let journal_chars_2 = `<div id="journal_chars_2">`;
    Object.entries(window.kh1.journal_chars_2_dict).forEach(([label, value]) => {
        if (typeof value == "number") {
            const idx = Math.floor(value / 16);
            const bit = value % 16;
            journal_chars_2 += `
            <label style="display: flex; align-items: center">
                <input
                    type="checkbox"
                    value=${value}
                    ${window.kh1.journal_chars[idx] & (1 << bit) ? "checked" : ""}
                >
                ${label}
            </label>`;
        }
        else {
            journal_chars_2 += `
            <h3>${label}</h3>
            <label style="display: flex; align-items: center">
                <input
                    type="radio"
                    name=${label}
                    value=0
                    checked
                >
                Locked
            </label>`;
            Object.entries(value).forEach(([k, v]) => {
                const idx = Math.floor(v / 16);
                const bit = v % 16;
                journal_chars_2 += `
                <label style="display: flex; align-items: center">
                    <input
                        type="radio"
                        name=${label}
                        value=${v}
                        ${window.kh1.journal_chars[idx] & (1 << bit) ? "checked" : ""}
                    >
                    ${k}
                </label>`;
            });
        }
    });
    journal_chars_2 += "</div>";
    kh1jchardiv.innerHTML = `
    <div>
        ${journal_chars_2}
    </div>`;
    journal_chars_2_callbacks();
}

function journal_chars_2_callbacks() {
    const journal_chars_2 = document.getElementById("journal_chars_2");
    journal_chars_2.addEventListener("change", (e) => {
        if (e.target.type == "checkbox") {
            const idx = Math.floor(e.target.value / 16);
            const bit = e.target.value % 16;
            if (e.target.checked)
                window.kh1.journal_chars[idx] |= (1 << bit);
            else
                window.kh1.journal_chars[idx] &= ~(1 << bit);
        }
        else {
            Object.entries(window.kh1.journal_chars_2_dict[e.target.name]).forEach(([label, value]) => {
                const idx = Math.floor(value / 16);
                const bit = value % 16;
                if (e.target.value == value)
                    window.kh1.journal_chars[idx] |= (1 << bit);
                else
                    window.kh1.journal_chars[idx] &= ~(1 << bit);
            });
        }
    });
}

function create_heartless() {
    const kh1jchardiv = document.getElementById("kh1jchardiv");
    const heartless_dict = window.kh1.fm ? window.kh1.heartless_fm_dict : window.kh1.heartless_dict;
    const heartless = `
    <div id="heartless">
        ${
            Object.entries(heartless_dict)
                .map(([label, value]) => `
                <label style="display: flex; gap: 10px; align-items: center">
                    ${label}:
                    <input
                        type="number"
                        name=${value}
                        min=0
                        max=9999
                        step=1
                        value=${window.kh1.heartless[value]}
                    >
                </label>`)
                .join("")
        }
    </div>`;
    const bosses = `
    <div id="bosses">
        ${
            Object.entries(window.kh1.journal_boss_dict)
                .map(([label, value]) => `
                <label style="display: flex; align-items: center">
                    <input
                        type="checkbox"
                        value=${value}
                        ${window.kh1.journal_chars[Math.floor(value / 16)] & (1 << value % 16) ? "checked" : ""}
                    >
                    ${label}
                </label>`)
                .join("")
        }
    </div>`;
    kh1jchardiv.innerHTML = `
    <div>
        <h3>Heartless Kill Counts:</h3>
        ${heartless}
        <h3>Heartless Bosses:</h3>
        ${bosses}
    </div>`;
    heartless_callbacks();
}

function heartless_callbacks() {
    const heartless = document.getElementById("heartless");
    heartless.addEventListener("change", (e) => {
        if (e.target.validity.valid)
            window.kh1.heartless[e.target.name] = e.target.value;
        e.target.value = window.kh1.heartless[e.target.name];
    });
    const bosses = document.getElementById("bosses");
    bosses.addEventListener("change", (e) => {
        const idx = Math.floor(e.target.value / 16);
        const bit = e.target.value % 16;
        if (e.target.checked)
            window.kh1.journal_chars[idx] |= (1 << bit);
        else
            window.kh1.journal_chars[idx] &= ~(1 << bit);
    });
}
