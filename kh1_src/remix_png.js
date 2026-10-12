import * as dt from "./datatypes.js"

class PNGEntry {
    constructor(idx, offset, data) {
        this.idx = idx;
        this.offset = offset;
        this.data = data;
        this.date_created = new dt.U32(offset+0x40, data);
        this.date_created_flag = new dt.U32(offset+0x44, data);
        this.date_modified = new dt.U32(offset+0x48, data);
        this.date_modified_flag = new dt.U32(offset+0x4C, data);
        this.size = new dt.U32(offset+0x50, data);
        this.unk_flag = new dt.U32(offset+0x54, data);
        this.padding = dt.Array(dt.U8, 0x100, offset+0x58, data);
    }
    
    get name() {
        return new TextDecoder()
            .decode(this.data.buffer.slice(this.offset, this.offset+0x40))
            .replace(/\0+$/, "");
    }
    
    set name(s) {
        s = new TextEncoder().encode(s);
        const buffer = new Uint8Array(this.data.buffer);
        if (s.length < 0x40) {
            buffer.set(s, this.offset);
            buffer.fill(0, this.offset+s.length, this.offset+0x40);
        }
        else {
            buffer.set(s.slice(0, 0x3F), this.offset);
            buffer[this.offset+0x3F] = 0;
        }
    }
}

export default class RemixPNG {
    constructor(game, file) {
        this.game = game;
        this.file = file;
        this.dicts = {
            "kh1": {
                "count": 200,
                "stride": 0x16C40,
                "size": 0x11EB09D,
            },
            "khrecom": {
                "count": 100,
                "stride": 0x3A30,
                "size": 0x188F5F,
            },
            "kh2": {
                "count": 100,
                "stride": 0x10FC0,
                "size": 0x6BED08,
            },
            "khbbs": {
                "count": 100,
                "stride": 0x13C00,
                "size": 0x7D3B94,
            },
            "khddd": {
                "count": 100,
                "stride": 0x16600,
                "size": 0x8DAEF8,
            },
        };
        this.key = null;
        this.entries = null;
        this.header_size = 0x70;
        this.encrypted_size = 0xF0;
        this.key_size = 0x10;
        this.key_offset = this.header_size + this.encrypted_size - this.key_size;
        this.entry_size = 0x158;
        this.base = this.header_size + this.count * this.entry_size;
        this.loaded = this._load();
    }

    async _load() {
        const buffer = await this.file.arrayBuffer();
        this.buffer = new Uint8Array(buffer);
        this.data = new DataView(buffer);
        this.parse_data();
    }
    
    xor() {
        if (this.key == null) return;
        for (let i = 0; i < this.encrypted_size; i++) {
            this.buffer[this.header_size+i] ^= this.key[i&15];
        }
    }
    
    parse_data() {
        this.key = this.buffer.slice(this.key_offset, this.key_offset+this.key_size);
        this.xor();
        this.entries = [];
        for (let i = 0; i < this.count; i++) {
            const entry = new PNGEntry(i, this.header_size+i*this.entry_size, this.data);
            this.entries.push(entry);
        }
    }
    
    save() {
        this.xor();
        const buffer = this.buffer.slice();
        this.xor();
        return new Blob([buffer], { type: "application/octet-stream" });
    }
    
    menu() {
        const app = document.getElementById("app");
        function row(entry) {
            return `
            <tr>
                <td>
                    ${
                        `<input
                            type="text"
                            name=${entry.idx}
                            value="${entry.name}"
                        >`
                    }
                </td>
                <td class="date_created_col">${new Date(entry.date_created.value*1000).toLocaleString("hu-HU")}</td>
                <td class="date_modified_col">${new Date(entry.date_modified.value*1000).toLocaleString("hu-HU")}</td>
                <td class="size_col">${entry.size.value.toString(16).toUpperCase().padStart(5, "0")}</td>
                <td>
                    ${`<button name=${entry.idx}>Download</button>`}
                </td>
                <td>
                    ${`<button name=${entry.idx}>Replace</button>`}
                </td>
            </tr>`;
        }
        const rows = this.entries
            .map((entry) => row(entry))
            .join("");
        app.innerHTML = `
        <div>
            <label id="error" style="color: red"></label>
        </div>
        <div>
            <table id="slots">
                <thead>
                    <tr>
                        <td>Filename</td>
                        <td>Date Created</td>
                        <td>Date Modified</td>
                        <td>Size</td>
                        <td></td>
                    </tr>
                </thead>
                <tbody>
                    ${rows}
                </tbody>
            </table>
        </div>`;
        const slots = document.getElementById("slots");
        slots.querySelectorAll("button").forEach(button => {
            button.addEventListener("click", async () => {
                const entry = this.entries[button.name];
                const offset = this.base+entry.idx*this.stride;
                if (button.innerHTML == "Download") {
                    const buffer = this.buffer.slice(offset, offset+entry.size.value)
                    const file = new Blob([buffer], { type: "application/octet-stream" });
                    try {
                        const picker = await window.showSaveFilePicker({suggestedName: entry.name});
                        const writable = await picker.createWritable();
                        await writable.write(file);
                        await writable.close();
                    } catch (e) {
                        if (e.name == "AbortError") return;
                        return e;
                    }
                }
                if (button.innerHTML == "Replace") {
                    try {
                        const picker = await window.showOpenFilePicker();
                        const file = await picker[0].getFile();
                        const buffer = new Uint8Array(await file.arrayBuffer());
                        const error = document.getElementById("error");
                        error.innerHTML = "";
                        if (buffer.length <= this.stride) {
                            this.buffer.set(buffer, offset);
                            entry.size.value = buffer.length;
                            if (buffer.length < this.stride) {
                                this.buffer.fill(0, offset+buffer.length, offset+this.stride);
                            }
                            if (entry.date_created.value == 0) {
                                const date = Date.now();
                                entry.date_created.value = Math.floor(date / 1000);
                                const date_created_col = slots.querySelectorAll("td.date_created_col")[entry.idx];
                                date_created_col.innerHTML = new Date(date).toLocaleString("hu-HU");
                                entry.date_modified.value = Math.floor(date / 1000);
                                const date_modified_col = slots.querySelectorAll("td.date_modified_col")[entry.idx];
                                date_modified_col.innerHTML = new Date(date).toLocaleString("hu-HU");
                            }
                            const size_col = slots.querySelectorAll("td.size_col")[entry.idx];
                            size_col.innerHTML = entry.size.value.toString(16).toUpperCase().padStart(5, "0");
                        }
                        else {
                            error.innerHTML = `File is too big! Max filesize is 0x${this.stride.toString(16).toUpperCase().padStart(5, "0")} bytes.`;
                            console.log(error.innerHTML);
                        }
                    } catch (e) {
                        if (e.name == "AbortError") return;
                        return e;
                    }
                }
            });
        });
        slots.querySelectorAll("input").forEach(input => {
            input.addEventListener("change", () => {
                const entry = this.entries[input.name];
                entry.name = input.value;
                input.value = entry.name;
            });
        });
    }
    
    get count() {
        return this.dicts[this.game].count;
    }
    
    get stride() {
        return this.dicts[this.game].stride;
    }
    
    get size() {
        return this.dicts[this.game].size;
    }
}
