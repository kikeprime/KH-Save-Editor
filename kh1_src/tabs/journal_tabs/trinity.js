export function create_trinity() {
    const kh1jdiv = document.getElementById("kh1jdiv");
    const trinity_unlock = `
    <div id="trinity_unlock">
        <h3>Trinity Unlock Flags:</h3>
        ${
            window.kh1.trinity_names
                .map((label, idx) => `
                <label style="display: flex; align-items: center">
                    <input
                        type="checkbox"
                        value=${1 << idx}
                        ${window.kh1.trinity_unlock.value & (1 << idx) ? "checked" : ""}
                    >
                    ${label}
                </label>`)
                .join("")
        }
    </div>`;
    kh1jdiv.innerHTML = `
    <div>
        ${trinity_unlock}
        <div>
            <h3>Trinity Type:</h3>
            <select id="kh1jtltabs">
                ${
                    window.kh1.trinity_names
                        .map((label, idx) => `<option value=${idx}>${label}</option>`)
                        .join("")
                }
            </select>
        </div>
        <div id="kh1jtldiv"></div>
    </div>`;
    const kh1jtltabs = document.getElementById("kh1jtltabs");
    const kh1jtldiv = document.getElementById("kh1jtldiv");
    function tab_sel() {
        const idx = Number(kh1jtltabs.value);
        kh1jtldiv.innerHTML = `
        <div>
            <h3>Count:</h3>
            <input
                type="number"
                id="trinity_count"
                name=${idx > 0 ? idx + 1 : idx}
                min=0
                max=255
                step=1
                value=${window.kh1.trinity_count[idx > 0 ? idx + 1 : idx]}
                disabled
            >
        </div>`
        kh1jtldiv.innerHTML += `
        <div id="trinity_flags">
            <h3>Unlocked Trinities:</h3>
            ${
                Object.entries(window.kh1.trinity_dict_list[idx])
                    .map(([label, value]) => {
                        const byte = value != 0x1A40 ?
                            window.kh1.trinity_flags[Math.floor(value / 16)] :
                            window.kh1.buffer[0x1C6C + Math.floor(value / 16)]
                        return `
                        <label style="display: flex; align-items: center">
                            <input
                                type="checkbox"
                                value=${value}
                                ${byte & (1 << value % 16) ? "checked" : ""}
                            >
                            ${label}
                        </label>`
                    })
                    .join("")
            }
        </div>`;
        trinity_callbacks();
    }
    kh1jtltabs.addEventListener("change", tab_sel);
    tab_sel();
}

function trinity_callbacks() {
    const trinity_unlock = document.getElementById("trinity_unlock");
    trinity_unlock.addEventListener("change", (e) => {
        if (e.target.checked)
            window.kh1.trinity_unlock.value |= e.target.value;
        else
            window.kh1.trinity_unlock.value &= ~e.target.value;
    });
    const trinity_count = document.getElementById("trinity_count");
    const trinity_flags = document.getElementById("trinity_flags");
    trinity_flags.addEventListener("change", (e) => {
        const idx = Math.floor(e.target.value / 16);
        const bit = e.target.value % 16;
        if (e.target.checked) {
            if (e.target.value != 0x1A40)
                window.kh1.trinity_flags[idx] |= (1 << bit);
            else
                window.kh1.buffer[0x1C6C + idx] |= (1 << bit);
        }
        else {
            if (e.target.value != 0x1A40)
                window.kh1.trinity_flags[idx] &= ~(1 << bit);
            else
                window.kh1.buffer[0x1C6C + idx] &= ~(1 << bit);
        }
        trinity_count.value = trinity_flags.querySelectorAll("input[type=checkbox]:checked").length;
        window.kh1.trinity_count[trinity_count.name] = trinity_count.value;
    });
}
