export function create_general() {
    const kh1div = document.getElementById("kh1div");
    const playtime = create_playtime();
    const curve = `
    <div>
        <h3>Leveling curve:</h3>
        <select id="curve">
            <option value=0>Dawn</option>
            <option value=1>Midday</option>
            <option value=2>Dusk</option>
        </select>
    </div>`;
    const path = `
    <div>
        <h3>Path:</h3>
        <select id="path">
            <option value=0>Warrior</option>
            <option value=1>Guardian</option>
            <option value=2>Mystic</option>
        </select>
    </div>`;
    const world_options = Object.entries(window.kh1.world_dict)
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
            value=${window.kh1.room.value}
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
            value=${window.kh1.flag.value}
        >
    </div>`;
    const party_options = Object.entries(window.kh1.character_dict)
        .map(([label, value]) => `\n\t<option value=${value}>${label}</option>`)
        .join("");
    const party = `
    <div>
        <h3>Party:</h3>
        <div style="display: flex">
            <select id="leader" disabled=true>
                ${party_options}
            </select>
            <select id="friend1">
                ${party_options}
            </select>
            <select id="friend2">
                ${party_options}
            </select>
            <select id="friend3">
                ${party_options}
            </select>
        </div>
    </div>`;
    const munny = `
    <div>
        <h3>Munny:</h3>
        <input
            type="number"
            id="munny"
            min=0
            max=0xFFFF
            step=1
            value=${window.kh1.munny.value}
        >
    </div>`;
    kh1div.innerHTML = `
    <div>
        ${playtime}
        <div style="display: flex; gap: 20px">
            ${curve}
            ${path}
        </div>
        <div style="display: flex; gap: 20px">
            ${world}
            ${room}
            ${flag}
        </div>
        ${party}
        ${munny}
    </div>`;
    general_callbacks();
}

function create_playtime() {
    if (window.kh1.playtime != null) {
        const playtime = window.kh1.get_playtime();
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
    return "";
}

function playtime_callbacks() {
    const playtime = document.getElementById("playtime");
    if (playtime == null)
        return;
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
            window.kh1.set_playtime(
                Number(hours.value),
                Number(minutes.value),
                Number(seconds.value),
                Number(fraction.value),
            );
        }
        const [h, m, s, f, cs] = window.kh1.get_playtime();
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
    const curve = document.getElementById("curve");
    curve.value = window.kh1.curve.value;
    curve.addEventListener("change", () => {
        window.kh1.curve.value = curve.value;
    });
    const path = document.getElementById("path");
    path.value = window.kh1.path.value;
    path.addEventListener("change", () => {
        window.kh1.path.value = path.value;
    });
    const world = document.getElementById("world");
    world.value = window.kh1.world.value;
    world.addEventListener("change", () => {
        window.kh1.world.value = world.value;
    });
    const room = document.getElementById("room");
    room.addEventListener("change", () => {
        if (room.validity.valid)
            window.kh1.room.value = room.value;
        room.value = window.kh1.room.value;
    });
    const flag = document.getElementById("flag");
    flag.addEventListener("change", () => {
        if (flag.validity.valid)
            window.kh1.flag.value = flag.value;
        flag.value = window.kh1.flag.value;
    });
    const leader = document.getElementById("leader");
    leader.value = window.kh1.party[0];
    leader.addEventListener("change", () => {
        window.kh1.party[0] = leader.value;
    });
    const friend1 = document.getElementById("friend1");
    friend1.value = window.kh1.party[1];
    friend1.addEventListener("change", () => {
        window.kh1.party[1] = friend1.value;
    });
    const friend2 = document.getElementById("friend2");
    friend2.value = window.kh1.party[2];
    friend2.addEventListener("change", () => {
        window.kh1.party[2] = friend2.value;
    });
    const friend3 = document.getElementById("friend3");
    friend3.value = window.kh1.party[3];
    friend3.addEventListener("change", () => {
        window.kh1.party[3] = friend3.value;
    });
    const munny = document.getElementById("munny");
    munny.addEventListener("change", () => {
        if (munny.validity.valid)
            window.kh1.munny.value = munny.value;
        munny.value = window.kh1.munny.value;
    });
}
