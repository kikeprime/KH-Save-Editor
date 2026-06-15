import os
import struct

from ctypes import *
from .khbbs_dicts import dicts
from .khbbs_helper import *
from .ppsspp import PPSSPP


class KHBBS:
    def __init__(self, slot=0, version=2, attach=False):
        dicts(self)
        if slot == 0:
            slot = 100
        self.version = version
        if self.version == 0:
            self.foldername = "ULJM05600" + f"{slot-1:04d}"
            self.filesize = 0x10970
            self.syssize = 0x11C00
        elif self.version == 1:
            self.foldername = "ULUS10505" + f"{slot-1:04d}"
            self.filesize = 0x11B40
            self.syssize = 0x13750
        elif self.version == 2:
            self.foldername = "ULJM05775" + f"{slot-1:04d}"
            self.filesize = 0x11E50
            self.syssize = 0x13B80
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
                    self.sysdata = (c_ubyte*self.syssize)(*sysfile.read())
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
        # self.difficulty = c_ubyte(data[0x11]) # Zero EXP needs it to be displayed
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
        commands = data[0x33FC:0x47FC]
        self.commands = [KHBBSCommand.init(commands[i*0x0A:(i+1)*0x0A], i, self.fm) for i in range(0x200)]
        abilities = data[0x4CB0:0x4D28]
        self.abilities = {
            k: KHBBSAbility(abilities[i*4:(i+1)*4], i)\
            for k, i in zip(self.ability_list, range(len(abilities)//4))
        }
        finishers = data[0x53F0:0x5470]
        self.finishers = [KHBBSFinisher.init(finishers[i*0x08:(i+1)*0x08], i) for i in range(16)]
        # I counted multiple times and there are only 20 slots in this version.
        dlinks = data[0x5470:0x5510]
        self.dlinks = [KHBBSDLink.init(dlinks[i*0x08:(i+1)*0x08], i) for i in range(20)]
        finisher_names = data[0x5510:0x5650]
        self.finisher_names = [bytearray(finisher_names[i*0x14:(i+1)*0x14]) for i in range(16)]
        self.character = KHBBSCharacter.init(self.name, data[0x5654:0x5684])
        decks = data[0x56B0:0x58CA]
        self.decks = [KHBBSDeckJP.init(decks[i*0xB2:(i+1)*0xB2], i) for i in range(3)]
        self.deck = c_ubyte(data[0x58D8])
        self.difficulty = c_ubyte(data[0x58FC])
    
    def __parse_data_vanilla_usa(self, data):
        commands = data[0x3488:0x4888]
        self.commands = [KHBBSCommand.init(commands[i*0x0A:(i+1)*0x0A], i, self.fm) for i in range(0x200)]
        abilities = data[0x4D3C:0x4DB4]
        self.abilities = {
            k: KHBBSAbility(abilities[i*4:(i+1)*4], i)\
            for k, i in zip(self.ability_list, range(len(abilities)//4))
        }
        finishers = data[0x561C:0x569C]
        self.finishers = [KHBBSFinisher.init(finishers[i*0x08:(i+1)*0x08], i) for i in range(16)]
        dlinks = data[0x569C:0x5744]
        self.dlinks = [KHBBSDLink.init(dlinks[i*0x08:(i+1)*0x08], i) for i in range(21)]
        finisher_names = data[0x5744:0x59A4]
        self.finisher_names = [bytearray(finisher_names[i*0x26:(i+1)*0x26]) for i in range(16)]
        self.character = KHBBSCharacter.init(self.name, data[0x59A8:0x59D8])
        decks = data[0x5A04:0x5C50]
        self.decks = [KHBBSDeck.init(decks[i*0xC4:(i+1)*0xC4], i) for i in range(3)]
        self.deck = c_ubyte(data[0x5C60])
        self.difficulty = c_ubyte(data[0x5C84])
    
    def __parse_data_fm(self, data):
        key_inventory = data[0x325A:0x32BE]
        inventory = data[0x335A:0x338A]
        key_inventory_new = data[0x33B8:0x3410]
        commands = data[0x3498:0x4898]
        self.commands = [KHBBSCommand.init(commands[i*0x0A:(i+1)*0x0A], i, self.fm) for i in range(0x200)]
        abilities = data[0x4D64:0x4DDC]
        self.abilities = {
            k: KHBBSAbility(abilities[i*4:(i+1)*4], i)\
            for k, i in zip(self.ability_list, range(len(abilities)//4))
        }
        self.command_styles = (c_ubyte*0x0D)(*data[0x4DDD:0x4DEA])
        self.unversed_killed = c_uint(int.from_bytes(data[0x4F18:0x4F1C][::-1]))
        finishers = data[0x5644:0x56C4]
        self.finishers = [KHBBSFinisher.init(finishers[i*0x08:(i+1)*0x08], i) for i in range(16)]
        dlinks = data[0x56C4:0x576C]
        self.dlinks = [KHBBSDLink.init(dlinks[i*0x08:(i+1)*0x08], i) for i in range(21)]
        finisher_names = data[0x576C:0x59CC]
        self.finisher_names = [bytearray(finisher_names[i*0x26:(i+1)*0x26]) for i in range(16)]
        self.character = KHBBSCharacter.init(self.name, data[0x59D0:0x5A00])
        decks = data[0x5A2C:0x5C78]
        self.decks = [KHBBSDeck.init(decks[i*0xC4:(i+1)*0xC4], i) for i in range(3)]
        self.deck = c_ubyte(data[0x5C88])
        self.difficulty = c_ubyte(data[0x5CAC])
        self.total_medals = c_uint(int.from_bytes(data[0xFE88:0xFE8C]))
        self.arena_missions = (c_ubyte*4)(*data[0xFE8C:0xFE90])

    def __save_shared(self):
        self.data[0x10] = self.reports
        self.data[0x11] = self.difficulty.value // 0x40
        self.data[0x14] = self.world
        self.data[0x15] = self.room
        self.data[0x16] = self.flag
        self.data[0x17] = self.character_type
        self.data[0x18:0x1C] = bytearray(self.playtime)
        for command in self.commands:
            command.save(self)
        for ability in self.abilities.values():
            ability.save(self)
        for finisher in self.finishers:
            finisher.save(self)
        for dlink in self.dlinks:
            dlink.save(self)
        self.character.save(self)
        for deck in self.decks:
            deck.save(self)
    
    def __save_vanilla_jp(self):
        self.data[0x58D8] = self.deck
        self.data[0x58FC] = self.difficulty
        for i in range(16):
            self.data[0x5510+i*0x14:0x5510+(i+1)*0x14] = self.finisher_names[i]
    
    def __save_vanilla_usa(self):
        self.data[0x5C60] = self.deck
        self.data[0x5C84] = self.difficulty
        for i in range(16):
            self.data[0x5744+i*0x26:0x5744+(i+1)*0x26] = self.finisher_names[i]
    
    def __save_fm(self):
        self.data[0x5C88] = self.deck
        self.data[0x5CAC] = self.difficulty
        for i in range(16):
            self.data[0x576C+i*0x26:0x576C+(i+1)*0x26] = self.finisher_names[i]

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
        if self.fm:
            game = "KHBBSFM"
        return f"{game}(\n    {self.character},\n    World: {self.world_dict[self.world.value]},\n)"
