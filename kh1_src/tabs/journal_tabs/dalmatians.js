export function create_dalmatians() {
    const kh1jdiv = document.getElementById("kh1jdiv");
    let dalmatians = `<div id="dalmatians">`;
    for (let i = 0; i < 99; i++) {
        const idx = Math.floor(i / 8);
        const bit = i % 8;
        dalmatians += `
        <label style="display: flex; align-items: center">
            <input
                type="checkbox"
                name=${idx}
                value=${1 << (7 - bit)}
                ${window.kh1.dalmatians[idx] & (1 << (7 - bit)) ? "checked" : ""}
            >
            ${"Puppy " + String(i + 1)}
        </label>`;
    }
    kh1jdiv.innerHTML = `
    <div>
        ${dalmatians}
    </div>`;
    dalmatians += "</div>";
    dalmatians_callbacks();
}

function dalmatians_callbacks() {
    const dalmatians = document.getElementById("dalmatians");
    dalmatians.addEventListener("change", (e) => {
        if (e.target.checked)
            window.kh1.dalmatians[e.target.name] |= e.target.value;
        else
            window.kh1.dalmatians[e.target.name] &= ~e.target.value;
    });
}
