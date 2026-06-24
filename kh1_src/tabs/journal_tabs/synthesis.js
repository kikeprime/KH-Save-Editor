export function create_synthesis() {
    const kh1jdiv = document.getElementById("kh1jdiv");
    let synthesis = `<div id="synthesis">`;
    Object.entries(window.kh1.synth_dict).forEach(([label, value]) => {
        const idx = Math.floor(value / 16);
        const bit = value % 8;
        synthesis += `
        <label style="display: flex; align-items: center">
            <input
                type="checkbox"
                name=${idx}
                value=${1 << bit}
                ${window.kh1.synth_flags[idx] & (1 << bit) ? "checked" : ""}
            >
            ${label}
        </label>`;
    });
    kh1jdiv.innerHTML = `
    <div>
        <h3>Synthesized Items:</h3>
        ${synthesis}
    </div>`;
    synthesis += "</div>";
    synthesis_callbacks();
}

function synthesis_callbacks() {
    const synthesis = document.getElementById("synthesis");
    synthesis.addEventListener("change", (e) => {
        if (e.target.checked)
            window.kh1.synth_flags[e.target.name] |= e.target.value;
        else
            window.kh1.synth_flags[e.target.name] &= ~e.target.value;
    });
}
