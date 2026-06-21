import * as d from "./dicts/index.js"


export default function dicts(obj) {
    main_dicts(obj)
    customize_dicts(obj)
    //inventory_dicts(obj)
    d.world_dicts(obj)
    //journal_dicts(obj)
    //trinity_dicts(obj)
    //minigame_dicts(obj)
    //gummi_dicts(obj)
    //treasure_dicts(obj)
}

function main_dicts(obj) {
    obj.character_dict = {
        "Sora": 0,
        "Donald": 1,
        "Goofy": 2,
        "Tarzan": 3,
        "Winnie the Pooh": 4,
        "Aladdin": 5,
        "Ariel": 6,
        "Jack Skellington": 7,
        "Peter Pan": 8,
        "Beast": 9,
        "None": 255
    }
    obj.ability_dict = {
        "Empty": 0x00,
        "High Jump": 0x01,
        "Mermaid Kick": 0x02,
        "Glide": 0x03,
        "Superglide": 0x04,
        "Treasure Magnet": 0x05,
        "Combo Plus": 0x06,
        "Air Combo Plus": 0x07,
        "Critical Plus": 0x08,
        "Second Wind": 0x09,
        "Scan": 0x0A,
        "Sonic Blade": 0x0B,
        "Ars Arcanum": 0x0C,
        "Strike Raid": 0x0D,
        "Ragnarok": 0x0E,
        "Trinity Limit": 0x0F,
        "Cheer": 0x10,
        "Vortex": 0x11,
        "Aerial Sweep": 0x12,
        "Counterattack": 0x13,
        "Blitz": 0x14,
        "Guard": 0x15,
        "Dodge Roll": 0x16,
        "MP Haste": 0x17,
        "MP Rage": 0x18,
        "Second Chance": 0x19,
        "Berserk": 0x1A,
        "Jackpot": 0x1B,
        "Lucky Strike": 0x1C,
        "Charge": 0x1D,
        "Rocket": 0x1E,
        "Tornado": 0x1F,
        "MP Gift": 0x20,
        "Raging Boar": 0x21,
        "Asp’s Bite": 0x22,
        "Healing Herb": 0x23,
        "Wind Armor": 0x24,
        "Crescent": 0x25,
        "Sandstorm": 0x26,
        "Applause!": 0x27,
        "Blazing Fury": 0x28,
        "Icy Terror": 0x29,
        "Bolts of Sorrow": 0x2A,
        "Ghostly Scream": 0x2B,
        "Hummingbird": 0x2C,
        "Time-Out": 0x2D,
        "Storm’s Eye": 0x2E,
        "Ferocious Lunge": 0x2F,
        "Furious Bellow": 0x30,
        "Spiral Wave": 0x31,
        "Thunder Potion": 0x32,
        "Cure Potion": 0x33,
        "Aero Potion": 0x34,
        // FM exclusives
        "Slapshot": 0x35,
        "Sliding Dash": 0x36,
        "Hurricane Blast": 0x37,
        "Ripple Drive": 0x38,
        "Stun Impact": 0x39,
        "Gravity Break": 0x3A,
        "Zantetsuken": 0x3B,
        "Tech Boost": 0x3C,
        "Encounter Plus": 0x3D,
        "Leaf Bracer": 0x3E,
        "Evolution": 0x3F,
        // Remix exclusives
        "EXP Zero": 0x40,
        "Combo Master": 0x41
    }
    obj.resistance_dict = {
        "Physical": 0x00,
        "Fire": 0x02,
        "Blizzard": 0x03,
        "Thunder": 0x04,
        "Dark": 0x05,
    }
}

function customize_dicts(obj) {
    obj.magicnames = ["Fire", "Blizzard", "Thunder", "Cure", "Gravity", "Stop", "Aero"]
    obj.magicnames2 = ["Fira", "Blizzara", "Thundara", "Cura", "Gravira", "Stopra", "Aerora"]
    obj.magicnames3 = ["Firaga", "Blizzaga", "Thundaga", "Curaga", "Graviga", "Stopga", "Aeroga"]
    obj.summon_dict = {
        "Empty": 0xFF,
        "Dumbo": 0x00,
        "Bambi": 0x01,
        "Genie": 0x02,
        "Tinker Bell": 0x03,
        "Mushu": 0x04,
        "Simba": 0x05,
        "Bahamut": 0x06
    }
    obj.customize_dict = {
        "Donald": {
            "Regular Attacks": {
                "offset": 0x16804,
                "bit": 0,
                "dict": 0,
            },
            "Offensive Magic": {
                "offset": 0x16804,
                "bit": 6,
                "dict": 0,
            },
            "Defensive Magic": {
                "offset": 0x16805,
                "bit": 0,
                "dict": 0,
            },
            "Advanced Magic": {
                "offset": 0x16805,
                "bit": 2,
                "dict": 0,
            },
            "HP items": {
                "offset": 0x16804,
                "bit": 2,
                "dict": 1,
            },
            "MP items": {
                "offset": 0x16804,
                "bit": 4,
                "dict": 1,
            },
        },
        "Goofy": {
            "Regular Attacks": {
                "offset": 0x16808,
                "bit": 0,
                "dict": 0,
            },
            "Support Actions": {
                "offset": 0x16809,
                "bit": 4,
                "dict": 0,
            },
            "Shield Techniques": {
                "offset": 0x16809,
                "bit": 6,
                "dict": 0,
            },
            "Special Attacks": {
                "offset": 0x1680A,
                "bit": 0,
                "dict": 0,
            },
            "HP items": {
                "offset": 0x16808,
                "bit": 2,
                "dict": 1,
            },
            "MP items": {
                "offset": 0x16808,
                "bit": 4,
                "dict": 1,
            },
        },
        "Tarzan": {
            "Regular Attacks": {
                "offset": 0x1680C,
                "bit": 0,
                "dict": 0,
            },
            "Defensive Moves": {
                "offset": 0x1680D,
                "bit": 6,
                "dict": 0,
            },
            "Special Attacks": {
                "offset": 0x1680E,
                "bit": 0,
                "dict": 0,
            },
            "HP items": {
                "offset": 0x1680C,
                "bit": 2,
                "dict": 1,
            },
            "MP items": {
                "offset": 0x1680C,
                "bit": 4,
                "dict": 1,
            },
        },
        "Winnie the Pooh": {
            "Regular Attacks": {
                "offset": 0x16810,
                "bit": 0,
                "dict": 0,
            },
            "Offensive Magic": {
                "offset": 0x16810,
                "bit": 6,
                "dict": 0,
            },
            "Defensive Magic": {
                "offset": 0x16811,
                "bit": 0,
                "dict": 0,
            },
            "Advanced Magic": {
                "offset": 0x16811,
                "bit": 2,
                "dict": 0,
            },
            "Support Actions": {
                "offset": 0x16811,
                "bit": 4,
                "dict": 0,
            },
            "Defensive Moves": {
                "offset": 0x16811,
                "bit": 6,
                "dict": 0,
            },
            "Special Attacks": {
                "offset": 0x16812,
                "bit": 0,
                "dict": 0,
            },
            "HP items": {
                "offset": 0x16810,
                "bit": 2,
                "dict": 1,
            },
            "MP items": {
                "offset": 0x16810,
                "bit": 4,
                "dict": 1,
            },
        },
        "Aladdin": {
            "Regular Attacks": {
                "offset": 0x16814,
                "bit": 0,
                "dict": 0,
            },
            "Special Attacks": {
                "offset": 0x16816,
                "bit": 0,
                "dict": 0,
            },
            "HP items": {
                "offset": 0x16814,
                "bit": 2,
                "dict": 1,
            },
            "MP items": {
                "offset": 0x16814,
                "bit": 4,
                "dict": 1,
            },
        },
        "Ariel": {
            "Regular Attacks": {
                "offset": 0x16818,
                "bit": 0,
                "dict": 0,
            },
            "Defensive Moves": {
                "offset": 0x16819,
                "bit": 6,
                "dict": 0,
            },
            "Special Attacks": {
                "offset": 0x1681A,
                "bit": 0,
                "dict": 0,
            },
            "HP items": {
                "offset": 0x16818,
                "bit": 2,
                "dict": 1,
            },
            "MP items": {
                "offset": 0x16818,
                "bit": 4,
                "dict": 1,
            },
        },
        "Jack Skellington": {
            "Regular Attacks": {
                "offset": 0x1681C,
                "bit": 0,
                "dict": 0,
            },
            "Special Attacks": {
                "offset": 0x1681E,
                "bit": 0,
                "dict": 0,
            },
            "HP items": {
                "offset": 0x1681C,
                "bit": 2,
                "dict": 1,
            },
            "MP items": {
                "offset": 0x1681C,
                "bit": 4,
                "dict": 1,
            },
        },
        "Peter Pan": {
            "Regular Attacks": {
                "offset": 0x16820,
                "bit": 0,
                "dict": 0,
            },
            "Defensive Moves": {
                "offset": 0x16821,
                "bit": 6,
                "dict": 0,
            },
            "Special Attacks": {
                "offset": 0x16822,
                "bit": 0,
                "dict": 0,
            },
            "HP items": {
                "offset": 0x16820,
                "bit": 2,
                "dict": 1,
            },
            "MP items": {
                "offset": 0x16820,
                "bit": 4,
                "dict": 1,
            },
        },
        "Beast": {
            "Regular Attacks": {
                "offset": 0x16824,
                "bit": 0,
                "dict": 0,
            },
            "Special Attacks": {
                "offset": 0x16826,
                "bit": 0,
                "dict": 0,
            },
            "HP items": {
                "offset": 0x16824,
                "bit": 2,
                "dict": 1,
            },
            "MP items": {
                "offset": 0x16824,
                "bit": 4,
                "dict": 1,
            },
        },
        // Possible pattern template
        "Character": {
            "Regular Attacks": {
                "offset": 0,
                "bit": 0,
                "dict": 0,
            },
            "HP items": {
                "offset": 0,
                "bit": 2,
                "dict": 1,
            },
            "MP items": {
                "offset": 0,
                "bit": 4,
                "dict": 1,
            },
            "Offensive Magic": {
                "offset": 0,
                "bit": 6,
                "dict": 0,
            },
            "Defensive Magic": {
                "offset": 1,
                "bit": 0,
                "dict": 0,
            },
            "Advanced Magic": {
                "offset": 1,
                "bit": 2,
                "dict": 0,
            },
            "Support Actions": {
                "offset": 1,
                "bit": 4,
                "dict": 0,
            },
            "Shield Techniques": {
                "offset": 1,
                "bit": 6,
                "dict": 0,
            },
            "Defensive Moves": {
                "offset": 1,
                "bit": 6,
                "dict": 0,
            },
            "Special Attacks": {
                "offset": 2,
                "bit": 0,
                "dict": 0,
            },
        },
    }
    obj.customize_list = [
        {
            "Constantly": 2,
            "Frequently": 1,
            "Occasionally": 0,
        },
        {
            "Immediately": 2,
            "Frequently": 1,
            "Only in emergency": 0,
        },
    ]
}
