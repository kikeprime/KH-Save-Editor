export function create_minigames() {
    const kh1jdiv = document.getElementById("kh1jdiv");
    kh1jdiv.innerHTML = `
    <div>
        <div>
            <h3>Minigame:</h3>
            <select id="kh1jmgtabs">
                ${
                    Object.entries(window.kh1.minigame_dict)
                        .map(([label, value]) => `<option value="${label}">${label}</option>`)
                        .join("")
                }
                <option value="Destiny Islands">Destiny Islands</option>
            </select>
        </div>
        <div id="kh1jmgdiv"></div>
    </div>`;
    const kh1jmgtabs = document.getElementById("kh1jmgtabs");
    kh1jmgtabs.addEventListener("change", tab_sel);
    tab_sel();
}

function tab_sel() {
    const kh1jmgtabs = document.getElementById("kh1jmgtabs");
    const tab = kh1jmgtabs.value;
    if (tab == "Destiny Islands") {
        create_minigame_di();
        minigame_di_callbacks();
    }
    else if (window.kh1.minigames_with_sub.includes(tab)) {
        create_minigame_with_sub(tab);
        minigame_with_sub_callbacks(tab);
    }
    else {
        create_minigame(tab);
        minigame_callbacks(tab);
    }
}

function create_minigame_di() {
    const kh1jmgdiv = document.getElementById("kh1jmgdiv");
    const soriku = `
    <div style="display: flex; gap: 10px">
        <label style="display: flex; align-items: center; gap: 10px">
            Sora:
            <input
                type="number"
                id="sorawins"
                min=0
                max=100
                step=1
                value=${window.kh1.sorawins.value}
            >
        </label>
        <label style="display: flex; align-items: center; gap: 10px">
            Riku:
            <input
                type="number"
                id="rikuwins"
                min=0
                max=100
                step=1
                value=${window.kh1.rikuwins.value}
            >
        </label>
    </div>`;
    const fftrio = `
    <div style="display: flex; gap: 10px">
        <label style="display: flex; align-items: center; gap: 10px">
            Tidus:
            <input
                type="number"
                id="tiduswins"
                min=0
                max=255
                step=1
                value=${window.kh1.tiduswins.value}
            >
        </label>
        <label style="display: flex; align-items: center; gap: 10px">
            Wakka:
            <input
                type="number"
                id="wakkawins"
                min=0
                max=255
                step=1
                value=${window.kh1.wakkawins.value}
            >
        </label>
        <label style="display: flex; align-items: center; gap: 10px">
            Selphie:
            <input
                type="number"
                id="selphiewins"
                min=0
                max=255
                step=1
                value=${window.kh1.selphiewins.value}
            >
        </label>
    </div>`;
    kh1jmgdiv.innerHTML = `
    <div>
        <h3>Sora vs. Riku</h3>
        ${soriku}
        <h3>Sora vs. FF Trio</h3>
        ${fftrio}
    </div>`;
}

function create_minigame_with_sub(tab) {
    const kh1jmgdiv = document.getElementById("kh1jmgdiv");
    function sub(value) {
        return Object.entries(value)
            .map(([p, t]) => create_time_record(tab, p, t))
            .join("");
    }
    kh1jmgdiv.innerHTML = `
    <div>
        ${
            Object.entries(window.kh1.minigame_dict[tab])
                .map(([label, value]) => `
                <div id="${label}">
                    <h3>${label}:</h3>
                    ${sub(value)}
                </div>`)
                .join("")
        }
    </div>`;
}

function create_minigame(tab) {
    const kh1jmgdiv = document.getElementById("kh1jmgdiv");
    if (tab in window.kh1.minigames_with_scores) {
        kh1jmgdiv.innerHTML = `
        <div id="${tab}">
            ${
                Object.entries(window.kh1.minigame_dict[tab])
                    .map(([p, t]) => create_score_record(tab, p, t))
                    .join("")
            }
        </div>`;
    }
    else {
        kh1jmgdiv.innerHTML = `
        <div id="${tab}">
            ${
                Object.entries(window.kh1.minigame_dict[tab])
                    .map(([p, t]) => create_time_record(tab, p, t))
                    .join("")
            }
        </div>`;
    }
}

function get_time(time, fps = 60) {
    return [
        Math.floor(Math.floor(time / fps) / 3600),
        Math.floor((Math.floor(time / fps) % 3600) / 60),
        (Math.floor(time / fps) % 3600) % 60,
        time % fps,
        Math.floor((time % fps * 100) / 60),
    ];
}

function set_time(hours, minutes, seconds, fraction, fps = 60) {
    return (hours * 3600 + minutes * 60 + seconds) * fps + fraction;
}

function create_time_record(tab, p, t) {
    const idx = Math.floor(t / 4);
    const raw = tab != "Olympus Coliseum" ? window.kh1.minigames[idx] : window.kh1.oc_minigames[idx];
    if (raw != -1) {
        const time = get_time(raw);
        return `
        <label style="margin-top: 10px; margin-bottom: 0px">${p}:</label>
        <div name=${idx} style="display: flex; gap: 20px">
            <input
                type="number"
                name="minutes"
                min=0
                max=59
                step=1
                value=${time[1]}
            >
            <input
                type="number"
                name="seconds"
                min=0
                max=59
                step=1
                value=${time[2]}
            >
            <input
                type="number"
                name="fraction"
                min=0
                max=59
                step=1
                value=${time[3]}
            >
            <input
                type="number"
                name="centiseconds"
                min=0
                max=99
                step=1
                value=${time[4]}
                disabled=true
            >
            <button name=${idx}>Unset</button>
        </div>`;
    }
    else {
        return `
        <div>
            <label style="margin-top: 10px; margin-bottom: 0px">${p}:</label>
            <label style="display: flex; align-items: center; gap: 10px">
                Unset record.
                <button name=${idx}>Initialize</button>
            </label>
        </div>`;
    }
}

function create_score_record(tab, p, t) {
    const idx = Math.floor(t / 4);
    const value = window.kh1.minigames[idx];
    return `
    <label style="margin-top: 10px; margin-bottom: 0px">${p}:</label>
    <label style="display: flex; align-items: center; gap: 10px">
        <input
            type="number"
            name=${idx}
            min=-1
            max=9999
            step=1
            value=${value}
        >
        ${window.kh1.minigames_with_scores[tab]}
    </label>`;
}

function minigame_di_callbacks() {
    const sorawins = document.getElementById("sorawins");
    sorawins.addEventListener("change", (e) => {
        if (e.target.validity.valid)
            window.kh1.sorawins.value = e.target.value;
        e.target.value = window.kh1.sorawins.value;
    });
    const rikuwins = document.getElementById("rikuwins");
    rikuwins.addEventListener("change", (e) => {
        if (e.target.validity.valid)
            window.kh1.rikuwins.value = e.target.value;
        e.target.value = window.kh1.rikuwins.value;
    });
    const tiduswins = document.getElementById("tiduswins");
    tiduswins.addEventListener("change", (e) => {
        if (e.target.validity.valid)
            window.kh1.tiduswins.value = e.target.value;
        e.target.value = window.kh1.tiduswins.value;
    });
    const wakkawins = document.getElementById("wakkawins");
    wakkawins.addEventListener("change", (e) => {
        if (e.target.validity.valid)
            window.kh1.wakkawins.value = e.target.value;
        e.target.value = window.kh1.wakkawins.value;
    });
    const selphiewins = document.getElementById("selphiewins");
    selphiewins.addEventListener("change", (e) => {
        if (e.target.validity.valid)
            window.kh1.selphiewins.value = e.target.value;
        e.target.value = window.kh1.selphiewins.value;
    });
}

function minigame_with_sub_callbacks(tab) {
    Object.entries(window.kh1.minigame_dict[tab])
        .forEach(([label, value]) => {
            const minigame = document.getElementById(label);
            minigame.addEventListener("click", (e) => {
                if (e.target.closest("button")) {
                    if (e.target.innerHTML == "Unset") {
                        if (tab != "Olympus Coliseum")
                            window.kh1.minigames[e.target.name] = -1;
                        else
                            window.kh1.oc_minigames[e.target.name] = -1;
                    }
                    else {
                        if (tab != "Olympus Coliseum")
                            window.kh1.minigames[e.target.name] = 0;
                        else
                            window.kh1.oc_minigames[e.target.name] = 0;
                    }
                    tab_sel();
                }
            });
            minigame.addEventListener("change", (e) => {
                const div = e.target.closest("div[name]");
                const inputs = div.querySelectorAll(`input[type="number"]:not([disabled])`);
                const values = [0];
                inputs.forEach(input => {
                    if (input.validity.valid)
                        values.push(Number(input.value));
                });
                if (values.length == 4) {
                    if (tab != "Olympus Coliseum")
                        window.kh1.minigames[div.getAttribute("name")] = set_time(...values);
                    else
                        window.kh1.oc_minigames[div.getAttribute("name")] = set_time(...values);
                }
                tab_sel();
            });
        });
}

function minigame_callbacks(tab) {
    const minigame = document.getElementById(tab);
    if (tab in kh1.minigames_with_scores) {
        minigame.addEventListener("change", (e) => {
            if (e.target.validity.valid)
                window.kh1.minigames[e.target.name] = e.target.value;
            e.target.value = window.kh1.minigames[e.target.name];
        });
    }
    else {
        minigame.addEventListener("click", (e) => {
            if (e.target.closest("button")) {
                if (e.target.innerHTML == "Unset")
                    window.kh1.minigames[e.target.name] = -1;
                else
                    window.kh1.minigames[e.target.name] = 0;
                tab_sel();
            }
        });
        minigame.addEventListener("change", (e) => {
            const div = e.target.closest("div[name]");
            const inputs = div.querySelectorAll(`input[type="number"]:not([disabled])`);
            const values = [0];
            inputs.forEach(input => {
                if (input.validity.valid)
                    values.push(Number(input.value));
            });
            if (values.length == 4)
                window.kh1.minigames[div.getAttribute("name")] = set_time(...values);
            tab_sel();
        });
    }
}
