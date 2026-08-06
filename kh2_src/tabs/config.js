export function create_config() {
    const kh2div = document.getElementById("kh2div");
    const difficulty = `
    <h3>Difficulty</h3>
    <select id="difficulty">
        <option value=0>Beginner</option>
        <option value=1>Standard</option>
        <option value=2>Proud</option>
        ${window.kh2.fm ? "<option value=3>Critical</option>" : ""}
    </select>`;
    kh2div.innerHTML = `
    <div>
        ${difficulty}
    </div>`;
    config_callbacks();
}

function config_callbacks() {
    const difficulty = document.getElementById("difficulty");
    difficulty.value = window.kh2.difficulty.value;
    difficulty.addEventListener("change", () => {
        window.kh2.difficulty.value = difficulty.value;
    });
}
