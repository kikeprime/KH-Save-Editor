from ctypes import *


class PCSX2:
    def __init__(self, addr, size, obj):
        addr = addr
        self.size = size
        self.obj = obj
        # 1.6.0 forks
        try:
            import pymem
            self.pcsx2 = pymem.Pymem("pcsx2.exe")
            EEmem = 0x20000000
            self.addr = EEmem + addr
            self.obj.data = (c_ubyte*self.size)(*self.pcsx2.read_bytes(self.addr, self.size))
        except:
            pass
        # Qt versions
        try:
            import pymem
            self.pcsx2 = pymem.Pymem("pcsx2-qt.exe")
            base = self.pcsx2.base_address
            EEmem = 0
            dos = self.pcsx2.read_bytes(base, 0x40)  # IMAGE_DOS_HEADER
            e_lfanew = int.from_bytes(dos[0x3C:0x40], "little")
            nt = self.pcsx2.read_bytes(base + e_lfanew, 0xF8)  # IMAGE_NT_HEADERS64
            export_rva = int.from_bytes(nt[0x88:0x8C], "little")
            export_dir = self.pcsx2.read_bytes(base + export_rva, 0x28)
            num_names = int.from_bytes(export_dir[0x18:0x1C], "little")
            names_rva = int.from_bytes(export_dir[0x20:0x24], "little")
            funcs_rva = int.from_bytes(export_dir[0x1C:0x20], "little")
            for i in range(num_names):
                name_rva = self.pcsx2.read_int(base + names_rva + i*4)
                name = self.pcsx2.read_string(base + name_rva)
                if name == "EEmem":
                    fn_rva = self.pcsx2.read_int(base + funcs_rva + i*4)
                    pointer_addr = base + fn_rva
                    EEmem = self.pcsx2.read_ulonglong(pointer_addr)
                    break
            self.addr = EEmem + addr
            self.obj.data = (c_ubyte*self.size)(*self.pcsx2.read_bytes(self.addr, self.size))
        except:
            pass
    
    def dump_to_emu(self):
        self.pcsx2.write_bytes(self.addr, bytes(self.obj.data), self.size)
