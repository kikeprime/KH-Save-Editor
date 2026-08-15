export function create_worlds() {
    const kh2div = document.getElementById("kh2div");
    kh2div.innerHTML = `
    <div>
        <div>
            <h3>World:</h3>
            <select id="kh2wtabs">
                ${
                    Object.keys(window.kh2.world_dict)
                        .map((label) => `<option value="${label}">${label}</option>`)
                        .join("")
                }
            </select>
        </div>
        <div id="kh2wtimediv"></div>
        <div>
            <h3>Tab:</h3>
            <select id="kh2wstabs">
                <option value="Progress Flags">Progress Flags</option>
                <option value="Place Scripts">Place Scripts</option>
            </select>
        </div>
        <div id="kh2wdiv"></div>
    </div>`;
    const kh2wtabs = document.getElementById("kh2wtabs");
    const kh2wstabs = document.getElementById("kh2wstabs");
    const kh2wtimediv = document.getElementById("kh2wtimediv");
    function tab_sel() {
        kh2wtimediv.innerHTML = create_playtime(window.kh2.world_dict[kh2wtabs.value] + 2);
        playtime_callbacks();
        switch (kh2wstabs.value) {
            case "Progress Flags": {
                create_progress_flags(kh2wtabs.value);
                break;
            }
            case "Place Scripts": {
                create_placescripts(kh2wtabs.value);
                break;
            }
        }
    }
    kh2wtabs.addEventListener("change", tab_sel);
    kh2wstabs.addEventListener("change", tab_sel);
    kh2wtabs.value = "Twilight Town";
    tab_sel();
}

function create_progress_flags(w) {
    const kh2wdiv = document.getElementById("kh2wdiv");
    kh2wdiv.innerHTML = `
    <div id="progress">
        <h3>Progress Flags:</h3>
        ${
            Object.entries(window.kh2.progress_dict[w])
                .map(([label, value]) => `
                <label style="display: flex; align-items: center">
                    <input
                        type="checkbox"
                        value=${value}
                        ${window.kh2.progress[w][Math.floor(value / 16)] & (1 << value % 16) ? "checked" : ""}
                    >
                    ${label}
                </label>`)
                .join("")
        }
    </div>`;
    progress_flags_callbacks(w);
}

function progress_flags_callbacks(w) {
    const progress = document.getElementById("progress");
    progress.addEventListener("change", (e) => {
        if (e.target.checked)
            window.kh2.progress[w][Math.floor(e.target.value / 16)] |= (1 << e.target.value % 16);
        else
            window.kh2.progress[w][Math.floor(e.target.value / 16)] &= ~(1 << e.target.value % 16);
    });
}

function create_placescripts(w) {
    const kh2wdiv = document.getElementById("kh2wdiv");
    if (window.kh2.fm) {
        let tbody = "";
        for (let i = 0; i < window.kh2.placescripts[w].length; i++) {
            tbody += `
            <tr>
                <td>
                    <input
                        type="number"
                        min=0
                        max=63
                        step=1
                        value=${i}
                        disabled=true
                    >
                </td>
                <td>
                    <input
                        type="number"
                        name="map"
                        min=0
                        max=255
                        step=1
                        value=${window.kh2.placescripts[w][i].map.value}
                    >
                </td>
                <td>
                    <input
                        type="number"
                        name="map2"
                        min=0
                        max=255
                        step=1
                        value=${window.kh2.placescripts[w][i].map2.value}
                    >
                </td>
                <td>
                    <input
                        type="number"
                        name="battle"
                        min=0
                        max=255
                        step=1
                        value=${window.kh2.placescripts[w][i].battle.value}
                    >
                </td>
                <td>
                    <input
                        type="number"
                        name="battle2"
                        min=0
                        max=255
                        step=1
                        value=${window.kh2.placescripts[w][i].battle2.value}
                    >
                </td>
                <td>
                    <input
                        type="number"
                        name="event"
                        min=0
                        max=255
                        step=1
                        value=${window.kh2.placescripts[w][i].event.value}
                    >
                </td>
                <td>
                    <input
                        type="number"
                        name="event2"
                        min=0
                        max=255
                        step=1
                        value=${window.kh2.placescripts[w][i].event2.value}
                    >
                </td>
            </tr>`;
        }
        kh2wdiv.innerHTML = `
        <div>
            <h3>Place Scripts:</h3>
            <table style="border-collapse: collapse; border: 2px solid">
                <thead>
                    <th scope="col">ID</th>
                    <th scope="col">Map</th>
                    <th scope="col">Map 2</th>
                    <th scope="col">Battle</th>
                    <th scope="col">Battle 2</th>
                    <th scope="col">Event</th>
                    <th scope="col">Event 2</th>
                </thead>
                <tbody id="placescripts">
                    ${tbody}
                </tbody>
            </table>
        </div>`;
    }
    else {
        let tbody = "";
        for (let i = 0; i < window.kh2.placescripts[w].length; i++) {
            tbody += `
            <tr>
                <td>
                    <input
                        type="number"
                        min=0
                        max=63
                        step=1
                        value=${i}
                        disabled=true
                    >
                </td>
                <td>
                    <input
                        type="number"
                        name="map"
                        min=0
                        max=255
                        step=1
                        value=${window.kh2.placescripts[w][i].map.value}
                    >
                </td>
                <td>
                    <input
                        type="number"
                        name="battle"
                        min=0
                        max=255
                        step=1
                        value=${window.kh2.placescripts[w][i].battle.value}
                    >
                </td>
                <td>
                    <input
                        type="number"
                        name="event"
                        min=0
                        max=255
                        step=1
                        value=${window.kh2.placescripts[w][i].event.value}
                    >
                </td>
            </tr>`;
        }
        kh2wdiv.innerHTML = `
        <div>
            <h3>Place Scripts:</h3>
            <table style="border-collapse: collapse; border: 2px solid">
                <thead>
                    <th scope="col">ID</th>
                    <th scope="col">Map</th>
                    <th scope="col">Battle</th>
                    <th scope="col">Event</th>
                </thead>
                <tbody id="placescripts">
                    ${tbody}
                </tbody>
            </table>
        </div>`;
    }
    placescripts_callbacks(w);
}

function placescripts_callbacks(w) {
    const placescripts = document.getElementById("placescripts");
    Object.entries(placescripts.children)
        .forEach(([i, row]) => {
            row.addEventListener("change", (e) => {
                if (e.target.validity.valid)
                    window.kh2.placescripts[w][i][e.target.name].value = e.target.value;
                e.target.value = window.kh2.placescripts[w][i][e.target.name].value;
            })
        });
}

function create_playtime(idx) {
    const playtime = window.kh2.get_playtime(window.kh2.playtimes[idx]);
    return `
    <h3>Playtime:</h3>
    <div id="playtime" style="display: flex; gap: 20px">
        <input
            type="number"
            id="hours"
            name=${idx}
            min=0
            max=400
            step=1
            value=${playtime[0]}
        >
        <input
            type="number"
            id="minutes"
            min=0
            max=59
            step=1
            value=${playtime[1]}
        >
        <input
            type="number"
            id="seconds"
            min=0
            max=59
            step=1
            value=${playtime[2]}
        >
        <input
            type="number"
            id="fraction"
            min=0
            max=59
            step=1
            value=${playtime[3]}
        >
        <input
            type="number"
            id="centiseconds"
            min=0
            max=99
            step=1
            value=${playtime[4]}
            disabled=true
        >
    </div>`;
}

function playtime_callbacks() {
    const hours = document.getElementById("hours");
    const minutes = document.getElementById("minutes");
    const seconds = document.getElementById("seconds");
    const fraction = document.getElementById("fraction");
    const centiseconds = document.getElementById("centiseconds");
    function update_playtime() {
        if (
            hours.validity.valid &&
            minutes.validity.valid &&
            seconds.validity.valid &&
            fraction.validity.valid
        ) {
            window.kh2.playtimes[hours.name] = window.kh2.set_playtime(
                Number(hours.value),
                Number(minutes.value),
                Number(seconds.value),
                Number(fraction.value),
            );
        }
        const [h, m, s, f, cs] = window.kh2.get_playtime(window.kh2.playtimes[hours.name]);
        hours.value = h;
        minutes.value = m;
        seconds.value = s;
        fraction.value = f;
        centiseconds.value = cs;
    }
    hours.addEventListener("change", update_playtime);
    minutes.addEventListener("change", update_playtime);
    seconds.addEventListener("change", update_playtime);
    fraction.addEventListener("change", update_playtime);
}
