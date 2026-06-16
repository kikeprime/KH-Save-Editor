import struct
from ctypes import *


class Array:
    def __init__(self, datatype, n, offset, data):
        self.datatype = datatype
        self.n = n
        self.offset = offset
        self.data = data
        self.array = [
            datatype(offset+i*datatype.size, data)\
            for i in range(self.n)
        ]
    
    def __getitem__(self, subscript):
        return self.array[subscript].value
    
    def __setitem__(self, key, value):
        self.array[key].value = value
    
    def __len__(self):
        return len(self.array)

    def __repr__(self):
        return str(self.array)


class U8:
    size = 1
    def __init__(self, offset, data):
        self.offset = offset
        self.data = data
    
    @property
    def value(self):
        return self.data[self.offset]
    
    @value.setter
    def value(self, v):
        self.data[self.offset] = v
    
    def __repr__(self):
        return str(self.value)


class U16:
    size = 2
    def __init__(self, offset, data):
        self.offset = offset
        self.data = data
    
    @property
    def value(self):
        return c_ushort(int.from_bytes(self.data[self.offset:self.offset+2][::-1])).value
    
    @value.setter
    def value(self, v):
        self.data[self.offset:self.offset+2] = bytearray(c_ushort(v))
    
    def __repr__(self):
        return str(self.value)


class S16:
    size = 2
    def __init__(self, offset, data):
        self.offset = offset
        self.data = data
    
    @property
    def value(self):
        return c_short(int.from_bytes(self.data[self.offset:self.offset+2][::-1])).value
    
    @value.setter
    def value(self, v):
        self.data[self.offset:self.offset+2] = bytearray(c_short(v))
    
    def __repr__(self):
        return str(self.value)


class U32:
    size = 4
    def __init__(self, offset, data):
        self.offset = offset
        self.data = data
    
    @property
    def value(self):
        return c_uint(int.from_bytes(self.data[self.offset:self.offset+4][::-1])).value
    
    @value.setter
    def value(self, v):
        self.data[self.offset:self.offset+4] = bytearray(c_uint(v))
    
    def __repr__(self):
        return str(self.value)


class S32:
    size = 4
    def __init__(self, offset, data):
        self.offset = offset
        self.data = data
    
    @property
    def value(self):
        return c_int(int.from_bytes(self.data[self.offset:self.offset+4][::-1])).value
    
    @value.setter
    def value(self, v):
        self.data[self.offset:self.offset+4] = bytearray(c_int(v))
    
    def __repr__(self):
        return str(self.value)


class F32:
    size = 4
    def __init__(self, offset, data):
        self.offset = offset
        self.data = data
    
    @property
    def value(self):
        return c_float(*struct.unpack("<f", bytearray(self.data[self.offset:self.offset+4]))).value
    
    @value.setter
    def value(self, v):
        self.data[self.offset:self.offset+4] = bytearray(c_float(v))
    
    def __repr__(self):
        return str(self.value)
