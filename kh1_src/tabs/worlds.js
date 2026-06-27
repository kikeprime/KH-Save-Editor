export function create_worlds() {
    const kh1div = document.getElementById("kh1div");
    const world_list = [...new Set([
        ...Object.entries(window.kh1.world_dict).map(([value, label]) => label),
        ...Object.entries(window.kh1.landingpoints_dict).map(([label, value]) => label),
    ])];
    kh1div.innerHTML = `
    <div>
        <div>
            <h3>World:</h3>
            <select id="kh1wtabs">
                ${
                    world_list
                        .map((label) => `<option value="${label}">${label}</option>`)
                        .join("")
                }
            </select>
        </div>
        <div id="kh1wdiv"></div>
    </div>`;
    const kh1wtabs = document.getElementById("kh1wtabs");
    const kh1wdiv = document.getElementById("kh1wdiv");
    function tab_sel() {
        let wm_status = "";
        let progress = "";
        let tw2_progress = "";
        const w = kh1wtabs.value;
        if (w in window.kh1.landingpoints_dict) {
            const lp = window.kh1.landingpoints_dict[w];
            wm_status = `
            <div>
                <h3>World Status:</h3>
                <select id="world_statuses" name=${lp[0]}>
                    ${
                        Object.entries(window.kh1.world_status_dict)
                            .map(([label, value]) => `<option value="${value}">${label}</option>`)
                            .join("")
                    }
                </select>
                ${lp.length > 1 ? "<h3>Landing Points:</h3>" : ""}
                <div id="landingpoints">
                    ${
                        lp.filter((value, idx) => idx > 0)
                            .map((label, idx) => 
                                `<label style="display: flex; align-items: center; gap: 10px">
                                    <input
                                        type="checkbox"
                                        name=${lp[0]}
                                        value=${1 << idx}
                                        ${window.kh1.landingpoints[lp[0]] & (1 << idx) ? "checked" : ""}
                                    >
                                    ${label}
                                </label>`
                            )
                            .join("")
                    }
                </div>
            </div>`;
        }
        if (w in window.kh1.world_progress_dict) {
            const idx = window.kh1.world_progress_dict[w]["index"];
            progress = `
            <div>
                <h3>Progress:</h3>
                <select id="world_progresses" name=${idx}>
                    ${
                        Object.entries(window.kh1.world_progress_dict[w])
                            .filter(([label, value]) => label != "index")
                            .map(([label, value]) => `<option value="${value}">${label}</option>`)
                            .join("")
                    }
                </select>
            </div>`;
        }
        if (w == "Traverse Town") {
            const idx = window.kh1.world_progress_dict[w+" 2"]["index"];
            tw2_progress = `
            <div>
                <h3>2nd visit progress:</h3>
                <select id="tw2_progress" name=${idx}>
                    ${
                        Object.entries(window.kh1.world_progress_dict[w+" 2"])
                            .filter(([label, value]) => label != "index")
                            .map(([label, value]) => `<option value="${value}">${label}</option>`)
                            .join("")
                    }
                </select>
            </div>`;
        }
        kh1wdiv.innerHTML = `
        <div>
            ${wm_status}
            ${progress}
            ${tw2_progress}
        </div>`;
        worlds_callbacks(w);
    }
    kh1wtabs.addEventListener("change", tab_sel);
    kh1wtabs.value = "Traverse Town";
    tab_sel();
}

function worlds_callbacks(w) {
    if (w in window.kh1.landingpoints_dict) {
        const world_statuses = document.getElementById("world_statuses");
        world_statuses.value = window.kh1.world_statuses[world_statuses.name];
        world_statuses.addEventListener("change", () => {
            window.kh1.world_statuses[world_statuses.name] = world_statuses.value;
        });
        const landingpoints = document.getElementById("landingpoints");
        landingpoints.addEventListener("change", (e) => {
            if (e.target.checked)
                window.kh1.landingpoints[e.target.name] |= e.target.value;
            else
                window.kh1.landingpoints[e.target.name] &= ~e.target.value;
        });
    }
    if (w in window.kh1.world_progress_dict) {
        const world_progresses = document.getElementById("world_progresses");
        world_progresses.value = window.kh1.world_progresses[world_progresses.name];
        world_progresses.addEventListener("change", () => {
            window.kh1.world_progresses[world_progresses.name] = world_progresses.value;
        });
    }
    if (w == "Traverse Town") {
        const tw2_progress = document.getElementById("tw2_progress");
        tw2_progress.value = window.kh1.world_progresses[tw2_progress.name];
        tw2_progress.addEventListener("change", () => {
            window.kh1.world_progresses[tw2_progress.name] = tw2_progress.value;
        });
    }
}
