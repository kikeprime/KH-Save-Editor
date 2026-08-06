import struct

from ctypes import *
from .kh2_dicts import *
from kh1_src.datatypes import *


class KH2Character:
    """
    Class for representing the character struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0xF4 bytes long.
    The structure is 0x100 bytes long in vanilla JP.
    """
    def __init__(self, name, data):
        self.name = name
        self.weapon = c_ushort(int.from_bytes(data[0x00:0x02][::-1]))
        # data[0x02:0x04] is unknown; padding?
        self.hp = c_ubyte(data[0x04])
        self.maxhp = c_ubyte(data[0x05])
        self.mp = c_ubyte(data[0x06])
        self.maxmp = c_ubyte(data[0x07])
        self.apboost = c_ubyte(data[0x08])
        self.strengthboost = c_ubyte(data[0x09])
        self.magicboost = c_ubyte(data[0x0A])
        self.defenseboost = c_ubyte(data[0x0B])
        # data[0x0C:0x0F] is unknown
        # Sora's data[0x0E] is the leveling path
        self.path = c_ubyte(data[0x0E])
        self.level = c_ubyte(data[0x0F])
        self.armorslots = c_ubyte(data[0x10])
        self.accessoryslots = c_ubyte(data[0x11])
        self.itemslots = c_ubyte(data[0x12])
        # data[0x13] is unknown
        self.armors = (c_ushort*8)(*struct.unpack("<8H", bytearray(data[0x14:0x24])))
        self.accessories = (c_ushort*8)(*struct.unpack("<8H", bytearray(data[0x24:0x34])))
        self.items = (c_ushort*8)(*struct.unpack("<8H", bytearray(data[0x34:0x44])))
        self.autoreload = (c_ushort*8)(*struct.unpack("<8H", bytearray(data[0x44:0x54])))
        self.abilities = (c_ushort*0x40)(*struct.unpack("<64H", bytearray(data[0x54:0xD4]))) # 63 usable
        self.battlestyle = c_ubyte(data[0xD4])
        # data[0xD5:0xDB] is unknown
        # data[0xDB] is the Ability Style slot for unintended abilities
        # like giving Donald Guard and Aerial Sweep then they will share this byte.
        # I exclude it so users won't edit it due to confusion.
        self.abilitystyles = (c_ubyte*4)(*data[0xDC:0xE0])
        # data[0xE0:0xF4] is unknown
    
    def save(self, obj):
        i = obj.character_dict[self.name]
        offset = 0x1660+i*(0x100 if obj.version == 0 else 0xF4) if not obj.fm else 0x24F0+i*0x114
        obj.data[offset+0x00:offset+0x02] = bytearray(self.weapon)
        obj.data[offset+0x04] = self.hp
        obj.data[offset+0x05] = self.maxhp
        obj.data[offset+0x06] = self.mp
        obj.data[offset+0x07] = self.maxmp
        obj.data[offset+0x08] = self.apboost
        obj.data[offset+0x09] = self.strengthboost
        obj.data[offset+0x0A] = self.magicboost
        obj.data[offset+0x0B] = self.defenseboost
        obj.data[offset+0x0F] = self.level
        obj.data[offset+0x10] = self.armorslots
        obj.data[offset+0x11] = self.accessoryslots
        obj.data[offset+0x12] = self.itemslots
        obj.data[offset+0x14:offset+0x24] = bytearray(self.armors)
        obj.data[offset+0x24:offset+0x34] = bytearray(self.accessories)
        obj.data[offset+0x34:offset+0x44] = bytearray(self.items)
        obj.data[offset+0x44:offset+0x54] = bytearray(self.autoreload)
        obj.data[offset+0x54:offset+0x54+2*len(self.abilities)] = bytearray(self.abilities)
        obj.data[offset+0x54+2*len(self.abilities)] = self.battlestyle
        obj.data[offset+0x54+2*len(self.abilities)+8:offset+0x54+2*len(self.abilities)+8+4] = bytearray(self.abilitystyles)

    def __repr__(self):
        dicts(self)
        return f"{self.name}(Level: {self.level.value}, Weapon: {list(self.weapon_dict.keys())[self.weapon.value]})"


class KH2FMCharacter(KH2Character):
    """
    Class for representing the Final Mix character struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0x114 bytes long.
    """
    def __init__(self, name, data):
        super().__init__(name, data)
        self.abilities = (c_ushort*0x50)(*struct.unpack("<80H", bytearray(data[0x54:0xF4]))) # 79 usable
        self.battlestyle = c_ubyte(data[0xF4])
        self.abilitystyles = (c_ubyte*4)(*data[0xFC:0x100])
        # data[0x100:0x114] is unknown


class KH2DriveForm:
    """
    Class for representing the Drive Form struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0x28 bytes long.
    """
    def __init__(self, name, data):
        self.name = name
        self.weapon = c_ushort(int.from_bytes(data[0x00:0x02][::-1]))
        self.level = c_ubyte(data[0x02])
        self.abilitylevel = c_ubyte(data[0x03])
        self.exp = c_uint(int.from_bytes(data[0x04:0x08][::-1])) # Antipoints for Antiform
        self.abilities = (c_ushort*0x10)(*struct.unpack("<16H", bytearray(data[0x08:0x28])))
    
    def save(self, obj):
        i = obj.drive_form_fm_dict[self.name] if obj.fm else obj.drive_form_dict[self.name]
        offset = (0x2360 if obj.version == 0 else 0x22C4)+i*0x28 if not obj.fm else 0x32F4+i*0x38
        obj.data[offset+0x00:offset+0x02] = bytearray(self.weapon)
        obj.data[offset+0x02] = self.level
        obj.data[offset+0x03] = self.abilitylevel
        obj.data[offset+0x04:offset+0x08] = bytearray(self.exp)
        obj.data[offset+0x08:offset+0x08+2*len(self.abilities)] = bytearray(self.abilities)

    def __repr__(self):
        dicts(self)
        if self.name != "Antiform":
            return f"{self.name}(Level: {self.level.value}, Weapon: {list(self.item_dict.keys())[self.weapon.value]}, EXP: {self.exp.value})"
        else:
            return f"{self.name}(Level: {self.level.value}, Weapon: {list(self.item_dict.keys())[self.weapon.value]}, Antipoints: {self.exp.value})"


class KH2FMDriveForm(KH2DriveForm):
    """
    Class for representing the Final Mix Drive Form struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0x38 bytes long.
    """
    def __init__(self, name, data):
        super().__init__(name, data)
        # Only difference is that 8 more abilities are possible
        self.abilities = (c_ushort*0x18)(*struct.unpack("<24H", bytearray(data[0x08:0x38])))


class KH2PlaceScript:
    def __init__(self, offset, data):
        self.map = U8(offset+0x00, data)
        self.battle = U8(offset+0x01, data)
        self.event = U8(offset+0x02, data)

    def __repr__(self):
        return f"KH2PlaceScript({self.map.value}, {self.battle.value}, {self.event.value})"


class KH2FMPlaceScript:
    def __init__(self, offset, data):
        self.map = U8(offset+0x00, data)
        self.map2 = U8(offset+0x01, data)
        self.battle = U8(offset+0x02, data)
        self.battle2 = U8(offset+0x03, data)
        self.event = U8(offset+0x04, data)
        self.event2 = U8(offset+0x05, data)
    
    def __repr__(self):
        return f"KH2FMPlaceScript({self.map.value}, {self.map2.value}, {self.battle.value}, {self.battle2.value}, {self.event.value}, {self.event2.value})"


class KH2Minigame:
    def __init__(self, name, data):
        self.name = name
        self.type = c_uint(int.from_bytes(data[0:4][::-1]))
        self.score = c_uint(int.from_bytes(data[4:8][::-1]))
    
    @property
    def value(self):
        if self.type.value == 0:
            return f"No Score ({self.score.value})"
        if self.type.value == 2:
            return f"Round {self.score.value}"
        if self.type.value == 3:
            return f"{self.score.value} Points"
        if self.type.value == 4:
            m = self.score.value // 3600
            s = (self.score.value % 3600) // 60
            f = ((self.score.value % 3600) % 60) * 100 // 60
            return f"Time: {m:02d}'{s:02d}''{f:02d}"
        if self.type.value == 6:
            return f"{self.score.value} Swings"
        return f"{self.score.value} Points, Type: {self.type.value}"
    
    def save(self, obj):
        i = obj.minigame_list.index(self.name)
        offset = 0x2E5C + i * 8
        if obj.version == 1:
            offset = 0x2DC0 + i * 8
        if obj.fm:
            offset = 0x3DB4 + i * 8
        obj.data[offset:offset+4] = bytearray(self.type)
        obj.data[offset+4:offset+8] = bytearray(self.score)
    
    def __repr__(self):
        return f"{self.name}: {self.value}"


class KH2GummiBlock:
    def __init__(self, data):
        pass


class KH2GummiShip:
    def __init__(self, data):
        pass
