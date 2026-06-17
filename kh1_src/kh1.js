import * as dt from "./datatypes.js"

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
        this.resistances = Array(dt.U8, 0x10, offset+0x08, data);
        this.accessoryslots = new dt.U8(offset+0x18, data);
        this.accessories = Array(dt.U8, 0x08, offset+0x19, data);
        this.itemslots = new dt.U8(offset+0x21, data);
        this.items = Array(dt.U8, 0x08, offset+0x22, data);
        this.weapon = new dt.U8(offset+0x32, data);
        this.submp = new dt.U16(offset+0x38, data);
        this.exp = new dt.U32(offset+0x3C, data);
        this.abilities = Array(dt.U8, 0x30, offset+0x40, data);
        this.magic = new dt.U8(offset+0x70, data);
    }
    
    str() {
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
        this.loaded = this._load();
    }
    
    async _load() {
        const buffer = await this.file.arrayBuffer();
        this.buffer = new Uint8Array(buffer);
        this.data = new DataView(buffer);
        this.parse_data();
    }
    
    parse_data() {
        this.header = new dt.U8(0x00, this.data);
        this.sora = new KH1Character("Sora", 0x04, this.data);
    }

    save() {
        return new Blob([this.buffer], { type: "application/octet-stream" });
    }
    
    str() {
        return `KH1(\n    Final Mix: ${this.fm}\n${this.sora.str()}\n)`;
    }
}
