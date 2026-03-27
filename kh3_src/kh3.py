import os
import struct

import hashlib
import zlib

from Crypto.Cipher import AES
from ctypes import *
from .kh3_dicts import dicts


class KH3Character:
    """
    The struct is 0x9C0 bytes long.
    """
    def __init__(self, name, data):
        self.data = data
        self.name = name


class KH3:
    def __init__(self, slot=0, account=""):
        dicts(self)
        if slot != 0:
            self.filename = f"KHIII_slot{slot}.bin"
            with open("files/kh3/" + self.filename, "rb") as file:
                self.data = bytearray(file.read())
            self.__get_account(account)
            self.__get_key()
            self.aes = AES.new(self.key, AES.MODE_ECB)
            if self.data[:4] != bytearray("S@vE", "utf-8"):
                self.decrypt()
                assert(self.data[:4] == bytearray("S@vE", "utf-8"))
            self.__parse_data(memoryview(self.data))
    
    def __parse_data(self, data):
        self.header = bytearray(data[0x00:0x04]).decode() # "S@vE"
        self.filesize = c_uint(int.from_bytes(data[0x04:0x08][::-1]))
        self.major_version = c_ushort(int.from_bytes(data[0x08:0x0A][::-1]))
        self.minor_version = c_ushort(int.from_bytes(data[0x0A:0x0C][::-1]))
        self.checksum = c_uint(int.from_bytes(data[0x0C:0x10][::-1]))
        self.difficulty = c_ubyte(data[0x14])
        self.world_logo = c_ubyte(data[0x18])
        self.playtime = c_uint(int.from_bytes(data[0x20:0x24][::-1]))
        self.exp = c_uint(int.from_bytes(data[0x24:0x28][::-1]))
        self.munny = c_uint(int.from_bytes(data[0x28:0x2C][::-1]))
        self.level = c_ubyte(data[0x2C])
        self.desire = c_ubyte(data[0x30])
        self.power = c_ubyte(data[0x31])
        self.party = (c_ubyte*5)(*data[0x32:0x37])
        self.save_clear = c_ubyte(data[0x39])
        self.save_location = c_ubyte(data[0x54])
        self.save_icon = c_ubyte(data[0x60])
        self.save_icon_dlc = c_ubyte(data[0x68])
        characters = data[0x1880:0xB480]
        self.keychain_upgrades = (c_ubyte*24)(*data[0xBB78:0xBB90])
    
    def save(self):
        mv = memoryview(self.data)
        mv[0x14] = self.difficulty.value
        mv[0x18] = self.world_logo.value
        mv[0x20:0x24] = bytearray(self.playtime)
        mv[0x24:0x28] = bytearray(self.exp)
        mv[0x28:0x2C] = bytearray(self.munny)
        mv[0x2C] = self.level.value
        mv[0x30] = self.desire.value
        mv[0x31] = self.power.value
        mv[0x32:0x37] = bytearray(self.party)
        
        # Checksum calculation right before dumping
        self.checksum.value = zlib.crc32(bytearray(self.data[0x10:0x10+self.filesize.value]))
        mv[0x0C:0x10] = bytearray(self.checksum)
        
        os.makedirs("saved/kh3/decrypted", exist_ok=True)
        with open(os.path.join("saved", "kh3", "decrypted", self.filename), "wb") as file:
            file.write(self.data)
        with open(os.path.join("saved", "kh3", self.filename), "wb") as file:
            file.write(self.encrypt())
        
    def decrypt(self):
        self.data = bytearray(self.aes.decrypt(self.data[:-17]))
    
    def encrypt(self):
        md5 = hashlib.md5(self.data[:self.filesize.value + 16]).digest()
        encrypted = bytearray(self.aes.encrypt(self.data))
        encrypted += bytearray([8]) + md5
        return encrypted
    
    def __get_account(self, account):
        os.makedirs("files/kh3/keys", exist_ok=True)
        if account == "":
            keys = os.listdir("files/kh3/keys")
            if len(keys) == 0:
                self.account = "1638"
            else:
                self.account = keys[0][:-4]
        else:
            self.account = account

    # Thanks for dedede123 for sharing that
    # PowerShell script on the OpenKH Discord!
    # The algorithm is just my port of that script's.
    def __get_key(self):
        self.key = bytearray(32)
        account = bytearray(self.account, "utf-8")
        key_mask = bytearray(
            "hN96q4X9f%BCURBV&pMT4kcvqTMhHYD&",
            "utf-8"
        )
        key_idx = bytearray(
            "ABCDE!#$%&FGHIJ012345KLMNOPqrstuvwxyzQRSTUVWXYZ6789abcdefgh},.<>ijklmnop()=~|-^+*;:[]{/?_@",
            "utf-8"
        )
        j = 1
        for i in range(32):
            idx = (key_mask[i] ^ account[j % len(account)]) % 0x5A
            self.key[i] = key_idx[idx]
            j += 1
        with open(os.path.join("files", "kh3", "keys", self.account + ".bin"), "wb") as file:
            file.write(self.key)
