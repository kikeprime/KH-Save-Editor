export function create_battle_record() {
    const kh1jdiv = document.getElementById("kh1jdiv");
    const heartless_killed = `
    <label style="display: flex; gap: 10px; align-items: center">
        Heartless defeated:
        <input
            type="number"
            id="heartless_killed"
            min=0
            max=9999
            step=1
            value=${window.kh1.heartless_killed.value}
        >
    </label>`;
    const deaths = `
    <label style="display: flex; gap: 10px; align-items: center">
        Times defeated:
        <input
            type="number"
            id="deaths"
            min=0
            max=9999
            step=1
            value=${window.kh1.deaths.value}
        >
    </label>`;
    const deflected = `
    <label style="display: flex; gap: 10px; align-items: center">
        Attacks deflected:
        <input
            type="number"
            id="deflected"
            min=0
            max=9999
            step=1
            value=${window.kh1.deflected.value}
        >
    </label>`;
    const hits = `
    <label style="display: flex; gap: 10px; align-items: center">
        Times hit by an enemy:
        <input
            type="number"
            id="hits"
            min=0
            max=9999
            step=1
            value=${window.kh1.hits.value}
        >
    </label>`;
    const item_usage = `
    <label style="display: flex; gap: 10px; align-items: center">
        Total item usage:
        <input
            type="number"
            id="item_usage"
            min=0
            max=9999
            step=1
            value=${window.kh1.item_usage.value}
        >
    </label>`;
    const friend_ko = `
    <label style="display: flex; gap: 10px; align-items: center">
        Party member knockouts:
        <input
            type="number"
            id="friend_ko"
            min=0
            max=9999
            step=1
            value=${window.kh1.friend_ko.value}
        >
    </label>`;
    const cure_on_friends = `
    <label style="display: flex; gap: 10px; align-items: center">
        Curative spells cast on friend:
        <input
            type="number"
            id="cure_on_friends"
            min=0
            max=9999
            step=1
            value=${window.kh1.cure_on_friends.value}
        >
    </label>`;
    const taken_damage = `
    <label style="display: flex; gap: 10px; align-items: center">
        Times taken damage:
        <input
            type="number"
            id="taken_damage"
            min=0
            max=9999
            step=1
            value=${window.kh1.taken_damage.value}
        >
    </label>`;
    const weapon_usage = `
    <label style="display: flex; gap: 10px; align-items: center">
        Times using your weapon:
        <input
            type="number"
            id="weapon_usage"
            min=0
            max=9999
            step=1
            value=${window.kh1.weapon_usage.value}
        >
    </label>`;
    kh1jdiv.innerHTML = `
    <div style="margin-top: 20px">
        ${heartless_killed}
        ${deaths}
        ${deflected}
        ${hits}
        ${item_usage}
        ${friend_ko}
        ${cure_on_friends}
        <h3>Hidden Statistics:</h3>
        ${taken_damage}
        ${weapon_usage}
    </div>`;
    battle_record_callbacks();
}

function battle_record_callbacks() {
    const heartless_killed = document.getElementById("heartless_killed");
    heartless_killed.addEventListener("change", () => {
        if (heartless_killed.validity.valid)
            window.kh1.heartless_killed.value = heartless_killed.value;
        heartless_killed.value = window.kh1.heartless_killed.value;
    });
    const deaths = document.getElementById("deaths");
    deaths.addEventListener("change", () => {
        if (deaths.validity.valid)
            window.kh1.deaths.value = deaths.value;
        deaths.value = window.kh1.deaths.value;
    });
    const deflected = document.getElementById("deflected");
    deflected.addEventListener("change", () => {
        if (deflected.validity.valid)
            window.kh1.deflected.value = deflected.value;
        deflected.value = window.kh1.deflected.value;
    });
    const hits = document.getElementById("hits");
    hits.addEventListener("change", () => {
        if (hits.validity.valid)
            window.kh1.hits.value = hits.value;
        hits.value = window.kh1.hits.value;
    });
    const item_usage = document.getElementById("item_usage");
    item_usage.addEventListener("change", () => {
        if (item_usage.validity.valid)
            window.kh1.item_usage.value = item_usage.value;
        item_usage.value = window.kh1.item_usage.value;
    });
    const friend_ko = document.getElementById("friend_ko");
    friend_ko.addEventListener("change", () => {
        if (friend_ko.validity.valid)
            window.kh1.friend_ko.value = friend_ko.value;
        friend_ko.value = window.kh1.friend_ko.value;
    });
    const cure_on_friends = document.getElementById("cure_on_friends");
    cure_on_friends.addEventListener("change", () => {
        if (cure_on_friends.validity.valid)
            window.kh1.cure_on_friends.value = cure_on_friends.value;
        cure_on_friends.value = window.kh1.cure_on_friends.value;
    });
    const taken_damage = document.getElementById("taken_damage");
    taken_damage.addEventListener("change", () => {
        if (taken_damage.validity.valid)
            window.kh1.taken_damage.value = taken_damage.value;
        taken_damage.value = window.kh1.taken_damage.value;
    });
    const weapon_usage = document.getElementById("weapon_usage");
    weapon_usage.addEventListener("change", () => {
        if (weapon_usage.validity.valid)
            window.kh1.weapon_usage.value = weapon_usage.value;
        weapon_usage.value = window.kh1.weapon_usage.value;
    });
}
