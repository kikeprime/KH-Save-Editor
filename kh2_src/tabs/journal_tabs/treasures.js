export function create_treasures() {
    const kh2jdiv = document.getElementById("kh2jdiv");
    function rows(w, t) {
        return t.map((row) => `
        <tr>
            ${
                row.map((v) => `
                <td>
                    <input
                        type="checkbox"
                        name="${w}"
                        value=${v}
                        style="margin-bottom: 10px; margin-right: 10px"
                        ${window.kh2.treasures[Math.floor(v / 16)] & (1 << v % 16) ? "checked" : ""}
                    >
                </td>`)
                    .join("")
            }
        </tr>`)
            .join("");
    }
    kh2jdiv.innerHTML = `
    <div id="treasures" style="-webkit-text-size-adjust: 100%; text-size-adjust: 100%;">
        ${
            Object.entries(window.kh2.treasure_dict)
                .map(([w, t]) => `
                <div>
                    <h3>${w}</h3>
                    <label style="margin-bottom: -20px" id="${w}">Click on a checkbox to see the content!</label>
                    <table>
                        ${rows(w, t)}
                    </table>
                </div>`)
                .join("")
        }
    </div>`;
    treasures_callbacks();
}

function treasures_callbacks() {
    const treasures = document.getElementById("treasures");
    treasures.addEventListener("change", (e) => {
        const w = document.getElementById(e.target.name);
        w.innerHTML = window.kh2.treasure_zip[e.target.name][e.target.value];
        if (e.target.checked)
            window.kh2.treasures[Math.floor(e.target.value / 16)] |= (1 << e.target.value % 16);
        else
            window.kh2.treasures[Math.floor(e.target.value / 16)] &= ~(1 << e.target.value % 16);
    });
}
