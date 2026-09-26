# Copilot taught me to setup the codecs but the codecs are now written by entirely me.
# Control codes from Crazycatz00's String Mapper
# String Mapper compatible

import codecs

decode_table = {
    0x00: "{eol}",
    0x01: " ",
    0x02: "{lf}", # the encode table will include Crazycatz00's {lf}
    # 0x08 will be handled in the functions
    # 0x08 is the color control code
    # color is RGBA so 0x08 + 4 bytes
    # button prompts 0x09 and a second byte
    0x0900: "{controller:squ}",
    0x0901: "{controller:tri}",
    0x0902: "{controller:x}",
    0x0903: "{controller:o}",
    0x0904: "{controller:analog}",
    0x0905: "{controller:arrows}",
    0x0906: "{controller:l1}",
    0x0907: "{controller:l2}",
    0x0908: "{controller:r1}",
    0x0909: "{controller:r2}",
    0x20: "—",
    0x21: "0",
    0x22: "1",
    0x23: "2",
    0x24: "3",
    0x25: "4",
    0x26: "5",
    0x27: "6",
    0x28: "7",
    0x29: "8",
    0x2A: "9",
    0x2B: "A",
    0x2C: "B",
    0x2D: "C",
    0x2E: "D",
    0x2F: "E",
    0x30: "F",
    0x31: "G",
    0x32: "H",
    0x33: "I",
    0x34: "J",
    0x35: "K",
    0x36: "L",
    0x37: "M",
    0x38: "N",
    0x39: "O",
    0x3A: "P",
    0x3B: "Q",
    0x3C: "R",
    0x3D: "S",
    0x3E: "T",
    0x3F: "U",
    0x40: "V",
    0x41: "W",
    0x42: "X",
    0x43: "Y",
    0x44: "Z",
    0x45: "a",
    0x46: "b",
    0x47: "c",
    0x48: "d",
    0x49: "e",
    0x4A: "f",
    0x4B: "g",
    0x4C: "h",
    0x4D: "i",
    0x4E: "j",
    0x4F: "k",
    0x50: "l",
    0x51: "m",
    0x52: "n",
    0x53: "o",
    0x54: "p",
    0x55: "q",
    0x56: "r",
    0x57: "s",
    0x58: "t",
    0x59: "u",
    0x5A: "v",
    0x5B: "w",
    0x5C: "x",
    0x5D: "y",
    0x5E: "z",
    0x5F: "!",
    0x60: "?",
    0x61: "&",
    0x62: "%",
    0x63: "+",
    0x64: "{-}",
    0x65: "{mX}",
    0x66: "/",
    0x67: "*",
    0x68: ".",
    0x69: ",",
    0x6A: "・",
    0x6B: ":",
    0x6C: ";",
    0x6D: "…",
    0x6E: "-",
    0x6F: "ー",
    0x70: "~",
    0x71: "'",
    0x72: "“",
    0x73: "{゛b}",
    0x74: "(",
    0x75: ")",
    0x76: "[",
    0x77: "]",
    0x78: "<",
    0x79: ">",
    0x7A: "★",
    0x7B: "☆",
    0x7C: "↑",
    0x7D: "↓",
    0x7E: "→",
    0x7F: "←",
    0x80: "●",
    0x81: "■",
    0x82: "{iPotion}",
    0x83: "{iTent}",
    0x84: "{iGem}",
    0x85: "{iAbility}",
    0x86: "{iKey}",
    0x87: "{iStaff}",
    0x88: "{iShield}",
    0x89: "{iRing}",
    0x8A: "{iHat}",
    0x8B: "{iMickey}",
    0x8C: "○",
    0x8D: "×",
    0x8E: "△",
    0x8F: "□",
    0x90: "▲",
    0x91: "▼",
    0x92: "►",
    0x93: "◄",
    0x94: "{iGummi0}",
    0x95: "{iGummi1}",
    0x96: "{iGummi2}",
    0x97: "{iGummi3}",
    0x98: "{iGummi4}",
    0x99: "{iGummi5}",
    0x9a: "{iGummi6}",
    0x9b: "{iGummi7}",
    0x9c: "{iGummi8}",
    0x9d: "{iGummi9}",
    0xA9: "®",
    0xC4: "{III}",
    0xC5: "{VII}",
    0xC6: "{VIII}",
    0xC7: "{X}",
    0xC8: "Œ",
    0xC9: "œ",
    0xCA: "¡",
    0xCB: "¿",
    0xCC: "À",
    0xCD: "Á",
    0xCE: "Â",
    0xCF: "Ä",
    0xD0: "Ç",
    0xD1: "È",
    0xD2: "É",
    0xD3: "Ê",
    0xD4: "Ë",
    0xD5: "Ì",
    0xD6: "Í",
    0xD7: "Î",
    0xD8: "Ï",
    0xD9: "Ñ",
    0xDA: "Ò",
    0xDB: "Ó",
    0xDC: "Ô",
    0xDD: "Ö",
    0xDE: "Ù",
    0xDF: "Ú",
    0xE0: "Û",
    0xE1: "Ü",
    0xE2: "ẞ",
    0xE3: "à",
    0xE4: "á",
    0xE5: "â",
    0xE6: "ä",
    0xE7: "ç",
    0xE8: "è",
    0xE9: "é",
    0xEA: "ê",
    0xEB: "ë",
    0xEC: "ì",
    0xED: "í",
    0xEE: "î",
    0xEF: "ï",
    0xF0: "ñ",
    0xF1: "ò",
    0xF2: "ó",
    0xF3: "ô",
    0xF4: "ö",
    0xF5: "ù",
    0xF6: "ú",
    0xF7: "û",
    0xF8: "ü",
    0xF9: "°",
    0xFA: "{---}",
    0xFB: "》",
    0xFC: "《",
}
decode_table = decode_table | \
               {i: "{" + f"0x{i:02X}" + "}" for i in range(0x100) if i not in decode_table.keys()}
encode_table = {v: k for k, v in decode_table.items()} | \
               {"{" + f"0x{i:02X}" + "}": i for i in range(0x100)} | \
               {"{" + f"{i:#02x}" + "}": i for i in range(0x100)} | \
               {"{" + f"{i:#02X}" + "}": i for i in range(0x100)} | \
               {"{" + f"0X{i:02x}" + "}": i for i in range(0x100)}
decode_table_jp = {
    0x00: "{eol}",
    0x01: " ",
    0x02: "{lf}",
    0x20: "—",
    0x21: "0",
    0x22: "1",
    0x23: "2",
    0x24: "3",
    0x25: "4",
    0x26: "5",
    0x27: "6",
    0x28: "7",
    0x29: "8",
    0x2A: "9",
    0x2B: "+",
    0x2C: "-",
    0x2D: "{mX}",
    0x2E: "A",
    0x2F: "B",
    0x30: "C",
    0x31: "D",
    0x32: "E",
    0x33: "F",
    0x34: "G",
    0x35: "H",
    0x36: "I",
    0x37: "J",
    0x38: "K",
    0x39: "L",
    0x3A: "M",
    0x3B: "N",
    0x3C: "O",
    0x3D: "P",
    0x3E: "Q",
    0x3F: "R",
    0x40: "S",
    0x41: "T",
    0x42: "U",
    0x43: "V",
    0x44: "W",
    0x45: "X",
    0x46: "Y",
    0x47: "Z",
    0x48: "!",
    0x49: "?",
    0x4A: "%",
    0x4B: "/",
    0x4C: "※",
    0x4D: "、",
    0x4E: "。",
    0x4F: ".",
    0x50: ",",
    0x51: ".",
    0x52: ":",
    0x53: "…",
    0x55: "ー",
    0x56: "~",
    0x57: "'",
    0x58: "゛",
    0x71: "×",
    0x90: "あ",
    0x91: "い",
    0x92: "う",
    0x93: "え",
    0x94: "お",
    0x95: "か",
    0x96: "き",
    0x97: "く",
    0x98: "け",
    0x99: "こ",
    0x9A: "さ",
    0x9B: "し",
    0x9C: "す",
    0x9D: "せ",
    0x9E: "そ",
    0x9F: "た",
    0xA0: "ち",
    0xA1: "つ",
    0xA2: "て",
    0xA3: "と",
    0xA4: "な",
    0xA5: "に",
    0xA6: "ぬ",
    0xA7: "ね",
    0xA8: "の",
    0xA9: "は",
    0xAA: "ひ",
    0xAB: "ふ",
    0xAC: "へ",
    0xAD: "ほ",
    0xAE: "ま",
    0xAF: "み",
    0xB0: "む",
    0xB1: "め",
    0xB2: "も",
    0xB3: "や",
    0xB4: "ゆ",
    0xB5: "よ",
    0xB6: "ら",
    0xB7: "り",
    0xB8: "る",
    0xB9: "れ",
    0xBA: "ろ",
    0xBB: "わ",
    0xBC: "を",
    0xBD: "ん",
    0xBE: "が",
    0xBF: "ぎ",
    0xC0: "ぐ",
    0xC1: "げ",
    0xC2: "ご",
    0xC3: "ざ",
    0xC2: "ご",
    0xC3: "ざ",
    0xC4: "じ",
    0xC5: "ず",
    0xC6: "ぜ",
    0xC7: "ぞ",
    0xC8: "だ",
    0xC9: "ぢ",
    0xCA: "づ",
    0xCB: "で",
    0xCC: "ど",
    0xCD: "ば",
    0xCE: "び",
    0xCF: "ぶ",
    0xD0: "べ",
    0xD1: "ぼ",
    0xD2: "ぱ",
    0xD3: "ぴ",
    0xD4: "ぷ",
    0xD5: "ぺ",
    0xD6: "ぽ",
    0xD7: "ぁ",
    0xD8: "ぃ",
    0xD9: "ぅ",
    0xDA: "ぇ",
    0xDB: "ぉ",
    0xDC: "ゃ",
    0xDD: "ゅ",
    0xDE: "ょ",
    0xDF: "っ",
    0xE0: "ア",
    0xE1: "イ",
    0xE2: "ウ",
    0xE3: "エ",
    0xE4: "オ",
    0xE5: "カ",
    0xE6: "キ",
    0xE7: "ク",
    0xE8: "ケ",
    0xE9: "コ",
    0xEA: "サ",
    0xEB: "シ",
    0xEC: "ス",
    0xED: "セ",
    0xEE: "ソ",
    0xEF: "タ",
    0xF0: "チ",
    0xF1: "ツ",
    0xF2: "テ",
    0xF3: "ト",
    0xF4: "ナ",
    0xF5: "ニ",
    0xF6: "ヌ",
    0xF7: "ネ",
    0xF8: "ノ",
    0xF9: "ハ",
    0xFA: "ヒ",
    0xFB: "フ",
    0xFC: "ヘ",
    0xFD: "ホ",
    0xFE: "マ",
    0xFF: "ミ",
    0x1819: "ム",
    0x181A: "珍",
    0x181B: "何",
    0x1900: "{ム}",
    0x1901: "メ",
    0x1902: "モ",
    0x1903: "ヤ",
    0x1904: "ユ",
    0x1905: "ヨ",
    0x1906: "ラ",
    0x1907: "リ",
    0x1908: "ル",
    0x1909: "レ",
    0x190A: "ロ",
    0x190B: "ワ",
    0x190C: "ヲ",
    0x190D: "ン",
    0x190E: "ガ",
    0x190F: "ギ",
    0x1910: "グ",
    0x1911: "ゲ",
    0x1912: "ゴ",
    0x1913: "ザ",
    0x1914: "ジ",
    0x1915: "ズ",
    0x1916: "ゼ",
    0x1917: "ゾ",
    0x1918: "ダ",
    0x1919: "ヂ",
    0x191A: "ヅ",
    0x191B: "デ",
    0x191C: "ド",
    0x191D: "バ",
    0x191E: "ビ",
    0x191F: "ブ",
    0x1920: "ベ",
    0x1921: "ボ",
    0x1922: "ヴ",
    0x1923: "パ",
    0x1924: "ピ",
    0x1925: "プ",
    0x1926: "ペ",
    0x1927: "ポ",
    0x1928: "ァ",
    0x1929: "ィ",
    0x192A: "ゥ",
    0x192B: "ェ",
    0x192C: "ォ",
    0x192D: "ャ",
    0x192E: "ュ",
    0x192F: "ョ",
    0x1930: "ッ",
    0x1942: "書",
    0x19A2: "巻",
}
decode_table_jp = decode_table_jp | \
               {i: "{" + f"0x{i:02X}" + "}" for i in range(0x100) if i not in decode_table_jp.keys()}
encode_table_jp = {v: k for k, v in decode_table_jp.items()} | \
               {"{" + f"0x{i:02X}" + "}": i for i in range(0x100)} | \
               {"{" + f"{i:#02x}" + "}": i for i in range(0x100)} | \
               {"{" + f"{i:#02X}" + "}": i for i in range(0x100)} | \
               {"{" + f"0X{i:02x}" + "}": i for i in range(0x100)}

# Step 2: encode/decode functions
def kh1us_encode(input_str):
    isseq = False
    seq = []
    i = 0
    out_bytes = bytearray()
    for ch in input_str:
        if ch == "{" and "}" in input_str[i:]:
            isseq = True
        if isseq and ch == "}":
            ch = "".join(seq) + ch
            isseq = False
        if isseq:
            seq.append(ch)
        elif len(seq) > 0:
            seq = []
        if not isseq:
            n = encode_table.get(ch, 0x01)
            out_bytes += bytearray(n.to_bytes((n.bit_length() + 7) // 8 if n != 0 else 1, "big"))
        i += 1
    return (bytes(out_bytes), len(input_str))

def kh1us_decode(input_bytes):
    out_chars = []
    i = 0
    while i < len(input_bytes):
        b = input_bytes[i]
        match b:
            case 0x00:
                out_chars.append(decode_table.get(b, "{" + f"0x{b:02X}" + "}"))
                break
            case 0x08:
                out_chars.append("{" + f"0x{b:02X}" + "}")
                if (i + 4 < len(input_bytes)):
                    out_chars.append("{" + f"0x{input_bytes[i+1]:02X}" + "}")
                    out_chars.append("{" + f"0x{input_bytes[i+2]:02X}" + "}")
                    out_chars.append("{" + f"0x{input_bytes[i+3]:02X}" + "}")
                    out_chars.append("{" + f"0x{input_bytes[i+4]:02X}" + "}")
                    i += 4
            case 0x09:
                out_chars.append("{" + f"0x{b:02X}" + "}")
                if (i + 1 < len(input_bytes)):
                    out_chars.append("{" + f"0x{input_bytes[i+1]:02X}" + "}")
                    i += 1
            case 0x0D:
                out_chars.append("{" + f"0x{b:02X}" + "}")
                if (i + 2 < len(input_bytes)):
                    out_chars.append("{" + f"0x{input_bytes[i+1]:02X}" + "}")
                    out_chars.append("{" + f"0x{input_bytes[i+2]:02X}" + "}")
                    i += 2
            case _:
                out_chars.append(decode_table.get(b, "{" + f"0x{b:02X}" + "}"))
        i += 1
    return ("".join(out_chars), len(input_bytes))

def kh1jp_encode(input_str):
    out_bytes = bytearray()
    for ch in input_str:
        if encode_table_jp.get(ch, 0x01) > 255:
            out_bytes += bytearray(encode_table_jp.get(ch, 0x01).to_bytes(2, "big"))
        else:
            out_bytes.append(encode_table_jp.get(ch, 0x01))
    out_bytes.append(0x00)
    return (bytes(out_bytes), len(input_str))

def kh1jp_decode(input_bytes):
    out_chars = []
    i = 0
    while i < len(input_bytes):
        b = input_bytes[i]
        if b == 0x0D and i + 1 < len(input_bytes):
            out_chars.append("{" + f"0x{b:02X}" + "}")
            b = input_bytes[i+1]
            out_chars.append("{" + f"0x{b:02X}" + "}")
            i += 2
            continue
        if 0x18 <= b <= 0x1E and i + 1 < len(input_bytes):
            b = int.from_bytes(input_bytes[i:i+2])
            i += 1
        out_chars.append(decode_table_jp.get(b, "{" + f"0x{b:02X}" + "}"))
        i += 1
        if b == 0x00:
            break
    return ("".join(out_chars), len(input_bytes))

# Step 3: search function
def kh1codec(name):
    if name == "kh1us":
        return codecs.CodecInfo(
            name="kh1us",
            encode=kh1us_encode,
            decode=kh1us_decode
        )
    if name == "kh1jp":
        return codecs.CodecInfo(
            name="kh1jp",
            encode=kh1jp_encode,
            decode=kh1jp_decode
        )
    return None

# Step 4: register it
codecs.register(kh1codec)
