export default class KH1 {
    constructor(data, fm) {
        this.data = data;
        this.fm = fm;
        this.parse_data();
    }
    
    parse_data() {
        
    }
    
    str() {
        return "KH1(" + this.data + ", FM=" + this.fm + ")";
    }
}
