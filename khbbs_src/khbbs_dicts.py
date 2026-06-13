from .dicts import *


def dicts(obj):
    main_dicts(obj)
    world_dicts(obj)
    weapon_dicts(obj)
    command_dicts(obj)

def main_dicts(obj):
    obj.character_dict = {
        "None": 0x00,
        "Ventus": 0x01,
        "Aqua": 0x02,
        "Terra": 0x03,
        "Armored Ventus": 0x04,
        "Armored Aqua": 0x05,
        "Armored Terra": 0x06,
        "Helmetless Ventus": 0x0D,
        "Helmetless Aqua": 0x0E,
        "Helmetless Terra": 0x0F,
    }

def world_dicts(obj):
    @property
    def world_dict(self):
        return {
            0x00: "World EX",
            0x01: "The Land of Departure",
            0x02: "Dwarf Woodlands",
            0x03: "Castle of Dreams",
            0x04: "Enchanted Dominion",
            0x05: "Mysterious Tower",
            0x06: "Radiant Garden",
            0x07: "Realm of Darkness" if hasattr(self, "fm") and self.fm else "Jungle Book",
            0x08: "Olympus Coliseum",
            0x09: "Deep Space",
            0x0A: "Destiny Islands",
            0x0B: "Neverland",
            0x0C: "Disney Town",
            0x0D: "Keyblade Graveyard",
            0x0F: "Mirage Arena",
            0x10: "Command Board",
            0x11: "World Map",
            0x12: "Hundred Acre Woods",
            0x17: "Jump Festa",
        }
    type(obj).world_dict = world_dict

def weapon_dicts(obj):
    @property
    def weapon_dict(self):
        return {
            "Empty": 0x00,
            "Wayward Wind": 0x01,
            "Rainfell": 0x02,
            "Earthshaker": 0x03,
            "Treasure Trove (Ventus)": 0x04,
            "Treasure Trove (Aqua)": 0x05,
            "Treasure Trove (Terra)": 0x06,
            "Stroke of Midnight (Ventus)": 0x07,
            "Stroke of Midnight (Aqua)": 0x08,
            "Stroke of Midnight (Terra)": 0x09,
            "Fairy Stars (Ventus)": 0x0A,
            "Fairy Stars (Aqua)": 0x0B,
            "Fairy Stars (Terra)": 0x0C,
            "Victory Line (Ventus)": 0x0D,
            "Victory Line (Aqua)": 0x0E,
            "Victory Line (Terra)": 0x0F,
            "Mark of a Hero (Ventus)": 0x10,
            "Mark of a Hero (Aqua)": 0x11,
            "Mark of a Hero (Terra)": 0x12,
            "Hyperdrive (Ventus)": 0x13,
            "Hyperdrive (Aqua)": 0x14,
            "Hyperdrive (Terra)": 0x15,
            "Pixie Petal (Ventus)": 0x16,
            "Pixie Petal (Aqua)": 0x17,
            "Pixie Petal (Terra)": 0x18,
            "Ultima Weapon (Ventus)": 0x19,
            "Ultima Weapon (Aqua)": 0x1A,
            "Ultima Weapon (Terra)": 0x1B,
            "Sweetstack (Ventus)": 0x1C,
            "Sweetstack (Aqua)": 0x1D,
            "Sweetstack (Terra)": 0x1E,
            "Kingdom Key D" if hasattr(self, "version") and self.version == 0 else "Unused 0x1F": 0x1F,
            "Unused 0x20": 0x20,
            "Frolic Frame": 0x21,
            "Lost Memory": 0x22,
            "Destiny's Embrace": 0x23,
            "Stormfall": 0x24,
            "Brightcrest": 0x25,
            "Darkgnaw": 0x26,
            "Ends of the Earth": 0x27,
            "Chaos Ripper": 0x28,
            "Ultima Cannon" if hasattr(self, "version") and self.version == 0 else "Void Gear (Ventus)": 0x29,
    } | ({
            "Void Gear (Aqua)": 0x2A,
            "Void Gear (Terra)": 0x2B,
            "No Name (Ventus)": 0x2C,
            "No Name (Aqua)": 0x2D,
            "No Name (Terra)": 0x2E,
            "Crown Unlimit (Ventus)": 0x2F,
            "Crown Unlimit (Aqua)": 0x30,
            "Crown Unlimit (Terra)": 0x31,
            "Master's Defender": 0x32,
            "Ultima Cannon": 0x33,
    } if hasattr(self, "version") and self.version > 0 else {})
    type(obj).weapon_dict = weapon_dict
