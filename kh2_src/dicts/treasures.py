from dash import html


def treasure_dicts(obj):
    # Icons
    consumable = html.Img(src="assets/item-consumable.png", height=24, style={"margin-bottom": -5})
    menu = html.Img(src="assets/item-tent.png", height=24, style={"margin-bottom": -5})
    key = html.Img(src="assets/item-key.png", height=24, style={"margin-bottom": -5})
    material = html.Img(src="assets/material.png", height=24, style={"margin-bottom": -5})
    keyblade = html.Img(src="assets/weapon-keyblade.png", height=24, style={"margin-bottom": -5})
    staff = html.Img(src="assets/weapon-staff.png", height=24, style={"margin-bottom": -5})
    shield = html.Img(src="assets/weapon-shield.png", height=24, style={"margin-bottom": -5})
    armor = html.Img(src="assets/armor.png", height=24, style={"margin-bottom": -5})
    accessory = html.Img(src="assets/accessory.png", height=24, style={"margin-bottom": -5})
    summon = html.Img(src="assets/ai-settings.png", height=24, style={"margin-bottom": -5})
    
    # Items
    potion = [consumable, "Potion"]
    hipotion = [consumable, "Hi-Potion"]
    ether = [consumable, "Ether"]
    elixir = [consumable, "Elixir"]
    megapotion = [consumable, "Mega-Potion"]
    megaether = [consumable, "Mega-Ether"]
    megalixir = [consumable, "Megalixir"]
    tent = [menu, "Tent"]
    drive = [menu, "Drive Recovery"]
    highdrive = [menu, "High Drive Recovery"]
    strengthboost = [menu, "Strength Boost"]
    magicboost = [menu, "Magic Boost"]
    defenseboost = [menu, "Defense Boost"]
    apboost = [menu, "AP Boost"]
    blazingshard = [material, "Blazing Shard"]
    blazingstone = [material, "Blazing Stone"]
    blazinggem = [material, "Blazing Gem"]
    blazingcrystal = [material, "Blazing Crystal"]
    lightningshard = [material, "Lightning Shard"]
    lightningstone = [material, "Lightning Stone"]
    lightninggem = [material, "Lightning Gem"]
    lightningcrystal = [material, "Lightning Crystal"]
    frostshard = [material, "Frost Shard"]
    froststone = [material, "Frost Stone"]
    frostgem = [material, "Frost Gem"]
    frostcrystal = [material, "Frost Crystal"]
    lucidshard = [material, "Lucid Shard"]
    lucidstone = [material, "Lucid Stone"]
    lucidgem = [material, "Lucid Gem"]
    lucidcrystal = [material, "Lucid Crystal"]
    powershard = [material, "Power Shard"]
    powerstone = [material, "Power Stone"]
    powergem = [material, "Power Gem"]
    powercrystal = [material, "Power Crystal"]
    darkshard = [material, "Dark Shard"]
    darkstone = [material, "Dark Stone"]
    darkgem = [material, "Dark Gem"]
    darkcrystal = [material, "Dark Crystal"]
    mythrilshard = [material, "Mythril Shard"]
    mythrilstone = [material, "Mythril Stone"]
    mythrilgem = [material, "Mythril Gem"]
    mythrilcrystal = [material, "Mythril Crystal"]
    remembranceshard = [material, "Remembrance Shard"]
    remembrancestone = [material, "Remembrance Stone"]
    remembrancegem = [material, "Remembrance Gem"]
    remembrancecrystal = [material, "Remembrance Crystal"]
    brightshard = [material, "Bright Shard"]
    brightstone = [material, "Bright Stone"]
    brightgem = [material, "Bright Gem"]
    brightcrystal = [material, "Bright Crystal"]
    energyshard = [material, "Energy Shard"]
    energystone = [material, "Energy Stone"]
    energygem = [material, "Energy Gem"]
    energycrystal = [material, "Energy Crystal"]
    serenityshard = [material, "Serenity Shard"]
    serenitystone = [material, "Serenity Stone"]
    serenitygem = [material, "Serenity Gem"]
    serenitycrystal = [material, "Serenity Crystal"]
    manifestillusion = [material, "Manifest Illusion"]
    lostillusion = [material, "Lost Illusion"]
    orichalcum = [material, "Orichalcum"]
    orichalcump = [material, "Orichalcum+"]
    tornpages = [key, "Torn Pages"]
    
    @property
    def treasure_dict(self):
        treasure_dict = {
            "Twilight Town": [
                [
                    0x280, 0x281, 0x273, 0x274,
                    0x275, 0x245, 0x246, 0x247,
                ],
                [
                    0x250, 0x251, 0x252, 0x2C5,
                    0x260, 0x261, 0x262, 0x2A2,
                ],
                [
                    0x2A3, 0x2A4, 0x2F7, 0x2A5,
                    0x2A6, 0x2A7, 0x2C0, 0x2C1,
                ],
                [
                    0x2C2, 0x2C3, 0x2B6, 0x2B7,
                    0x267, 0x270, 0x271, 0x272,
                ],
                [
                    0x285, 0x286, 0x287, 0x292,
                    0x293, 0x295, 0x2A1,
                ],
            ],
            "Simulated Twilight Town": [
                [
                    0x1E1, 0x255, 0x256, 0x257,
                    0x263, 0x264, 0x265, 0x266,
                ],
                [
                    0x282, 0x283, 0x284, 0x290,
                    0x291, 0x294, 0x2A0, 0x2B1,
                ],
            ],
            "Hollow Bastion": [
                [
                    0x1A1, 0x1A2, 0x1A3, 0x1C7,
                    0x2F1, 0x1D4, 0x194, 0x195,
                ],
                [
                    0x1A7, 0x1B0, 0x1B1, 0x1D1,
                    0x187, 0x186, 0x1D3, 0x2F2,
                ],
                [
                    0x182, 0x2D1, 0x183, 0x184,
                    0x2D3, 0x1D5,
                ],
            ],
            "Beast's Castle": [
                [
                    0x0F5, 0x0F6, 0x2E7, 0x0F2,
                    0x0F3, 0x0F7, 0x100, 0x101,
                ],
                [
                    0x102, 0x103, 0x104, 0x105,
                    0x2F0, 0x110, 0x111, 0x112,
                ],
                [
                    0x115, 0x113, 0x106, 0x107,
                    0x0F4,
                ],
            ],
            "Olympus Coliseum": [
                [
                    0x0C0, 0x0D6, 0x0D7, 0x0E0,
                    0x0E1, 0x0E2, 0x0C4, 0x0C3,
                ],
                [
                    0x0C5, 0x0C6, 0x2E6, 0x0E3,
                    0x0E4, 0x0E5, 0x0E6, 0x0E7,
                ],
                [
                    0x0F0, 0x0D4, 0x0D0, 0x0D2,
                ],
            ],
            "Agrabah": [
                [
                    0x033, 0x034, 0x035, 0x036,
                    0x037, 0x040, 0x2E3, 0x041,
                ],
                [
                    0x042, 0x043, 0x044, 0x045,
                    0x046, 0x2F5, 0x047, 0x050,
                ],
                [
                    0x052, 0x053, 0x054, 0x055,
                    0x2C7, 0x056, 0x2E4, 0x2E5,
                ],
                [
                    0x051, 0x2C6,
                ],
            ],
            "The Land of Dragons": [
                [
                    0x001, 0x2D7, 0x2E0, 0x011,
                    0x012, 0x013, 0x014, 0x015,
                ],
                [
                    0x016, 0x017, 0x020, 0x021,
                    0x022, 0x023, 0x024, 0x025,
                ],
                [
                    0x026, 0x027, 0x030, 0x031,
                    0x032,
                ],
            ],
            "Hundred Acre Woods": [
                [
                    0x1D7, 0x094, 0x095, 0x0A4,
                    0x0A2, 0x0A3, 0x1E0, 0x097,
                ],
                [
                    0x0A0, 0x0A7, 0x0A5, 0x0A6,
                    0x0B1, 0x0B2, 0x0B3, 0x0B4,
                ],
                [
                    0x0B6, 0x0B7, 0x1D6, 0x091,
                ],
            ],
            "Pride Lands": [
                [
                    0x2D4, 0x230, 0x231, 0x225,
                    0x226, 0x227, 0x2F3, 0x2F4,
                ],
                [
                    0x243, 0x214, 0x215, 0x220,
                    0x221, 0x222, 0x223, 0x224,
                ],
                [
                    0x232, 0x233, 0x234, 0x235,
                    0x236, 0x237, 0x240, 0x2D5,
                ],
                [
                    0x241,
                ],
            ],
            "Disney Castle": [
                [
                    0x081, 0x082, 0x083, 0x084,
                    0x085, 0x086, 0x087, 0x080,
                ],
            ],
            "Timeless River": [
                [
                    0x060, 0x061, 0x063, 0x064,
                    0x065, 0x066, 0x067,
                ],
            ],
            "Halloween Town": [
                [
                    0x142, 0x143, 0x141, 0x137,
                    0x140, 0x144, 0x145, 0x146,
                ],
                [
                    0x150, 0x151, 0x152, 0x153,
                    0x156, 0x154,
                ],
            ],
            "Port Royal": [
                [
                    0x161, 0x162, 0x163, 0x164,
                    0x165, 0x166, 0x167, 0x171,
                ],
                [
                    0x172, 0x1E7, 0x1F0, 0x174,
                    0x175, 0x1F1, 0x173, 0x176,
                ],
                [
                    0x177, 0x1F2, 0x180, 0x181,
                    0x1F3,
                ],
            ],
            "Space Paranoids": [
                [
                    0x1E2, 0x116, 0x121, 0x122,
                    0x123, 0x2F6, 0x124, 0x125,
                ],
                [
                    0x131, 0x2E1, 0x134, 0x135,
                    0x136, 0x2D0,
                ],
            ],
            "The World That Never Was": [
                [
                    0x1F4, 0x1F5, 0x1F6, 0x1F7,
                    0x213, 0x300, 0x301, 0x1E5,
                ],
                [
                    0x2E2, 0x200, 0x201, 0x1E6,
                    0x202, 0x203, 0x204, 0x207,
                ],
                [
                    0x210, 0x211, 0x212,
                ],
            ],
        }
        if hasattr(self, "fm") and self.fm:
            treasure_dict["Hollow Bastion"][2] += [0x302, 0x303]
            treasure_dict["Hollow Bastion"] += [
                [
                    0x304, 0x305, 0x306, 0x307,
                    0x310, 0x311, 0x312, 0x313,
                ],
                [
                    0x314, 0x315, 0x316, 0x317,
                    0x320, 0x321, 0x322, 0x323,
                ],
                [
                    0x324, 0x325, 0x326, 0x331,
                    0x332, 0x333,
                ],
            ]
        return treasure_dict
    type(obj).treasure_dict = treasure_dict
    
    @property
    def treasure_list(self):
        treasure_list = {
            "Twilight Town": [
                [
                    potion, mythrilshard, potion, mythrilshard,
                    hipotion, hipotion, apboost, tent,
                ],
                [
                    mythrilshard, potion, mythrilshard, potion,
                    tent, hipotion, mythrilshard, potion,
                ],
                [
                    hipotion, ether, ether, mythrilshard,
                    [key, "Tower Map"], mythrilstone, mythrilgem, orichalcum,
                ],
                [
                    apboost, mythrilcrystal, orichalcum, mythrilcrystal,
                    orichalcump, mythrilshard, mythrilcrystal, apboost,
                ],
                [
                    mythrilcrystal, mythrilstone, elixir, mythrilcrystal,
                    mythrilstone, orichalcum, [key, "Ultimate Recipe"],
                ],
            ],
            "Simulated Twilight Town": [
                [
                    ["Station of Serenity: ", consumable, "Potion"], ["Central Station: ", consumable, "Potion 1"], ["Central Station: ", consumable, "Hi-Potion"], ["Central Station: ", consumable, "Potion 2"],
                    ["Sunset Terrace: ", accessory, "Ability Ring"], ["Sunset Terrace: ", consumable, "Hi-Potion"], ["Sunset Terrace: ", consumable, "Potion 1"], ["Sunset Terrace: ", consumable, "Potion 2"],
                ],
                [
                    ["Mansion: Foyer: ", consumable, "Hi-Potion"], ["Mansion: Foyer: ", consumable, "Potion 1"], ["Mansion: Foyer: ", consumable, "Potion 2"], ["Mansion: Dining Room: ", armor, "Elven Bandana"],
                    ["Mansion: Dining Room: ", consumable, "Potion"], ["Mansion: Dining Room: ", consumable, "Hi-Potion"], ["Mansion: Basement Corridor: ", consumable, "Hi-Potion"], ["Station of Calling: ", consumable, "Potion"],
                ],
            ],
            "Hollow Bastion": [
                [
                    drive, apboost, hipotion, mythrilshard,
                    tent, [key, "Castle Perimeter Map"], mythrilgem, apboost,
                ],
                [
                    mythrilstone, mythrilcrystal, hipotion, apboost,
                    [key, "Skill Recipe"], [summon, "Ukulele Charm"], [key, "Moon Recipe"], apboost,
                ],
                [
                    tornpages, [key, "The Great Maw Map"], elixir, apboost,
                    [keyblade, "Gull Wing"], [armor, "Cosmic Chain"],
                ],
            ],
            "Beast's Castle": [
                [
                    apboost, hipotion, mythrilshard, [key, "Castle Map"],
                    mythrilshard, hipotion, tent, hipotion,
                ],
                [
                    mythrilshard, drive, mythrilshard, apboost,
                    tent, [key, "Basement Map"], apboost, mythrilshard,
                ],
                [
                    hipotion, megapotion, mythrilshard, tent,
                    [key, "Mega-Recipe"],
                ],
            ],
            "Olympus Coliseum": [
                [
                    strengthboost, mythrilshard, mythrilstone, ether,
                    apboost, hipotion, [key, "Underworld Map"], mythrilshard,
                ],
                [
                    hipotion, apboost, mythrilshard, hipotion,
                    ether, mythrilshard, mythrilstone, tent,
                ],
                [
                    apboost, [key, "Caverns Map"], mythrilshard, apboost,
                ],
            ],
            "Agrabah": [
                [
                    drive, mythrilshard, hipotion, apboost,
                    mythrilstone, mythrilshard, megaether, mythrilgem,
                ],
                [
                    hipotion, hipotion, apboost, mythrilshard,
                    [accessory, "Skill Ring"], mythrilstone, drive, mythrilshard,
                ],
                [
                    mythrilstone, apboost, mythrilshard, hipotion,
                    [key, "Cave of Wonders Map"], apboost, apboost, serenityshard,
                ],
                [
                    tornpages, [key, "Ruins Map"],
                ],
            ],
            "The Land of Dragons": [
                [
                    hipotion, ether, mythrilshard, hipotion,
                    mythrilshard, hipotion, [key, "Recovery Recipe"], ether,
                ],
                [
                    mythrilshard, apboost, hipotion, hipotion,
                    apboost, tornpages, [key, "Palace Map"], apboost,
                ],
                [
                    [key, "Queen Recipe"], apboost, [shield, "Ogre Shield"], mythrilcrystal,
                    orichalcum,
                ],
            ],
            "Hundred Acre Woods": [
                [
                    [key, "100 Acre Wood Map"], apboost, mythrilstone, defenseboost,
                    apboost, mythrilgem, [accessory, "Draw Ring"], mythrilcrystal,
                ],
                [
                    apboost, magicboost, apboost, orichalcum,
                    mythrilgem, apboost, orichalcum, [key, "Guard Recipe"],
                ],
                [
                    mythrilcrystal, apboost, [accessory, "Cosmic Ring"], [key, "Style Recipe"],
                ],
            ],
            "Pride Lands": [
                [
                    [key, "Savannah Map"], ether, mythrilstone, hipotion,
                    mythrilstone, ether, apboost, mythrilshard,
                ],
                [
                    [key, "Pride Rock Map"], mythrilstone, megaether, hipotion,
                    apboost, mythrilgem, mythrilstone, tent,
                ],
                [
                    mythrilshard, hipotion, mythrilstone, serenitystone,
                    mythrilstone, hipotion, [key, "Oasis Map"], tornpages,
                ],
                [
                    apboost,
                ],
            ],
            "Disney Castle": [
                [
                    mythrilshard, [key, "Star Recipe"], apboost, mythrilstone,
                    ether, hipotion, mythrilshard, tornpages,
                ],
            ],
            "Timeless River": [
                [
                    [key, "Cornerstone Hill Map"], drive, mythrilshard, hipotion,
                    mythrilstone, apboost, hipotion,
                ],
            ],
            "Halloween Town": [
                [
                    hipotion, mythrilshard, [key, "Halloween Town Map"], mythrilstone,
                    megapotion, hipotion, mythrilstone, apboost,
                ],
                [
                    hipotion, mythrilgem, ether, mythrilstone,
                    [key, "Christmas Town Map"], apboost,
                ],
            ],
            "Port Royal": [
                [
                    [key, "Naval Map"], mythrilstone, ether, ether,
                    apboost, mythrilshard, mythrilgem, ether,
                ],
                [
                    mythrilshard, apboost, apboost, mythrilshard,
                    ether, megapotion, [summon, "Feather Charm"], apboost,
                ],
                [
                    orichalcum, [staff, "Meteor Staff"], highdrive, [key, "King Recipe"],
                    mythrilcrystal,
                ],
            ],
            "Space Paranoids": [
                [
                    [key, "Pit Cell Area Map"], mythrilcrystal, megapotion, mythrilstone,
                    mythrilgem, drive, tent, apboost,
                ],
                [
                    [key, "I/O Tower Map"], [armor, "Gaia Belt"], apboost, orichalcump,
                    [accessory, "Cosmic Arts"], [key, "Central Computer Core Map"],
                ],
            ],
            "The World That Never Was": [
                [
                    mythrilstone, mythrilcrystal, apboost, orichalcum,
                    mythrilcrystal, apboost, mythrilstone, [key, "Dark City Map"],
                ],
                [
                    orichalcump, mythrilgem, orichalcum, [armor, "Cosmic Belt"],
                    mythrilgem, orichalcum, mythrilcrystal, mythrilstone,
                ],
                [
                    apboost, mythrilcrystal, orichalcum,
                ],
            ],
        }
        if hasattr(self, "fm") and self.fm:
            treasure_list["Hollow Bastion"][0][4] = darkshard
            treasure_list["Hollow Bastion"][1][2] = darkcrystal
            treasure_list["Hollow Bastion"][2][2] = energycrystal
            treasure_list["Hollow Bastion"][2] += [apboost, powercrystal]
            treasure_list["Hollow Bastion"] += [
                [
                    frostcrystal, manifestillusion, apboost, remembrancegem,
                    serenitygem, apboost, serenitycrystal, manifestillusion,
                ],
                [
                    serenitygem, [key, "Dark Remembrance Map"], serenitycrystal, remembrancecrystal,
                    apboost, manifestillusion, apboost, apboost,
                ],
                [
                    [key, "Depths of Remembrance Map"], strengthboost, magicboost, [key, "Garden of Assemblage Map"],
                    lostillusion, [key, "Proof of Nonexistence"],
                ],
            ]
            treasure_list["Beast's Castle"][0][4] = [key, "Mega-Recipe"]
            treasure_list["Beast's Castle"][0][5] = mythrilshard
            treasure_list["Beast's Castle"][1][1] = powershard
            treasure_list["Beast's Castle"][1][4] = brightstone
            treasure_list["Beast's Castle"][2][1] = lucidshard
            treasure_list["Beast's Castle"][2][4] = blazingshard
            treasure_list["Olympus Coliseum"][1][0] = lucidshard
            treasure_list["Olympus Coliseum"][1][3] = brightshard
            treasure_list["Olympus Coliseum"][1][7] = lucidstone
            treasure_list["Agrabah"][0][0] = darkshard
            treasure_list["Agrabah"][0][6] = serenityshard
            treasure_list["Agrabah"][1][0] = powershard
            treasure_list["Agrabah"][1][6] = powerstone
            treasure_list["Agrabah"][2][7] = serenitygem
            treasure_list["The Land of Dragons"][0][0] = darkshard
            treasure_list["The Land of Dragons"][0][5] = lightningshard
            treasure_list["The Land of Dragons"][1][2] = darkshard
            treasure_list["The Land of Dragons"][1][3] = frostshard
            treasure_list["Pride Lands"][0][1] = darkgem
            treasure_list["Pride Lands"][0][3] = frostgem
            treasure_list["Pride Lands"][0][5] = brightstone
            treasure_list["Pride Lands"][1][2] = serenitycrystal
            treasure_list["Pride Lands"][1][3] = energystone
            treasure_list["Pride Lands"][1][7] = lucidgem
            treasure_list["Pride Lands"][2][1] = serenitygem
            treasure_list["Pride Lands"][2][3] = serenitygem
            treasure_list["Pride Lands"][2][5] = serenitycrystal
            treasure_list["Disney Castle"][0][4] = blazingstone
            treasure_list["Disney Castle"][0][5] = blazingshard
            treasure_list["Timeless River"][0][1] = frostshard
            treasure_list["Timeless River"][0][6] = froststone
        return treasure_list
    type(obj).treasure_list = treasure_list
    
    @property
    def treasure_zip(self):
        treasure_zip = {}
        for w in self.treasure_dict.keys():
            d = {}
            for idxs, labels in zip(self.treasure_dict[w], self.treasure_list[w]):
                for i, l in zip(idxs, labels):
                    d[i] = l
            treasure_zip[w] = d
        return treasure_zip
    type(obj).treasure_zip = treasure_zip
