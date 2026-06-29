export function create_general() {
    const kh2div = document.getElementById("kh2div");
    const playtime = create_playtime();
    const path = `
    <div>
        <h3>Path:</h3>
        <select id="path">
            <option value=0>Warrior</option>
            <option value=1>Guardian</option>
            <option value=2>Mystic</option>
        </select>
    </div>`;
    const world_options = Object.entries(window.kh2.world_dict)
        .map(([value, label]) => `\n\t<option value=${value}>${label}</option>`)
        .join("");
    const world = `
    <div>
        <h3>World:</h3>
        <select id="world">
            ${world_options}
        </select>
    </div>`;
    const room = `
    <div>
        <h3>Room:</h3>
        <input
            type="number"
            id="room"
            min=0
            max=255
            step=1
            value=${window.kh2.room.value}
        >
    </div>`;
    const flag = `
    <div>
        <h3>Flag:</h3>
        <input
            type="number"
            id="flag"
            min=0
            max=255
            step=1
            value=${window.kh2.flag.value}
        >
    </div>`;
    const munny = `
    <div>
        <h3>Munny:</h3>
        <input
            type="number"
            id="munny"
            min=0
            max=${0xFFFFFFFF}
            step=1
            value=${window.kh2.munny.value}
        >
    </div>`;
    const exp = `
    <div>
        <h3>EXP:</h3>
        <input
            type="number"
            id="exp"
            min=0
            max=${0xFFFFFFFF}
            step=1
            value=${window.kh2.exp.value}
        >
    </div>`;
    const form_options = Object.entries(window.fm ? window.kh2.form_fm_dict : window.kh2.form_dict)
        .map(([label, value]) => `\n\t<option value=${value}>${label}</option>`)
        .join("");
    const current_form = `
    <div>
        <h3>Current Form:</h3>
        <select id="current_form">
            ${form_options}
        </select>
    </div>`;
    const summon_options = Object.entries(window.kh2.summon_dict)
        .map(([label, value]) => `\n\t<option value=${value}>${label}</option>`)
        .join("");
    const current_summon = `
    <div>
        <h3>Current Summon:</h3>
        <select id="current_summon">
            ${summon_options}
        </select>
    </div>`;
    kh2div.innerHTML = `
    <div>
        ${playtime}
        ${path}
        <div style="display: flex; gap: 20px">
            ${world}
            ${room}
            ${flag}
        </div>
        ${munny}
        ${exp}
        ${current_form}
        ${current_summon}
    </div>`;
    general_callbacks();
}

function create_playtime() {
    const playtime = window.kh2.get_playtime(window.kh2.playtimes[0]);
    console.log(`Playtime: ${playtime}`);
    return `
    <h3>Playtime:</h3>
    <div id="playtime" style="display: flex; gap: 20px">
        <input
            type="number"
            id="hours"
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
            window.kh2.playtimes[0] = window.kh2.set_playtime(
                Number(hours.value),
                Number(minutes.value),
                Number(seconds.value),
                Number(fraction.value),
            );
        }
        const [h, m, s, f, cs] = window.kh2.get_playtime(window.kh2.playtimes[0]);
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

function general_callbacks() {
    playtime_callbacks();
    const path = document.getElementById("path");
    path.value = window.kh2.characters[0].path.value;
    path.addEventListener("change", () => {
        window.kh2.characters[0].path.value = path.value;
    });
    const world = document.getElementById("world");
    world.value = window.kh2.world.value;
    world.addEventListener("change", () => {
        window.kh2.world.value = world.value;
    });
    const room = document.getElementById("room");
    room.addEventListener("change", () => {
        if (room.validity.valid)
            window.kh2.room.value = room.value;
        room.value = window.kh2.room.value;
    });
    const flag = document.getElementById("flag");
    flag.addEventListener("change", () => {
        if (flag.validity.valid)
            window.kh2.flag.value = flag.value;
        flag.value = window.kh2.flag.value;
    });
    const munny = document.getElementById("munny");
    munny.addEventListener("change", () => {
        if (munny.validity.valid)
            window.kh2.munny.value = munny.value;
        munny.value = window.kh2.munny.value;
    });
    const exp = document.getElementById("exp");
    exp.addEventListener("change", () => {
        if (exp.validity.valid)
            window.kh2.exp.value = exp.value;
        exp.value = window.kh2.exp.value;
    });
    const current_form = document.getElementById("current_form");
    current_form.value = window.kh2.current_form.value;
    current_form.addEventListener("change", () => {
        window.kh2.current_form.value = current_form.value;
    });
    const current_summon = document.getElementById("current_summon");
    current_summon.value = window.kh2.current_summon.value;
    current_summon.addEventListener("change", () => {
        window.kh2.current_summon.value = current_summon.value;
    });
}
