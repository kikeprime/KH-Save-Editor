export function create_flags() {
    const kh1jdiv = document.getElementById("kh1jdiv");
    const journal_unlock = `
    <div id="journal_unlock">
        <label style="display: flex; align-items: center">
            <input
                type="checkbox"
                value=${1 << 3}
                ${window.kh1.journal_unlock.value & (1 << 3) ? "checked" : ""}
            >
            Jiminy's Journal unlocked
        </label>
    </div>`;
    kh1jdiv.innerHTML = `
    <div>
        ${journal_unlock}
    </div>`;
    flags_callbacks();
}

function flags_callbacks() {
    const journal_unlock = document.getElementById("journal_unlock");
    journal_unlock.addEventListener("change", (e) => {
        if (e.target.checked)
            window.kh1.journal_unlock.value |= e.target.value;
        else
            window.kh1.journal_unlock.value &= ~e.target.value;
    });
}
