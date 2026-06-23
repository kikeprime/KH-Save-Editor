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
        this.cure_on_friends = new dt.U16(0x0836, this.data);
        this.heartless_killed = new dt.U16(0x083E, this.data);
        this.deflected = new dt.U16(0x0844, this.data);
        this.taken_damage = new dt.U16(0x0846, this.data);
        this.item_usage = new dt.U16(0x0848, this.data);
        this.hits = new dt.U16(0x084A, this.data);
        this.friend_ko = new dt.U16(0x084C, this.data);
        this.deaths = new dt.U16(0x084E, this.data);
        this.weapon_usage = new dt.U16(0x0856, this.data);
        
        this.dalmatian_event = new dt.U8(0x0E3A, this.data);
        this.dalmatian_gifts = dt.Array(dt.U8, 10, 0x0E3C, this.data);
        this.dalmatian_gift_ready = new dt.U8(0x0E47, this.data);
        
        this.currentcup = new dt.U8(0x0F26, this.data);
        this.philcup = new dt.U8(0x0F36, this.data);
        this.pegasuscup = new dt.U8(0x0F37, this.data);
        this.herculescup = new dt.U8(0x0F38, this.data);
        this.hadescup = new dt.U8(0x0F39, this.data);
        this.oc_minigames = dt.Array(dt.S32, 0x18, 0x0F4C, this.data);
        this.goldmatch = new dt.U8(0x0F69, this.data);
        this.platinummatch = new dt.U8(0x0F6A, this.data);
        
        this.tiduswins = new dt.U8(0x101B, this.data);
        this.wakkawins = new dt.U8(0x101C, this.data);
        this.selphiewins = new dt.U8(0x101D, this.data);
        
        this.sorawins = new dt.U16(0x1036, this.data);
        this.rikuwins = new dt.U16(0x1038, this.data);
        
        this.tidus_event = new dt.U8(0x103A, this.data);
        this.wakka_event = new dt.U8(0x103B, this.data);
        this.selphie_event = new dt.U8(0x103C, this.data);
        
        this.tidus_beaten = new dt.U8(0x105F, this.data);
        this.wakka_beaten = new dt.U8(0x1060, this.data);
        this.selphie_beaten = new dt.U8(0x1061, this.data);
        
        this.weapon_backup = new dt.U8(0x1114, this.data);
        
        this.slides = dt.Array(dt.U8, 6, 0x1207, this.data);
        this.slides_watched = new dt.U8(0x1212, this.data);

        this.world_progresses = dt.Array(dt.U8, 20, 0x1500, this.data);
        
        this.journal_chars = dt.Array(dt.U8, 23, 0x16E3, this.data);
        this.dalmatians = dt.Array(dt.U8, 13, 0x1703, this.data);
        this.minigames = dt.Array(dt.S32, 0x46, 0x1728, this.data);
        this.chronicles = dt.Array(dt.U32, 10, 0x1997, this.data);
        this.reports = dt.Array(dt.U8, 2, 0x19C0, this.data);
        this.journal_unlock = new dt.U8(0x19C4, this.data);
        this.synth_flags = dt.Array(dt.U8, 5, 0x19C8, this.data);
        
        this.trinity_unlock = new dt.U8(0x1C1B, this.data);
        this.trinity_count = dt.Array(dt.U8, 6, 0x1C66, this.data);
        this.trinity_flags = dt.Array(dt.U8, 0x48, 0x1C6C, this.data);
        
        this.clams = dt.Array(dt.U8, 2, 0x1DA9, this.data);
        this.large_chest_state = new dt.U8(0x1DAB, this.data);
        
        this.bigben = dt.Array(dt.U8, 2, 0x1E61, this.data);
        
        this.world_statuses = dt.Array(dt.U8, 15, 0x1EF0, this.data);
        this.landingpoints = dt.Array(dt.U8, 15, 0x1EFF, this.data);
        
        this.world = new dt.U32(0x2040, this.data);
        this.room = new dt.U32(0x2044, this.data);
        this.flag = new dt.U32(0x2048, this.data);
        
        this.gummi_tutorial = new dt.U8(0x2405, this.data);
        this.selectedship = new dt.U8(0x2410, this.data);
        
        this.gummiblocks = dt.Array(dt.U8, 108, 0xBE78, this.data);
        
        this.gummi_decelerate = new dt.U32(0xBF01, this.data);
        this.gummi_accelerate = new dt.U32(0xBF05, this.data);
        this.gummi_transform = new dt.U32(0xBF09, this.data);
        this.gummi_scannon = new dt.U32(0xBF0D, this.data);
        this.gummi_mcannon = new dt.U32(0xBF11, this.data);
        this.gummi_lcannon = new dt.U32(0xBF15, this.data);
        this.gummi_slaser = new dt.U32(0xBF19, this.data);
        this.gummi_mlaser = new dt.U32(0xBF1D, this.data);
        this.gummi_llaser = new dt.U32(0xBF21, this.data);
        
        this.autolock = new dt.U32(0x16400, this.data);
        this.targetlock = new dt.U32(0x16404, this.data);
        this.camera = new dt.U32(0x16408, this.data);
        this.vibration = new dt.U32(0x16410, this.data);
        this.sound = new dt.U32(0x16414, this.data);
        this.datainstall = new dt.U32(0x16418, this.data);
        this.munny = new dt.U32(0x1641C, this.data);
        this.journal_complete = new dt.U8(0x16474, this.data);

        // Final Mix stuff
        if (this.fm) {
            this.heartless = dt.Array(dt.U16, 51, 0x07D8, this.data);
            this.shortcuts = dt.Array(dt.U8, 3, 0x0844, this.data);
            this.cure_on_friends = new dt.U16(0x084E, this.data);
            this.heartless_killed = new dt.U16(0x0856, this.data);
            this.deflected = new dt.U16(0x085C, this.data);
            this.taken_damage = new dt.U16(0x085E, this.data);
            this.item_usage = new dt.U16(0x0860, this.data);
            this.hits = new dt.U16(0x0862, this.data);
            this.friend_ko = new dt.U16(0x0864, this.data);
            this.deaths = new dt.U16(0x0866, this.data);
            this.weapon_usage = new dt.U16(0x086E, this.data);
            this.xemnas = new dt.U8(0x1118, this.data);
            this.gummiblocks = dt.Array(dt.U8, 160, 0xBE78, this.data);
            this.gummi_decelerate = new dt.U32(0xBF41, this.data);
            this.gummi_accelerate = new dt.U32(0xBF45, this.data);
            this.gummi_transform = new dt.U32(0xBF49, this.data);
            this.gummi_scannon = new dt.U32(0xBF4D, this.data);
            this.gummi_mcannon = new dt.U32(0xBF51, this.data);
            this.gummi_lcannon = new dt.U32(0xBF55, this.data);
            this.gummi_slaser = new dt.U32(0xBF59, this.data);
            this.gummi_mlaser = new dt.U32(0xBF5D, this.data);
            this.gummi_llaser = new dt.U32(0xBF61, this.data);
            this.difficulty = new dt.U32(0x1642C, this.data);
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
                <option value="Gummi Ships">Gummi Ships</option>
            </select>
        </div>`;
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
                case "Inventory": {
                    tabs.create_inventory();
                    break;
                }
                case "Config": {
                    tabs.create_config();
                    break;
                }
                case "Gummi Ships": {
                    tabs.create_gummi();
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
