export function create_general() {
    const kh02div = document.getElementById("kh02div");
    const vibration = `
    <div>
        <h3>Vibration</h3>
        <select id="vibration">
            <option value=0>Off</option>
            <option value=${1 << 0}>On</option>
        </select>
    </div>`;
    const camera_vertical = `
    <div>
        <h3>Invert Camera Vertical</h3>
        <select id="camera_vertical">
            <option value=0>Normal</option>
            <option value=${1 << 1}>Inverted</option>
        </select>
    </div>`;
    const camera_horizontal = `
    <div>
        <h3>Invert Camera Horizontal</h3>
        <select id="camera_horizontal">
            <option value=0>Normal</option>
            <option value=${1 << 2}>Inverted</option>
        </select>
    </div>`;
    const minimap = `
    <div>
        <h3>Minimap</h3>
        <select id="minimap">
            <option value=0>Off</option>
            <option value=${1 << 3}>On</option>
        </select>
    </div>`;
    const subtitles = `
    <div>
        <h3>Subtitles</h3>
        <select id="subtitles">
            <option value=0>Off</option>
            <option value=${1 << 4}>On</option>
        </select>
    </div>`;
    const exp_gain = `
    <div>
        <h3>EXP Gain</h3>
        <select id="exp_gain">
            <option value=0>Off</option>
            <option value=${1 << 6}>On</option>
        </select>
    </div>`;
    kh02div.innerHTML = `
    <div>
        ${vibration}
        ${camera_vertical}
        ${camera_horizontal}
        ${minimap}
        ${subtitles}
        ${exp_gain}
    </div>`;
    general_callbacks();
}

function general_callbacks() {
    const vibration = document.getElementById("vibration");
    vibration.value = window.kh02.config.value & (1 << 0);
    vibration.addEventListener("change", () => {
        if (vibration.value != 0)
            window.kh02.config.value |= (1 << 0);
        else
            window.kh02.config.value &= ~(1 << 0);
    });
    const camera_vertical = document.getElementById("camera_vertical");
    camera_vertical.value = window.kh02.config.value & (1 << 1);
    camera_vertical.addEventListener("change", () => {
        if (camera_vertical.value != 0)
            window.kh02.config.value |= (1 << 1);
        else
            window.kh02.config.value &= ~(1 << 1);
    });
    const camera_horizontal = document.getElementById("camera_horizontal");
    camera_horizontal.value = window.kh02.config.value & (1 << 2);
    camera_horizontal.addEventListener("change", () => {
        if (camera_horizontal.value != 0)
            window.kh02.config.value |= (1 << 2);
        else
            window.kh02.config.value &= ~(1 << 2);
    });
    const minimap = document.getElementById("minimap");
    minimap.value = window.kh02.config.value & (1 << 3);
    minimap.addEventListener("change", () => {
        if (minimap.value != 0)
            window.kh02.config.value |= (1 << 3);
        else
            window.kh02.config.value &= ~(1 << 3);
    });
    const subtitles = document.getElementById("subtitles");
    subtitles.value = window.kh02.config.value & (1 << 4);
    subtitles.addEventListener("change", () => {
        if (subtitles.value != 0)
            window.kh02.config.value |= (1 << 4);
        else
            window.kh02.config.value &= ~(1 << 4);
    });
    const exp_gain = document.getElementById("exp_gain");
    exp_gain.value = window.kh02.config.value & (1 << 6);
    exp_gain.addEventListener("change", () => {
        if (exp_gain.value != 0)
            window.kh02.config.value |= (1 << 6);
        else
            window.kh02.config.value &= ~(1 << 6);
    });
}
