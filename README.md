# Kingdom Hearts Save Editor Online
List of supported games:
- Kingdom Hearts (all vanilla releases)
- Kingdom Hearts Final Mix (Remix too)
- Kingdom Hearts II Japan
- Kingdom Hearts II USA (EU should be the same as this)
- Kingdom Hearts II Final Mix (Remix too)

Only supported in the Dash version:
- Kingdom Hearts Birth by Sleep Japan
- Kingdom Hearts Birth by Sleep USA (EU should be the same as this)
- Kingdom Hearts Birth by Sleep Final Mix (Remix too)
- Kingdom Hearts III + ReMind (PC only)

The idea to write my own save editor came from the fact that Kingdom Save Editor is abandoned and it is very barebones in terms of knowledge and it can't be run on Android. For a university assignment I had to work with the ipywidgets Python package so I thought I could use it for my save editor. It turned out that it's not optimized for small screens so I was looking for GUI packages. I mostly stayed with Python since it can be easily used on Android. So after multiple restarts and a second university class influence I landed on Dash.

However, I learned about GitHub Pages and the idea of having an online save editor fascinated me so here we go.

So I want to emphasize that the priority is to run the app on smartphones hence the overly vertical alignment.

## How to use
- Select the game and its version. The dropdown groups the selectable versions by game.
- Select a file with the browser's file picker.
- The parser doesn't care for now what file you provide so BE CAREFUL with the game and version choices!
- Make sure the selected game is correct before you press save. The game version doesn't matter but the game does.

# Features
The feature list reflects the Dash version as of writing.

## What not to expect
- Don't expect support for the PC Remix PNG files, use Kingdom Save Editor for them. I have no reason to copy that functionality.
- No memory card file support. Use folder type memory card and put the save slot's folder into the repo's files folder that YOU need to create.
- The online version CANNOT attach to emulators.

## KH1 features
- Support for both vanilla and Final Mix save files.
- Playtime: Hours, minutes, seconds and the modulo 60 since it's stored in frames which are seconds times 60 (in NTSC builds; I haven't tested any PAL versions).
- Characters:
    - Base Stats
    - Sub MP: The orange MP bar. See the repo's wiki for how it works.
    - Elemental Resistances
    - Abilities
    - Equipment
    - Equipped Items
    - Spells that a party member can use.
- Leveling Curve and Path
- Magic levels
- Unlocked Summons
- Jiminy's Journal:
    - Ansem's Report unlock flags
    - Character and Heartless journal entries
    - Heartless kill counts
    - 99 Puppies unlock flags
    - Everything Trinity related
    - Mini Game records. Includes the Destiny Islands scores too.
    - Battle Report (—Battle Record—):
        - Includes a few hidden statistics too.
    - Treasure Chest and Atlantica Clam flags. (Vanilla chest contents aren't always correct yet but FM should be 100% correct.)
    - Synthesis flags
- Config menu options. It reflects the PS2 versions' options. Some of them are repurposed in Remix versions. PS3 and PC differs in that PC repurposes more options.
- World statuses and landing point flags
- Gummi Ships:
    - Name
    - Block Count
    - Assembly Area
    - Transform Pair
    - Every property of its Gummi Blocks:
        - Type
        - Coordinates
        - Orientation
        - Color (for now you must specify its ID because I haven't named the shades)
    - Gummi Inventory including Final Mix exclusives
    - Gummi Ship Control Config (PC Remix ignores it but PS3 Remix doesn't)
- Inventory and Ability dropdowns feature Final Mix exclusives in vanilla mode for modding reasons.
- The kh1.py file documents more known fields than the current app can edit. You can for example reset the Xemnas fight.
- PCSX2 attach:
    - Set slot to 0.
    - Set if you play vanilla or FM; vanilla means the USA ROM, won't work with other vanilla ROMs
    - Compatible with BOTH PCSX2 1.6.0 and PCSX2 Qt!
    - Windows only
    - Dumps the memory to file.

## KH2 features
- Support for vanilla Japanese, vanilla USA and Final Mix save files. Vanilla JP is entirely my research because it greatly differs from vanilla USA so I had to rediscover the equivalent fields.
- Global playtime
- Leveling path
- World, room, flag
- Munny
- EXP
- Current Drive Form and Summon
- Characters:
    - Level
    - Current and max HP and MP
    - Number of applied AP, Strength, Magic and Defense Boosts
    - Equipment
    - Abilities. Due to technical reasons I only allow you to fill max - 2 slots.
    - Auto Reload
    - Shortcuts for Sora, battle style and ability styles for allies
- Drive Forms
- Inventory
- Jiminy's Journal:
    - Bestiary:
        - Heartless and Nobody kill counts
        - Reaction Command counters
        - Limit max scores
    - Minigame records
- Worlds:
    - Playtime
    - Progress flags
- Difficulty
- PCSX2 attach: Works exactly the same as for KH1.

## KHBBS features
- Support for vanilla Japanese, vanilla USA and Final Mix save files.
- Playtime: Hours, minutes, seconds
- Character type
- Character:
    - Weapon
    - EXP
    - Level
    - Current and max HP
    - Base Strength, Magic, Defense stats
    - Arena Medals and Arena Level
    - Munny technically belongs here too.
- Commands:
    - Decks:
        - Equipped deck
        - Deck's name
        - Slots
    - Command List
    - Finishers along with their names
    - Abilities
    - D-Links
- World, room, flag
- Munny
- Difficulty
- PPSSPP attach
    - Works like the KH1 and KH2 PCSX2 attaches
    - However, PSP KHBBSFM seems to have some kind of memory protection so you need to load the dumped save file to see the changes.
    - Works with both 32 bit and 64 bit exes.
    - Windows only

## KH3 features
- Support for both raw encrypted and decrypted save files
- Proper decryption and encryption
- You need to provide your account ID if it's not 1638
- Saving will put out both encrypted and decrypted files
- Playtime
- Desire and Power Choices
- Party
- Munny
- EXP
- Difficulty
- Advanced general options:
    - Map Path and Map Spawn
    - Player Script and Player Pawn

# Documentation
For now, on the `main` branch `kh1_src/kh1.py` and `kh2_src/kh2.py` double as save file documentations for the respective games. It's another long term goal to create user-friendly documentations.
The repo's wiki is created for that user-friendly documentation but is nowhere near from being up-to-date.

# Known issues
- It's heavily work in progress so expect issues.
- There are placeholder tabs that won't show anything. This isn't a bug, they just aren't implemented yet.

# Special thanks
- Xeeynamo: [Kingdom Save Editor](https://github.com/Xeeynamo/KingdomSaveEditor) the main inspiration of the project
- [Game Tools Collection](https://github.com/RyudoSynbios/game-tools-collection/blob/master/src/lib/templates/kingdom-hearts-ps2) for an [online PS2 KH1 save editor](https://game-tools-collection.com/kingdom-hearts-ps2/save-editor) that provided lots of used info
- GICU for providing various [KH1 flags](https://github.com/gaithern/KH1FM-RANDOMIZER/blob/36569375fa6f12074e02f6a2b9b09175e76a53cf/Static%20Files/scripts/1fmRandoSendAPLocations.lua) like the treasure chests and other helps
- dedede123 & fungualtissue1230 for the PowerShell script to decrypt and encrypt the KH3 PC save files
- The OpenKH community for various helps including modding the KH games
- The RetroAchievements community for the Code Notes and the fun sets and not just the KH ones
