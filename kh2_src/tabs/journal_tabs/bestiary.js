export function create_bestiary() {
    const kh2jdiv = document.getElementById("kh2jdiv");
    kh2jdiv.innerHTML = `
    <div>
        <div>
            <h3>Sub Entry:</h3>
            <select id="kh2jbtabs">
                <option value="The Heartless">The Heartless</option>
                <option value="The Nobodies">The Nobodies</option>
                <option value="Reaction Commands">Reaction Commands</option>
                <option value="Limits">${window.kh2.fm ? "Limits" : "Combo Attacks"}</option>
            </select>
        </div>
        <div id="kh2jbdiv"></div>
    </div>`;
    const kh2jbtabs = document.getElementById("kh2jbtabs");
    function tab_sel() {
        switch (kh2jbtabs.value) {
            case "The Heartless": {
                create_heartless();
                break;
            }
            case "The Nobodies": {
                create_nobodies();
                break;
            }
            case "Reaction Commands": {
                create_rcs();
                break;
            }
            case "Limits": {
                create_limits();
                break;
            }
        }
    }
    kh2jbtabs.addEventListener("change", tab_sel);
    tab_sel();
}

function create_heartless() {
    const kh2jbdiv = document.getElementById("kh2jbdiv");
    const heartless = `
    <div id="heartless">
        ${
            window.kh2.heartless_list
                .filter((k) => window.kh2.heartless_dict[k] < window.kh2.heartless.length)
                .map((label) => `
                <label style="display: flex; gap: 10px; align-items: center">
                    ${label}:
                    <input
                        type="number"
                        name=${window.kh2.heartless_dict[label]}
                        min=0
                        max=999999
                        step=1
                        value=${window.kh2.heartless[window.kh2.heartless_dict[label]]}
                    >
                </label>`)
                .join("")
        }
    </div>`;
    kh2jbdiv.innerHTML = `
    <div>
        <h3>Heartless Kill Counts:</h3>
        ${heartless}
    </div>`;
    heartless_callbacks();
}

function heartless_callbacks() {
    const heartless = document.getElementById("heartless");
    heartless.addEventListener("change", (e) => {
        if (e.target.validity.valid)
            window.kh2.heartless[e.target.name] = e.target.value;
        e.target.value = window.kh2.heartless[e.target.name];
    });
}

function create_nobodies() {
    const kh2jbdiv = document.getElementById("kh2jbdiv");
    const nobodies = `
    <div id="nobodies">
        ${
            window.kh2.nobody_list
                .map((label) => `
                <label style="display: flex; gap: 10px; align-items: center">
                    ${label}:
                    <input
                        type="number"
                        name=${window.kh2.nobody_dict[label]}
                        min=0
                        max=999999
                        step=1
                        value=${window.kh2.nobodies[window.kh2.nobody_dict[label]]}
                    >
                </label>`)
                .join("")
        }
    </div>`;
    kh2jbdiv.innerHTML = `
    <div>
        <h3>Nobody Kill Counts:</h3>
        ${nobodies}
    </div>`;
    nobodies_callbacks();
}

function nobodies_callbacks() {
    const nobodies = document.getElementById("nobodies");
    nobodies.addEventListener("change", (e) => {
        if (e.target.validity.valid)
            window.kh2.nobodies[e.target.name] = e.target.value;
        e.target.value = window.kh2.nobodies[e.target.name];
    });
}

function create_rcs() {
    const kh2jbdiv = document.getElementById("kh2jbdiv");
    const rcs = `
    <div id="rcs">
        ${
            Object.entries(window.kh2.rc_list_dict)
                .filter(([label, value]) => window.kh2.rc_dict[value[0]] < window.kh2.rc_usage.length)
                .map(([label, value]) => `
                <div style="-webkit-text-size-adjust: 100%; text-size-adjust: 100%;">
                    <h3>${label}:</h3>
                    ${
                        value
                            .map((rc) => `
                            <label style="display: flex; gap: 10px; align-items: center">
                                ${rc}:
                                <input
                                    type="number"
                                    name=${window.kh2.rc_dict[rc]}
                                    min=0
                                    max=9999
                                    step=1
                                    value=${window.kh2.rc_usage[window.kh2.rc_dict[rc]]}
                                >
                            </label>`)
                            .join("")
                    }
                </div>`)
                .join("")
        }
    </div>`;
    kh2jbdiv.innerHTML = `
    <div>
        ${rcs}
    </div>`;
    rcs_callbacks();
}

function rcs_callbacks() {
    const rcs = document.getElementById("rcs");
    rcs.addEventListener("change", (e) => {
        if (e.target.validity.valid)
            window.kh2.rc_usage[e.target.name] = e.target.value;
        e.target.value = window.kh2.rc_usage[e.target.name];
    });
}

function create_limits() {
    const kh2jbdiv = document.getElementById("kh2jbdiv");
    const limit_usage = `
    <div id="limit_usage">
        ${
            window.kh2.limit_list
                .filter((k) => window.kh2.limit_dict[k] < window.kh2.limit_usage.length)
                .map((label) => `
                <label style="display: flex; gap: 10px; align-items: center">
                    ${label}:
                    <input
                        type="number"
                        name=${window.kh2.limit_dict[label]}
                        min=0
                        max=999999
                        step=1
                        value=${window.kh2.limit_usage[window.kh2.limit_dict[label]]}
                    >
                </label>`)
                .join("")
        }
    </div>`;
    kh2jbdiv.innerHTML = `
    <div>
        <h3>Limit Hit Counts:</h3>
        ${limit_usage}
    </div>`;
    limit_usage_callbacks();
}

function limit_usage_callbacks() {
    const limit_usage = document.getElementById("limit_usage");
    limit_usage.addEventListener("change", (e) => {
        if (e.target.validity.valid)
            window.kh2.limit_usage[e.target.name] = e.target.value;
        e.target.value = window.kh2.limit_usage[e.target.name];
    });
}
