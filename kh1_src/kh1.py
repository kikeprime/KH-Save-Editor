import os
import struct

from ctypes import *


class KH1Character:
    """
    Class for representing the character struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0x74 bytes long.
    """
    def __init__(self, name, data):
        self.name = name
        self.level = c_ubyte(data[0])
        self.hp = c_ubyte(data[1])
        self.maxhp = c_ubyte(data[2])
        self.mp = c_ubyte(data[3])
        self.maxmp = c_ubyte(data[4])
        self.maxap = c_ubyte(data[5])
        self.strength = c_ubyte(data[6])
        self.defense = c_ubyte(data[7])
        # data[0x08:0x18] is unknown, full of 0x64
        self.accessoryslots = c_ubyte(data[0x18])
        self.accessories = (c_ubyte*8)(*data[0x19:0x21])
        self.itemslots = c_ubyte(data[0x21])
        self.items = (c_ubyte*8)(*data[0x22:0x2A])
        # data[0x2A:0x32] is unknown
        self.weapon = c_ubyte(data[0x32])
        # data[0x33:0x38] is unknown
        self.submp = c_ushort(int.from_bytes(data[0x38:0x3A][::-1])) # 30 or 0x1E means 1 MP
        # data[0x3A:0x3C]is unknown
        self.exp = c_uint(int.from_bytes(data[0x3C:0x40][::-1]))
        self.abilities = (c_ubyte*48)(*data[0x40:0x70]) # Pooh has unknown data here with invalid ability IDs.
        self.magic = c_ubyte(data[0x70])
        # data[0x71:0x74] is unknown


class KH1GummiBlock:
    def __init__(self, data):
        pass


class KH1GummiShip:
    def __init__(self, data):
        self.blockcount = c_ushort(int.from_bytes(data[0x00:0x02][::-1]))
        self.x = c_ushort(int.from_bytes(data[0x02:0x04][::-1]))
        self.y = c_ushort(int.from_bytes(data[0x04:0x06][::-1]))
        self.z = c_ushort(int.from_bytes(data[0x06:0x08][::-1]))
        self.transformpair = c_ushort(int.from_bytes(data[0x08:0x0A][::-1]))
        self.name = bytearray(data[0x4C:0x56])


class KH1:
    def __init__(self, slot=0, fm=False):
        self.dicts()
        self.trinity_dicts()
        self.gummi_dicts()
        if slot != 0:
            self.fm = fm
            if self.fm:
                self.filename = "BISLPS-25198-" + f"{slot:02d}"
            else:
                self.filename = "BASLUS-20370-" + f"{slot:02d}"
            if os.path.exists(os.path.join("files", self.filename, self.filename)):
                with open(os.path.join("files", self.filename, self.filename), "rb") as file:
                    self.data = (c_ubyte*0x16C00)(*file.read())
            else:
                with open("files/" + self.filename, "rb") as file:
                    self.data = (c_ubyte*0x16C00)(*file.read())
            self.__parse_data(self.data)
            self.sysdata = None
            if os.path.exists(os.path.join("files", self.filename, "system.bin")):
                with open(os.path.join("files", self.filename, "system.bin"), "rb") as sysfile:
                    self.sysdata = (c_ubyte*0x400)(*sysfile.read())
                # Playtime in seconds * 60 but possibly in seconds * 50 in PAL versions
                self.playtime = c_uint(int.from_bytes(self.sysdata[0x10:0x14][::-1]))

    def __parse_data(self, data):
        # For FM the currently loaded save file starts at 0x3F8380 in the memory according to the RetroAchievements code notes.
        # For vanilla USA it starts at 0x3F1C90.
        # For vanilla JP it starts at 0x3F2080.
        self.header = c_uint(int.from_bytes(data[0x00:0x04:-1])) # 4 in vanilla, 5 in FM
        # self.characters = data[0x04:0x048C]
        self.sora = KH1Character("Sora", data[0x04:0x04+0x74])
        self.donald = KH1Character("Donald", data[0x04+0x74:0x04+2*0x74])
        self.goofy = KH1Character("Goofy", data[0x04+2*0x74:0x04+3*0x74])
        self.tarzan = KH1Character("Tarzan", data[0x04+3*0x74:0x04+4*0x74])
        self.pooh = KH1Character("Winnie the Pooh", data[0x04+4*0x74:0x04+5*0x74])
        self.aladdin = KH1Character("Aladdin", data[0x04+5*0x74:0x04+6*0x74])
        self.ariel = KH1Character("Ariel", data[0x04+6*0x74:0x04+7*0x74])
        self.jack = KH1Character("Jack Skellington", data[0x04+7*0x74:0x04+8*0x74])
        self.peterpan = KH1Character("Peter Pan", data[0x04+8*0x74:0x04+9*0x74])
        self.beast = KH1Character("Beast", data[0x04+9*0x74:0x04+10*0x74])
        self.characters = [
            self.sora, self.donald, self.goofy,
            self.tarzan, self.pooh, self.aladdin,
            self.ariel, self.jack, self.peterpan,
            self.beast
        ]
        self.path = c_ubyte(data[0x048C])
        self.curve = c_ubyte(data[0x048D])
        self.party = (c_ubyte*4)(*data[0x048E:0x0492])
        self.magiclevels = (c_ubyte*7)(*data[0x0492:0x0499])
        # data[0x0499] is unknown
        # I gave it to inventory so the array and item indices match
        self.inventory = (c_ubyte*256)(*data[0x0499:0x0599])
        self.shared_abilities = (c_ubyte*48)(*data[0x0599:0x05C9])
        # data[0x05C9:0x05CC] is unknown.
        self.di_chest_flag = c_ubyte(data[0x05CC])
        
        self.summons = (c_ubyte*7)(*data[0x07D0:0x07D7])
        # data[0x07D7:0x07D8] is unknown.
        self.heartless = (c_ushort*36)(*struct.unpack("<36H", bytearray(data[0x07D8:0x0820])))
        # data[0x0820:0x082C] is unknown.
        self.shortcuts = (c_ubyte*3)(*data[0x082C:0x082F])
        # data[0x082F:0x0836] is unknown.
        self.cure_on_friends = c_ushort(int.from_bytes(data[0x0836:0x0838][::-1]))
        # data[0x0838:0x083E] is unknown.
        self.heartless_killed = c_ushort(int.from_bytes(data[0x083E:0x0840][::-1]))
        # data[0x0840:0x0844] is unknown.
        self.deflected = c_ushort(int.from_bytes(data[0x0844:0x0846][::-1]))
        # data[0x0846:0x0848] is unknown.
        self.item_usage = c_ushort(int.from_bytes(data[0x0848:0x084A][::-1]))
        self.hits = c_ushort(int.from_bytes(data[0x084A:0x084C][::-1]))
        self.friend_ko = c_ushort(int.from_bytes(data[0x084C:0x084E][::-1]))
        self.deaths = c_ushort(int.from_bytes(data[0x084E:0x0850][::-1]))

        self.currentcup = c_ubyte(data[0x0F26])
        self.philcup = c_ubyte(data[0x0F36])
        self.pegasuscup = c_ubyte(data[0x0F37])
        self.herculescup = c_ubyte(data[0x0F38])
        self.hadescup = c_ubyte(data[0x0F39])
        self.platinummatch = c_ubyte(data[0x0F6A])

        self.tiduswins = c_ubyte(data[0x101B])
        self.wakkawins = c_ubyte(data[0x101C])
        self.selphiewins = c_ubyte(data[0x101D])

        self.sorawins = c_ushort(int.from_bytes(data[0x1036:0x1038][::-1]))
        self.rikuwins = c_ushort(int.from_bytes(data[0x1038:0x103A][::-1]))

        self.slides = (c_ubyte*6)(*data[0x1207:0x120D])
        self.slides_watched = c_ubyte(data[0x1212])

        self.world_progresses = (c_ubyte*20)(*data[0x1500:0x1514])
        
        self.raft = bytearray(data[0x16D1:0x16DB])
        
        # Entries existing since vanilla JP use data[0x16E3:0x16F3]
        # Sephiroth, Ice Titan, Jasmine 2 use 0x16F7, Xemnas uses 0x16F8
        self.journal_chars = (c_ubyte*23)(*data[0x16E3:0x16FA])
        # self.boss_journal = (c_ubyte*4)(*data[0x16F6:0x16FA])
        # data[0x16FA:0x1703] is unknown
        self.dalmatians = (c_ubyte*13)(*data[0x1703:0x1710])
        
        self.chronicles = (c_ubyte*10)(*data[0x1997:0x19BF:4])
        self.reports = (c_ubyte*2)(*data[0x19C0:0x19C2])
        self.journal_unlock = c_ubyte(data[0x19C4]) # bit index 3, 0x1F for completed game so needs further investigation

        self.trinity_unlock = c_ubyte(data[0x1C1B])
        self.trinity_count = (c_ubyte*6)(*data[0x1C66:0x1C6C]) # Jump, Unused, Charge, Ladder, Push, Detect
        # The Trinity flags spread across these.
        # The OC Lobby Push isn't here but at 0x1E10 bit index 0.
        self.trinity_flags = (c_ubyte*0x48)(*data[0x1C6C:0x1CB4])
        
        self.world_statuses = (c_ubyte*15)(*data[0x1EF0:0x1EFF])
        self.landingpoints = (c_ubyte*15)(*data[0x1EFF:0x1F0E])
        
        self.world = c_uint(int.from_bytes(data[0x2040:0x2044][::-1]))
        self.room = c_uint(int.from_bytes(data[0x2044:0x2048][::-1]))
        self.flag = c_uint(int.from_bytes(data[0x2048:0x204C][::-1]))

        self.GUMI = bytearray(data[0x2400:0x2404]).decode() # ASCII string "GUMI"
        # data[0x2404] seems to be a version code, 0 for vanilla and 1 for FM, needs further investigation.
        self.gummi_tutorial = c_ubyte(data[0x2405]) # might be an int # reseting wipes gummi data
        # data[0x2409:0x2410] is [1, 2, 3, 4, 5, 6, 7] for me
        self.selectedship = c_ubyte(data[0x2410])
        # self.gummiships = data[0x241C:0xBE7C], based on the start offsets of each ship
        # which I've confirmed but the last ship overlaps with the 1st 4 blocks which are also confirmed.
        self.gummiships = [KH1GummiShip(data[0x241C+i*0x0F70:0x241C+(i+1)*0x0F70]) for i in range(10)]
        self.gummiblocks = (c_ubyte*108)(*data[0xBE78:0xBEE4])

        self.gummi_decelerate = c_uint(int.from_bytes(data[0xBF01:0xBF05][::-1]))
        self.gummi_accelerate = c_uint(int.from_bytes(data[0xBF05:0xBF09][::-1]))
        self.gummi_transform = c_uint(int.from_bytes(data[0xBF09:0xBF0D][::-1]))
        self.gummi_scannon = c_uint(int.from_bytes(data[0xBF0D:0xBF11][::-1]))
        self.gummi_mcannon = c_uint(int.from_bytes(data[0xBF11:0xBF15][::-1]))
        self.gummi_lcannon = c_uint(int.from_bytes(data[0xBF15:0xBF19][::-1]))
        self.gummi_slaser = c_uint(int.from_bytes(data[0xBF19:0xBF1D][::-1]))
        self.gummi_mlaser = c_uint(int.from_bytes(data[0xBF1D:0xBF21][::-1]))
        self.gummi_llaser = c_uint(int.from_bytes(data[0xBF21:0xBF25][::-1]))
        
        self.autolock = c_uint(int.from_bytes(data[0x16400:0x16404][::-1]))
        self.targetlock = c_uint(int.from_bytes(data[0x16404:0x16408][::-1]))
        self.camera = c_uint(int.from_bytes(data[0x16408:0x1640C][::-1]))
        # data[0x1640C:0x16410] is unknown
        self.vibration = c_uint(int.from_bytes(data[0x16410:0x16414][::-1]))
        self.sound = c_uint(int.from_bytes(data[0x16414:0x16418][::-1]))
        self.datainstall = c_uint(int.from_bytes(data[0x16418:0x1641C][::-1])) # JP/FM
        self.difficulty = c_uint(int.from_bytes(data[0x16418:0x1641C][::-1])) # USA/EU
        
        self.munny = c_uint(int.from_bytes(data[0x1641C:0x16420][::-1]))

        # Final Mix stuff
        if self.fm:
            self.heartless = (c_ushort*51)(*struct.unpack("<51H", bytearray(data[0x07D8:0x083E])))
            self.shortcuts = (c_ubyte*3)(*data[0x0844:0x0847])
            self.cure_on_friends = c_ushort(int.from_bytes(data[0x084E:0x0850][::-1]))
            self.heartless_killed = c_ushort(int.from_bytes(data[0x0856:0x0858][::-1]))
            self.deflected = c_ushort(int.from_bytes(data[0x085C:0x085E][::-1]))
            self.item_usage = c_ushort(int.from_bytes(data[0x0860:0x0862][::-1]))
            self.hits = c_ushort(int.from_bytes(data[0x0862:0x0864][::-1]))
            self.friend_ko = c_ushort(int.from_bytes(data[0x0864:0x0868][::-1]))
            self.deaths = c_ushort(int.from_bytes(data[0x0868:0x086A][::-1]))
            self.xemnas = c_ubyte(data[0x1118])
            self.gummiblocks = (c_ubyte*160)(*data[0xBE78:0xBF18]) # 144 bytes until last Design Gummi
            self.gummi_decelerate = c_uint(int.from_bytes(data[0xBF41:0xBF45][::-1]))
            self.gummi_accelerate = c_uint(int.from_bytes(data[0xBF45:0xBF49][::-1]))
            self.gummi_transform = c_uint(int.from_bytes(data[0xBF49:0xBF4D][::-1]))
            self.gummi_scannon = c_uint(int.from_bytes(data[0xBF4D:0xBF51][::-1]))
            self.gummi_mcannon = c_uint(int.from_bytes(data[0xBF51:0xBF55][::-1]))
            self.gummi_lcannon = c_uint(int.from_bytes(data[0xBF55:0xBF59][::-1]))
            self.gummi_slaser = c_uint(int.from_bytes(data[0xBF59:0xBF5D][::-1]))
            self.gummi_mlaser = c_uint(int.from_bytes(data[0xBF5D:0xBF61][::-1]))
            self.gummi_llaser = c_uint(int.from_bytes(data[0xBF61:0xBF65][::-1]))
            self.difficulty = c_uint(int.from_bytes(data[0x1642C:0x16430][::-1]))

    def __save_characters(self):
        i = 0
        for c in self.characters:
            self.data[0x04+i*0x74+0x00] = c.level
            self.data[0x04+i*0x74+0x01] = c.hp
            self.data[0x04+i*0x74+0x02] = c.maxhp
            self.data[0x04+i*0x74+0x03] = c.mp
            self.data[0x04+i*0x74+0x04] = c.maxmp
            self.data[0x04+i*0x74+0x05] = c.maxap
            self.data[0x04+i*0x74+0x06] = c.strength
            self.data[0x04+i*0x74+0x07] = c.defense
            self.data[0x04+i*0x74+0x18] = c.accessoryslots
            self.data[0x04+i*0x74+0x19:0x04+i*0x74+0x21] = bytearray(c.accessories)
            self.data[0x04+i*0x74+0x21] = c.itemslots
            self.data[0x04+i*0x74+0x22:0x04+i*0x74+0x2A] = bytearray(c.items)
            self.data[0x04+i*0x74+0x32] = c.weapon
            self.data[0x04+i*0x74+0x38:0x04+i*0x74+0x3A] = bytearray(c.submp)
            self.data[0x04+i*0x74+0x3C:0x04+i*0x74+0x40] = bytearray(c.exp)
            self.data[0x04+i*0x74+0x40:0x04+i*0x74+0x70] = bytearray(c.abilities)
            self.data[0x04+i*0x74+0x70] = c.magic
            i += 1
        
    def __save_shared(self):
        self.data[0x048D] = self.curve
        self.data[0x048E:0x0492] = bytearray(self.party)
        self.data[0x0499:0x0599] = bytearray(self.inventory)
        self.data[0x0599:0x05C9] = bytearray(self.shared_abilities)

        self.data[0x1036:0x1038] = bytearray(self.sorawins)
        self.data[0x1038:0x103A] = bytearray(self.rikuwins)

        self.data[0x1207:0x120D] = bytearray(self.slides)
        self.data[0x1212] = self.slides_watched
        
        self.data[0x1500:0x1514] = bytearray(self.world_progresses)
        
        self.data[0x16D1:0x16DB] = self.raft
        
        self.data[0x16E3:0x16FA] = bytearray(self.journal_chars)
        self.data[0x1703:0x1710] = bytearray(self.dalmatians)
        
        self.data[0x1997:0x19BF:4] = bytearray(self.chronicles)
        self.data[0x19C0:0x19C2] = bytearray(self.reports)
        self.data[0x19C4] = self.journal_unlock
        
        self.data[0x1C1B] = self.trinity_unlock
        self.data[0x1C66:0x1C6C] = bytearray(self.trinity_count)
        self.data[0x1C6C:0x1CB4] = bytearray(self.trinity_flags)
        
        self.data[0x1EF0:0x1EFF] = bytearray(self.world_statuses)
        self.data[0x1EFF:0x1F0E] = bytearray(self.landingpoints)
        
        self.data[0x2040:0x2044] = bytearray(self.world)
        self.data[0x2044:0x2048] = bytearray(self.room)
        self.data[0x2048:0x204C] = bytearray(self.flag)
        
        self.data[0x2405] = self.gummi_tutorial
        self.data[0x2410] = self.selectedship
        
        self.data[0x16400:0x16404] = bytearray(self.autolock)
        self.data[0x16404:0x16408] = bytearray(self.targetlock)
        self.data[0x16408:0x1640C] = bytearray(self.camera)
        self.data[0x16410:0x16414] = bytearray(self.vibration)
        self.data[0x16414:0x16418] = bytearray(self.sound)
        self.data[0x16418:0x1641C] = bytearray(self.datainstall)
        self.data[0x1641C:0x16420] = bytearray(self.munny)

    def __save_vanilla(self):
        self.data[0x07D8:0x0820] = bytearray(self.heartless)
        self.data[0x082C:0x082F] = bytearray(self.shortcuts)
        self.data[0xBE78:0xBEE4] = bytearray(self.gummiblocks)
        self.data[0xBF01:0xBF05] = bytearray(self.gummi_decelerate)
        self.data[0xBF05:0xBF09] = bytearray(self.gummi_accelerate)
        self.data[0xBF09:0xBF0D] = bytearray(self.gummi_transform)
        self.data[0xBF0D:0xBF11] = bytearray(self.gummi_scannon)
        self.data[0xBF11:0xBF15] = bytearray(self.gummi_mcannon)
        self.data[0xBF15:0xBF19] = bytearray(self.gummi_lcannon)
        self.data[0xBF19:0xBF1D] = bytearray(self.gummi_slaser)
        self.data[0xBF1D:0xBF21] = bytearray(self.gummi_mlaser)
        self.data[0xBF21:0xBF25] = bytearray(self.gummi_llaser)

    def __save_fm(self):
        self.data[0x07D8:0x083E] = bytearray(self.heartless)
        self.data[0x0844:0x0847] = bytearray(self.shortcuts)
        
        self.data[0x1118] = self.xemnas

        self.data[0xBE78:0xBF18] = bytearray(self.gummiblocks)
        self.data[0xBF41:0xBF45] = bytearray(self.gummi_decelerate)
        self.data[0xBF45:0xBF49] = bytearray(self.gummi_accelerate)
        self.data[0xBF49:0xBF4D] = bytearray(self.gummi_transform)
        self.data[0xBF4D:0xBF51] = bytearray(self.gummi_scannon)
        self.data[0xBF51:0xBF55] = bytearray(self.gummi_mcannon)
        self.data[0xBF55:0xBF59] = bytearray(self.gummi_lcannon)
        self.data[0xBF59:0xBF5D] = bytearray(self.gummi_slaser)
        self.data[0xBF5D:0xBF61] = bytearray(self.gummi_mlaser)
        self.data[0xBF61:0xBF65] = bytearray(self.gummi_llaser)

        self.data[0x1642C:0x16430] = bytearray(self.difficulty)

    def save(self):
        if self.sysdata is not None:
            self.sysdata[0x10:0x14] = bytearray(self.playtime)

        self.__save_characters()
        self.__save_shared()
        if self.fm:
            self.__save_fm()
        else:
            self.__save_vanilla()

        if os.path.exists(os.path.join("files", self.filename, self.filename)):
            os.makedirs("saved/" + self.filename, exist_ok=True)
            with open(os.path.join("saved", self.filename, self.filename), "wb") as file:
                file.write(self.data)
        else:
            with open("saved/" + self.filename, "wb") as file:
                file.write(self.data)
        if self.sysdata is not None:
            with open(os.path.join("saved", self.filename, "system.bin"), "wb") as sysfile:
                sysfile.write(self.sysdata)

    def dicts(self):
        self.character_dict = {
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
        self.ability_dict = {
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
            # FM exclusives
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
            # Remix exclusives
            "EXP Zero": 0x40,
            "Combo Master": 0x41
        }
        self.item1_dict = {
            "Empty": 0x00,
            "Potion": 0x01,
            "Hi-Potion": 0x02,
            "Ether": 0x03,
            "Elixir": 0x04,
            "Unused 0x05": 0x05,
            "Mega-Potion": 0x06,
            "Mega-Ether": 0x07,
            "Megalixir": 0x08,
            "Fury Stone": 0x09,
            "Power Stone": 0x0A,
            "Energy Stone": 0x0B,
            "Blazing Stone": 0x0C,
            "Frost Stone": 0x0D,
            "Lightning Stone": 0x0E,
            "Dazzling Stone": 0x0F,
            "Stormy Stone": 0x10
        }
        self.accessory_dict =  {
            "Empty": 0x00,
            "Protect Chain": 0x11,
            "Protera Chain": 0x12,
            "Protega Chain": 0x13,
            "Fire Ring": 0x14,
            "Fira Ring": 0x15,
            "Firaga Ring": 0x16,
            "Blizzard Ring": 0x17,
            "Blizzara Ring": 0x18,
            "Blizzaga Ring": 0x19,
            "Thunder Ring": 0x1A,
            "Thundara Ring": 0x1B,
            "Thundaga Ring": 0x1C,
            "Ability Stud": 0x1D,
            "Guard Earring": 0x1E,
            "Master Earring": 0x1F,
            "Chaos Ring": 0x20,
            "Dark Ring": 0x21,
            "Element Ring": 0x22,
            "Three Stars": 0x23,
            "Power Chain": 0x24,
            "Golem Chain": 0x25,
            "Titan Chain": 0x26,
            "Energy Bangle": 0x27,
            "Angel Bangle": 0x28,
            "Gaia Bangle": 0x29,
            "Magic Armlet": 0x2A,
            "Rune Armlet": 0x2B,
            "Atlas Armlet": 0x2C,
            "Heartguard": 0x2D,
            "Ribbon": 0x2E,
            "Crystal Crown": 0x2F,
            "Brave Warrior": 0x30,
            "Ifrit's Horn": 0x31,
            "Inferno Band": 0x32,
            "White Fang": 0x33,
            "Ray of Light": 0x34,
            "Holy Circlet": 0x35,
            "Raven's Claw": 0x36,
            "Omega Arts": 0x37,
            "EXP Earring": 0x38,
            "Unused 0x39": 0x39,
            "EXP Ring": 0x3A,
            "EXP Bracelet": 0x3B,
            "EXP Necklace": 0x3C,
            "Firagun Band": 0x3D,
            "Blizzagun Band": 0x3E,
            "Thundagun Band": 0x3F,
            "Ifrit Belt": 0x40,
            "Shiva Belt": 0x41,
            "Ramuh Belt": 0x42,
            "Moogle Badge": 0x43,
            "Cosmic Arts": 0x44,
            "Royal Crown": 0x45,
            "Prime Cap": 0x46,
            "Obsidian Ring": 0x47,
            "Unused 0x48": 0x48,
            "Unused 0x49": 0x49,
            "Unused 0x4A": 0x4A,
            "Unused 0x4B": 0x4B,
            "Unused 0x4C": 0x4C,
            "Unused 0x4D": 0x4D,
            "Unused 0x4E": 0x4E,
            "Unused 0x4F": 0x4F,
            "Unused 0x50": 0x50
        }
        self.weapon_dict = {
            "Empty": 0x00,
            "Kingdom Key": 0x51,
            "Dream Sword": 0x52,
            "Dream Shield": 0x53,
            "Dream Rod": 0x54,
            "Wooden Sword": 0x55,
            "Jungle King": 0x56,
            "Three Wishes": 0x57,
            "Fairy Harp": 0x58,
            "Pumpkinhead": 0x59,
            "Crabclaw": 0x5A,
            "Divine Rose": 0x5B,
            "Spellbinder": 0x5C,
            "Olympia": 0x5D,
            "Lionheart": 0x5E,
            "Metal Chocobo": 0x5F,
            "Oathkeeper": 0x60,
            "Oblivion": 0x61,
            "Lady Luck": 0x62,
            "Wishing Star": 0x63,
            "Ultima Weapon": 0x64,
            "Diamond Dust": 0x65,
            "One-Winged Angel": 0x66,
            "Mage's Staff": 0x67,
            "Morning Star": 0x68,
            "Shooting Star": 0x69,
            "Magus Staff": 0x6A,
            "Wisdom Staff": 0x6B,
            "Warhammer": 0x6C,
            "Silver Mallet": 0x6D,
            "Grand Mallet": 0x6E,
            "Lord Fortune": 0x6F,
            "Violetta": 0x70,
            "Dream Rod (Donald)": 0x71,
            "Save the Queen": 0x72,
            "Wizard’s Relic": 0x73,
            "Meteor Strike": 0x74,
            "Fantasista": 0x75,
            "Unused Weapon (Donald)": 0x76,
            "Knight’s Shield": 0x77,
            "Mythril Shield": 0x78,
            "Onyx Shield": 0x79,
            "Stout Shield": 0x7A,
            "Golem Shield": 0x7B,
            "Adamant Shield": 0x7C,
            "Smasher": 0x7D,
            "Gigas Fist": 0x7E,
            "Genji Shield": 0x7F,
            "Herc’s Shield": 0x80,
            "Dream Shield (Goofy)": 0x81,
            "Save the King": 0x82,
            "Defender": 0x83,
            "Mighty Shield": 0x84,
            "Seven Elements": 0x85,
            "Unused Weapon (Goofy)": 0x86,
            "Spear (Tarzan)": 0x87,
            "No Weapon (Pooh)": 0x88,
            "Sword (Aladdin)": 0x89,
            "No Weapon (Ariel)": 0x8A,
            "No Weapon (Jack)": 0x8B,
            "Dagger (Peter Pan)": 0x8C,
            "Claws (Beast)": 0x8D
        }
        self.item2_dict = {
            "Tent": 0x8E,
            "Camping Set": 0x8F,
            "Cottage": 0x90,
            "Unused 0x91": 0x91,
            "Unused 0x92": 0x92,
            "Unused 0x93": 0x93,
            "Unused 0x94": 0x94,
            "Ansem's Report 11": 0x95,
            "Ansem's Report 12": 0x96,
            "Ansem's Report 13": 0x97,
            "Power Up": 0x98,
            "Defense Up": 0x99,
            "AP Up": 0x9A,
            "Serenity Power": 0x9B,
            "Dark Matter": 0x9C,
            "Mythril Stone": 0x9D,
            "Fire Arts": 0x9E,
            "Blizzard Arts": 0x9F,
            "Thunder Arts": 0xA0,
            "Cure Arts": 0xA1,
            "Gravity Arts": 0xA2,
            "Stop Arts": 0xA3,
            "Aero Arts": 0xA4,
            "Shiitake Rank": 0xA5,
            "Matsutake Rank": 0xA6,
            "Mystery Mold": 0xA7,
            "Ansem's Report 1": 0xA8,
            "Ansem's Report 2": 0xA9,
            "Ansem's Report 3": 0xAA,
            "Ansem's Report 4": 0xAB,
            "Ansem's Report 5": 0xAC,
            "Ansem's Report 6": 0xAD,
            "Ansem's Report 7": 0xAE,
            "Ansem's Report 8": 0xAF,
            "Ansem's Report 9": 0xB0,
            "Ansem's Report 10": 0xB1,
            "Khama Vol. 8": 0xB2,
            "Salegg Vol. 6": 0xB3,
            "Azal Vol. 3": 0xB4,
            "Mava Vol. 3": 0xB5,
            "Mava Vol. 6": 0xB6,
            "Theon Vol. 6": 0xB7,
            "Nahara Vol. 5": 0xB8,
            "Hafet Vol. 4": 0xB9,
            "Empty Bottle": 0xBA,
            "Old Book": 0xBB,
            "Emblem Piece 1": 0xBC,
            "Emblem Piece 2": 0xBD,
            "Emblem Piece 3": 0xBE,
            "Emblem Piece 4": 0xBF,
            "Log": 0xC0,
            "Cloth": 0xC1,
            "Rope": 0xC2,
            "Seagull Egg": 0xC3,
            "Fish": 0xC4,
            "Mushroom": 0xC5,
            "Coconut": 0xC6,
            "Drinking Water": 0xC7,
            "Navi-G Piece 1": 0xC8,
            "Navi-G Piece 2": 0xC9,
            "Navi-Gummi 1": 0xCA,
            "Navi-G Piece 3": 0xCB,
            "Navi-G Piece 4": 0xCC,
            "Navi-Gummi 2": 0xCD,
            "Watergleam": 0xCE,
            "Naturespark": 0xCF,
            "Fireglow": 0xD0,
            "Earthshine": 0xD1,
            "Crystal Trident": 0xD2,
            "Postcard": 0xD3,
            "Torn Page 1": 0xD4,
            "Torn Page 2": 0xD5,
            "Torn Page 3": 0xD6,
            "Torn Page 4": 0xD7,
            "Torn Page 5": 0xD8,
            "Slide 1": 0xD9,
            "Slide 2": 0xDA,
            "Slide 3": 0xDB,
            "Slide 4": 0xDC,
            "Slide 5": 0xDD,
            "Slide 6": 0xDE,
            "Footprints": 0xDF,
            "Claw Marks": 0xE0,
            "Stench": 0xE1,
            "Antenna": 0xE2,
            "Forget-Me-Not": 0xE3,
            "Jack-In-The-Box": 0xE4,
            "Entry Pass": 0xE5,
            "Hero License": 0xE6,
            "Pretty Stone": 0xE7,
            "Unused 0xE8": 0xE8,
            "Lucid Shard": 0xE9,
            "Lucid Gem": 0xEA,
            "Lucid Crystal": 0xEB,
            "Spirit Shard": 0xEC,
            "Spirit Gem": 0xED,
            "Power Shard": 0xEE,
            "Power Gem": 0xEF,
            "Power Crystal": 0xF0,
            "Blaze Shard": 0xF1,
            "Blaze Gem": 0xF2,
            "Frost Shard": 0xF3,
            "Frost Gem": 0xF4,
            "Thunder Shard": 0xF5,
            "Thunder Gem": 0xF6,
            "Shiny Crystal": 0xF7,
            "Bright Shard": 0xF8,
            "Bright Gem": 0xF9,
            "Bright Crystal": 0xFA,
            "Mystery Goo": 0xFB,
            "Gale": 0xFC,
            "Mythril Shard": 0xFD,
            "Mythril": 0xFE,
            "Orichalcum": 0xFF
        }
        self.item_dict = self.item1_dict | self.accessory_dict | self.weapon_dict | self.item2_dict
        self.world_dict = {
            0x00: "Dive to the Heart",
            0x01: "Destiny Islands",
            0x02: "Disney Castle",
            0x03: "Traverse Town",
            0x04: "Wonderland",
            0x05: "Deep Jungle",
            0x06: "Hundred Acre Woods",
            #0x07: "Unused 0x07",
            0x08: "Agrabah",
            0x09: "Atlantica",
            0x0A: "Halloween Town",
            0x0B: "Olympus Coliseum",
            0x0C: "Monstro",
            0x0D: "Neverland",
            #0x0E: "Unused 0x0E",
            0x0F: "Hollow Bastion",
            0x10: "End of the World"
        }
        self.magicnames = ["Fire", "Blizzard", "Thunder", "Cure", "Gravity", "Stop", "Aero"]
        self.magicnames2 = ["Fira", "Blizzara", "Thundara", "Cura", "Gravira", "Stopra", "Aerora"]
        self.magicnames3 = ["Firaga", "Blizzaga", "Thundaga", "Curaga", "Graviga", "Stopga", "Aeroga"]
        self.heartlessnames = [
            "Soldier", "Shadow",
            "Powerwild", "Bouncywild",
            "Large Body", "Fat Bandit",
            "Sea Neon", "Sheltering Zone",
            "Bandit", "Pirate",
            "Red Nocturne", "Blue Rhapsody", "Yellow Opera", "Green Requiem",
            "Wizard", "Air Soldier",
            "Pot Spider", "Barrel Spider", "Unused 19",
            "Wight Knight", "Air Pirate", "Gargoyle", "Search Ghost",
            "Aquatank", "Screwdriver",
            "Unused 26", "Battleship",
            "Darkball", "Invisible", "Behemoth",
            "Wyvern", "Angel Star", "Defender",
            "White Mushroom", "Black Fungus", "Rare Truffle"
        ]
        self.heartless_dict = {
            "Shadow": 0x01,
            "Soldier": 0x00,
            "Large Body": 0x04,
            "Red Nocturne": 0x0A,
            "Blue Rhapsody": 0x0B,
            "Yellow Opera": 0x0C,
            "Green Requiem": 0x0D,
            "Powerwild": 0x02,
            "Bouncywild": 0x03,
            "Air Solider": 0x0F,
            "Bandit": 0x08,
            "Fat Bandit": 0x05,
            "Pot Spider": 0x10,
            "Barrel Spider": 0x11,
            "Search Ghost": 0x16,
            "Sea Neon": 0x06,
            "Sheltering Zone": 0x07,
            "Screwdriver": 0x18,
            "Aquatank": 0x17,
            "Wight Knight": 0x13,
            "Gargoyle": 0x15,
            "Pirate": 0x09,
            "Air Pirate": 0x14,
            "Battleship": 0x1A,
            "Darkball": 0x1B,
            "Defender": 0x20,
            "Wyvern": 0x1E,
            "Wizard": 0x0E,
            "Behemoth": 0x1D,
            "Invisible": 0x1C,
            "Angel Star": 0x1F,
            "White Mushroom": 0x21,
            "Black Fungus": 0x22,
            "Rare Truffle": 0x23,
            "Unused 19": 0x12,
            "Unused 26": 0x19,
        }
        self.fmheartlessnames = [
            "Soldier", "Shadow",
            "Powerwild", "Bouncywild",
            "Large Body", "Fat Bandit",
            "Sea Neon", "Sheltering Zone",
            "Bandit", "Pirate",
            "Red Nocturne", "Blue Rhapsody", "Yellow Opera", "Green Requiem",
            "Wizard", "Air Soldier",
            "Pot Spider", "Barrel Spider", "Pot Scorpion",
            "Wight Knight", "Air Pirate", "Gargoyle", "Search Ghost",
            "Aquatank", "Screwdriver",
            "Chimera", "Battleship",
            "Darkball", "Invisible", "Behemoth",
            "Wyvern", "Angel Star", "Defender",
            "White Mushroom", "Black Fungus", "Rare Truffle",
            "Unused 37", "Unused 38", "Unused 39",
            "Pink Agaricus", "Neoshadow", "Stealth Soldier", "Gigas Shadow",
            "Sniperwild", "Black Ballade",
            "Jet Balloon", "Unused 47", "Grand Ghost",
            "Destroyed Behemoth", "Arch Behemoth", "Sneak Army"
        ]
        self.heartless_fm_dict = {
            "Shadow": 0x01,
            "Gigas Shadow": 0x2A,
            "Soldier": 0x00,
            "Stealth Soldier": 0x29,
            "Large Body": 0x04,
            "Red Nocturne": 0x0A,
            "Blue Rhapsody": 0x0B,
            "Yellow Opera": 0x0C,
            "Green Requiem": 0x0D,
            "Black Ballade": 0x2C,
            "Powerwild": 0x02,
            "Bouncywild": 0x03,
            "Sniperwild": 0x2B,
            "Air Solider": 0x0F,
            "Bandit": 0x08,
            "Fat Bandit": 0x05,
            "Pot Spider": 0x10,
            "Barrel Spider": 0x11,
            "Pot Scorpion": 0x12,
            "Search Ghost": 0x16,
            "Grand Ghost": 0x2F,
            "Sea Neon": 0x06,
            "Sheltering Zone": 0x07,
            "Screwdriver": 0x18,
            "Aquatank": 0x17,
            "Wight Knight": 0x13,
            "Gargoyle": 0x15,
            "Chimera": 0x19,
            "Pirate": 0x09,
            "Air Pirate": 0x14,
            "Battleship": 0x1A,
            "Jet Balloon": 0x2D,
            "Darkball": 0x1B,
            "Defender": 0x20,
            "Wyvern": 0x1E,
            "Wizard": 0x0E,
            "Behemoth": 0x1D,
            "Destroyed Behemoth": 0x30,
            "Arch Behemoth": 0x31,
            "Invisible": 0x1C,
            "Angel Star": 0x1F,
            "Neoshadow": 0x28,
            "White Mushroom": 0x21,
            "Black Fungus": 0x22,
            "Rare Truffle": 0x23,
            "Pink Agaricus": 0x27,
            "Sneak Army": 0x32,
            "Unused 37": 0x24,
            "Unused 38": 0x25,
            "Unused 39": 0x26,
            "Unused 47": 0x2E,
        }
        self.summon_dict = {
            "Empty": 0xFF,
            "Dumbo": 0x00,
            "Bambi": 0x01,
            "Genie": 0x02,
            "Tinker Bell": 0x03,
            "Mushu": 0x04,
            "Simba": 0x05,
            "Bahamut": 0x06
        }
        # The value is the number of parts.
        self.chronicles_dict = {
            "Sora's Story": 5,
            "Wonderland": 3,
            "Olympus Coliseum": 3,
            "Deep Jungle": 3,
            "Agrabah": 3,
            "Monstro": 3,
            "Hundred Acre Woods": 2,
            "Atlantica": 3,
            "Halloween Town": 3,
            "Neverland": 3,
        }
        # Byte index * 16 + bit index
        # Characters with multiple entry flags only have 1 set at a time.
        self.journal_chars_1_dict = {
            # Page 1
            "Sora 1": 0x07,
            "Sora 2": 0x06,
            "Riku 1": 0x05,
            "Riku 2": 0x04,
            "Riku 3": 0x03,
            "Riku 4": 0x02,
            "Kairi 1": 0x01,
            "Kairi 2": 0x00,
            "Mickey Mouse": 0x17,
            "Donald Duck 1": 0x16,
            "Donald Duck 2": 0x15,
            "Goofy 1": 0x14,
            "Goofy 2": 0x13,
            "Minnie Mouse": 0x12,
            "Daisy Duck": 0x11,
            # Page 2
            "Pluto": 0x10,
            "Chip": 0x27,
            "Dale": 0x26,
            "Huey": 0x25,
            "Dewey": 0x24,
            "Louie": 0x23,
            "Merlin": 0x22,
            "Fairy Godmother": 0x21,
            # Page 3
            "Pongo": 0x20,
            "Perdita": 0x37,
            "99 Puppies": 0x36,
            "Brooms": 0x35,
            "Leon": 0x34,
            "Yuffie": 0x33,
            "Aerith": 0x32,
            "Cloud": 0x31,
            # Page 4
            "Sephiroth": 0x142,
            "Cid": 0x30,
            "Tidus": 0x47,
            "Selphie": 0x46,
            "Wakka": 0x45,
            "Moogles": 0x44,
            "Snow White": 0x42,
            "Cinderella": 0x41,
            # Page 5
            "Aurora": 0x40,
            "Bell": 0x57,
            "Beast": 0x56,
            "Maleficent 1": 0x55,
            "Maleficent 2": 0x54,
            "Maleficent 3": 0x53,
            "Dragon": 0x52,
            "Ansem 1": 0x43,
            "Ansem 2": 0x51,
            "?": 0x156,
        }
        self.journal_chars_2_dict = {
            # Page 1
            "Dumbo": 0x50,
            "Bambi": 0x67,
            "Mushu": 0x66,
            "Simba": 0x65,
            "Alice 1": 0x64,
            "Alice 2": 0x63,
            "Queen of Hearts": 0x62,
            "Cards (Hearts)": 0x61,
            "Cards (Spades)": 0x60,
            # Page 2
            "White Rabbit": 0x77,
            "Chesire Cat": 0x76,
            "Doorknob": 0x75,
            "Hercules": 0x74,
            "Philoctetes": 0x73,
            "Hades 1": 0x72,
            "Hades 2": 0x71,
            "Cerberus": 0x70,
            "Rock Titan": 0x87,
            # Page 3
            "Ice Titan": 0x141,
            "Tarzan": 0x86,
            "Jane Porter": 0x85,
            "Clayton 1": 0x84,
            "Clayton 2": 0x83,
            "Terk": 0x82,
            "Kerchak": 0x81,
            "Kala": 0x80,
            "Sabor": 0x97,
            # Page 4
            "Aladdin 1": 0x96,
            "Aladdin 2": 0x95,
            "Genie 1": 0x94,
            "Genie 2": 0x93,
            "Jasmine 1": 0x92,
            "Jasmine 2": 0x140,
            "Jafar 1": 0x91,
            "Jafar 2": 0x90,
            "Jafar-Genie": 0xA7,
            "Abu": 0xA6,
            "Iago": 0xA5,
            "Carpet": 0xA4,
            # Page 5
            "Pinocchio 1": 0xA3,
            "Pinocchio 2": 0xA2,
            "Geppetto 1": 0xA1,
            "Geppetto 2": 0xA0,
            "Jiminy Cricket": 0xB7,
            "Ariel 1": 0xB6,
            "Ariel 2": 0xB5,
            "King Triton": 0xB4,
            "Ursula 1": 0xB3,
            "Ursula 2": 0xB2,
            "Sebastian": 0xB1,
            "Flounder": 0xB0,
            # Page 6
            "Jetsam": 0xC7,
            "Flotsam": 0xC6,
            "Jack Skellington": 0xC5,
            "Sally": 0xC4,
            "Oogie Boogie 1": 0xC3,
            "Oogie Boogie 2": 0xC2,
            "Dr. Finkelstein": 0xC1,
            "Zero": 0xC0,
            "Lock": 0xD7,
            # Page 7
            "Shock": 0xD6,
            "Barrel": 0xD5,
            "The Mayor": 0xD4,
            "Peter Pan": 0xD3,
            "Tinker Bell 1": 0xD2,
            "Tinker Bell 2": 0xD1,
            "Wendy": 0xD0,
            "Captain Hook 1": 0xE7,
            "Captain Hook 2": 0xE6,
            "Mr. Smee": 0xE5,
            # Page 8
            "The Crocodile": 0xE4,
            "Winnie the Pooh": 0xE3,
            "Piglet": 0xE2,
            "Tigger": 0xE1,
            "Owl": 0xE0,
            "Rabbit": 0xF7,
            "Eeyore": 0xF6,
            "Roo": 0xF5,
        }
        self.journal_boss_dict = {
            "Darkside": 0x132,
            "Guard Armor": 0x131,
            "Red Armor": 0x161,
            "Opposite Armor": 0x130,
            "Trickmaster": 0x147,
            "Stealth Sneak": 0x146,
            "Pot Centipede": 0x145,
            "Parasite Cage": 0x144,
            "Kurt Zisa": 0x157,
            "Phantom": 0x143,
        }
    
    def trinity_dicts(self):
        self.trinity_names = [
            "Trinity Jump",
            "Trinity Charge",
            "Trinity Ladder",
            "Trinity Push",
            "Trinity Detect",
        ]
        self.trinity_dict_list = [
            {
                "Traverse Town: 1st District: At the World Exit": 0x06,
                "Traverse Town: 1st District: On the balcony": 0x05,
                "Traverse Town: Magician's Study": 0x450,
                "Traverse Town: 3rd District": 0x473,
                "Wonderland: Lotus Forest: 1": 0x25,
                "Wonderland: Lotus Forest: 2": 0x26,
                "Olympus Coliseum: Coliseum Gates: 1": 0x45,
                "Olympus Coliseum: Coliseum Gates: 2": 0x46,
                "Deep Jungle: Climbing Trees": 0x64,
                "Deep Jungle: Camp": 0x65,
                "Agrabah: Bazaar": 0x86,
                "Agrabah: Silent Chamber": 0x82,
                "Monstro: Chamber 5": 0xA3,
                "Monstro: Throat": 0xA4,
                "Monstro: Mouth": 0xA5,
                "Hollow Bastion: Dungeon": 0xF5,
                "Hollow Bastion: Great Crest": 0xF6,
            },
            {
                "Traverse Town: 1st District": 0x447,
                "Traverse Town: 2nd District": 0x454,
                "Traverse Town: Alleyway": 0x455,
                "Agrabah: Treasure Room": 0x83,
                "Halloween Town: Oogie's Manor": 0xC6,
                "Hollow Bastion: Entrance Hall": 0x107,
            },
            {
                "Traverse Town: Accessory Shop": 0x463,
                "Wonderland: Bizarre Room": 0x23,
                "Wonderland: Rabbit Hole": 0x24,
                "Olympus Coliseum: Coliseum Gates": 0x43,
                "Deep Jungle: Treetop": 0x63,
                "Agrabah: Agrabah: Storage": 0x85,
                "Monstro: Mouth": 0xA6,
                "Neverland: Ship: Cabin": 0xE0,
                "Hollow Bastion: Library": 0x106,
            },
            {
                "Traverse Town: Mystical House": 0x16,
                # Has special treatment since its out of bounds.
                "Olympus Coliseum: Coliseum: Lobby": 0x1A40,
                "Agrabah: Cave: Hall": 0x84,
                "Neverland: Ship: Hold": 0xE1,
            },
            {},
        ]
    
    def gummi_dicts(self):
        self.gummi_block_cockpit_dict = {
            "Cure-G": 0x00,
            "Curaga-G": 0x01,
            "Life-G": 0x02,
            "Full-Life-G": 0x03,
        }
        self.gummi_block_engine_dict = {
            "Fire-G": 0x04,
            "Fira-G": 0x05,
            "Firaga-G": 0x06,
            "Flare-G": 0x07,
            "Holy-G": 0x08,
        }
        self.gummi_block_armor_dict = {
            "Protect-G 1": 0x09,
            "Protect-G 2": 0x0A,
            "Protect-G 3": 0x0B,
            "Protect-G 4": 0x0C,
            "Protect-G 5": 0x0D,
            "Protect-G 6": 0x0E,
            "Protect-G 7": 0x0F,
            "Protect-G 8": 0x10,
            "Shell-G 1": 0x11,
            "Shell-G 2": 0x12,
            "Shell-G 3": 0x13,
            "Shell-G 4": 0x14,
            "Shell-G 5": 0x15,
            "Shell-G 6": 0x16,
            "Shell-G 7": 0x17,
            "Shell-G 8": 0x18,
            "Dispel-G 1": 0x19,
            "Dispel-G 2": 0x1A,
            "Dispel-G 3": 0x1B,
            "Dispel-G 4": 0x1C,
            "Dispel-G 5": 0x1D,
            "Dispel-G 6": 0x1E,
            "Dispel-G 7": 0x1F,
            "Dispel-G 8": 0x20,
        }
        self.gummi_block_wing_dict = {
            "Aerora-G 1": 0x21,
            "Aerora-G 2": 0x22,
            "Aeroga-G 1": 0x23,
            "Aeroga-G 2": 0x24,
            "Tornado-G 1": 0x25,
            "Tornado-G 2": 0x26,
            "Float-G 1": 0x27,
            "Float-G 2": 0x28,
            "Aero-G 1": 0x29,
            "Aero-G 2": 0x2A,
            "Aero-G 3": 0x2B,
        }
        self.gummi_block_special_dict = {
            "Drain-G 1": 0x2C,
            "Drain-G 2": 0x2D,
            "Osmose-G 1": 0x2E,
            "Osmose-G 2": 0x2F,
            "Transform-G": 0x30,
            "Warp-G": 0x31,
            "Scan-G 1": 0x32,
            "Scan-G 2": 0x33,
            "Haste-G": 0x34,
            "Haste2-G": 0x35,
            "Shield-G": 0x36,
            "Shield2-G": 0x37,
            "Esuna-G 1": 0x38,
            "Esuna-G 2": 0x39,
        }
        self.gummi_block_weapon_dict = {
            "Thunder-G": 0x3A,
            "Thundara-G": 0x3B,
            "Thundaga-G": 0x3C,
            "Comet-G": 0x3D,
            "Meteor-G": 0x3E,
            "Ultima-G": 0x3F,
        }
        self.gummi_block_upgrade_dict = {
            "Spray": 0x40,
            "Palette": 0x41,
            "SYS.UP1": 0x42,
            "SYS.UP2": 0x43,
            "COM.LV1": 0x44,
            "COM.LV2": 0x45,
            "COM.LV3": 0x46,
        }
        self.gummi_blueprint_dict = {
            "Kingdom": 0x47,
            "Hyperion": 0x48,
            "Geppetto": 0x49,
            "Cid": 0x4A,
            "Leon": 0x4B,
            "Yuffie": 0x4C,
            "Aerith": 0x4D,
            "Cactuar": 0x4E,
            "Chocobo": 0x4F,
            "Cindy": 0x50,
            "Shiva": 0x51,
            "Lamia": 0x52,
            "Sandy": 0x53,
            "Sylph": 0x54,
            "Carbuncle": 0x55,
            "Mindy": 0x56,
            "Goblin": 0x57,
            "Bomb": 0x58,
            "Remora": 0x59,
            "Ahriman": 0x5A,
            "Imp": 0x5B,
            "Siren": 0x5C,
            "Stingray": 0x5D,
            "Catoblepas": 0x5E,
            "Adamant": 0x5F,
            "Serpent": 0x60,
            "Ifrit": 0x61,
            "Odin": 0x62,
            "Atomos": 0x63,
            "Golem": 0x64,
            "Diablos": 0x65,
            "Deathguise": 0x66,
            "Typhoon": 0x67,
            "Alexander": 0x68,
            "Leviathan": 0x69,
            "Ramuh": 0x6A,
            "Omega": 0x6B,
        }
        self.gummi_blueprint_fm_dict = {
            "Moogle": 0x6C,
            "Valefor": 0x6D,
            "Pupu": 0x6E,
            "Cerberus": 0x6F,
            "Tonberry": 0x70,
            "Pandaemonium": 0x71,
            "Ixion": 0x72,
            "Gilgamesh": 0x73,
            "Phoenix": 0x74,
            "Eden": 0x75,
            "Bahamut": 0x76,
        }
        self.gummi_block_design_dict = {
            "Wheel-G": 0x80,
            "Fang-G": 0x81,
            "Horn-G": 0x82,
            "Angel-G": 0x83,
            "Dark-G": 0x84,
            "Shoes-G": 0x85,
            "Rock-G 1": 0x86,
            "Rock-G 2": 0x87,
            "Scissors-G 1": 0x88,
            "Scissors-G 2": 0x89,
            "Paper-G 1": 0x8A,
            "Paper-G 2": 0x8B,
            "Crown-G": 0x8C,
            "Drill-G": 0x8D,
            "Caterpillar-G 1": 0x8E,
            "Caterpillar-G 2": 0x8F,
        }
        self.gummi_max_list = [
            # Cockpits
            1, 1,
            1, 1,
            # Engines
            6, 6, 4,
            4, 2,
            # Armors
            99, 99, 99, 30, 30, 10, 10, 10,
            99, 99, 99, 20, 20, 8, 8, 8,
            99, 99, 99, 10, 10, 6, 6, 6,
            # Wings
            30, 30,
            20, 20,
            10, 10,
            10, 10,
            99, 99, 99,
            # Specials
            4, 4,
            2, 2,
            1, 1,
            2, 2,
            2, 2,
            1, 1,
            6, 10,
            # Weapons
            10, 8, 6,
            8, 6, 4,
            # Upgrades
            1, 1,
            1, 1,
            1, 1, 1,
            # All blueprints have 1 max.
        ]
