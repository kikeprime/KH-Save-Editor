import * as dt from "../kh1_src/datatypes.js"
import dicts from "./kh3_dicts.js"
//import * as h from "./kh3_helper.js"
import * as tabs from "./tabs/index.js"

export default class KH3 {
    constructor(file, version, account) {
        this.file = file
        this.version = version;
        this.get_account(account);
        this.get_key();
        dicts(this);
        this.loaded = this._load();
    }
    
    async _load() {
        const buffer = await this.file.arrayBuffer();
        if (new TextDecoder().decode(buffer.slice(0, 4)) != "S@vE") {
            const encrypted = new Uint8Array(buffer);
            this.aes = new aesjs.ModeOfOperation.ecb(this.key);
            this.buffer = this.aes.decrypt(encrypted.slice(0, encrypted.length - 17));
            this.data = new DataView(this.buffer.buffer);
        }
        else {
            this.buffer = new Uint8Array(buffer);
            this.data = new DataView(buffer);
        }
        this.parse_data();
    }
    
    parse_data() {
        this.filesize = new dt.U32(0x04, this.data);
        this.major_version = new dt.U16(0x08, this.data);
        this.minor_version = new dt.U16(0x0A, this.data);
        this.checksum = new dt.U32(0x0C, this.data);
        this.difficulty = new dt.U8(0x14, this.data);
        this.world_logo = new dt.U8(0x18, this.data);
        this.playtime = new dt.U32(0x20, this.data);
        this.exp = new dt.U32(0x24, this.data);
        this.munny = new dt.U32(0x28, this.data);
        this.level = new dt.U8(0x2C, this.data);
        this.desire = new dt.U8(0x30, this.data);
        this.power = new dt.U8(0x31, this.data);
        this.party = dt.Array(dt.U8, 5, 0x32, this.data);
        this.save_clear = new dt.U8(0x39, this.data);
        this.save_location = new dt.U8(0x54, this.data);
        this.save_icon = new dt.U8(0x60, this.data);
        this.save_icon_dlc = new dt.U8(0x68, this.data);
        this.keychain_upgrades = dt.Array(dt.U8, 24, 0xBB78, this.data);
        this.map_path = dt.Array(dt.U8, 0x100, 0xBBA0, this.data);
        this.map_spawn = dt.Array(dt.U8, 0x40, 0xBCA0, this.data);
        this.player_script = dt.Array(dt.U8, 0x100, 0xBCE0, this.data);
        this.player_pawn = dt.Array(dt.U8, 0x100, 0xBDE0, this.data);
    }

    save(encrypted) {
        this.checksum.value = CRC32.buf(this.buffer.slice(0x10, 0x10 + this.filesize.value));
        if (encrypted) {
            const hash = md5.array(this.buffer.slice(0, this.filesize.value + 16));
            const buffer = new Uint8Array(this.buffer.length + 17);
            buffer.set(this.aes.encrypt(this.buffer), 0);
            buffer[this.buffer.length] = 8;
            buffer.set(hash, this.buffer.length + 1);
            return new Blob([buffer], { type: "application/octet-stream" });
        }
        else
            return new Blob([this.buffer], { type: "application/octet-stream" });
    }
    
    menu() {
        const app = document.getElementById("app");
        const tabs_kh3_html = `
        <div>
            <h2>KH3 Tabs:</h2>
            <select id="tabs_kh3">
                <option value="General">General</option>
                <option value="Characters">Characters</option>
                <option value="Inventory">Inventory</option>
                <option value="Jiminy's Journal">Gummiphone</option>
                <option value="Config">Config</option>
                <option value="Worlds">Worlds</option>
                <option value="Misc">Misc</option>
                <option value="Gummi Ships">Gummi Ships</option>
            </select>
        </div>`;
        app.innerHTML = `${tabs_kh3_html}<div id="kh3div"></div>`;
        const tabs_kh3 = document.getElementById("tabs_kh3");
        const kh3div = document.getElementById("kh3div");
        tabs.create_general();
        tabs_kh3.addEventListener("change", () => {
            switch (tabs_kh3.value) {
                case "General": {
                    tabs.create_general();
                    break;
                }
                /*
                case "Characters": {
                    tabs.create_characters();
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
                    kh3div.innerHTML = "";
                    break;
                }
            }
        });    }
    
    get_account(account) {
        if (account == "")
            this.account = "1638";
        else
            this.account = account;
    }
    
    get_key() {
        this.key = new Uint8Array(32);
        const account = new TextEncoder().encode(this.account);
        const key_mask = new TextEncoder().encode(
            "hN96q4X9f%BCURBV&pMT4kcvqTMhHYD&"
        );
        const key_idx = new TextEncoder().encode(
            "ABCDE!#$%&FGHIJ012345KLMNOPqrstuvwxyzQRSTUVWXYZ6789abcdefgh},.<>ijklmnop()=~|-^+*;:[]{/?_@"
        );
        let j = 1;
        for (let i = 0; i < 32; i++) {
            const idx = (key_mask[i] ^ account[j % account.length]) % 0x5A;
            this.key[i] = key_idx[idx];
            j++;
        }
    }
    get_playtime(time, fps = 1) {
        return [
            Math.floor(Math.floor(time / fps) / 3600),
            Math.floor((Math.floor(time / fps) % 3600) / 60),
            (Math.floor(time / fps) % 3600) % 60,
            time % fps,
            Math.floor((time % fps * 100) / 60),
        ];
    }
    
    set_playtime(hours, minutes, seconds, fraction, fps = 1) {
        return (hours * 3600 + minutes * 60 + seconds) * fps + fraction;
    }

    toString() {
        return `KH3(
    Version: ${["Vanilla PS4", "Critical Mode Update PS4", "ReMind PS4", "ReMind PC"][this.version]}
    Desire: ${["Vitality", "Wisdom", "Balance"][this.desire.value]}
    Power: ${["Warrior", "Mystic", "Guardian"][this.power.value]}
    Difficulty: ${["Beginner", "Standard", "Proud", "Critical"][this.difficulty.value]}
)`;
    }
}
