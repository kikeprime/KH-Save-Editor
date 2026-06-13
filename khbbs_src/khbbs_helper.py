import struct

from ctypes import *
from .khbbs_dicts import dicts


class KHBBSCharacter(Structure):
    """
    Class for representing the character struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0x30 bytes long.
    """
    _fields_ = [
        ("exp", c_int),
        ("munny", c_uint),
        ("medals", c_uint),
        ("level", c_ushort),
        ("hp", c_ushort),
        ("maxhp", c_ushort),
        ("unk12", c_ubyte*6),
        ("magic", c_ushort),
        ("defense", c_ushort),
        ("arenalevel", c_ushort),
        ("unk1e", c_ubyte*4),
        #("physical_resistance", c_ushort),
        ("fire_resistance", c_ushort),
        ("blizzard_resistance", c_ushort),
        ("thunder_resistance", c_ushort),
        ("dark_resistance", c_ushort),
        ("weapon", c_ushort),
        ("unk2c", c_ubyte*2),
        ("strength", c_ushort),
    ]
    
    def init(name, data):
        obj = KHBBSCharacter.from_buffer_copy(bytearray(data))
        obj.name = name
        return obj

    def save(self, obj):
        offset = 0
        if obj.version == 0:
            offset = 0x5654
        if obj.version == 1:
            offset = 0x59A8
        if obj.fm:
            offset = 0x59D0
        obj.data[offset:offset+sizeof(self)] = bytearray(self)

    def __repr__(self):
        dicts(self)
        return f"{self.name}(Level: {self.level}, Weapon: {list(self.weapon_dict.keys())[self.weapon]})"


class KHBBSCommand(Structure):
    """
    Class for representing the command struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0x0A bytes long.
    """
    _fields_ = [
        ("id", c_ushort),
        ("level", c_ushort),
        ("cp", c_ushort),
        ("ability", c_ushort),
        ("state", c_ushort),
    ]
    
    def init(data, idx, fm):
        obj = KHBBSCommand.from_buffer_copy(bytearray(data))
        obj.idx = idx
        obj.fm = fm
        return obj
    
    def save(self, obj):
        offset = 0
        if obj.version == 0:
            offset = 0x33FC
        if obj.version == 1:
            offset = 0x3488
        if obj.fm:
            offset = 0x3498
        offset += self.idx * 0x0A
        obj.data[offset:offset+sizeof(self)] = bytearray(self)

    def __repr__(self):
        dicts(self)
        command_dict = {v: k for k, v in self.command_dict.items()}
        ability_dict = {v: k for k, v in self.ability_dict.items()}
        name = command_dict[self.id]
        ability = ability_dict[self.ability]
        return \
            f"{name}(" +\
            f"\n\tLevel: {self.level}" +\
            f"\n\tCP: {self.cp}" +\
            f"\n\tAbility: {ability}" +\
            f"\n\tState: 0x{self.state:04X}" +\
            f"\n)"


class KHBBSAbility:
    """
    Class for handling the abilities.
    I didn't want to use properties because
    I think they bloat the code but I had to.
    I hate the Osaka Team more and more.
    """
    def __init__(self, data, idx):
        self.data = (c_ubyte*4)(*data)
        self.idx = idx
    
    @property
    def num_on(self):
        return self.data[0] % 0b1000
    
    @num_on.setter
    def num_on(self, num):
        self.data[0] &= ~0b111
        self.data[0] += num % 8
    
    @property
    def num_unlocked(self):
        return self.data[0] // 0b1000000 + (self.data[1] & (1 << 0)) * 4
    
    @num_unlocked.setter
    def num_unlocked(self, num):
        self.data[0] &= ~0b1100000
        self.data[0] += (num % 4) << 6
        self.data[1] &= ~(1 << 0)
        self.data[1] += (num // 4)
    
    def active(self, idx: int):
        return self.data[1] & (1 << idx) != 0
    
    def set_active(self, idx: int, b: bool):
        self.data[1] &= ~(1 << idx)
        if b:
            self.data[1] |= (1 << idx)
    
    @property
    def unread(self):
        return self.data[1] & (1 << 6) != 0
    
    @unread.setter
    def unread(self, b: bool):
        self.data[1] &= ~(1 << 6)
        if b:
            self.data[1] |= (1 << 6)
    
    @property
    def read(self):
        return self.data[1] & (1 << 7) != 0
    
    @read.setter
    def read(self, b: bool):
        self.data[1] &= ~(1 << 7)
        if b:
            self.data[1] |= (1 << 7)
    
    @property
    def mastered_message(self):
        return self.data[2] & (1 << 2) != 0
    
    @mastered_message.setter
    def mastered_message(self, b: bool):
        self.data[2] &= ~(1 << 2)
        if b:
            self.data[2] |= (1 << 2)
    
    def save(self, obj):
        offset = 0
        if obj.version == 0:
            offset = 0x4CB0
        if obj.version == 1:
            offset = 0x4D3C
        if obj.fm:
            offset = 0x4D64
        offset += self.idx * 0x04
        obj.data[offset+0x00:offset+0x04] = bytearray(self.data)
    
    def __repr__(self):
        dicts(self)
        name = self.ability_list[self.idx]
        return \
            f"{name}(" +\
            f"\n\tTurned on: {self.num_on}" +\
            f"\n\tUnlocked: {self.num_unlocked}" +\
            f"\n\tActive 1: {self.active(1)}" +\
            f"\n\tActive 2: {self.active(2)}" +\
            f"\n\tActive 3: {self.active(3)}" +\
            f"\n\tActive 4: {self.active(4)}" +\
            f"\n\tActive 5: {self.active(5)}" +\
            f"\n\tUnread: {self.unread}" +\
            f"\n\tRead: {self.read}" +\
            f"\n\tMastered message: {self.mastered_message}" +\
            f"\n)"


class KHBBSDLink(Structure):
    """
    Class for representing the D-Link struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0x08 bytes long.
    """
    _fields_ = [
        ("id", c_ushort),
        ("unk2", c_ubyte),
        ("state", c_ubyte),
        ("unk4", c_ubyte*4),
    ]
    
    def init(data, idx):
        obj = KHBBSDLink.from_buffer_copy(bytearray(data))
        obj.idx = idx
        return obj
    
    @property
    def on(self):
        return self.state & (1 << 7) != 0
    
    @on.setter
    def on(self, b: bool):
        self.state &= ~(1 << 7)
        if b:
            self.state |= (1 << 7)
    
    @property
    def ability_1(self):
        return self.state & (1 << 0) != 0
    
    @ability_1.setter
    def ability_1(self, b: bool):
        self.state &= ~(1 << 0)
        if b:
            self.state |= (1 << 0)
    
    @property
    def ability_2(self):
        return self.state & (1 << 1) != 0
    
    @ability_2.setter
    def ability_2(self, b: bool):
        self.state &= ~(1 << 1)
        if b:
            self.state |= (1 << 1)
    
    def save(self, obj):
        offset = 0
        if obj.version == 0:
            offset = 0x5470
        if obj.version == 1:
            offset = 0x569C
        if obj.fm:
            offset = 0x56C4
        offset += self.idx * 0x08
        obj.data[offset:offset+sizeof(self)] = bytearray(self)

    def __repr__(self):
        dicts(self)
        dlink_dict = {v: k for k, v in self.dlink_dict.items()}
        name = dlink_dict[self.id]
        return \
            f"{name}(" +\
            f"\n\tOn: {self.on}" +\
            f"\n\tAbility 1: {self.ability_1}" +\
            f"\n\tAbility 2: {self.ability_2}" +\
            f"\n\tState: 0x{self.state:02X}" +\
            f"\n)"


class KHBBSFinisher(Structure):
    """
    Class for representing the Finisher struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0x08 bytes long.
    """
    _fields_ = [
        ("id", c_ushort),
        ("state", c_ushort),
        ("exp", c_uint),
    ]
    
    def init(data, idx):
        obj = KHBBSFinisher.from_buffer_copy(bytearray(data))
        obj.idx = idx
        return obj

    def save(self, obj):
        offset = 0
        if obj.version == 0:
            offset = 0x53F0
        if obj.version == 1:
            offset = 0x561C
        if obj.fm:
            offset = 0x5644
        offset += self.idx * 0x08
        obj.data[offset:offset+sizeof(self)] = bytearray(self)

    def __repr__(self):
        dicts(self)
        finisher_dict = {v: k for k, v in self.finisher_dict.items()}
        name = finisher_dict[self.id]
        state = ["Empty", "Locked", "Unlocked"][self.state]
        return \
            f"{name}(" +\
            f"\n\tState: {state}" +\
            f"\n\tEXP: {self.exp}" +\
            f"\n)"


class KHBBSDeckCommand(Structure):
    """
    Class for representing the Deck Command struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0x06 bytes long.
    """
    _fields_ = [
        ("id", c_short),
        ("unk", c_ubyte*4),
    ]


class KHBBSDeck(Structure):
    """
    Class for representing the Deck struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0xC4 bytes long.
    """
    _fields_ = [
        ("battle_commands", KHBBSDeckCommand*8),
        ("action_commands", KHBBSDeckCommand*10),
        ("shotlock", KHBBSDeckCommand),
        ("unk72", c_ubyte*0x14),
        ("name", c_ubyte*0x10),
        ("unk96", c_ubyte*(0xC4-0x96)),
    ]
    
    def init(data, idx):
        obj = KHBBSDeck.from_buffer_copy(bytearray(data))
        obj.idx = idx
        return obj

    def save(self, obj):
        offset = 0
        if obj.version == 1:
            offset = 0x5A04
        if obj.fm:
            offset = 0x5A2C
        offset += self.idx * sizeof(self)
        obj.data[offset:offset+sizeof(self)] = bytearray(self)

    def __repr__(self):
        dicts(self)
        name = bytearray(self.name).decode("Shift-JIS")
        return \
            f"{name}(" +\
            f"\n\tBattle Commands:\n\t{bytearray(self.battle_commands)}" +\
            f"\n\tAction Commands:\n\t{bytearray(self.action_commands)}" +\
            f"\n\tShotlock:\n\t{bytearray(self.shotlock)}" +\
            f"\n)"


class KHBBSDeckJP(Structure):
    """
    Class for representing the vanilla JP Deck struct.
    So in C/C++ I'd use a struct instead.
    The structure is 0xB2 bytes long.
    I couldn't avoid full copying.
    """
    _fields_ = [
        ("battle_commands", KHBBSDeckCommand*8),
        ("action_commands", KHBBSDeckCommand*10),
        ("shotlock", KHBBSDeckCommand),
        ("unk72", c_ubyte*0x14),
        ("name", c_ubyte*0x10),
        ("unk96", c_ubyte*(0xB2-0x96)),
    ]
    
    def init(data, idx):
        obj = KHBBSDeckJP.from_buffer_copy(bytearray(data))
        obj.idx = idx
        return obj

    def save(self, obj):
        offset = 0x56B0
        offset += self.idx * sizeof(self)
        obj.data[offset:offset+sizeof(self)] = bytearray(self)

    def __repr__(self):
        dicts(self)
        name = bytearray(self.name).decode("Shift-JIS")
        return \
            f"{name}(" +\
            f"\n\tBattle Commands:\n\t{bytearray(self.battle_commands)}" +\
            f"\n\tAction Commands:\n\t{bytearray(self.action_commands)}" +\
            f"\n\tShotlock:\n\t{bytearray(self.shotlock)}" +\
            f"\n)"
