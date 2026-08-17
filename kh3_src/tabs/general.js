export function create_general() {
    const kh3div = document.getElementById("kh3div");
    const playtime = create_playtime();
    const power = `
    <div>
        <h3>Power:</h3>
        <select id="power">
            <option value=0>Warrior</option>
            <option value=1>Mystic</option>
            <option value=2>Guardian</option>
        </select>
    </div>`;
    const desire = `
    <div>
        <h3>Desire:</h3>
        <select id="desire">
            <option value=0>Vitality</option>
            <option value=1>Wisdom</option>
            <option value=2>Balance</option>
        </select>
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
            value=${window.kh3.munny.value}
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
            value=${window.kh3.exp.value}
        >
    </div>`;
    const difficulty = `
    <h3>Difficulty</h3>
    <select id="difficulty">
        <option value=0>Beginner</option>
        <option value=1>Standard</option>
        <option value=2>Proud</option>
        ${window.kh3.version > 0 ? "<option value=3>Critical</option>" : ""}
    </select>`;
    const decoder = new TextDecoder("utf-8");
    const path = decoder.decode(new Uint8Array(window.kh3.map_path));
    const map_path = `
    <div>
        <h4>Map Path:</h4>
        <input
            type="text"
            id="map_path"
            value="${path.slice(0, path.indexOf('\0'))}"
            style="width: 500px"
        >
    </div>`;
    const spawn = decoder.decode(new Uint8Array(window.kh3.map_spawn));
    const map_spawn = `
    <div>
        <h4>Map Spawn:</h4>
        <input
            type="text"
            id="map_spawn"
            value="${spawn.slice(0, spawn.indexOf('\0'))}"
            style="width: 500px"
        >
    </div>`;
    const script = decoder.decode(new Uint8Array(window.kh3.player_script));
    const player_script = `
    <div>
        <h4>Player Script:</h4>
        <input
            type="text"
            id="player_script"
            value="${script.slice(0, script.indexOf('\0'))}"
            style="width: 500px"
        >
    </div>`;
    const pawn = decoder.decode(new Uint8Array(window.kh3.player_pawn));
    const player_pawn = `
    <div>
        <h4>Player Pawn:</h4>
        <input
            type="text"
            id="player_pawn"
            value="${pawn.slice(0, pawn.indexOf('\0'))}"
            style="width: 500px"
        >
    </div>`;
    kh3div.innerHTML = `
    <div>
        ${playtime}
        ${power}
        ${desire}
        ${munny}
        ${exp}
        ${difficulty}
        <h3>Advanced Options</h3>
        <h3>Room Mod</h3>
        ${map_path}
        ${map_spawn}
        <h3>Player Mod</h3>
        ${player_script}
        ${player_pawn}
    </div>`;
    general_callbacks();
}

function create_playtime() {
    const playtime = window.kh3.get_playtime(window.kh3.playtime.value);
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
    </div>`;
}

function playtime_callbacks() {
    const hours = document.getElementById("hours");
    const minutes = document.getElementById("minutes");
    const seconds = document.getElementById("seconds");
    function update_playtime() {
        if (
            hours.validity.valid &&
            minutes.validity.valid &&
            seconds.validity.valid
        ) {
            window.kh3.playtime.value = window.kh3.set_playtime(
                Number(hours.value),
                Number(minutes.value),
                Number(seconds.value),
                Number(0),
            );
        }
        const [h, m, s, f, cs] = window.kh3.get_playtime(window.kh3.playtime.value);
        hours.value = h;
        minutes.value = m;
        seconds.value = s;
    }
    hours.addEventListener("change", update_playtime);
    minutes.addEventListener("change", update_playtime);
    seconds.addEventListener("change", update_playtime);
}

function general_callbacks() {
    playtime_callbacks();
    const power = document.getElementById("power");
    power.value = window.kh3.power.value;
    power.addEventListener("change", () => {
        window.kh3.power.value = power.value;
    });
    const desire = document.getElementById("desire");
    desire.value = window.kh3.desire.value;
    desire.addEventListener("change", () => {
        window.kh3.desire.value = desire.value;
    });
    const munny = document.getElementById("munny");
    munny.addEventListener("change", () => {
        if (munny.validity.valid)
            window.kh3.munny.value = munny.value;
        munny.value = window.kh3.munny.value;
    });
    const exp = document.getElementById("exp");
    exp.addEventListener("change", () => {
        if (exp.validity.valid)
            window.kh3.exp.value = exp.value;
        exp.value = window.kh3.exp.value;
    });
    const difficulty = document.getElementById("difficulty");
    difficulty.value = window.kh3.difficulty.value;
    difficulty.addEventListener("change", () => {
        window.kh3.difficulty.value = difficulty.value;
    });
    const decoder = new TextDecoder("utf-8");
    const encoder = new TextEncoder("utf-8");
    const map_path = document.getElementById("map_path");
    map_path.addEventListener("change", () => {
        window.kh3.map_path.fill(0);
        for (let i = 0; i < map_path.value.length; i++) {
            window.kh3.map_path[i] = encoder.encode(map_path.value)[i];
        }
        const path = decoder.decode(new Uint8Array(window.kh3.map_path));
        map_path.value = path.slice(0, path.indexOf('\0'));
    });
    const map_spawn = document.getElementById("map_spawn");
    map_spawn.addEventListener("change", () => {
        window.kh3.map_spawn.fill(0);
        for (let i = 0; i < map_spawn.value.length; i++) {
            window.kh3.map_spawn[i] = encoder.encode(map_spawn.value)[i];
        }
        const spawn = decoder.decode(new Uint8Array(window.kh3.map_spawn));
        map_spawn.value = spawn.slice(0, spawn.indexOf('\0'));
    });
    const player_script = document.getElementById("player_script");
    player_script.addEventListener("change", () => {
        window.kh3.player_script.fill(0);
        for (let i = 0; i < player_script.value.length; i++) {
            window.kh3.player_script[i] = encoder.encode(player_script.value)[i];
        }
        const script = decoder.decode(new Uint8Array(window.kh3.player_script));
        player_script.value = script.slice(0, script.indexOf('\0'));
    });
    const player_pawn = document.getElementById("player_pawn");
    player_pawn.addEventListener("change", () => {
        window.kh3.player_pawn.fill(0);
        for (let i = 0; i < player_pawn.value.length; i++) {
            window.kh3.player_pawn[i] = encoder.encode(player_pawn.value)[i];
        }
        const pawn = decoder.decode(new Uint8Array(window.kh3.player_pawn));
        player_pawn.value = pawn.slice(0, pawn.indexOf('\0'));
    });
}
