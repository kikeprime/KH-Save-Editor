export default class KH1String {
    constructor(n, offset, buffer) {
        this.n = n;
        this.offset = offset;
        this.buffer = buffer;
    }
    
    decode(codec = "kh1us") {
        let decode_table = undefined;
        switch (codec) {
            case "kh1us": {
                decode_table = this.decode_table;
                break;
            }
            default: {
                decode_table = this.decode_table;
                break;
            }
        }
        let s = "";
        for (let i = this.offset; i < this.offset + this.n; i++) {
            const b = this.buffer[i];
            switch (b) {
                case 0x08: {
                    if (i + 4 < this.offset + this.n) {
                        s += `{0x${b.toString(16).toUpperCase().padStart(2, "0")}}`;
                        s += `{0x${this.buffer[i + 1].toString(16).toUpperCase().padStart(2, "0")}}`;
                        s += `{0x${this.buffer[i + 2].toString(16).toUpperCase().padStart(2, "0")}}`;
                        s += `{0x${this.buffer[i + 3].toString(16).toUpperCase().padStart(2, "0")}}`;
                        s += `{0x${this.buffer[i + 4].toString(16).toUpperCase().padStart(2, "0")}}`;
                        i += 4;
                        break;
                    }
                }
                case 0x09: {
                    if (i + 1 < this.offset + this.n) {
                        s += decode_table[b * 0x100 + this.buffer[i + 1]];
                        i++;
                        break;
                    }
                }
                default: {
                    s += decode_table[b];
                    break;
                }
            }
        }
        return s;
    }
    
    encode(s, codec = "kh1us") {
        const out = [];
        let i = 0;
        while (i < s.length) {
            const c = s[i];
            if (c == "{") {
                const end = s.indexOf("}", i);
                if (end === -1) {
                    return false;
                }
                const token = s.slice(i, end + 1);
                out.push(this.encode_table[token]);
                i = end + 1;
                continue;
            }
            out.push(this.encode_table[c] ?? 1);
            i++;
        }
        for (i = 0; i < Math.min(this.n, out.length); i++) {
            this.buffer[this.offset + i] = out[i];
        }
        return true;
    }
    
    toString() {
        return this.decode();
    }
    
    static decode_table() {
        const decode_table = {
            0x00: "{0x00}",
            0x01: " ",
            0x02: "\n", // the encode table will include Crazycatz00's {lf}
            // 0x08 will be handled in the functions
            // 0x08 is the color control code
            // color is RGBA so 0x08 + 4 bytes
            // button prompts 0x09 and a second byte
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
            0x2a: "9",
            0x2b: "A",
            0x2c: "B",
            0x2d: "C",
            0x2e: "D",
            0x2f: "E",
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
            0x3a: "P",
            0x3b: "Q",
            0x3c: "R",
            0x3d: "S",
            0x3e: "T",
            0x3f: "U",
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
            0x4a: "f",
            0x4b: "g",
            0x4c: "h",
            0x4d: "i",
            0x4e: "j",
            0x4f: "k",
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
            0x5a: "v",
            0x5b: "w",
            0x5c: "x",
            0x5d: "y",
            0x5e: "z",
            0x5f: "!",
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
            0x6a: "・",
            0x6b: ":",
            0x6c: ";",
            0x6d: "…",
            0x6e: "-",
            0x6f: "ー",
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
            0x7a: "★",
            0x7b: "☆",
            0x7c: "↑",
            0x7d: "↓",
            0x7e: "→",
            0x7f: "←",
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
            0x8a: "{iHat}",
            0x8b: "{iMickey}",
            0x8c: "○",
            0x8d: "×",
            0x8e: "△",
            0x8f: "□",
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
            0xa9: "®",
            0xc4: "{III}",
            0xc5: "{VII}",
            0xc6: "{VIII}",
            0xc7: "{X}",
            0xc8: "Œ",
            0xc9: "œ",
            0xca: "¡",
            0xcb: "¿",
            0xcc: "À",
            0xcd: "Á",
            0xce: "Â",
            0xcf: "Ä",
            0xd0: "Ç",
            0xd1: "È",
            0xd2: "É",
            0xd3: "Ê",
            0xd4: "Ë",
            0xd5: "Ì",
            0xd6: "Í",
            0xd7: "Î",
            0xd8: "Ï",
            0xd9: "Ñ",
            0xda: "Ò",
            0xdb: "Ó",
            0xdc: "Ô",
            0xdd: "Ö",
            0xde: "Ù",
            0xdf: "Ú",
            0xe0: "Û",
            0xe1: "Ü",
            0xe2: "ẞ",
            0xe3: "à",
            0xe4: "á",
            0xe5: "â",
            0xe6: "ä",
            0xe7: "ç",
            0xe8: "è",
            0xe9: "é",
            0xea: "ê",
            0xeb: "ë",
            0xec: "ì",
            0xed: "í",
            0xee: "î",
            0xef: "ï",
            0xf0: "ñ",
            0xf1: "ò",
            0xf2: "ó",
            0xf3: "ô",
            0xf4: "ö",
            0xf5: "ù",
            0xf6: "ú",
            0xf7: "û",
            0xf8: "ü",
            0xf9: "°",
            0xFA: "{---}",
            0xfb: "》",
            0xfc: "《",
        };
        let fallback_table = {};
        for (let i = 0; i < 0x100; i++) {
            if (!(i in decode_table))
                fallback_table[i] = `{0x${i.toString(16).toUpperCase().padStart(2, "0")}}`;
        }
        return {
            ...decode_table,
            ...fallback_table,
        };
    }
    
    get decode_table() {
        return KH1String.decode_table();
    }
    
    static encode_table() {
        const encode_table = Object.fromEntries(
            Object.entries(KH1String.decode_table())
                .map(([k, v]) => [v, Number(k)])
        );
        let fallback_table = {};
        for (let i = 0; i < 0x100; i++) {
            fallback_table[`{0x${i.toString(16).toUpperCase().padStart(2, "0")}}`] = i;
        }
        return {
            ...encode_table,
            ...fallback_table,
        };
    }
    
    get encode_table() {
        return KH1String.encode_table();
    }
}
