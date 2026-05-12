import os
import struct

from ctypes import *
from .khbbs_dicts import dicts
from .ppsspp import PPSSPP


class KHBBSCharacter:
    """
    Class for representing the character struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0x30 bytes long.
    """
    def __init__(self, name, data):
        self.name = name
        self.exp = c_uint(int.from_bytes(data[0x00:0x04][::-1]))
        self.munny = c_uint(int.from_bytes(data[0x04:0x08][::-1]))
        self.medals = c_uint(int.from_bytes(data[0x08:0x0C][::-1]))
        self.level = c_ushort(int.from_bytes(data[0x0C:0x0E][::-1]))
        self.hp = c_ushort(int.from_bytes(data[0x0E:0x10][::-1]))
        self.maxhp = c_ushort(int.from_bytes(data[0x10:0x12][::-1]))
        # Unknown part
        # 3 resistances maybe?
        self.magic = c_ushort(int.from_bytes(data[0x18:0x1A][::-1]))
        self.defense = c_ushort(int.from_bytes(data[0x1A:0x1C][::-1]))
        self.arenalevel = c_ushort(int.from_bytes(data[0x1C:0x1E][::-1]))
        # Unknown part
        # self.physical_resistance = c_ushort(int.from_bytes(data[0x20:0x22][::-1])) # hunch
        self.fire_resistance = c_ushort(int.from_bytes(data[0x22:0x24][::-1]))
        self.blizzard_resistance = c_ushort(int.from_bytes(data[0x24:0x26][::-1]))
        self.thunder_resistance = c_ushort(int.from_bytes(data[0x26:0x28][::-1]))
        self.dark_resistance = c_ushort(int.from_bytes(data[0x28:0x2A][::-1]))
        self.weapon = c_ushort(int.from_bytes(data[0x2A:0x2C][::-1]))
        self.strength = c_ushort(int.from_bytes(data[0x2E:0x30][::-1]))
    
    def save(self, obj):
        if obj.version == 0:
            offset = 0x59A8
        if obj.version == 1:
            offset = 0x59A8
        if obj.fm:
            offset = 0x59D0
        obj.data[offset+0x00:offset+0x04] = bytearray(self.exp)
        obj.data[offset+0x04:offset+0x08] = bytearray(self.munny)
        obj.data[offset+0x08:offset+0x0C] = bytearray(self.medals)
        obj.data[offset+0x0C:offset+0x0E] = bytearray(self.level)
        obj.data[offset+0x0E:offset+0x10] = bytearray(self.hp)
        obj.data[offset+0x10:offset+0x12] = bytearray(self.maxhp)
        obj.data[offset+0x18:offset+0x1A] = bytearray(self.magic)
        obj.data[offset+0x1A:offset+0x1C] = bytearray(self.defense)
        obj.data[offset+0x1C:offset+0x1E] = bytearray(self.arenalevel)
        obj.data[offset+0x22:offset+0x24] = bytearray(self.fire_resistance)
        obj.data[offset+0x24:offset+0x26] = bytearray(self.blizzard_resistance)
        obj.data[offset+0x26:offset+0x28] = bytearray(self.thunder_resistance)
        obj.data[offset+0x28:offset+0x2A] = bytearray(self.dark_resistance)
        obj.data[offset+0x2A:offset+0x2C] = bytearray(self.weapon)
        obj.data[offset+0x2E:offset+0x30] = bytearray(self.strength)

    def __repr__(self):
        dicts(self)
        return f"{self.name}(Level: {self.level.value}, Weapon: {list(self.weapon_dict.keys())[self.weapon.value]})"


class KHBBS:
    def __init__(self, slot=0, version=2, attach=False):
        dicts(self)
        if slot == 0:
            slot = 100
        self.version = version
        if self.version == 0:
            self.foldername = "ULJM05600" + f"{slot-1:04d}"
            self.filesize = 0x11B40
        elif self.version == 1:
            self.foldername = "ULUS10505" + f"{slot-1:04d}"
            self.filesize = 0x11B40
        elif self.version == 2:
            self.foldername = "ULJM05775" + f"{slot-1:04d}"
            self.filesize = 0x11E50
        if slot != 100:
            if os.path.exists(os.path.join("files", "khbbs", self.foldername, "SAVEDATA.DAT")):
                with open(os.path.join("files", "khbbs", self.foldername, "SAVEDATA.DAT"), "rb") as file:
                    self.data = (c_ubyte*self.filesize)(*file.read())
            else:
                with open("files/khbbs/SAVEDATA.DAT", "rb") as file:
                    self.data = (c_ubyte*self.filesize)(*file.read())
            self.__parse_data(self.data)
            # I don't think I'll actually support it but let's put this here just in case.
            self.sysdata = None
            if os.path.exists(os.path.join("files", "khbbs", self.foldername[:-4], "SYSTEM.DAT")):
                with open(os.path.join("files", "khbbs", self.foldername[:-4], "SYSTEM.DAT"), "rb") as sysfile:
                    self.sysdata = (c_ubyte*0x13B80)(*sysfile.read())
        if attach:
            if self.version == 0:
                self.addr = 0x00000000
            elif self.version == 1:
                self.addr = 0x00000000
            elif self.version == 2:
                self.addr = 0x09F25EF0
            self.sysdata = None
            self.ppsspp = PPSSPP(self.addr, self.filesize, self)
            self.__parse_data(self.data)

    def __parse_data(self, data):
        # For FM the currently loaded save file starts at 0x09F25EF0 in the memory.
        # For vanilla USA it starts at ?.
        # For vanilla JP it starts at ?.
        self.header = bytearray(data[0x00:0x04]) # BBSD
        # JP: 0x18, USA: 0x1C, FM: 0x1D
        self.ver = c_uint(int.from_bytes(data[0x04:0x08][::-1]))
        self.size = c_uint(int.from_bytes(data[0x08:0x0C][::-1])) # should be the same as filesize
        assert(self.size.value == self.filesize)
        self.checksum = c_uint(int.from_bytes(data[0x0C:0x10][::-1]))
        self.reports = c_ubyte(data[0x10])
        self.world = c_ubyte(data[0x14])
        self.room = c_ubyte(data[0x15])
        self.flag = c_ubyte(data[0x16])
        self.character_type = c_ubyte(data[0x17])
        self.playtime = c_uint(int.from_bytes(data[0x18:0x1C][::-1]))
        if self.version == 0:
            self.__parse_data_vanilla_jp(data)
        elif self.version == 1:
            self.__parse_data_vanilla_usa(data)
        elif self.version == 2:
            self.__parse_data_fm(data)
    
    def __parse_data_vanilla_jp(self, data):
        pass
    
    def __parse_data_vanilla_usa(self, data):
        pass
    
    def __parse_data_fm(self, data):
        self.character = KHBBSCharacter(self.name, data[0x59D0:0x5A00])

    def __save_shared(self):
        self.data[0x10] = self.reports
        self.data[0x14] = self.world
        self.data[0x15] = self.room
        self.data[0x16] = self.flag
        self.data[0x17] = self.character_type
        self.data[0x18:0x1C] = bytearray(self.playtime)
        self.character.save(self)
    
    def __save_vanilla_jp(self):
        pass
    
    def __save_vanilla_usa(self):
        pass
    
    def __save_fm(self):
        pass

    def save(self):
        self.__save_shared()
        if self.version == 0:
            self.__save_vanilla_jp()
        elif self.version == 1:
            self.__save_vanilla_usa()
        else:
            self.__save_fm()
        # Calculate checksum right before dumping the file
        self.checksum = self.calculate_checksum(self.data)
        self.data[0x0C:0x10] = bytearray(self.checksum)
        
        os.makedirs("saved/khbbs/" + self.foldername, exist_ok=True)
        with open(os.path.join("saved", "khbbs", self.foldername, "SAVEDATA.DAT"), "wb") as file:
            file.write(self.data)
        if self.sysdata is not None:
            os.makedirs("saved/khbbs/" + self.foldername[:-4], exist_ok=True)
            with open(os.path.join("saved", "khbbs", self.foldername[:-4], "SYSTEM.DAT"), "wb") as sysfile:
                sysfile.write(self.sysdata)
        if hasattr(self, "ppsspp"):
            self.ppsspp.dump_to_emu()

    """
    Calculates the checksum of the save file.
    Same algorithm is used in all versions.
    """
    def calculate_checksum(self, data):
        checksum = 0
        for i in range(0x10, self.filesize, 4):
            checksum += int.from_bytes(data[i:i+4][::-1])
        return c_uint(checksum)

    @property
    def fm(self):
        return self.version == 2

    @property
    def name(self):
        return {v: k for k, v in self.character_dict.items()}[self.character_type.value]

    def __repr__(self):
        if self.version == 0:
            game = "KHBBSJP"
        if self.version == 1:
            game = "KHBBSUSA"
        else:
            game = "KHBBSFM"
        return f"{game}(\n    {self.character},\n    World: {self.world_dict[self.world.value]},\n)"
