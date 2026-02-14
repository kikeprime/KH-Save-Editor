import os
import struct

from ctypes import *
from .kh1_dicts import dicts


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
        self.submp = c_ushort(int.from_bytes(data[0x38:0x3A:-1])) # 30 or 0x1E means 1 MP
        # data[0x3A:0x3C] is unknown
        self.exp = c_uint(int.from_bytes(data[0x3C:0x40:-1]))
        self.abilities = (c_ubyte*48)(*data[0x40:0x70]) # Pooh has unknown data here with invalid ability IDs.
        self.magic = c_ubyte(data[0x70])
        # data[0x71:0x74] is unknown


class KH1GummiBlock:
    def __init__(self, data):
        pass


class KH1GummiShip:
    def __init__(self, data):
        self.blockcount = c_ushort(int.from_bytes(data[0x00:0x02:-1]))
        self.x = c_ushort(int.from_bytes(data[0x02:0x04:-1]))
        self.y = c_ushort(int.from_bytes(data[0x04:0x06:-1]))
        self.z = c_ushort(int.from_bytes(data[0x06:0x08:-1]))
        self.transformpair = c_ushort(int.from_bytes(data[0x08:0x0A:-1]))
        self.name = bytearray(data[0x4C:0x56])


class KH1:
    def __init__(self, slot=0, fm=False):
        dicts(self)
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
                self.playtime = c_uint(int.from_bytes(self.sysdata[0x10:0x14:-1]))

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
        self.cure_on_friends = c_ushort(int.from_bytes(data[0x0836:0x0838:-1]))
        # data[0x0838:0x083E] is unknown.
        self.heartless_killed = c_ushort(int.from_bytes(data[0x083E:0x0840:-1]))
        # data[0x0840:0x0844] is unknown.
        self.deflected = c_ushort(int.from_bytes(data[0x0844:0x0846:-1]))
        # data[0x0846:0x0848] is unknown.
        self.item_usage = c_ushort(int.from_bytes(data[0x0848:0x084A:-1]))
        self.hits = c_ushort(int.from_bytes(data[0x084A:0x084C:-1]))
        self.friend_ko = c_ushort(int.from_bytes(data[0x084C:0x084E:-1]))
        self.deaths = c_ushort(int.from_bytes(data[0x084E:0x0850:-1]))

        self.currentcup = c_ubyte(data[0x0F26])
        self.philcup = c_ubyte(data[0x0F36])
        self.pegasuscup = c_ubyte(data[0x0F37])
        self.herculescup = c_ubyte(data[0x0F38])
        self.hadescup = c_ubyte(data[0x0F39])
        self.platinummatch = c_ubyte(data[0x0F6A])

        self.tiduswins = c_ubyte(data[0x101B])
        self.wakkawins = c_ubyte(data[0x101C])
        self.selphiewins = c_ubyte(data[0x101D])

        self.sorawins = c_ushort(int.from_bytes(data[0x1036:0x1038:-1]))
        self.rikuwins = c_ushort(int.from_bytes(data[0x1038:0x103A:-1]))

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
        
        self.world = c_uint(int.from_bytes(data[0x2040:0x2044:-1]))
        self.room = c_uint(int.from_bytes(data[0x2044:0x2048:-1]))
        self.flag = c_uint(int.from_bytes(data[0x2048:0x204C:-1]))

        self.GUMI = bytearray(data[0x2400:0x2404]).decode() # ASCII string "GUMI"
        # data[0x2404] seems to be a version code, 0 for vanilla and 1 for FM, needs further investigation.
        self.gummi_tutorial = c_ubyte(data[0x2405]) # might be an int # reseting wipes gummi data
        # data[0x2409:0x2410] is [1, 2, 3, 4, 5, 6, 7] for me
        self.selectedship = c_ubyte(data[0x2410])
        # self.gummiships = data[0x241C:0xBE7C], based on the start offsets of each ship
        # which I've confirmed but the last ship overlaps with the 1st 4 blocks which are also confirmed.
        self.gummiships = [KH1GummiShip(data[0x241C+i*0x0F70:0x241C+(i+1)*0x0F70]) for i in range(10)]
        self.gummiblocks = (c_ubyte*108)(*data[0xBE78:0xBEE4])

        self.gummi_decelerate = c_uint(int.from_bytes(data[0xBF01:0xBF05:-1]))
        self.gummi_accelerate = c_uint(int.from_bytes(data[0xBF05:0xBF09:-1]))
        self.gummi_transform = c_uint(int.from_bytes(data[0xBF09:0xBF0D:-1]))
        self.gummi_scannon = c_uint(int.from_bytes(data[0xBF0D:0xBF11:-1]))
        self.gummi_mcannon = c_uint(int.from_bytes(data[0xBF11:0xBF15:-1]))
        self.gummi_lcannon = c_uint(int.from_bytes(data[0xBF15:0xBF19:-1]))
        self.gummi_slaser = c_uint(int.from_bytes(data[0xBF19:0xBF1D:-1]))
        self.gummi_mlaser = c_uint(int.from_bytes(data[0xBF1D:0xBF21:-1]))
        self.gummi_llaser = c_uint(int.from_bytes(data[0xBF21:0xBF25:-1]))
        
        self.autolock = c_uint(int.from_bytes(data[0x16400:0x16404:-1]))
        self.targetlock = c_uint(int.from_bytes(data[0x16404:0x16408:-1]))
        self.camera = c_uint(int.from_bytes(data[0x16408:0x1640C:-1]))
        # data[0x1640C:0x16410] is unknown
        self.vibration = c_uint(int.from_bytes(data[0x16410:0x16414:-1]))
        self.sound = c_uint(int.from_bytes(data[0x16414:0x16418:-1]))
        self.datainstall = c_uint(int.from_bytes(data[0x16418:0x1641C:-1])) # JP/FM
        self.difficulty = c_uint(int.from_bytes(data[0x16418:0x1641C:-1])) # USA/EU
        
        self.munny = c_uint(int.from_bytes(data[0x1641C:0x16420:-1]))

        # Final Mix stuff
        if self.fm:
            self.heartless = (c_ushort*51)(*struct.unpack("<51H", bytearray(data[0x07D8:0x083E])))
            self.shortcuts = (c_ubyte*3)(*data[0x0844:0x0847])
            self.cure_on_friends = c_ushort(int.from_bytes(data[0x084E:0x0850:-1]))
            self.heartless_killed = c_ushort(int.from_bytes(data[0x0856:0x0858:-1]))
            self.deflected = c_ushort(int.from_bytes(data[0x085C:0x085E:-1]))
            self.item_usage = c_ushort(int.from_bytes(data[0x0860:0x0862:-1]))
            self.hits = c_ushort(int.from_bytes(data[0x0862:0x0864:-1]))
            self.friend_ko = c_ushort(int.from_bytes(data[0x0864:0x0868:-1]))
            self.deaths = c_ushort(int.from_bytes(data[0x0868:0x086A:-1]))
            self.xemnas = c_ubyte(data[0x1118])
            self.gummiblocks = (c_ubyte*160)(*data[0xBE78:0xBF18]) # 144 bytes until last Design Gummi
            self.gummi_decelerate = c_uint(int.from_bytes(data[0xBF41:0xBF45:-1]))
            self.gummi_accelerate = c_uint(int.from_bytes(data[0xBF45:0xBF49:-1]))
            self.gummi_transform = c_uint(int.from_bytes(data[0xBF49:0xBF4D:-1]))
            self.gummi_scannon = c_uint(int.from_bytes(data[0xBF4D:0xBF51:-1]))
            self.gummi_mcannon = c_uint(int.from_bytes(data[0xBF51:0xBF55:-1]))
            self.gummi_lcannon = c_uint(int.from_bytes(data[0xBF55:0xBF59:-1]))
            self.gummi_slaser = c_uint(int.from_bytes(data[0xBF59:0xBF5D:-1]))
            self.gummi_mlaser = c_uint(int.from_bytes(data[0xBF5D:0xBF61:-1]))
            self.gummi_llaser = c_uint(int.from_bytes(data[0xBF61:0xBF65:-1]))
            self.difficulty = c_uint(int.from_bytes(data[0x1642C:0x16430:-1]))

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
