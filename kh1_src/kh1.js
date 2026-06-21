import * as dt from "./datatypes.js"
import dicts from "./kh1_dicts.js"
import * as tabs from "./tabs/index.js"

class KH1Character {
    constructor(name, offset, data) {
        this.name = name;
        this.data = data;
        this.level = new dt.U8(offset+0x00, data);
        this.hp = new dt.U8(offset+0x01, data);
        this.maxhp = new dt.U8(offset+0x02, data);
        this.mp = new dt.U8(offset+0x03, data);
        this.maxmp = new dt.U8(offset+0x04, data);
        this.maxap = new dt.U8(offset+0x05, data);
        this.strength = new dt.U8(offset+0x06, data);
        this.defense = new dt.U8(offset+0x07, data);
        this.resistances = dt.Array(dt.U8, 0x10, offset+0x08, data);
        this.accessoryslots = new dt.U8(offset+0x18, data);
        this.accessories = dt.Array(dt.U8, 0x08, offset+0x19, data);
        this.itemslots = new dt.U8(offset+0x21, data);
        this.items = dt.Array(dt.U8, 0x08, offset+0x22, data);
        this.weapon = new dt.U8(offset+0x32, data);
        this.submp = new dt.U16(offset+0x38, data);
        this.exp = new dt.U32(offset+0x3C, data);
        this.abilities = dt.Array(dt.U8, 0x30, offset+0x40, data);
        this.magic = new dt.U8(offset+0x70, data);
    }
    
    toString() {
        return `${this.name}(
    Level: ${this.level.value}
    HP: ${this.hp.value}
    Max HP: ${this.maxhp.value}
    MP: ${this.mp.value}
    Max MP: ${this.maxmp.value}
    Max AP: ${this.maxap.value}
    Strength: ${this.strength.value}
    Defense: ${this.defense.value}
    Accessory Slots: ${this.accessoryslots.value}
    Item Slots: ${this.itemslots.value}
    Sub MP: ${this.submp.value} (${this.submp.value / 0x1E} ${this.submp.value % 0x1E})
    EXP: ${this.exp.value}
)`;
    }
}

export default class KH1 {
    constructor(file, fm) {
        this.file = file
        this.fm = fm;
        dicts(this);
        this.loaded = this._load();
    }
    
    async _load() {
        const buffer = await this.file.arrayBuffer();
        this.buffer = new Uint8Array(buffer);
        this.data = new DataView(buffer);
        this.parse_data();
    }
    
    async load_sys(file) {
        this.sysfile = file
        const buffer = await this.sysfile.arrayBuffer();
        this.sysbuffer = new Uint8Array(buffer);
        this.sysdata = new DataView(buffer);
        this.playtime = new dt.U32(0x10, this.sysdata);
    }
    
    parse_data() {
        this.header = new dt.U8(0x00, this.data);
        this.sora = new KH1Character("Sora", 0x04, this.data);
        this.donald = new KH1Character("Donald", 0x04+0x74, this.data);
        this.goofy = new KH1Character("Goofy", 0x04+2*0x74, this.data);
        this.tarzan = new KH1Character("Tarzan", 0x04+3*0x74, this.data);
        this.pooh = new KH1Character("Winnie the Pooh", 0x04+4*0x74, this.data);
        this.aladdin = new KH1Character("Aladdin", 0x04+5*0x74, this.data);
        this.ariel = new KH1Character("Ariel", 0x04+6*0x74, this.data);
        this.jack = new KH1Character("Jack Skellington", 0x04+7*0x74, this.data);
        this.peterpan = new KH1Character("Peter Pan", 0x04+8*0x74, this.data);
        this.beast = new KH1Character("Beast", 0x04+9*0x74, this.data);
        this.characters = [
            this.sora, this.donald, this.goofy,
            this.tarzan, this.pooh, this.aladdin,
            this.ariel, this.jack, this.peterpan,
            this.beast,
        ];
        this.path = new dt.U8(0x048C, this.data);
        this.curve = new dt.U8(0x048D, this.data);
        this.party = dt.Array(dt.U8, 4, 0x048E, this.data);
        this.magiclevels = dt.Array(dt.U8, 7, 0x0492, this.data);
        this.inventory = dt.Array(dt.U8, 0x100, 0x0499, this.data);
        this.shared_abilities = dt.Array(dt.U8, 0x30, 0x0599, this.data);
        this.treasures = dt.Array(dt.U8, 0x01FD, 0x05CC, this.data);
        this.summons = dt.Array(dt.U8, 7, 0x07D0, this.data);
        this.heartless = dt.Array(dt.U16, 36, 0x07D8, this.data);
        this.shortcuts = dt.Array(dt.U8, 3, 0x082C, this.data);
        this.world = new dt.U32(0x2040, this.data);
        this.room = new dt.U32(0x2044, this.data);
        this.flag = new dt.U32(0x2048, this.data);
        this.munny = new dt.U32(0x1641C, this.data);
        
        // Final Mix stuff
        if (this.fm) {
            this.heartless = dt.Array(dt.U16, 51, 0x07D8, this.data);
            this.shortcuts = dt.Array(dt.U8, 3, 0x0844, this.data);
        }
    }

    save() {
        return new Blob([this.buffer], { type: "application/octet-stream" });
    }
    
    syssave() {
        return new Blob([this.sysbuffer], { type: "application/octet-stream" });
    }
    
    menu() {
        const app = document.getElementById("app");
        const tabs_kh1_html = `
        <div>
            <h2>KH1 Tabs:</h2>
            <select id="tabs_kh1">
                <option value="General">General</option>
                <option value="Characters">Characters</option>
                <option value="Inventory">Inventory</option>
                <option value="Jiminy's Journal">Jiminy's Journal</option>
                <option value="Config">Config</option>
                <option value="Worlds">Worlds</option>
                <option value="Misc">Misc</option>
            </select>
        </div>
        `;
        app.innerHTML = `${tabs_kh1_html}<div id="kh1div"></div>`;
        const tabs_kh1 = document.getElementById("tabs_kh1");
        const kh1div = document.getElementById("kh1div");
        tabs.create_general();
        tabs_kh1.addEventListener("change", () => {
            switch (tabs_kh1.value) {
                case "General": {
                    tabs.create_general();
                    break;
                }
                case "Characters": {
                    tabs.create_characters();
                    break;
                }
                default: {
                    kh1div.innerHTML = "";
                    break;
                }
            }
        });
    }
    
    get_playtime(fps = 60) {
        return [
            Math.floor(Math.floor(this.playtime.value / fps) / 3600),
            Math.floor((Math.floor(this.playtime.value / fps) % 3600) / 60),
            (Math.floor(this.playtime.value / fps) % 3600) % 60,
            this.playtime.value % fps,
            Math.floor((this.playtime.value % fps * 100) / 60),
        ];
    }
    
    set_playtime(hours, minutes, seconds, fraction, fps = 60) {
        this.playtime.value = (hours * 3600 + minutes * 60 + seconds) * fps + fraction;
    }
    
    toString() {
        return `KH1(
    Final Mix: ${this.fm}
${String(this.sora)}
    Path: ${["Warrior", "Guardian", "Mystic"][this.path.value]}
    Curve: ${["Dawn", "Midday", "Dusk"][this.curve.value]}
)`;
    }
}
