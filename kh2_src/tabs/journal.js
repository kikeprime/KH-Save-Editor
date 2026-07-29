import * as tabs from "./journal_tabs/index.js"

export function create_journal() {
    const kh2div = document.getElementById("kh2div");
    kh2div.innerHTML = `
    <div>
        <div>
            <h3>Entry:</h3>
            <select id="kh2jtabs">
                <option value="Journal Flags">Journal Flags</option>
                <option value="Ansem Reports">Ansem Reports</option>
                <option value="Character Files">Character Files</option>
                <option value="Bestiary">Bestiary</option>
                <option value="Treasures">Treasures</option>
                <option value="Puzzle Pieces">Puzzle Pieces</option>
                <option value="Maps">Maps</option>
                <option value="Missions">Missions</option>
                <option value="Minigames">Minigames</option>
                <option value="Synthesis Notes">Synthesis Notes</option>
            </select>
        </div>
        <div id="kh2jdiv"></div>
    </div>`;
    const kh2jtabs = document.getElementById("kh2jtabs");
    const kh2jdiv = document.getElementById("kh2jdiv");
    function tab_sel() {
        switch (kh2jtabs.value) {
            /*
            case "Journal Flags": {
                tabs.create_flags();
                break;
            }
            case "Ansem Reports": {
                tabs.create_reports();
                break;
            }
            case "Character Files": {
                tabs.create_character_files();
                break;
            }
            */
            case "Bestiary": {
                tabs.create_bestiary();
                break;
            }
            /*
            case "Treasures": {
                tabs.create_treasures();
                break;
            }
            */
            case "Minigames": {
                tabs.create_minigames();
                break;
            }
            /*
            case "Synthesis Notes": {
                tabs.create_synthesis_notes();
                break;
            }
            */
            default: {
                kh2jdiv.innerHTML = "";
                break;
            }
        }
    }
    kh2jtabs.addEventListener("change", tab_sel);
    tab_sel();
}
