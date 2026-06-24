export function create_reports() {
    const kh1jdiv = document.getElementById("kh1jdiv");
    let reports = `<div id="reports">`;
    for (let i = 0; i < 13; i++) {
        const idx = Math.floor(i / 8);
        const bit = i % 8;
        reports += `
        <label style="display: flex; align-items: center">
            <input
                type="checkbox"
                name=${idx}
                value=${1 << (7 - bit)}
                ${window.kh1.reports[idx] & (1 << (7 - bit)) ? "checked" : ""}
            >
            ${"Ansem's Report " + String(i + 1)}
        </label>`;
    }
    kh1jdiv.innerHTML = `
    <div>
        ${reports}
    </div>`;
    reports += "</div>";
    reports_callbacks();
}

function reports_callbacks() {
    const reports = document.getElementById("reports");
    reports.addEventListener("change", (e) => {
        if (e.target.checked)
            window.kh1.reports[e.target.name] |= e.target.value;
        else
            window.kh1.reports[e.target.name] &= ~e.target.value;
    });
}
