from ctypes import *
FindWindowW = windll.user32.FindWindowW
SendMessageW = windll.user32.SendMessageW

class PPSSPP:
    def __init__(self, addr, size, obj):
        addr = addr
        self.size = size
        self.obj = obj
        try:
            import pymem
            self.ppsspp = pymem.Pymem("PPSSPPWindows.exe")
            win = FindWindowW("PPSSPPWnd", None)
            WM_USER_GET_BASE_POINTER = 0xB118
            lower = SendMessageW(win, WM_USER_GET_BASE_POINTER, 0, 0)
            base = lower
            self.addr = base + addr
            self.obj.data = (c_ubyte*self.size)(*self.ppsspp.read_bytes(self.addr, self.size))
        except:
            pass
        try:
            import pymem
            self.ppsspp = pymem.Pymem("PPSSPPWindows64.exe")
            win = FindWindowW("PPSSPPWnd", None)
            WM_USER_GET_BASE_POINTER = 0xB118
            lower = SendMessageW(win, WM_USER_GET_BASE_POINTER, 0, 0)
            upper = SendMessageW(win, WM_USER_GET_BASE_POINTER, 0, 1)
            base = upper * 0x100000000 + lower
            self.addr = base + addr
            self.obj.data = (c_ubyte*self.size)(*self.ppsspp.read_bytes(self.addr, self.size))
        except:
            pass

    def dump_to_emu(self):
        self.ppsspp.write_bytes(self.addr, bytes(self.obj.data), self.size)
