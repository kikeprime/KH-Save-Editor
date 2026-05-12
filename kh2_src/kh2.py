import os
import struct

from ctypes import *
from .kh2_dicts import *
from .kh2_helper import *
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
        self.world = c_ubyte(data[0x0C])
        self.room = c_ubyte(data[0x0D])
        self.flag = c_ubyte(data[0x0E])
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
                KH2PlaceScript(placescripts[i*64*3+j*3:i*64*3+j*3+3])\
                for j in range(64)
            ]\
            for i, w in self.world_dict.items()
        }
        # with open("saved/KH2PlaceScripts.json", "w") as jf:
            # json.dump(self.placescripts, jf, indent=4, default=str)
        progress = data[0x0E50:0x10B0]
        self.progress = {w: (c_ubyte*0x20)(*progress[i*0x20:(i+1)*0x20]) for i, w in self.world_dict.items()}
        self.munny = c_uint(int.from_bytes(data[0x1600:0x1604][::-1]))
        self.playtimes = (c_uint*0x15)(*struct.unpack("<21I", bytearray(data[0x1604:0x1658])))
        self.difficulty = c_ubyte(data[0x1658])
        characters = data[0x1660:0x2360]
        self.characters = [
            KH2Character(k, characters[v*0x100:(v+1)*0x100])\
            for k, v in self.character_dict.items()
        ]
        self.path = c_ubyte(data[0x166E]) # One of Sora's unknown values
        forms = data[0x2360:0x24C8]
        self.forms = [
            KH2DriveForm(k, forms[v*0x28:(v+1)*0x28])\
            for k, v in self.drive_form_dict.items()
        ]
        self.current_form = c_ubyte(data[0x24C8])
        self.current_summon = c_ubyte(data[0x24C9])
        self.summon_level = c_ubyte(data[0x24CA])
        self.drive_gauge = c_ubyte(data[0x24CC])
        self.drive = c_ubyte(data[0x24CD])
        self.maxdrive = c_ubyte(data[0x24CE])
        self.inventory = (c_ubyte*0x118)(*data[0x2524:0x263C])
        self.exp = c_uint(int.from_bytes(data[0x2684:0x2688][::-1]))
        self.shortcuts = (c_ushort*4)(*struct.unpack("<4H", bytearray(data[0x269C:0x26A4])))
        self.bonuslevel = c_uint(int.from_bytes(data[0x26A4:0x26A8][::-1]))
        self.heartless = (c_uint*0x2F)(*struct.unpack("<47I", bytearray(data[0x26EC:0x27A8])))
        self.nobodies = (c_uint*0x0C)(*struct.unpack("<12I", bytearray(data[0x286C:0x289C])))
        self.rc_usage = (c_ushort*0x30)(*struct.unpack("<48H", bytearray(data[0x28EE:0x294E])))
        self.limit_usage = (c_ushort*0x15)(*struct.unpack("<21H", bytearray(data[0x2CEC:0x2D16])))
        
        minigames = data[0x2E5C:0x2F3C]
        self.minigames = [KH2Minigame(self.minigame_list[i], minigames[i*8:(i+1)*8]) for i in range(len(minigames)//8)]
    
    def __parse_data_vanilla_usa(self, data):
        placescripts = data[0x10:0x0E50]
        self.placescripts = {
            w: [
                KH2PlaceScript(placescripts[i*64*3+j*3:i*64*3+j*3+3])\
                for j in range(64)
            ]\
            for i, w in self.world_dict.items()
        }
        # with open("saved/KH2PlaceScripts.json", "w") as jf:
            # json.dump(self.placescripts, jf, indent=4, default=str)
        progress = data[0x0E50:0x10B0]
        self.progress = {w: (c_ubyte*0x20)(*progress[i*0x20:(i+1)*0x20]) for i, w in self.world_dict.items()}
        self.munny = c_uint(int.from_bytes(data[0x1600:0x1604][::-1]))
        self.playtimes = (c_uint*0x15)(*struct.unpack("<21I", bytearray(data[0x1604:0x1658])))
        self.difficulty = c_ubyte(data[0x1658])
        characters = data[0x1660:0x22C4]
        self.characters = [
            KH2Character(k, characters[v*0xF4:(v+1)*0xF4])\
            for k, v in self.character_dict.items()
        ]
        self.path = c_ubyte(data[0x166E]) # One of Sora's unknown values
        # print(self)
        forms = data[0x22C4:0x242C]
        self.forms = [
            KH2DriveForm(k, forms[v*0x28:(v+1)*0x28])\
            for k, v in self.drive_form_dict.items()
        ]
        self.current_form = c_ubyte(data[0x242C])
        self.current_summon = c_ubyte(data[0x242D])
        self.summon_level = c_ubyte(data[0x242E])
        self.drive_gauge = c_ubyte(data[0x2430])
        self.drive = c_ubyte(data[0x2431])
        self.maxdrive = c_ubyte(data[0x2432])
        self.inventory = (c_ubyte*0x118)(*data[0x2488:0x25A0])
        self.exp = c_uint(int.from_bytes(data[0x25E8:0x25EC][::-1]))
        
        self.shortcuts = (c_ushort*4)(*struct.unpack("<4H", bytearray(data[0x2600:0x2608])))
        self.bonuslevel = c_uint(int.from_bytes(data[0x2608:0x260C][::-1]))
        
        self.heartless = (c_uint*0x2F)(*struct.unpack("<47I", bytearray(data[0x2650:0x270C])))
        self.nobodies = (c_uint*0x0C)(*struct.unpack("<12I", bytearray(data[0x27D0:0x2800])))
        self.rc_usage = (c_ushort*0x30)(*struct.unpack("<48H", bytearray(data[0x2852:0x28B2])))
        self.limit_usage = (c_ushort*0x15)(*struct.unpack("<21H", bytearray(data[0x2C50:0x2C7A])))
        
        minigames = data[0x2DC0:0x2EA0]
        self.minigames = [KH2Minigame(self.minigame_list[i], minigames[i*8:(i+1)*8]) for i in range(len(minigames)//8)]
        
        self.synthesis_creations = (c_ubyte*5)(*data[0x3741:0x3746])
        self.synthesis_exp = c_uint(int.from_bytes(data[0x3758:0x375C][::-1]))
        self.synthesis_inventory = (c_uint*0x32)(*struct.unpack("<50I", bytearray(data[0x375C:0x3824])))
        self.synthesis_log = (c_uint*0x32)(*struct.unpack("<50I", bytearray(data[0x3824:0x38EC])))
        
        self.gummi_treasure_percents = (c_float*0x01A1)(*struct.unpack("<417f", bytearray(data[0xACE0:0xB364])))
    
    def __parse_data_fm(self, data):
        placescripts = data[0x10:0x1C90]
        self.placescripts = {
            w: [
                KH2FMPlaceScript(placescripts[i*64*6+j*6:i*64*6+j*6+6])\
                for j in range(64)
            ] for i, w in self.world_dict.items()
        }
        # with open("saved/KH2FMPlaceScripts.json", "w") as jf:
            # json.dump(self.placescripts, jf, indent=4, default=str)
        progress = data[0x1C90:0x2150]
        self.progress = {w: (c_ubyte*0x20)(*progress[i*0x20:(i+1)*0x20]) for i, w in self.world_dict.items()}
        self.munny = c_uint(int.from_bytes(data[0x2440:0x2444][::-1]))
        self.playtimes = (c_uint*0x15)(*struct.unpack("<21I", bytearray(data[0x2444:0x2498])))
        self.difficulty = c_ubyte(data[0x2498])
        self.puzzles = (c_ubyte*0x30)(*data[0x24A0:0x24D0])
        characters = data[0x24F0:0x32F4]
        self.characters = [
            KH2FMCharacter(k, characters[v*0x114:(v+1)*0x114])\
            for k, v in self.character_dict.items()
        ]
        self.path = c_ubyte(data[0x24FE]) # One of Sora's unknown values
        forms = data[0x32F4:0x3524]
        self.forms = [
            KH2FMDriveForm(k, forms[v*0x38:(v+1)*0x38])\
            for k, v in self.drive_form_fm_dict.items()
        ]
        self.current_form = c_ubyte(data[0x3524])
        self.current_summon = c_ubyte(data[0x3525])
        self.summon_level = c_ubyte(data[0x3526])
        self.drive_gauge = c_ubyte(data[0x3528])
        self.drive = c_ubyte(data[0x3529])
        self.maxdrive = c_ubyte(data[0x352A])
        self.party = (c_ubyte*(19*4))(*data[0x3534:0x3580])
        self.inventory = (c_ubyte*0x138)(*data[0x3580:0x36B8])
        self.form_unlock = c_ubyte(data[0x36C0])
        self.summon_unlock = c_ubyte(data[0x36C4])
        self.reports = (c_ubyte*3)(*data[0x36C4:0x36C7])
        self.limit_form_unlock = c_ubyte(data[0x36CA]) # bit index 3
        self.exp = c_uint(int.from_bytes(data[0x36E0:0x36E4][::-1]))
        self.shortcuts = (c_ushort*4)(*struct.unpack("<4H", bytearray(data[0x36F8:0x3700])))
        self.bonuslevel = c_uint(int.from_bytes(data[0x3700:0x3704][::-1]))
        self.heartless = (c_uint*0x48)(*struct.unpack("<72I", bytearray(data[0x3748:0x3868])))
        self.nobodies = (c_uint*0x0C)(*struct.unpack("<12I", bytearray(data[0x38C8:0x38F8])))
        self.rc_usage = (c_ushort*0x33)(*struct.unpack("<51H", bytearray(data[0x394A:0x39B0])))
        self.limit_usage = (c_ushort*0x15)(*struct.unpack("<21H", bytearray(data[0x3D48:0x3D72])))
        minigames = data[0x3DB4:0x3EF4]
        self.minigames = [KH2Minigame(self.minigame_list[i], minigames[i*8:(i+1)*8]) for i in range(len(minigames)//8)]
        self.form_usage = (c_ushort*0x0A)(*struct.unpack("<10H", bytearray(data[0x3FD6:0x3FEA])))
        self.weapon_backup = c_ushort(int.from_bytes(data[0x3FEA:0x3FEC][::-1]))
        # At 0x4438 starts something like a 0x60 long struct 15? times.
        # At 0x4C38 starts The Heartless tab's "New" flags.
        # At 0x4C42 starts The Nobodies tab's "New" flags.
        # After 0x4D40 there are Journal "New" flags.
        # From 0x4DA0 these affect the Puzzle Pieces tab.
    
    def __save_shared(self):
        self.data[0x0C] = self.world
        self.data[0x0D] = self.room
        self.data[0x0E] = self.flag
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
        self.data[0x1600:0x1604] = bytearray(self.munny)
        self.data[0x1604:0x1658] = bytearray(self.playtimes)
        self.data[0x1658] = self.difficulty
        self.data[0x166E] = self.path
        self.data[0x24C8] = self.current_form
        self.data[0x24C9] = self.current_summon
        self.data[0x24CA] = self.summon_level
        self.data[0x24CC] = self.drive_gauge
        self.data[0x24CD] = self.drive
        self.data[0x24CE] = self.maxdrive
        self.data[0x2524:0x263C] = bytearray(self.inventory)
        self.data[0x2684:0x2688] = bytearray(self.exp)
        self.data[0x269C:0x26A4] = bytearray(self.shortcuts)
        self.data[0x26A4:0x26A8] = bytearray(self.bonuslevel)
        self.data[0x26EC:0x27A8] = bytearray(self.heartless)
        self.data[0x286C:0x289C] = bytearray(self.nobodies)
        self.data[0x28EE:0x294E] = bytearray(self.rc_usage)
        self.data[0x2CEC:0x2D16] = bytearray(self.limit_usage)
    
    def __save_vanilla_usa(self):
        for i, w in self.world_dict.items():
            for j in range(len(self.progress[w])):
                self.data[0x0E50+i*0x20+j] = self.progress[w][j]
        self.data[0x1600:0x1604] = bytearray(self.munny)
        self.data[0x1604:0x1658] = bytearray(self.playtimes)
        self.data[0x1658] = self.difficulty
        self.data[0x166E] = self.path
        self.data[0x242C] = self.current_form
        self.data[0x242D] = self.current_summon
        self.data[0x242E] = self.summon_level
        self.data[0x2430] = self.drive_gauge
        self.data[0x2431] = self.drive
        self.data[0x2432] = self.maxdrive
        self.data[0x2488:0x25A0] = bytearray(self.inventory)
        self.data[0x25E8:0x25EC] = bytearray(self.exp)
        self.data[0x2600:0x2608] = bytearray(self.shortcuts)
        self.data[0x2608:0x260C] = bytearray(self.bonuslevel)
        self.data[0x2650:0x270C] = bytearray(self.heartless)
        self.data[0x27D0:0x2800] = bytearray(self.nobodies)
        self.data[0x2852:0x28B2] = bytearray(self.rc_usage)
        self.data[0x2C50:0x2C7A] = bytearray(self.limit_usage)
    
    def __save_fm(self):
        for i, w in self.world_dict.items():
            for j in range(len(self.progress[w])):
                self.data[0x1C90+i*0x20+j] = self.progress[w][j]
        self.data[0x2440:0x2444] = bytearray(self.munny)
        self.data[0x2444:0x2498] = bytearray(self.playtimes)
        self.data[0x2498] = self.difficulty
        self.data[0x24FE] = self.path
        self.data[0x3524] = self.current_form
        self.data[0x3525] = self.current_summon
        self.data[0x3526] = self.summon_level
        self.data[0x3528] = self.drive_gauge
        self.data[0x3529] = self.drive
        self.data[0x352A] = self.maxdrive
        self.data[0x3534:0x3580] = bytearray(self.party)
        self.data[0x3580:0x36B8] = bytearray(self.inventory)
        self.data[0x36E0:0x36E4] = bytearray(self.exp)
        self.data[0x36F8:0x3700] = bytearray(self.shortcuts)
        self.data[0x3700:0x3704] = bytearray(self.bonuslevel)
        self.data[0x3748:0x3868] = bytearray(self.heartless)
        self.data[0x38C8:0x38F8] = bytearray(self.nobodies)
        self.data[0x394A:0x39B0] = bytearray(self.rc_usage)
        self.data[0x3D48:0x3D72] = bytearray(self.limit_usage)
        self.data[0x3FD6:0x3FEA] = bytearray(self.form_usage)
        self.data[0x3FEA:0x3FEC] = bytearray(self.weapon_backup)

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
