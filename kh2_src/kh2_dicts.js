import * as d from "./dicts/index.js"


export default function dicts(obj) {
    main_dicts(obj)
    d.item_dicts(obj)
    d.stock_dicts(obj)
    d.command_dicts(obj)
    d.world_dicts(obj)
    d.bestiary_dicts(obj)
    d.minigame_dicts(obj)
}

function main_dicts(obj) {
    obj.character_dict = {
        "Sora": 0x00,
        "Donald": 0x01,
        "Goofy": 0x02,
        "King Mickey": 0x03,
        "Auron": 0x04,
        "Mulan": 0x05,
        "Aladdin": 0x06,
        "Jack Sparrow": 0x07,
        "Beast": 0x08,
        "Jack Skellington": 0x09,
        "Simba": 0x0A,
        "Tron": 0x0B,
        "Riku": 0x0C,
    }
    // Drive Form structs
    obj.drive_form_dict = {
        "Valor Form": 0x00,
        "Wisdom Form": 0x01,
        "Master Form": 0x02,
        "Final Form": 0x03,
        "Antiform": 0x04,
        "Lion Sora": 0x05,
        "Unused 0x06": 0x06,
        "Unused 0x07": 0x07,
        "Dual Wield Roxas": 0x08,
    }
    obj.drive_form_fm_dict = {
        "Valor Form": 0x00,
        "Wisdom Form": 0x01,
        "Limit Form": 0x02,
        "Master Form": 0x03,
        "Final Form": 0x04,
        "Antiform": 0x05,
        "Lion Sora": 0x06,
        "Unused 0x07": 0x07,
        "Unused 0x08": 0x08,
        "Dual Wield Roxas": 0x09,
    }
    // Current Drive Form
    obj.form_dict = {
        "Base Sora": 0x00,
        "Valor Form": 0x01,
        "Wisdom Form": 0x02,
        "Master Form": 0x03,
        "Final Form": 0x04,
        "Antiform": 0x05,
        "King Mickey": 0x06,
    }
    obj.form_fm_dict = {
        "Base Sora": 0x00,
        "Valor Form": 0x01,
        "Wisdom Form": 0x02,
        "Limit Form": 0x03,
        "Master Form": 0x04,
        "Final Form": 0x05,
        "Antiform": 0x06,
        "King Mickey": 0x07,
    }
    obj.summon_dict = {
        "None": 0x00,
        "Chicken Little": 0x01,
        "Genie": 0x02,
        "Stitch": 0x03,
        "Peter Pan": 0x04,
    }
}
