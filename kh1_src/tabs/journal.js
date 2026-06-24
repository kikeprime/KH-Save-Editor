import * as tabs from "./journal_tabs/index.js"

export function create_journal() {
    const kh1div = document.getElementById("kh1div");
    kh1div.innerHTML = `
    <div>
        <div>
            <h3>Entry:</h3>
            <select id="kh1jtabs">
                <option value="Journal Flags">Journal Flags</option>
                <option value="Chronicles">Chronicles</option>
                <option value="Ansem's Report">Ansem's Report</option>
                <option value="Characters">Characters</option>
                <option value="101 Dalmatians">101 Dalmatians</option>
                <option value="Trinity List">Trinity List</option>
                <option value="Mini Games">Mini Games</option>
                <option value="—Battle Record—">—Battle Record—</option>
                <option value="Treasures">Treasures</option>
                <option value="Synthesis">Synthesis</option>
            </select>
        </div>
        <div id="kh1jdiv"></div>
    </div>`;
    const kh1jtabs = document.getElementById("kh1jtabs");
    const kh1jdiv = document.getElementById("kh1jdiv");
    function tab_sel() {
        switch (kh1jtabs.value) {
            case "Journal Flags": {
                tabs.create_flags();
                break;
            }
            case "Chronicles": {
                tabs.create_chronicles();
                break;
            }
            case "Ansem's Report": {
                tabs.create_reports();
                break;
            }
            case "Characters": {
                tabs.create_journal_characters();
                break;
            }
            case "101 Dalmatians": {
                tabs.create_dalmatians();
                break;
            }
            case "Synthesis": {
                tabs.create_synthesis();
                break;
            }
            default: {
                kh1jdiv.innerHTML = "";
                break;
            }
        }
    }
    kh1jtabs.addEventListener("change", tab_sel);
    tab_sel();
}
