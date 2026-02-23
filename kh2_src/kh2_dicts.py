from .dicts import *


def dicts(obj):
    main_dicts(obj)
    item_dicts(obj)
    command_dicts(obj)
    world_dicts(obj)
    bestiary_dicts(obj)

def main_dicts(obj):
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
    # Drive Form structs
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
    # Current Drive Form
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

def item_dicts(obj):
    obj.item_dict = item_dict
    obj.weapon_dict = weapon_dict
    obj.armor_list = armor_list
    obj.accessory_list = accessory_list
    obj.ability_list = ability_list
    
    obj.inventory_dict = inventory_dict
    obj.stock_dict = stock_dict.copy()
    obj.stock_dict["Unused"] = sorted([
        k for k in obj.inventory_dict\
        if "Unused" in k\
        or "Dummy" in k\
        and k != "Antiform Dummy"
    ])
    l = []
    for k in obj.stock_dict:
        l += obj.stock_dict[k]
    obj.stock_dict["Key Items"] = sorted([k for k in obj.inventory_dict if k not in l])

def command_dicts(obj):
    obj.command_dict = command_dict
    obj.shortcut_list = [
        "Empty",
        "Fire", "Fira", "Firaga",
        "Blizzard", "Blizzara", "Blizzaga",
        "Thunder", "Thundara", "Thundaga",
        "Cure", "Cura", "Curaga",
        "Magnet", "Magnera", "Magnega",
        "Reflect", "Reflera", "Reflega",
        "Potion", "Hi-Potion", "Mega-Potion",
        "Ether", "Mega-Ether",
        "Elixir", "Megalixir",
        "Valor Form", "Wisdom Form", "Limit Form",
        "Master Form", "Final Form", "Antiform",
    ]

def world_dicts(obj):
    obj.WorldCount = 19
    obj.world_dict = {
        0x00: "World ZZ",
        0x01: "End of Sea",
        0x02: "Twilight Town",
        0x03: "Destiny Islands",
        0x04: "Hollow Bastion",
        0x05: "Beast's Castle",
        0x06: "Olympus Coliseum",
        0x07: "Agrabah",
        0x08: "The Land of Dragons",
        0x09: "Hundred Acre Woods",
        0x0A: "Pride Lands",
        0x0B: "Atlantica",
        0x0C: "Disney Castle",
        0x0D: "Timeless River",
        0x0E: "Halloween Town",
        0x0F: "World Map",
        0x10: "Port Royal",
        0x11: "Space Paranoids",
        0x12: "The World That Never Was",
    }

def bestiary_dicts(obj):
    obj.heartless_dict = heartless_dict
    obj.heartless_list = heartless_list
    obj.nobody_dict = nobody_dict
    obj.nobody_list = nobody_list
    obj.rc_dict = rc_dict
    obj.rc_list_dict = rc_list_dict
    obj.limit_dict = limit_dict
    obj.limit_list = limit_list
