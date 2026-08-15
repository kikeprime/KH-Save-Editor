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
The feature list is in the `main` branch's README.

## What not to expect
- Don't expect support for the PC Remix PNG files, use Kingdom Save Editor for them. I have no reason to copy that functionality.
- No memory card file support. Use folder type memory card and put the save slot's folder into the repo's files folder that YOU need to create.
- The online version CANNOT attach to emulators.

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
