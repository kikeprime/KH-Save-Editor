export function create_misc() {
    const kh1div = document.getElementById("kh1div");
    const raft = `
    <div>
        <h3>Name of the raft:</h3>
        <input
            type="text"
            id="raft"
            value="${window.kh1.raft.decode()}"
        >
    </div>`;
    const weapon_options = Object.entries(window.kh1.weapon_dict)
        .filter(([label, value]) => value < window.kh1.weapon_dict["Mage's Staff"])
        .map(([label, value]) => `\n\t<option value=${value}>${label}</option>`)
        .join("");
    const weapon_backup = `
    <div>
        <h3>Backed up keychain:</h3>
        <select id="weapon_backup">
            ${weapon_options}
        </select>
    </div>`;
    kh1div.innerHTML = `
    <div>
        ${raft}
        ${weapon_backup}
    </div>`;
    misc_callbacks();
}

function misc_callbacks() {
    const raft = document.getElementById("raft");
    raft.addEventListener("change", () => {
        window.kh1.raft.encode(raft.value);
        raft.value = window.kh1.raft.decode();
    });
    const weapon_backup = document.getElementById("weapon_backup");
    weapon_backup.value = window.kh1.weapon_backup.value;
    weapon_backup.addEventListener("change", () => {
        window.kh1.weapon_backup.value = weapon_backup.value;
    });
}
