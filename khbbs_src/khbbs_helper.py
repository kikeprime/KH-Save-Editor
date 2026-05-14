import struct

from ctypes import *
from .khbbs_dicts import dicts


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
        offset = 0
        if obj.version == 0:
            offset = 0x5654
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


class KHBBSCommand:
    """
    Class for representing the command struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0x0A bytes long.
    """
    def __init__(self, data, idx, fm):
        self.idx = idx
        self.fm = fm
        self.id = c_ushort(int.from_bytes(data[0x00:0x02][::-1]))
        self.level = c_ushort(int.from_bytes(data[0x02:0x04][::-1]))
        self.cp = c_ushort(int.from_bytes(data[0x04:0x06][::-1]))
        self.ability = c_ushort(int.from_bytes(data[0x06:0x08][::-1]))
        self.flags = c_ushort(int.from_bytes(data[0x08:0x0A][::-1]))
    
    def save(self, obj):
        offset = 0
        if obj.version == 0:
            offset = 0x33FC
        if obj.version == 1:
            offset = 0x3488
        if obj.fm:
            offset = 0x3498
        offset += self.idx * 0x0A
        obj.data[offset+0x00:offset+0x02] = bytearray(self.id)
        obj.data[offset+0x02:offset+0x04] = bytearray(self.level)
        obj.data[offset+0x04:offset+0x06] = bytearray(self.cp)
        obj.data[offset+0x06:offset+0x08] = bytearray(self.ability)
        obj.data[offset+0x08:offset+0x0A] = bytearray(self.flags)

    def __repr__(self):
        dicts(self)
        command_dict = {v: k for k, v in self.command_dict.items()}
        ability_dict = {v: k for k, v in self.ability_dict.items()}
        name = command_dict[self.id.value]
        ability = ability_dict[self.ability.value]
        return f"{name}(Level: {self.level.value}, CP: {self.cp.value}, Ability: {ability}, Flags: 0x{self.flags.value:04X})"
