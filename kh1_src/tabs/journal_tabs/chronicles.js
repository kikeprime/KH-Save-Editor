export function create_chronicles() {
    const kh1jdiv = document.getElementById("kh1jdiv");
    let chronicles = `<div id="chronicles">`;
    Object.entries(window.kh1.chronicles_dict).forEach(([label, value], idx) => {
        chronicles += `
        <h3>${label}</h3>
        <label style="display: flex; align-items: center">
            <input
                type="radio"
                name=${idx}
                value=0
                ${window.kh1.chronicles[idx] == 0 ? "checked" : ""}
            >
            Locked
        </label>`;
        for (let i = 0; i < value; i++) {
            chronicles += `
            <label style="display: flex; align-items: center">
                <input
                    type="radio"
                    name=${idx}
                    value=${1 << (7 - i)}
                    ${window.kh1.chronicles[idx] & (1 << (7 - i)) ? "checked" : ""}
                >
                ${"Part " + String(i + 1)}
            </label>`;
        }
    });
    chronicles += "</div>";
    kh1jdiv.innerHTML = `
    <div>
        ${chronicles}
    </div>`;
    chronicles_callbacks();
}

function chronicles_callbacks() {
    const chronicles = document.getElementById("chronicles");
    chronicles.addEventListener("change", (e) => {
        window.kh1.chronicles[e.target.name] = e.target.value;
    });
}
