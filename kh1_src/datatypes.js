export function Array(datatype, n, offset, data) {
    const array = [];
    for (let i = 0; i < n; i++) {
        array.push(
            new datatype(offset + i * datatype.size, data)
        );
    }
    return new Proxy(array, {
        get(a, idx) {
            if (typeof idx == "string" && Number.isInteger(Number(idx)))
                return a[idx].value;
            return a[idx];
        },
        set(a, idx, value) {
            if (typeof idx == "string" && Number.isInteger(Number(idx))) {
                a[idx].value = value;
                return true;
            }
            a[idx] = value;
            return true;
        },
    });
}

export class U8 {
    static size = 1;
    
    constructor(offset, data) {
        this.offset = offset;
        this.data = data;
    }
    
    get value() {
        return this.data.getUint8(this.offset);
    }
    
    set value(x) {
        return this.data.setUint8(this.offset, x);
    }
}

export class U16 {
    static size = 2;
    
    constructor(offset, data) {
        this.offset = offset;
        this.data = data;
    }
    
    get value() {
        return this.data.getUint16(this.offset, true);
    }
    
    set value(x) {
        return this.data.setUint16(this.offset, x, true);
    }
}

export class S16 {
    static size = 2;
    
    constructor(offset, data) {
        this.offset = offset;
        this.data = data;
    }
    
    get value() {
        return this.data.getInt16(this.offset, true);
    }
    
    set value(x) {
        return this.data.setInt16(this.offset, x, true);
    }
}

export class U32 {
    static size = 4;
    
    constructor(offset, data) {
        this.offset = offset;
        this.data = data;
    }
    
    get value() {
        return this.data.getUint32(this.offset, true);
    }
    
    set value(x) {
        return this.data.setUint32(this.offset, x, true);
    }
}

export class S32 {
    static size = 4;
    
    constructor(offset, data) {
        this.offset = offset;
        this.data = data;
    }
    
    get value() {
        return this.data.getInt32(this.offset, true);
    }
    
    set value(x) {
        return this.data.setInt32(this.offset, x, true);
    }
}

export class F32 {
    static size = 4;
    
    constructor(offset, data) {
        this.offset = offset;
        this.data = data;
    }
    
    get value() {
        return this.data.getFloat32(this.offset, true);
    }
    
    set value(x) {
        return this.data.setFloat32(this.offset, x, true);
    }
}
