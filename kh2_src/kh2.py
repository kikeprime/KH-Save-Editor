import os
import struct

from ctypes import *
from .kh2_dicts import *


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
        inventory_dicts(self)
        return f"{self.name}(Level: {self.level.value}, Weapon: {list(self.item_dict.keys())[self.weapon.value]})"


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
        if self.name != "Antiform":
            return f"{self.name}(Level: {self.level.value}, Weapon: {self.weapon.value}, EXP: {self.exp.value})"
        else:
            return f"{self.name}(Level: {self.level.value}, Weapon: {self.weapon.value}, Antipoints: {self.exp.value})"


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
    def __init__(self, data):
        self.map = data[0]
        self.battle = data[1]
        self.event = data[2]

    def __repr__(self):
        return f"KH2PlaceScript({self.map}, {self.battle}, {self.event})"


class KH2FMPlaceScript:
    def __init__(self, data):
        self.map = data[0]
        self.map2 = data[1]
        self.battle = data[2]
        self.battle2 = data[3]
        self.event = data[4]
        self.event2 = data[5]
    
    def __repr__(self):
        return f"KH2FMPlaceScript({self.map}, {self.map2}, {self.battle}, {self.battle2}, {self.event}, {self.event2})"


class KH2GummiBlock:
    def __init__(self, data):
        pass


class KH2GummiShip:
    def __init__(self, data):
        pass


class KH2:
    def __init__(self, slot=0, version=1):
        dicts(self)
        if slot != 0:
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
            if os.path.exists(os.path.join("files", self.filename, self.filename)):
                with open(os.path.join("files", self.filename, self.filename), "rb") as file:
                    self.data = (c_ubyte*self.filesize)(*file.read())
            else:
                with open("files/" + self.filename, "rb") as file:
                    self.data = (c_ubyte*self.filesize)(*file.read())
            self.__parse_data(self.data)
            self.sysdata = None
            if os.path.exists(os.path.join("files", self.filename[:-2]+"SYS", self.filename[:-2]+"SYS")):
                with open(os.path.join("files", self.filename[:-2]+"SYS", self.filename[:-2]+"SYS"), "rb") as sysfile:
                    self.sysdata = (c_ubyte*0x400)(*sysfile.read())

    def __parse_data(self, data):
        # For FM the currently loaded save file starts at 0x32BB30 in the memory.
        # For vanilla USA it starts at 0x33E860.
        # For vanilla JP it starts at 0x33DCE0.
        self.header = bytearray(data[0x00:0x04]) # KH2 + region specific letter: J for JP/FM, U for USA
        # JP: 0x2A, USA: 0x2D, FM: 0x3A
        self.ver = c_uint(int.from_bytes(data[0x04:0x08]))
        self.checksum = c_uint(int.from_bytes(data[0x08:0x0C]))
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
        self.inventory = (c_ubyte*0x118)(*data[0x2524:0x263C])
        self.exp = c_uint(int.from_bytes(data[0x2684:0x2688][::-1]))
        self.shortcuts = (c_ushort*4)(*struct.unpack("<4H", bytearray(data[0x269C:0x26A4])))
        self.bonuslevel = c_uint(int.from_bytes(data[0x26A4:0x26A8][::-1]))
        self.heartless = (c_uint*0x2F)(*struct.unpack("<47I", bytearray(data[0x26EC:0x27A8])))
        self.nobodies = (c_uint*0x0C)(*struct.unpack("<12I", bytearray(data[0x286C:0x289C])))
        self.rc_usage = (c_ushort*0x30)(*struct.unpack("<48H", bytearray(data[0x28EE:0x294E])))
        self.limit_usage = (c_ushort*0x15)(*struct.unpack("<21H", bytearray(data[0x2CEC:0x2D16])))
    
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
        self.inventory = (c_ubyte*0x118)(*data[0x2488:0x25A0])
        self.exp = c_uint(int.from_bytes(data[0x25E8:0x25EC][::-1]))
        
        self.shortcuts = (c_ushort*4)(*struct.unpack("<4H", bytearray(data[0x2600:0x2608])))
        self.bonuslevel = c_uint(int.from_bytes(data[0x2608:0x260C][::-1]))
        
        self.heartless = (c_uint*0x2F)(*struct.unpack("<47I", bytearray(data[0x2650:0x270C])))
        self.nobodies = (c_uint*0x0C)(*struct.unpack("<12I", bytearray(data[0x27D0:0x2800])))
        self.rc_usage = (c_ushort*0x30)(*struct.unpack("<48H", bytearray(data[0x2852:0x28B2])))
        self.limit_usage = (c_ushort*0x15)(*struct.unpack("<21H", bytearray(data[0x2C50:0x2C7A])))
        
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
        self.munny = c_uint(int.from_bytes(data[0x2440:0x2444][::-1]))
        self.playtimes = (c_uint*0x15)(*struct.unpack("<21I", bytearray(data[0x2444:0x2498])))
        self.difficulty = c_ubyte(data[0x2498])
        self.puzzles = (c_ubyte*0x30)(*data[0x24A0:0x24D0])
        characters = data[0x24F0:0x32F4]
        self.characters = [
            KH2FMCharacter(k, characters[v*0x114:(v+1)*0x114])\
            for k, v in self.character_dict.items()
        ]
        self.path = c_ubyte(data[0x24FE]) # One of Sora's unknown values?
        forms = data[0x32F4:0x3524]
        self.forms = [
            KH2FMDriveForm(k, forms[v*0x38:(v+1)*0x38])\
            for k, v in self.drive_form_fm_dict.items()
        ]
        self.current_form = c_ubyte(data[0x3524])
        self.current_summon = c_ubyte(data[0x3525])
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
        self.rc_usage = (c_ushort*0x30)(*struct.unpack("<48H", bytearray(data[0x394A:0x39AA])))
        self.limit_usage = (c_ushort*0x15)(*struct.unpack("<21H", bytearray(data[0x3D48:0x3D72])))
        self.weapon_backup = c_ushort(int.from_bytes(data[0x3FEA:0x3FEC]))
    
    def __save_shared(self):
        self.data[0x0C] = self.world
        self.data[0x0D] = self.room
        self.data[0x0E] = self.flag
        for c in self.characters:
            c.save(self)
        for f in self.forms:
            f.save(self)
    
    def __save_vanilla_jp(self):
        self.data[0x1600:0x1604] = bytearray(self.munny)
        self.data[0x1604:0x1658] = bytearray(self.playtimes)
        self.data[0x1658] = self.difficulty
        self.data[0x166E] = self.path
        self.data[0x24C8] = self.current_form
        self.data[0x24C9] = self.current_summon
        self.data[0x2524:0x263C] = bytearray(self.inventory)
        self.data[0x2684:0x2688] = bytearray(self.exp)
        self.data[0x269C:0x26A4] = bytearray(self.shortcuts)
        self.data[0x26A4:0x26A8] = bytearray(self.bonuslevel)
    
    def __save_vanilla_usa(self):
        self.data[0x1600:0x1604] = bytearray(self.munny)
        self.data[0x1604:0x1658] = bytearray(self.playtimes)
        self.data[0x1658] = self.difficulty
        self.data[0x166E] = self.path
        self.data[0x242C] = self.current_form
        self.data[0x242D] = self.current_summon
        self.data[0x2488:0x25A0] = bytearray(self.inventory)
        self.data[0x25E8:0x25EC] = bytearray(self.exp)
        self.data[0x2600:0x2608] = bytearray(self.shortcuts)
        self.data[0x2608:0x260C] = bytearray(self.bonuslevel)
        self.data[0x2650:0x270C] = bytearray(self.heartless)
        self.data[0x27D0:0x2800] = bytearray(self.nobodies)
        self.data[0x2852:0x28B2] = bytearray(self.rc_usage)
        self.data[0x2C50:0x2C7A] = bytearray(self.limit_usage)
    
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
        self.checksum = KH2.calculate_checksum(self.data)
        self.data[0x08:0x0C] = bytearray(self.checksum)
        
        os.makedirs("saved/" + self.filename, exist_ok=True)
        with open(os.path.join("saved", self.filename, self.filename), "wb") as file:
            file.write(self.data)
        if self.sysdata is not None:
            os.makedirs("saved/" + self.filename[:-2]+"SYS", exist_ok=True)
            with open(os.path.join("saved", self.filename[:-2]+"SYS", self.filename[:-2]+"SYS"), "wb") as sysfile:
                sysfile.write(self.sysdata)
    
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
