export function create_minigames() {
    const kh2jdiv = document.getElementById("kh2jdiv");
    const minigame_list = window.kh2.minigame_list
        .filter((name, i) => i < window.kh2.minigames.length);
    const minigame_list_dict = Object.entries(window.kh2.minigame_list_dict)
        .filter(([label, value]) => minigame_list.includes(value[0]));
    const minigames = `
    <div id="minigames" style="-webkit-text-size-adjust: 100%; text-size-adjust: 100%;">
        ${
            minigame_list_dict
                .map(([world, mgs]) => `
                <div>
                    <h3>${world}:</h3>
                    ${
                        mgs
                            .filter((mg) => minigame_list.includes(mg))
                            .map((mg) => create_minigame(mg))
                            .join("")
                    }
                </div>`)
                .join("")
        }
    </div>`;
    kh2jdiv.innerHTML = `
    <div>
        ${minigames}
    </div>`;
    minigames_callbacks(minigame_list);
}

function create_minigame(mg) {
    const idx = window.kh2.minigame_list.indexOf(mg);
    let score = "";
    if (window.kh2.minigame_type_dict[window.kh2.minigames[idx].type.value] != "Time") {
        score = `
        <input
            type="number"
            name=${idx}
            min=0
            max=999999
            step=1
            value=${window.kh2.minigames[idx].score.value}
        >`;
    }
    else {
        const time = window.kh2.get_playtime(window.kh2.minigames[idx].score.value);
        score = `
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
        </div>`;
    }
    const type_dd = `
    <select name=${idx}>
        ${
            Object.entries(window.kh2.minigame_type_dict)
                .map(([value, label]) => `<option value=${value}>${label}</option>`)
                .join("")
        }
    </select>`;
    return `
    <div id="${mg}">
        <h4>${mg}:</h4>
        <div style="display: flex; gap: 10px; align-items: center">
            ${score}
            ${type_dd}
        </div>
    </div>`;
}

function minigames_callbacks(minigame_list) {
    const minigames = document.getElementById("minigames");
    minigames.querySelectorAll("select").forEach(select => {
        select.value = window.kh2.minigames[select.name].type.value;
        select.addEventListener("change", () => {
            window.kh2.minigames[select.name].type.value = select.value;
            create_minigames();
        });
    });
    minigame_list.forEach((mg) => {
        const idx = window.kh2.minigame_list.indexOf(mg);
        const minigame = document.getElementById(mg);
        minigame.addEventListener("change", (e) => {
            if (window.kh2.minigame_type_dict[window.kh2.minigames[idx].type.value] == "Time") {
                const inputs = minigame.querySelectorAll(`input[type="number"]:not([disabled])`);
                const values = [0];
                inputs.forEach(input => {
                    if (input.validity.valid)
                        values.push(Number(input.value));
                });
                if (values.length == 4) {
                    window.kh2.minigames[idx].score.value = window.kh2.set_playtime(...values);
                }
                create_minigames();
            }
            else if (e.target.type == "number") {
                if (e.target.validity.valid)
                    window.kh2.minigames[e.target.name].score.value = e.target.value;
                e.target.value = window.kh2.minigames[e.target.name].score.value;
             }
        });
    });
}
