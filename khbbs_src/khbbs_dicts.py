from .dicts import *


def dicts(obj):
    main_dicts(obj)

def main_dicts(obj):
    obj.character_dict = {
        "None": 0x00,
        "Ventus": 0x01,
        "Aqua": 0x02,
        "Terra": 0x03,
        "Armored Ventus": 0x04,
        "Armored Aqua": 0x05,
        "Armored Terra": 0x06,
    }
