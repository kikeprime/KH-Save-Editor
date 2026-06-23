export function create_config() {
    const kh1div = document.getElementById("kh1div");
    const autolock = `
    <select id="autolock">
        <option value=0>On</option>
        <option value=1>Off</option>
    </select>`;
    const targetlock = `
    <select id="targetlock">
        <option value=0>Auto</option>
        <option value=1>Manual</option>
    </select>`;
    const camera = `
    <select id="camera">
        <option value=0>Auto</option>
        <option value=1>Manual</option>
    </select>`;
    const vibration = `
    <select id="vibration">
        <option value=0>On</option>
        <option value=1>Off</option>
    </select>`;
    const sound = `
    <select id="sound">
        <option value=0>Stereo</option>
        <option value=1>Mono</option>
    </select>`;
    const datainstall = `
    <select id="datainstall">
        <option value=0>DVD-ROM${window.kh1.fm ? "" : " / Normal"}</option>
        <option value=1>Hard Drive${window.kh1.fm ? "" : " / Expert"}</option>
    </select>`;
    const difficulty = !window.kh1.fm ? "" : `
    <h3>Difficulty</h3>
    <select id="difficulty">
        <option value=0>Beginner</option>
        <option value=1>Standard</option>
        <option value=2>Proud</option>
    </select>`;
    kh1div.innerHTML = `
    <div>
        <h3>Auto Lock</h3>
            ${autolock}
        <h3>Target Lock</h3>
            ${targetlock}
        <h3>Camera</h3>
            ${camera}
        <h3>Vibration</h3>
            ${vibration}
        <h3>Sound</h3>
            ${sound}
        <h3>Data Install${window.kh1.fm ? "" : " / Difficulty"}</h3>
            ${datainstall}
        ${difficulty}
    </div>`;
    config_callbacks();
}

function config_callbacks() {
    const autolock = document.getElementById("autolock");
    autolock.value = window.kh1.autolock.value;
    autolock.addEventListener("change", () => {
        window.kh1.autolock.value = autolock.value;
    });
    const targetlock = document.getElementById("targetlock");
    targetlock.value = window.kh1.targetlock.value;
    targetlock.addEventListener("change", () => {
        window.kh1.targetlock.value = targetlock.value;
    });
    const camera = document.getElementById("camera");
    camera.value = window.kh1.camera.value;
    camera.addEventListener("change", () => {
        window.kh1.camera.value = camera.value;
    });
    const vibration = document.getElementById("vibration");
    vibration.value = window.kh1.vibration.value;
    vibration.addEventListener("change", () => {
        window.kh1.vibration.value = vibration.value;
    });
    const sound = document.getElementById("sound");
    sound.value = window.kh1.sound.value;
    sound.addEventListener("change", () => {
        window.kh1.sound.value = sound.value;
    });
    const datainstall = document.getElementById("datainstall");
    datainstall.value = window.kh1.datainstall.value;
    datainstall.addEventListener("change", () => {
        window.kh1.datainstall.value = datainstall.value;
    });
    if (window.kh1.fm) {
        const difficulty = document.getElementById("difficulty");
        difficulty.value = window.kh1.difficulty.value;
        difficulty.addEventListener("change", () => {
            window.kh1.difficulty.value = difficulty.value;
        });
    }
}
