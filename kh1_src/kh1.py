import os
import struct

from ctypes import *
from .datatypes import *
from .kh1_dicts import dicts
from .pcsx2 import PCSX2


class KH1Character:
    """
    Class for representing the character struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0x74 bytes long.
    """
    def __init__(self, name, offset, data):
        self.name = name
        self.offset = offset
        self.data = data
        self.level = U8(offset+0x00, data)
        self.hp = U8(offset+0x01, data)
        self.maxhp = U8(offset+0x02, data)
        self.mp = U8(offset+0x03, data)
        self.maxmp = U8(offset+0x04, data)
        self.maxap = U8(offset+0x05, data)
        self.strength = U8(offset+0x06, data)
        self.defense = U8(offset+0x07, data)
        self.resistances = Array(U8, 0x10, offset+0x08, data)
        self.accessoryslots = U8(offset+0x18, data)
        self.accessories = Array(U8, 0x08, offset+0x19, data)
        self.itemslots = U8(offset+0x21, data)
        self.items = Array(U8, 0x08, offset+0x22, data)
        # data[0x2A:0x32] is unknown
        self.weapon = U8(offset+0x32, data)
        # data[0x33:0x38] is unknown
        self.submp = U16(offset+0x38, data)
        # data[0x3A:0x3C] is unknown
        self.exp = U32(offset+0x3C, data)
        self.abilities = Array(U8, 0x30, offset+0x40, data)
        self.magic = U8(offset+0x70, data)
        # data[0x71:0x74] is unknown


class KH1GummiBlock:
    """
    Class for representing the Gummi Blocks of Gummi Ships.
    The structure is 0x0C bytes long.
    """
    def __init__(self, offset, data):
        self.offset = offset
        self.data = data
        self.xz = U8(offset+0x00, data)
        self._y = U8(offset+0x01, data)
        self.r = U16(offset+0x02, data)
        self.id = U8(offset+0x04, data)
        self.color = U8(offset+0x08, data)

    @property
    def x(self):
        return self.xz.value % 16
    
    @x.setter
    def x(self, value):
        self.xz.value = self.z * 16 + value

    @property
    def y(self):
        return self._y.value
    
    @y.setter
    def y(self, value):
        self._y.value = value
    
    @property
    def z(self):
        return self.xz.value // 16
    
    @z.setter
    def z(self, value):
        self.xz.value = value * 16 + self.x
    
    colors = [
        "white", "yellow", "orange", "red", "purple", "blue", "lightblue", "green",
        "white", "yellow", "orange", "red", "purple", "blue", "lightblue", "green",
        "white", "yellow", "orange", "red", "purple", "blue", "lightblue", "green",
        "white", "yellow", "orange", "red", "purple", "blue", "lightblue", "green",
        "white", "yellow", "orange", "red", "purple", "blue", "lightblue", "green",
        "white", "yellow", "orange", "red", "purple", "blue", "lightblue", "green",
        "white", "yellow", "orange", "red", "purple", "blue", "lightblue", "green",
        "black", "yellow", "orange", "red", "purple", "blue", "lightblue", "green",
    ]
    
    def __repr__(self):
        dicts(self)
        return f"{self.gummi_block_dict[self.id.value]}(X={self.x}, Y={self.y}, Z={self.z}, R={self.r.value:04X}, C={self.color.value})"


class KH1GummiShip:
    """
    Class for representing the Gummi Ships.
    The structure is 0x0F70 bytes long.
    """
    def __init__(self, offset, data):
        self.offset = offset
        self.data = data
        self.blockcount = U16(offset+0x00, data)
        self.x = U16(offset+0x02, data)
        self.y = U16(offset+0x04, data)
        self.z = U16(offset+0x06, data)
        self.transformpair = U16(offset+0x08, data)
        self.name = bytearray(data[offset+0x4C:offset+0x56])
        blocks = data[offset+0x6C:offset+0x09CC]
        self.blocks = [KH1GummiBlock(offset+0x6C+i*0x0C, data) for i in range(200)]
    
    def save(self):
        self.data[self.offset+0x4C:self.offset+0x56] = self.name


class KH1GummiMission:
    def __init__(self, offset, data):
        self.offset = offset
        self.data = data
        self.enemies = U32(offset+0x00, data)
        self.obstacles = U32(offset+0x04, data)
        self.power = U32(offset+0x08, data)
        self.armor = U32(offset+0x0C, data)
        self.shields = U32(offset+0x10, data)
        self.special = U32(offset+0x14, data)
        self.blocks = U32(offset+0x18, data)
        self.blueprints = U32(offset+0x1C, data)
        self.world = U32(offset+0x20, data)


class KH1:
    def __init__(self, slot=0, fm=False, attach=False):
        dicts(self)
        self.fm = fm
        if self.fm:
            self.filename = "BISLPS-25198-" + f"{slot:02d}"
        else:
            self.filename = "BASLUS-20370-" + f"{slot:02d}"
        if slot != 0:
            if os.path.exists(os.path.join("files", "kh1", self.filename, self.filename)):
                with open(os.path.join("files", "kh1", self.filename, self.filename), "rb") as file:
                    self.data = (c_ubyte*0x16C00)(*file.read())
            else:
                with open("files/kh1/" + self.filename, "rb") as file:
                    self.data = (c_ubyte*0x16C00)(*file.read())
            self.__parse_data()
            self.sysdata = None
            if os.path.exists(os.path.join("files", "kh1", self.filename, "system.bin")):
                with open(os.path.join("files", "kh1", self.filename, "system.bin"), "rb") as sysfile:
                    self.sysdata = (c_ubyte*0x400)(*sysfile.read())
                self.level_sys = U32(0x08, self.sysdata)
                self.munny_sys = U32(0x0C, self.sysdata)
                # Playtime in seconds * 60 but possibly in seconds * 50 in PAL versions
                self.playtime = U32(0x10, self.sysdata)
                self.difficulty_sys = U32(0x14, self.sysdata)
                if self.fm:
                    self.difficulty_sys = U32(0x38, self.sysdata)
        if attach:
            self.sysdata = None
            self.addr = 0x3F8380 if self.fm else 0x3F1C90
            self.pcsx2 = PCSX2(self.addr, 0x16C00, self)
            self.__parse_data()

    def __parse_data(self):
        # For FM the currently loaded save file starts at 0x3F8380 in the memory according to the RetroAchievements code notes.
        # For vanilla USA it starts at 0x3F1C90.
        # For vanilla JP it starts at 0x3F2080.
        self.header = U32(0x00, self.data) # 4 in vanilla, 5 in FM
        # self.characters = data[0x04:0x048C]
        self.sora = KH1Character("Sora", 0x04, self.data)
        self.donald = KH1Character("Donald", 0x04+0x74, self.data)
        self.goofy = KH1Character("Goofy", 0x04+2*0x74, self.data)
        self.tarzan = KH1Character("Tarzan", 0x04+3*0x74, self.data)
        self.pooh = KH1Character("Winnie the Pooh", 0x04+4*0x74, self.data)
        self.aladdin = KH1Character("Aladdin", 0x04+5*0x74, self.data)
        self.ariel = KH1Character("Ariel", 0x04+6*0x74, self.data)
        self.jack = KH1Character("Jack Skellington", 0x04+7*0x74, self.data)
        self.peterpan = KH1Character("Peter Pan", 0x04+8*0x74, self.data)
        self.beast = KH1Character("Beast", 0x04+9*0x74, self.data)
        self.characters = [
            self.sora, self.donald, self.goofy,
            self.tarzan, self.pooh, self.aladdin,
            self.ariel, self.jack, self.peterpan,
            self.beast
        ]
        self.path = U8(0x048C, self.data)
        self.curve = U8(0x048D, self.data)
        self.party = Array(U8, 4, 0x048E, self.data)
        self.magiclevels = Array(U8, 7, 0x0492, self.data)
        # data[0x0499] is unknown
        # I gave it to inventory so the array and item indices match
        self.inventory = Array(U8, 0x100, 0x0499, self.data)
        self.shared_abilities = Array(U8, 0x30, 0x0599, self.data)
        # data[0x05C9:0x05CC] is unknown.
        self.di_chest_flag = U8(0x05CC, self.data)
        self.treasures = Array(U8, 0x01FD, 0x05CC, self.data)
        self.summons = Array(U8, 7, 0x07D0, self.data)
        # data[0x07D7] is unknown.
        self.heartless = Array(U16, 36, 0x07D8, self.data)
        # data[0x0820:0x082C] is unknown.
        self.shortcuts = Array(U8, 3, 0x082C, self.data)
        # data[0x082F:0x0836] is unknown.
        self.cure_on_friends = U16(0x0836, self.data)
        # data[0x0838:0x083E] is unknown.
        self.heartless_killed = U16(0x083E, self.data)
        # data[0x0840:0x0844] is unknown.
        self.deflected = U16(0x0844, self.data)
        self.taken_damage = U16(0x0846, self.data)
        self.item_usage = U16(0x0848, self.data)
        self.hits = U16(0x084A, self.data)
        self.friend_ko = U16(0x084C, self.data)
        self.deaths = U16(0x084E, self.data)
        # data[0x0850:0x0856] is unknown.
        self.weapon_usage = U16(0x0856, self.data)

        self.dalmatian_event = U8(0x0E3A, self.data)
        self.dalmatian_gifts = Array(U8, 10, 0x0E3C, self.data)
        # data[0x0E46] is unknown.
        self.dalmatian_gift_ready = U8(0x0E47, self.data)

        self.currentcup = U8(0x0F26, self.data)
        self.philcup = U8(0x0F36, self.data)
        self.pegasuscup = U8(0x0F37, self.data)
        self.herculescup = U8(0x0F38, self.data)
        self.hadescup = U8(0x0F39, self.data)
        # oc_minigames[0x10:0x14] and oc_minigames[0x1C:0x20] aren't used for minigame times
        self.oc_minigames = Array(S32, 0x18, 0x0F4C, self.data)
        # oc_minigames[0x1D:0x1F] anyway
        self.goldmatch = U8(0x0F69, self.data)
        self.platinummatch = U8(0x0F6A, self.data)
        
        self.tiduswins = U8(0x101B, self.data)
        self.wakkawins = U8(0x101C, self.data)
        self.selphiewins = U8(0x101D, self.data)
        
        self.sorawins = U16(0x1036, self.data)
        self.rikuwins = U16(0x1038, self.data)
        self.tidus_event = U8(0x103A, self.data)
        self.wakka_event = U8(0x103B, self.data)
        self.selphie_event = U8(0x103C, self.data)
        
        self.tidus_beaten = U8(0x105F, self.data)
        self.wakka_beaten = U8(0x1060, self.data)
        self.selphie_beaten = U8(0x1061, self.data)
        
        self.weapon_backup = U8(0x1114, self.data)
        
        self.slides = Array(U8, 6, 0x1207, self.data)
        self.slides_watched = U8(0x1212, self.data)

        self.world_progresses = Array(U8, 20, 0x1500, self.data)
        
        self.raft = bytearray(self.data[0x16D1:0x16DB])
        
        # Entries existing since vanilla JP use data[0x16E3:0x16F3]
        # Sephiroth, Ice Titan, Jasmine 2 use 0x16F7
        # Kurt Zisa, Xemnas use 0x16F8, Red Armor uses 0x16F9
        self.journal_chars = Array(U8, 23, 0x16E3, self.data)
        # self.boss_journal = (c_ubyte*4)(*data[0x16F6:0x16FA])
        # data[0x16FA:0x1703] is unknown
        self.dalmatians = Array(U8, 13, 0x1703, self.data)
        # needs to be signed because no record is -1
        self.minigames = Array(S32, 0x46, 0x1728, self.data)
        self.chronicles = Array(U32, 10, 0x1997, self.data)
        self.reports = Array(U8, 2, 0x19C0, self.data)
        self.journal_unlock = U8(0x19C4, self.data) # bit index 3, 0x1F for completed game so needs further investigation
        self.synth_flags = Array(U8, 5, 0x19C8, self.data)
        
        self.trinity_unlock = U8(0x1C1B, self.data)
        self.trinity_count = Array(U8, 6, 0x1C66, self.data) # Jump, Unused, Charge, Ladder, Push, Detect
        # The Trinity flags spread across these.
        # The OC Lobby Push isn't here but at 0x1E10 bit index 0.
        self.trinity_flags = Array(U8, 0x48, 0x1C6C, self.data)
        
        self.clams = Array(U8, 2, 0x1DA9, self.data)
        self.large_chest_state = U8(0x1DAB, self.data)
        
        self.bigben = Array(U8, 2, 0x1E61, self.data) # Neverland Aero Upgrade Chest flag is here
        
        self.world_statuses = Array(U8, 15, 0x1EF0, self.data)
        self.landingpoints = Array(U8, 15, 0x1EFF, self.data)
        
        self.world = U32(0x2040, self.data)
        self.room = U32(0x2044, self.data)
        self.flag = U32(0x2048, self.data)

        self.GUMI = bytearray(self.data[0x2400:0x2404]).decode() # ASCII string "GUMI"
        # data[0x2404] seems to be a version code, 0 for vanilla and 1 for FM, needs further investigation.
        self.gummi_tutorial = U8(0x2405, self.data)
        # data[0x2409:0x2410] is [1, 2, 3, 4, 5, 6, 7] for me
        self.selectedship = U8(0x2410, self.data)
        # self.gummiships = data[0x241C:0xBE7C], based on the start offsets of each ship
        # which I've confirmed but the last ship overlaps with the 1st 4 blocks which are also confirmed.
        self.gummiships = [KH1GummiShip(0x241C+i*0x0F70, self.data) for i in range(10)]
        self.gummiblocks = Array(U8, 108, 0xBE78, self.data)

        self.gummi_decelerate = U32(0xBF01, self.data)
        self.gummi_accelerate = U32(0xBF05, self.data)
        self.gummi_transform = U32(0xBF09, self.data)
        self.gummi_scannon = U32(0xBF0D, self.data)
        self.gummi_mcannon = U32(0xBF11, self.data)
        self.gummi_lcannon = U32(0xBF15, self.data)
        self.gummi_slaser = U32(0xBF19, self.data)
        self.gummi_mlaser = U32(0xBF1D, self.data)
        self.gummi_llaser = U32(0xBF21, self.data)
        
        self.autolock = U32(0x16400, self.data)
        self.targetlock = U32(0x16404, self.data)
        self.camera = U32(0x16408, self.data)
        # data[0x1640C:0x16410] is unknown
        self.vibration = U32(0x16410, self.data)
        self.sound = U32(0x16414, self.data)
        self.datainstall = U32(0x16418, self.data) # JP/FM
        self.difficulty = U32(0x16418, self.data) # USA/EU
        self.munny = U32(0x1641C, self.data)
        # 4 bytes for each party member; I've found the rule so I'll update the dicts later
        self.customize = self.data[0x16804:0x16828]

        # Final Mix stuff
        if self.fm:
            self.heartless = Array(U16, 51, 0x07D8, self.data)
            self.shortcuts = Array(U8, 3, 0x0844, self.data)
            self.cure_on_friends = U16(0x084E, self.data)
            self.heartless_killed = U16(0x0856, self.data)
            self.deflected = U16(0x085C, self.data)
            self.taken_damage = U16(0x085E, self.data)
            self.item_usage = U16(0x0860, self.data)
            self.hits = U16(0x0862, self.data)
            self.friend_ko = U16(0x0864, self.data)
            self.deaths = U16(0x0866, self.data)
            self.weapon_usage = U16(0x086E, self.data)
            self.xemnas = U8(0x1118, self.data)
            self.gummiblocks = Array(U8, 160, 0xBE78, self.data) # 144 bytes until the last Design Gummi
            self.gummi_decelerate = U32(0xBF41, self.data)
            self.gummi_accelerate = U32(0xBF45, self.data)
            self.gummi_transform = U32(0xBF49, self.data)
            self.gummi_scannon = U32(0xBF4D, self.data)
            self.gummi_mcannon = U32(0xBF51, self.data)
            self.gummi_lcannon = U32(0xBF55, self.data)
            self.gummi_slaser = U32(0xBF59, self.data)
            self.gummi_mlaser = U32(0xBF5D, self.data)
            self.gummi_llaser = U32(0xBF61, self.data)
            gummi_missions = self.data[0xC0E0:0xCC60]
            self.gummi_missions = [KH1GummiMission(0xC0E0+i*16*4, self.data) for i in range(46)]
            self.difficulty = U32(0x1642C, self.data)
            self.journal_complete = U8(0x16474, self.data)
    
    def __save_shared(self):
        self.data[0x16D1:0x16DB] = self.raft
        for gummiship in self.gummiships:
            gummiship.save()
        # self.data[0x16804:0x16828] = bytearray(self.customize)

    def __save_vanilla(self):
        pass

    def __save_fm(self):
        pass

    def save(self):
        self.__save_shared()
        if self.fm:
            self.__save_fm()
        else:
            self.__save_vanilla()
        
        os.makedirs("saved/kh1/" + self.filename, exist_ok=True)
        with open(os.path.join("saved", "kh1", self.filename, self.filename), "wb") as file:
            file.write(self.data)
        if self.sysdata is not None:
            with open(os.path.join("saved", "kh1", self.filename, "system.bin"), "wb") as sysfile:
                sysfile.write(self.sysdata)
        if hasattr(self, "pcsx2"):
            self.pcsx2.dump_to_emu()
