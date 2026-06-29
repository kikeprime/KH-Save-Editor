import * as dt from "/kh1_src/datatypes.js"
import dicts from "./kh2_dicts.js"
import * as h from "./kh2_helper.js"
import * as tabs from "./tabs/index.js"

export default class KH2 {
    constructor(file, version) {
        this.file = file
        this.version = version;
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
    }
    
    parse_data() {
        this.header = dt.Array(dt.U8, 0x04, 0x00, this.data);
        this.ver = new dt.U32(0x04, this.data);
        this.checksum = new dt.U32(0x08, this.data);
        this.world = new dt.U8(0x0C, this.data);
        this.room = new dt.U8(0x0D, this.data);
        this.flag = new dt.U8(0x0E, this.data);
        if (this.version == 0)
            this.parse_data_vanilla_jp()
        else if (this.version == 1)
            this.parse_data_vanilla_usa()
        else if (this.version == 2)
            this.parse_data_fm()
    }
    
    parse_data_vanilla_jp() {
        this.placescripts = {};
        Object.entries(this.world_dict)
            .forEach(([i, w]) => {
                this.placescripts[w] = [];
                for (let j = 0; j < 64; j++) {
                    this.placescripts[w].push(new h.KH2PlaceScript(0x10+i*64*3+j*3, this.data));
                }
            });
        this.munny = new dt.U32(0x1600, this.data);
        this.playtimes = dt.Array(dt.U32, 0x15, 0x1604, this.data);
        this.difficulty = new dt.U8(0x1658, this.data);
        this.characters = [];
        Object.entries(this.character_dict)
            .forEach(([name, i]) => {
                this.characters.push(new h.KH2Character(name, 0x1660 + i * 0x100, this.data));
            });
        this.forms = [];
        Object.entries(this.drive_form_dict)
            .forEach(([name, i]) => {
                //this.forms.push(new h.KH2DriveForm(name, 0x2360 + i * 0x28, this.data));
            });
        this.current_form = new dt.U8(0x24C8, this.data);
        this.current_summon = new dt.U8(0x24C9, this.data);
        this.summon_level = new dt.U8(0x24CA, this.data);
        this.drive_gauge = new dt.U8(0x24CC, this.data);
        this.drive = new dt.U8(0x24CD, this.data);
        this.maxdrive = new dt.U8(0x24CE, this.data);
        this.inventory = dt.Array(dt.U8, 0x118, 0x2524, this.data);
        this.exp = new dt.U32(0x2684, this.data);
        this.shortcuts = dt.Array(dt.U16, 4, 0x269C, this.data);
        this.bonuslevel = new dt.U32(0x26A4, this.data);
        this.heartless = dt.Array(dt.U32, 0x2F, 0x26EC, this.data);
        this.nobodies = dt.Array(dt.U32, 0x0C, 0x286C, this.data);
        this.rc_usage = dt.Array(dt.U16, 0x30, 0x28EE, this.data);
        this.limit_usage = dt.Array(dt.U16, 0x15, 0x2CEC, this.data);
    }
    
    parse_data_vanilla_usa() {
        this.placescripts = {};
        Object.entries(this.world_dict)
            .forEach(([i, w]) => {
                this.placescripts[w] = [];
                for (let j = 0; j < 64; j++) {
                    this.placescripts[w].push(new h.KH2PlaceScript(0x10+i*64*3+j*3, this.data));
                }
            });
        this.munny = new dt.U32(0x1600, this.data);
        this.playtimes = dt.Array(dt.U32, 0x15, 0x1604, this.data);
        this.difficulty = new dt.U8(0x1658, this.data);
        this.characters = [];
        Object.entries(this.character_dict)
            .forEach(([name, i]) => {
                this.characters.push(new h.KH2Character(name, 0x1660 + i * 0xF4, this.data));
            });
        this.current_form = new dt.U8(0x242C, this.data);
        this.current_summon = new dt.U8(0x242D, this.data);
        this.summon_level = new dt.U8(0x242E, this.data);
        this.drive_gauge = new dt.U8(0x2430, this.data);
        this.drive = new dt.U8(0x2431, this.data);
        this.maxdrive = new dt.U8(0x2432, this.data);
        this.inventory = dt.Array(dt.U8, 0x118, 0x2488, this.data);
        this.exp = new dt.U32(0x25E8, this.data);
        this.shortcuts = dt.Array(dt.U16, 4, 0x2600, this.data);
        this.bonuslevel = new dt.U32(0x2608, this.data);
        this.heartless = dt.Array(dt.U32, 0x2F, 0x2650, this.data);
        this.nobodies = dt.Array(dt.U32, 0x0C, 0x27D0, this.data);
        this.rc_usage = dt.Array(dt.U16, 0x30, 0x2852, this.data);
        this.limit_usage = dt.Array(dt.U16, 0x15, 0x2C50, this.data);
        
        this.synthesis_creations = dt.Array(dt.U8, 5, 0x3741, this.data);
        this.synthesis_exp = new dt.U32(0x3758, this.data);
        this.synthesis_inventory = dt.Array(dt.U32, 0x32, 0x375C, this.data);
        this.synthesis_log = dt.Array(dt.U32, 0x32, 0x3824, this.data);
        
        this.gummi_treasure_percents = dt.Array(dt.F32, 0x01A1, 0xACE0, this.data);
    }
    
    parse_data_fm() {
        this.placescripts = {};
        Object.entries(this.world_dict)
            .forEach(([i, w]) => {
                this.placescripts[w] = [];
                for (let j = 0; j < 64; j++) {
                    this.placescripts[w].push(new h.KH2FMPlaceScript(0x10+i*64*6+j*6, this.data));
                }
            });
        this.munny = new dt.U32(0x2440, this.data);
        this.playtimes = dt.Array(dt.U32, 0x15, 0x2444, this.data);
        this.difficulty = new dt.U8(0x2498, this.data);
        this.puzzles = dt.Array(dt.U8, 0x30, 0x24A0, this.data);
        this.characters = [];
        Object.entries(this.character_dict)
            .forEach(([name, i]) => {
                this.characters.push(new h.KH2FMCharacter(name, 0x24F0 + i * 0x114, this.data));
            });
        this.current_form = new dt.U8(0x3524, this.data);
        this.current_summon = new dt.U8(0x3525, this.data);
        this.summon_level = new dt.U8(0x3526, this.data);
        this.drive_gauge = new dt.U8(0x3528, this.data);
        this.drive = new dt.U8(0x3529, this.data);
        this.maxdrive = new dt.U8(0x352A, this.data);
        
        this.party = dt.Array(dt.U8, 19 * 4, 0x3534, this.data);
        this.inventory = dt.Array(dt.U8, 0x138, 0x3580, this.data);
        
        this.form_unlock = new dt.U8(0x36C0, this.data);
        this.summon_unlock = new dt.U8(0x36C4, this.data);
        this.reports = dt.Array(dt.U8, 3, 0x36C4, this.data);
        this.limit_form_unlock = new dt.U8(0x36CA, this.data);
        
        this.exp = new dt.U32(0x36E0, this.data);
        this.shortcuts = dt.Array(dt.U16, 4, 0x36F8, this.data);
        this.bonuslevel = new dt.U32(0x3700, this.data);
        
        this.heartless = dt.Array(dt.U32, 0x48, 0x3748, this.data);
        this.nobodies = dt.Array(dt.U32, 0x0C, 0x38C8, this.data);
        this.rc_usage = dt.Array(dt.U16, 0x33, 0x394A, this.data);
        this.limit_usage = dt.Array(dt.U16, 0x15, 0x3D48, this.data);
        
        this.form_usage = dt.Array(dt.U16, 0x0A, 0x3FD6, this.data);
        this.weapon_backup = new dt.U16(0x3FEA, this.data);
    }
    
    __calculate_checksum(crc_table, offset, length, checksum) {
        checksum >>>= 0;
        for (let i = offset; i < offset + length; i++) {
            checksum = crc_table[((checksum >> 24) ^ this.buffer[i]) & 0xFF] ^ ((checksum << 8) >>> 0);
            checksum >>>= 0;
        }
        return (checksum ^ 0xFFFFFFFF) >>> 0;
    }
    
    calculate_checksum() {
        const CrcPolynomial = 0x04c11db7;
        const crc_table = new Uint32Array(0x100);
        for (let i = 0; i < 0x100; i++) {
            let r = (i << 24) | 0;
            for (let j = 0; j < 0xFF; j++) {
                r = (r << 1 ^ (r < 0 ? CrcPolynomial : 0)) | 0;
            }
            crc_table[i] = r >>> 0;
        }
        this.checksum.value = this.__calculate_checksum(crc_table, 0, 8, 0xFFFFFFFF);
        this.checksum.value = this.__calculate_checksum(crc_table, 0x0C, this.buffer.length - 0x0C, this.checksum.value ^ 0xFFFFFFFF);
    }

    save() {
        this.calculate_checksum();
        return new Blob([this.buffer], { type: "application/octet-stream" });
    }
    
    syssave() {
        return new Blob([this.sysbuffer], { type: "application/octet-stream" });
    }
    
    menu() {
        const app = document.getElementById("app");
        const tabs_kh2_html = `
        <div>
            <h2>KH2 Tabs:</h2>
            <select id="tabs_kh2">
                <option value="General">General</option>
                <option value="Characters">Characters</option>
                <option value="Drive Forms">Drive Forms</option>
                <option value="Inventory">Inventory</option>
                <option value="Jiminy's Journal">Jiminy's Journal</option>
                <option value="Config">Config</option>
                <option value="Worlds">Worlds</option>
                <option value="Misc">Misc</option>
                <option value="Gummi Ships">Gummi Ships</option>
            </select>
        </div>`;
        app.innerHTML = `${tabs_kh2_html}<div id="kh2div"></div>`;
        const tabs_kh2 = document.getElementById("tabs_kh2");
        const kh2div = document.getElementById("kh2div");
        tabs.create_general();
        tabs_kh2.addEventListener("change", () => {
            switch (tabs_kh2.value) {
                case "General": {
                    tabs.create_general();
                    break;
                }
                /*
                case "Characters": {
                    tabs.create_characters();
                    break;
                }
                case "Drive Forms": {
                    tabs.create_forms();
                    break;
                }
                case "Inventory": {
                    tabs.create_inventory();
                    break;
                }
                case "Jiminy's Journal": {
                    tabs.create_journal();
                    break;
                }
                case "Config": {
                    tabs.create_config();
                    break;
                }
                case "Worlds": {
                    tabs.create_worlds();
                    break;
                }
                case "Misc": {
                    tabs.create_misc();
                    break;
                }
                case "Gummi Ships": {
                    tabs.create_gummi();
                    break;
                }
                */
                default: {
                    kh2div.innerHTML = "";
                    break;
                }
            }
        });
    }
    
    get_playtime(time, fps = 60) {
        return [
            Math.floor(Math.floor(time / fps) / 3600),
            Math.floor((Math.floor(time / fps) % 3600) / 60),
            (Math.floor(time / fps) % 3600) % 60,
            time % fps,
            Math.floor((time % fps * 100) / 60),
        ];
    }
    
    set_playtime(hours, minutes, seconds, fraction, fps = 60) {
        return (hours * 3600 + minutes * 60 + seconds) * fps + fraction;
    }
    
    get fm() {
        return version == 2;
    }
    
    toString() {
        return `KH2(
    Version: ${["Vanilla JP", "Vanilla USA", "Final Mix"][this.version]}
${String(this.characters[0])}
    Path: ${["Warrior", "Guardian", "Mystic"][this.characters[0].path.value]}
)`;
    }
}
