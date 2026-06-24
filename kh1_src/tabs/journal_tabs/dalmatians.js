export function create_dalmatians() {
    const kh1jdiv = document.getElementById("kh1jdiv");
    const events = `
    <div>
        <label style="display: flex; align-items: center">
            <input
                type="checkbox"
                id="dalmatian_event"
                ${window.kh1.dalmatian_event.value == 1 ? "checked" : ""}
            >
            Watched all puppies event
        </label>
        <label style="display: flex; align-items: center">
            <input
                type="checkbox"
                id="dalmatian_gift_ready"
                ${window.kh1.dalmatian_gift_ready.value == 1 ? "checked" : ""}
            >
            Pongo & Perdita has a gift for you
        </label>
    </div>`;
    const gift_list = [
        "Curaga-G",
        "Firaga-G",
        "Thundara-G",
        "Mythril Shard",
        "Torn Page & Mythril",
        "Megalixir",
        "Orichalcum",
        "Ultima-G",
        window.kh1.fm ? "Tech Boost" : "Ribbon",
        "Gummi Set & Aero Upgrade",
    ];
    let gifts = `<div id="dalmatian_gifts">`;
    for (let i = 0; i < 10; i++) {
        gifts += `
        <label style="display: flex; align-items: center">
            <input
                type="checkbox"
                name=${i}
                ${window.kh1.dalmatian_gifts[i] == 1 ? "checked" : ""}
            >
            ${gift_list[i]}
        </label>`;
    }
    gifts += `</div>`;
    let dalmatians = `<div id="dalmatians">`;
    for (let i = 0; i < 99; i++) {
        const idx = Math.floor(i / 8);
        const bit = i % 8;
        if (i % 7 == 0 && i < 49 || i % 7 == 1 && i >= 49)
            dalmatians += `<div style="display: flex; gap: 10px">`;
        dalmatians += `
        <label style="display: flex; align-items: center">
            <input
                type="checkbox"
                name=${idx}
                value=${1 << (7 - bit)}
                ${window.kh1.dalmatians[idx] & (1 << (7 - bit)) ? "checked" : ""}
            >
            ${"Puppy " + String(i + 1)}
        </label>`;
        if (i % 7 == 6 && i < 49 || i % 7 == 0 && i >= 49)
            dalmatians += "</div>";
    }
    dalmatians += "</div>";
    kh1jdiv.innerHTML = `
    <div>
        <h3>Event Flags:</h3>
        ${events}
        <h3>Gift Flags:</h3>
        ${gifts}
        <h3>Puppy Flags:</h3>
        ${dalmatians}
    </div>`;
    dalmatians_callbacks();
}

function dalmatians_callbacks() {
    const dalmatian_event = document.getElementById("dalmatian_event");
    dalmatian_event.addEventListener("change", () => {
        if (dalmatian_event.checked)
            window.kh1.dalmatian_event.value = 1;
        else
            window.kh1.dalmatian_event.value = 0;
    });
    const dalmatian_gift_ready = document.getElementById("dalmatian_gift_ready");
    dalmatian_gift_ready.addEventListener("change", () => {
        if (dalmatian_gift_ready.checked)
            window.kh1.dalmatian_gift_ready.value = 1;
        else
            window.kh1.dalmatian_gift_ready.value = 0;
    });
    const dalmatian_gifts = document.getElementById("dalmatian_gifts");
    dalmatian_gifts.addEventListener("change", (e) => {
        if (e.target.checked)
            window.kh1.dalmatian_gifts[e.target.name] = 1;
        else
            window.kh1.dalmatian_gifts[e.target.name] = 0;
    });
    const dalmatians = document.getElementById("dalmatians");
    dalmatians.addEventListener("change", (e) => {
        if (e.target.checked)
            window.kh1.dalmatians[e.target.name] |= e.target.value;
        else
            window.kh1.dalmatians[e.target.name] &= ~e.target.value;
    });
}
