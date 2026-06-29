import * as dt from "/kh1_src/datatypes.js"
import dicts from "./kh2_dicts.js"

export class KH2Character {
    constructor(name, offset, data) {
        this.name = name;
        this.data = data;
        this.weapon = new dt.U16(offset+0x00, data);
        this.hp = new dt.U8(offset+0x04, data);
        this.maxhp = new dt.U8(offset+0x05, data);
        this.mp = new dt.U8(offset+0x06, data);
        this.maxmp = new dt.U8(offset+0x07, data);
        this.apboost = new dt.U8(offset+0x08, data);
        this.strengthboost = new dt.U8(offset+0x09, data);
        this.magicboost = new dt.U8(offset+0x0A, data);
        this.defenseboost = new dt.U8(offset+0x0B, data);
        this.path = new dt.U8(offset+0x0E, data);
        this.level = new dt.U8(offset+0x0F, data);
        this.armorslots = new dt.U8(offset+0x10, data);
        this.accessoryslots = new dt.U8(offset+0x11, data);
        this.itemslots = new dt.U8(offset+0x12, data);
        this.armors = dt.Array(dt.U16, 0x08, offset+0x14, data);
        this.accessories = dt.Array(dt.U16, 0x08, offset+0x24, data);
        this.items = dt.Array(dt.U16, 0x08, offset+0x34, data);
        this.autoreload = dt.Array(dt.U16, 0x08, offset+0x44, data);
        this.abilities = dt.Array(dt.U16, 0x40, offset+0x54, data);
        this.battlestyle = new dt.U8(offset+0xD4, data);
        this.abilitystyles = dt.Array(dt.U8, 0x04, offset+0xDC, data);
    }
    
    toString() {
        return `${this.name}(
    Level: ${this.level.value}
    HP: ${this.hp.value}
    Max HP: ${this.maxhp.value}
    MP: ${this.mp.value}
    Max MP: ${this.maxmp.value}
    AP Boosts: ${this.apboost.value}
    Strength Boosts: ${this.strengthboost.value}
    Magic Boosts: ${this.magicboost.value}
    Defense Boosts: ${this.defenseboost.value}
    Armor Slots: ${this.armorslots.value}
    Accessory Slots: ${this.accessoryslots.value}
    Item Slots: ${this.itemslots.value}
)`;
    }
}

export class KH2FMCharacter extends KH2Character {
    constructor(name, offset, data) {
        super(name, offset, data);
        this.abilities = dt.Array(dt.U16, 0x50, offset+0x54, data);
        this.battlestyle = new dt.U8(offset+0xF4, data);
        this.abilitystyles = dt.Array(dt.U8, 0x04, offset+0xFC, data);
    }
}

export class KH2PlaceScript {
    constructor(offset, data) {
        this.map = new dt.U8(offset+0x00, data);
        this.battle = new dt.U8(offset+0x01, data);
        this.event = new dt.U8(offset+0x02, data);
    }
}

export class KH2FMPlaceScript {
    constructor(offset, data) {
        this.map = new dt.U8(offset+0x00, data);
        this.map2 = new dt.U8(offset+0x01, data);
        this.battle = new dt.U8(offset+0x02, data);
        this.battle2 = new dt.U8(offset+0x03, data);
        this.event = new dt.U8(offset+0x04, data);
        this.event2 = new dt.U8(offset+0x05, data);
    }
}
