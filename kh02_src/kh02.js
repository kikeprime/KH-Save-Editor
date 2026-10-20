import * as dt from "../kh1_src/datatypes.js"
import dicts from "./kh02_dicts.js"
//import * as h from "./kh02_helper.js"
import * as tabs from "./tabs/index.js"

export default class KH02 {
    constructor(file, pc, account) {
        this.file = file;
        this.pc = pc;
        this.get_account(account);
        this.get_key();
        dicts(this);
        this.size = 0x1725B0;
        this.loaded = this._load();
    }
    
    async _load() {
        const buffer = await this.file.arrayBuffer();
        if (this.pc && new TextDecoder().decode(buffer.slice(0x29, 0x29 + 4)) != "SAVE") {
            this.png = new Uint8Array(buffer);
            this.aes = new aesjs.ModeOfOperation.ecb(this.key);
            this.buffer = this.aes.decrypt(this.png.slice(0x29, 0x29 + this.size));
            this.data = new DataView(this.buffer.buffer);
        }
        else {
            this.buffer = new Uint8Array(buffer);
            this.data = new DataView(buffer);
        }
        this.parse_data();
    }
    
    parse_data() {
        this.major_version = new dt.U32(0x04, this.data);
        this.filesize = new dt.U32(0x08, this.data);
        this.config = new dt.U8(0x10, this.data);
        this.camera_speed = new dt.U32(0x14, this.data);
        this.brightness = new dt.U32(0x18, this.data);
        this.theater_watched = new dt.U32(0x1C, this.data);
        this.theater_mode = new dt.U32(0x38, this.data);
    }

    save(encrypted) {
        if (this.pc && encrypted) {
            const hash = md5.array(this.buffer);
            this.png.set(this.aes.encrypt(this.buffer), 0x29);
            this.png.set(hash, 0x29 + this.buffer.length + 1);
            return new Blob([this.png], { type: "application/octet-stream" });
        }
        else
            return new Blob([this.buffer], { type: "application/octet-stream" });
    }
    
    menu() {
        const app = document.getElementById("app");
        const tabs_kh02_html = `
        <div>
            <h2>KH0.2 Tabs:</h2>
            <select id="tabs_kh02">
                <option value="General">General</option>
                <option value="Characters">Characters</option>
                <option value="Inventory">Inventory</option>
                <option value="Config">Config</option>
                <option value="Misc">Misc</option>
            </select>
        </div>`;
        app.innerHTML = `${tabs_kh02_html}<div id="kh02div"></div>`;
        const tabs_kh02 = document.getElementById("tabs_kh02");
        const kh02div = document.getElementById("kh02div");
        tabs.create_general();
        tabs_kh02.addEventListener("change", () => {
            switch (tabs_kh02.value) {
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
                case "Config": {
                    tabs.create_config();
                    break;
                }
                case "Misc": {
                    tabs.create_misc();
                    break;
                }
                */
                default: {
                    kh02div.innerHTML = "";
                    break;
                }
            }
        });
    }
    
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
            "u&nDPi-Mi5qpMkm)fcT4vqHYDTMh&t8z"
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
        return `KH02(
    PNG: ${this.pc},
    Internal Filesize: 0x${this.filesize.value.toString(16).toUpperCase()},
    Camera Speed: ${this.camera_speed.value},
    Brightness: ${this.brightness.value},
)`;
    }
}
