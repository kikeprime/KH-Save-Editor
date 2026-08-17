import os
import struct

import hashlib
import zlib

from Crypto.Cipher import AES
from ctypes import *
from .kh3_dicts import dicts
from kh1_src.datatypes import *


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
        self.__get_account(account)
        self.__get_key()
        self.aes = AES.new(self.key, AES.MODE_ECB)
        if slot != 0:
            self.filename = f"KHIII_slot{slot}.bin"
            with open("files/kh3/" + self.filename, "rb") as file:
                self.data = bytearray(file.read())
            if self.data[:4] != bytearray("S@vE", "utf-8"):
                self.decrypt()
                assert(self.data[:4] == bytearray("S@vE", "utf-8"))
            self.mv = memoryview(self.data)
            self.__parse_data()
    
    def __parse_data(self):
        self.header = bytearray(self.mv[0x00:0x04]).decode() # "S@vE"
        self.filesize = U32(0x04, self.mv)
        self.major_version = U16(0x08, self.mv)
        self.minor_version = U16(0x0A, self.mv)
        self.checksum = U32(0x0C, self.mv)
        self.difficulty = U8(0x14, self.mv)
        self.world_logo = U8(0x18, self.mv)
        self.playtime = U32(0x20, self.mv)
        self.exp = U32(0x24, self.mv)
        self.munny = U32(0x28, self.mv)
        self.level = U8(0x2C, self.mv)
        self.desire = U8(0x30, self.mv)
        self.power = U8(0x31, self.mv)
        self.party = Array(U8, 5, 0x32, self.mv)
        self.save_clear = U8(0x39, self.mv)
        self.save_location = U8(0x54, self.mv)
        self.save_icon = U8(0x60, self.mv)
        self.save_icon_dlc = U8(0x68, self.mv)
        characters = self.mv[0x1880:0xB480]
        self.keychain_upgrades = Array(U8, 24, 0xBB78, self.mv)
        self.map_path = bytearray(self.mv[0xBBA0:0xBCA0])
        self.map_spawn = bytearray(self.mv[0xBCA0:0xBCE0])
        self.player_script = bytearray(self.mv[0xBCE0:0xBDE0])
        self.player_pawn = bytearray(self.mv[0xBDE0:0xBEE0])
    
    def save(self):
        # Checksum calculation right before dumping
        self.checksum.value = zlib.crc32(bytearray(self.data[0x10:0x10+self.filesize.value]))

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
