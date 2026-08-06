import os
import struct

from ctypes import *
from .kh2_dicts import *
from .kh2_helper import *
from kh1_src.datatypes import *
from kh1_src.pcsx2 import PCSX2


class KH2:
    def __init__(self, slot=0, version=1, attach=False):
        dicts(self)
        if slot == 0:
            slot = 100
        self.version = version
        if self.version == 0:
            self.filename = "BISLPM-66233-" + f"{slot-1:02d}"
            self.filesize = 0xB830
        elif self.version == 1:
            self.filename = "BASLUS-21005-" + f"{slot-1:02d}"
            self.filesize = 0xB4E0
        elif self.version == 2:
            self.filename = "BISLPM-66675FM-" + f"{slot-1:02d}"
            self.filesize = 0x10FC0
        if slot != 100:
            if os.path.exists(os.path.join("files", "kh2", self.filename, self.filename)):
                with open(os.path.join("files", "kh2", self.filename, self.filename), "rb") as file:
                    self.data = (c_ubyte*self.filesize)(*file.read())
            else:
                with open("files/kh2/" + self.filename, "rb") as file:
                    self.data = (c_ubyte*self.filesize)(*file.read())
            self.__parse_data(self.data)
            self.sysdata = None
            if os.path.exists(os.path.join("files", "kh2", self.filename[:-2]+"SYS", self.filename[:-2]+"SYS")):
                with open(os.path.join("files", "kh2", self.filename[:-2]+"SYS", self.filename[:-2]+"SYS"), "rb") as sysfile:
                    self.sysdata = (c_ubyte*0x400)(*sysfile.read())
        if attach:
            if self.version == 0:
                self.addr = 0x33DCE0
            elif self.version == 1:
                self.addr = 0x33E860
            elif self.version == 2:
                self.addr = 0x32BB30
            self.sysdata = None
            self.pcsx2 = PCSX2(self.addr, self.filesize, self)
            self.__parse_data(self.data)

    def __parse_data(self, data):
        # For FM the currently loaded save file starts at 0x32BB30 in the memory.
        # For vanilla USA it starts at 0x33E860.
        # For vanilla JP it starts at 0x33DCE0.
        self.header = bytearray(data[0x00:0x04]) # KH2 + region specific letter: J for JP/FM, U for USA
        # JP: 0x2A, USA: 0x2D, FM: 0x3A
        self.ver = c_uint(int.from_bytes(data[0x04:0x08][::-1]))
        self.checksum = c_uint(int.from_bytes(data[0x08:0x0C][::-1]))
        self.world = U8(0x0C, self.data)
        self.room = U8(0x0D, self.data)
        self.flag = U8(0x0E, self.data)
        if self.version == 0:
            self.__parse_data_vanilla_jp(data)
        elif self.version == 1:
            self.__parse_data_vanilla_usa(data)
        elif self.version == 2:
            self.__parse_data_fm(data)
    
    def __parse_data_vanilla_jp(self, data):
        placescripts = data[0x10:0x0E50]
        self.placescripts = {
            w: [
                KH2PlaceScript(i*64*3+j*3, self.data) for j in range(64)
            ]\
            for i, w in self.world_dict.items()
        }
        # with open("saved/KH2PlaceScripts.json", "w") as jf:
            # json.dump(self.placescripts, jf, indent=4, default=str)
        progress = data[0x0E50:0x10B0]
        self.progress = {w: Array(U8, 0x20, 0x0E50 + i*0x20, self.data) for i, w in self.world_dict.items()}
        self.munny = U32(0x1600, self.data)
        self.playtimes = Array(U32, 0x15, 0x1604, self.data)
        self.difficulty = U8(0x1658, self.data)
        characters = data[0x1660:0x2360]
        self.characters = [
            KH2Character(k, characters[v*0x100:(v+1)*0x100])\
            for k, v in self.character_dict.items()
        ]
        self.path = U8(0x166E, self.data) # One of Sora's unknown values
        forms = data[0x2360:0x24C8]
        self.forms = [
            KH2DriveForm(k, forms[v*0x28:(v+1)*0x28])\
            for k, v in self.drive_form_dict.items()
        ]
        self.current_form = U8(0x24C8, self.data)
        self.current_summon = U8(0x24C9, self.data)
        self.summon_level = U8(0x24CA, self.data)
        self.drive_gauge = U8(0x24CC, self.data)
        self.drive = U8(0x24CD, self.data)
        self.maxdrive = U8(0x24CE, self.data)
        self.inventory = Array(U8, 0x118, 0x2524, self.data)
        self.exp = U32(0x2684, self.data)
        self.shortcuts = Array(U16, 4, 0x269C, self.data)
        self.bonuslevel = U32(0x26A4, self.data)
        self.heartless = Array(U32, 0x2F, 0x26EC, self.data)
        self.nobodies = Array(U32, 0x0C, 0x286C, self.data)
        self.rc_usage = Array(U16, 0x30, 0x28EE, self.data)
        self.limit_usage = Array(U16, 0x15, 0x2CEC, self.data)
        
        minigames = data[0x2E5C:0x2F3C]
        self.minigames = [KH2Minigame(self.minigame_list[i], minigames[i*8:(i+1)*8]) for i in range(len(minigames)//8)]
    
    def __parse_data_vanilla_usa(self, data):
        placescripts = data[0x10:0x0E50]
        self.placescripts = {
            w: [
                KH2PlaceScript(i*64*3+j*3, self.data) for j in range(64)
            ]\
            for i, w in self.world_dict.items()
        }
        # with open("saved/KH2PlaceScripts.json", "w") as jf:
            # json.dump(self.placescripts, jf, indent=4, default=str)
        progress = data[0x0E50:0x10B0]
        self.progress = {w: Array(U8, 0x20, 0x0E50 + i*0x20, self.data) for i, w in self.world_dict.items()}
        self.munny = U32(0x1600, self.data)
        self.playtimes = Array(U32, 0x15, 0x1604, self.data)
        self.difficulty = U8(0x1658, self.data)
        characters = data[0x1660:0x22C4]
        self.characters = [
            KH2Character(k, characters[v*0xF4:(v+1)*0xF4])\
            for k, v in self.character_dict.items()
        ]
        self.path = U8(0x166E, self.data) # One of Sora's unknown values
        forms = data[0x22C4:0x242C]
        self.forms = [
            KH2DriveForm(k, forms[v*0x28:(v+1)*0x28])\
            for k, v in self.drive_form_dict.items()
        ]
        self.current_form = U8(0x242C, self.data)
        self.current_summon = U8(0x242D, self.data)
        self.summon_level = U8(0x242E, self.data)
        self.drive_gauge = U8(0x2430, self.data)
        self.drive = U8(0x2431, self.data)
        self.maxdrive = U8(0x2432, self.data)
        self.inventory = Array(U8, 0x118, 0x2488, self.data)
        self.exp = U32(0x25E8, self.data)
        
        self.shortcuts = Array(U16, 4, 0x2600, self.data)
        self.bonuslevel = U32(0x2608, self.data)
        
        self.heartless = Array(U32, 0x2F, 0x2650, self.data)
        self.nobodies = Array(U32, 0x0C, 0x27D0, self.data)
        self.rc_usage = Array(U16, 0x30, 0x2852, self.data)
        self.limit_usage = Array(U16, 0x15, 0x2C50, self.data)
        
        minigames = data[0x2DC0:0x2EA0]
        self.minigames = [KH2Minigame(self.minigame_list[i], minigames[i*8:(i+1)*8]) for i in range(len(minigames)//8)]
        
        self.synthesis_creations = Array(U8, 5, 0x3741, self.data)
        self.synthesis_exp = U32(0x3758, self.data)
        self.synthesis_inventory = Array(U32, 0x32, 0x375C, self.data)
        self.synthesis_log = Array(U32, 0x32, 0x3824, self.data)
        
        self.gummi_treasure_percents = Array(F32, 0x01A1, 0xACE0, self.data)

    def __parse_data_fm(self, data):
        placescripts = data[0x10:0x1C90]
        self.placescripts = {
            w: [
                KH2FMPlaceScript(i*64*6+j*6, self.data) for j in range(64)
            ] for i, w in self.world_dict.items()
        }
        # with open("saved/KH2FMPlaceScripts.json", "w") as jf:
            # json.dump(self.placescripts, jf, indent=4, default=str)
        progress = data[0x1C90:0x2150]
        self.progress = {w: Array(U8, 0x20, 0x1C90 + i*0x20, self.data) for i, w in self.world_dict.items()}
        self.munny = U32(0x2440, self.data)
        self.playtimes = Array(U32, 0x15, 0x2444, self.data)
        self.difficulty = U8(0x2498, self.data)
        self.puzzles = Array(U8, 0x30, 0x24A0, self.data)
        characters = data[0x24F0:0x32F4]
        self.characters = [
            KH2FMCharacter(k, characters[v*0x114:(v+1)*0x114])\
            for k, v in self.character_dict.items()
        ]
        self.path = U8(0x24FE, self.data) # One of Sora's unknown values
        forms = data[0x32F4:0x3524]
        self.forms = [
            KH2FMDriveForm(k, forms[v*0x38:(v+1)*0x38])\
            for k, v in self.drive_form_fm_dict.items()
        ]
        self.current_form = U8(0x3524, self.data)
        self.current_summon = U8(0x3525, self.data)
        self.summon_level = U8(0x3526, self.data)
        self.drive_gauge = U8(0x3528, self.data)
        self.drive = U8(0x3529, self.data)
        self.maxdrive = U8(0x352A, self.data)
        self.party = Array(U8, 19*4, 0x3534, self.data)
        self.inventory = Array(U8, 0x138, 0x3580, self.data)
        self.form_unlock = U8(0x36C0, self.data)
        self.summon_unlock = U8(0x36C4, self.data)
        self.reports = Array(U8, 3, 0x36C4, self.data)
        self.limit_form_unlock = U8(0x36CA, self.data) # bit index 3
        self.exp = U32(0x36E0, self.data)
        self.shortcuts = Array(U16, 4, 0x36F8, self.data)
        self.bonuslevel = U32(0x3700, self.data)
        self.heartless = Array(U32, 0x48, 0x3748, self.data)
        self.limit_form_shortcuts_refined = Array(U16, 4, 0x371C, self.data)
        self.nobodies = Array(U32, 0x0C, 0x38C8, self.data)
        self.rc_usage = Array(U16, 0x33, 0x394A, self.data)
        self.limit_usage = Array(U16, 0x15, 0x3D48, self.data)
        minigames = data[0x3DB4:0x3EF4]
        self.minigames = [KH2Minigame(self.minigame_list[i], minigames[i*8:(i+1)*8]) for i in range(len(minigames)//8)]
        self.form_usage = Array(U16, 0x0A, 0x3FD6, self.data)
        self.weapon_backup = U16(0x3FEA, self.data)
        # At 0x4438 starts something like a 0x60 long struct 15? times.
        # At 0x4C38 starts The Heartless tab's "New" flags.
        # At 0x4C42 starts The Nobodies tab's "New" flags.
        # After 0x4D40 there are Journal "New" flags.
        # From 0x4DA0 these affect the Puzzle Pieces tab.
        self.shortcut_sets_refined = Array(U16, 3*4, 0x10108, self.data)
    
    def __save_shared(self):
        for c in self.characters:
            c.save(self)
        for f in self.forms:
            f.save(self)
        for mg in self.minigames:
            mg.save(self)
    
    def __save_vanilla_jp(self):
        for i, w in self.world_dict.items():
            for j in range(len(self.progress[w])):
                self.data[0x0E50+i*0x20+j] = self.progress[w][j]

    def __save_vanilla_usa(self):
        for i, w in self.world_dict.items():
            for j in range(len(self.progress[w])):
                self.data[0x0E50+i*0x20+j] = self.progress[w][j]

    def __save_fm(self):
        for i, w in self.world_dict.items():
            for j in range(len(self.progress[w])):
                self.data[0x1C90+i*0x20+j] = self.progress[w][j]

    def save(self):
        self.__save_shared()
        if self.version == 0:
            self.__save_vanilla_jp()
        elif self.version == 1:
            self.__save_vanilla_usa()
        else:
            self.__save_fm()
        # Calculate checksum right before dumping the file
        self.checksum = KH2.calculate_checksum(self.data)
        self.data[0x08:0x0C] = bytearray(self.checksum)
        
        os.makedirs("saved/kh2/" + self.filename, exist_ok=True)
        with open(os.path.join("saved", "kh2", self.filename, self.filename), "wb") as file:
            file.write(self.data)
        if self.sysdata is not None:
            os.makedirs("saved/kh2/" + self.filename[:-2]+"SYS", exist_ok=True)
            with open(os.path.join("saved", "kh2", self.filename[:-2]+"SYS", self.filename[:-2]+"SYS"), "wb") as sysfile:
                sysfile.write(self.sysdata)
        if hasattr(self, "pcsx2"):
            self.pcsx2.dump_to_emu()
        
    @staticmethod
    def __calculate_checksum(data, crc_table, offset, length, checksum):
        checksum = c_uint(checksum)
        for i in range(offset, offset + length):
            checksum.value = crc_table[(checksum.value >> 24) ^ data[i]] ^ (checksum.value << 8)
        return c_uint(checksum.value ^ 0xFFFFFFFF)
    
    """
    Calculates the checksum of the save file.
    Same algorithm is used in all versions.
    """
    @staticmethod
    def calculate_checksum(data):
        CrcPolynomial = 0x04c11db7;
        crc_table = [0 for x in range(0x100)]
        for x in range(0x100):
            r = c_int(x << 24)
            for j in range(0xFF):
                r.value = r.value << 1 ^ (CrcPolynomial if r.value < 0 else 0)
            crc_table[x] = c_uint(r.value).value
        checksum = KH2.__calculate_checksum(data, crc_table, 0, 8, 0xFFFFFFFF)
        # print(format(checksum.value, "04X"))
        checksum = KH2.__calculate_checksum(data, crc_table, 0x0C, len(data)-0x0C, checksum.value ^ 0xFFFFFFFF)
        return checksum
    
    @property
    def fm(self):
        return self.version == 2
    
    def __repr__(self):
        if not self.fm:
            return f"{self.header.decode()}(\n    {self.characters[0]},\n    World: {self.world_dict[self.world.value]},\n)"
        else:
            return f"KH2FM(\n    {self.characters[0]},\n    World: {self.world_dict[self.world.value]},\n)"
