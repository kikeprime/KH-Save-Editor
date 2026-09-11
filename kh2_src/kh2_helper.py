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
    def __init__(self, name, offset, data):
        self.name = name
        self.weapon = c_ushort(int.from_bytes(data[0x00:0x02][::-1]))
        # data[0x02:0x04] is unknown; padding?
        self.hp = U8(offset+0x04, data)
        self.maxhp = U8(offset+0x05, data)
        self.mp = U8(offset+0x06, data)
        self.maxmp = U8(offset+0x07, data)
        self.apboost = U8(offset+0x08, data)
        self.strengthboost = U8(offset+0x09, data)
        self.magicboost = U8(offset+0x0A, data)
        self.defenseboost = U8(offset+0x0B, data)
        # data[0x0C:0x0F] is unknown
        # Sora's data[0x0E] is the leveling path
        self.path = U8(offset+0x0E, data)
        self.level = U8(offset+0x0F, data)
        self.armorslots = U8(offset+0x10, data)
        self.accessoryslots = U8(offset+0x11, data)
        self.itemslots = U8(offset+0x12, data)
        # data[0x13] is unknown
        self.armors = Array(U16, 0x08, offset+0x14, data)
        self.accessories = Array(U16, 0x08, offset+0x24, data)
        self.items = Array(U16, 0x08, offset+0x34, data)
        self.autoreload = Array(U16, 0x08, offset+0x44, data)
        self.abilities = Array(U16, 0x40, offset+0x54, data)
        self.battlestyle = U8(offset+0xD4, data)
        # data[0xD5:0xDB] is unknown
        # data[0xDB] is the Ability Style slot for unintended abilities
        # like giving Donald Guard and Aerial Sweep then they will share this byte.
        # I exclude it so users won't edit it due to confusion.
        self.abilitystyles = Array(U8, 0x04, offset+0xDC, data)
        # data[0xE0:0xF4] is unknown
    
    def __repr__(self):
        dicts(self)
        return f"{self.name}(Level: {self.level.value}, Weapon: {list(self.item_dict.keys())[self.weapon.value]})"


class KH2FMCharacter(KH2Character):
    """
    Class for representing the Final Mix character struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0x114 bytes long.
    """
    def __init__(self, name, offset, data):
        super().__init__(name, offset, data)
        self.abilities = Array(U16, 0x50, offset+0x54, data)
        self.battlestyle = U8(offset+0xF4, data)
        self.abilitystyles = Array(U8, 0x04, offset+0xFC, data)
        # data[0x100:0x114] is unknown


class KH2DriveForm:
    """
    Class for representing the Drive Form struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0x28 bytes long.
    """
    def __init__(self, name, offset, data):
        self.name = name
        self.weapon = U16(offset+0x00, data)
        self.level = U8(offset+0x02, data)
        self.abilitylevel = U8(offset+0x03, data)
        self.exp = U32(offset+0x04, data)
        self.abilities = Array(U16, 0x10, offset+0x08, data)
    
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
    def __init__(self, name, offset, data):
        super().__init__(name, offset, data)
        # Only difference is that 8 more abilities are possible
        self.abilities = Array(U16, 0x18, offset+0x08, data)


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
    def __init__(self, name, offset, data):
        self.name = name
        self.type = U32(offset+0x00, data)
        self.score = U32(offset+0x00, data)
    
    @property
    def value(self):
        if self.type.value == 0:
            return f"No Score ({self.score.value})"
        if self.type.value == 1:
            return f"No Score, Type: 1 ({self.score.value})"
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
    
    def __repr__(self):
        return f"{self.name}: {self.value}"


class KH2GummiBlock:
    def __init__(self, data):
        pass


class KH2GummiShip:
    def __init__(self, data):
        pass
