# Kingdom Heart Save Editor
For now only KH1, KH1FM, vanilla JP KH2, vanilla USA/EU KH2 and KH2FM are supported. Any other KH game is a very longterm goal.

The idea to write my own save editor came from the fact that Kingdom Save Editor is abandoned and it is very barebones in terms of knowledge and it can't be run on Android. For a university assignment I had to work with the ipywidgets Python package so I thought I could use it for my save editor. It turned out that it's not optimized for small screens so I was looking for GUI packages. I mostly stayed with Python since it can be easily used on Android. So after multiple restarts and a second university class influence I landed on Dash.

So I want to emphasize that the priority is to run the app on smartphones hence the overly vertical alignment.

# How to run
This is a Plotly Dash app written in Python so you need to have Python installed.
After then install the dash package via pip install dash.

Open a terminal in the repo's folder and run the command "python kh1se.py" alternatively if you have Jupyter Notebook installed you can run the 1st code cell in the ipynb file. I recommend the latter on Android. For KH2 do the same with kh2se.py.

Create a files and a saved folder in the repo's folder. Put your save files or even better save slot folders into the files folder. The app saves modified files into the saved folder. The output will ALWAYS be a folder slot to avoid issues.

# Features
## What not to expect
- Don't expect support for the PC Remix PNG files, use Kingdom Save Editor for them. I have no reason to copy that functionality.
- No memory card file support. Use folder type memory card and put the save slot's folder into the repo's files folder that YOU need to create.
- PCSX2 attach.

## KH1 features
- Support for both vanilla and Final Mix save files.
- Playtime: Hours, minutes, seconds and the modulo 60 since it's stored in frames which are seconds $\cdot$ 60 (in NTSC builds; I haven't tested any PAL versions).
- Most of what Kingdom Save Editor is capable of.
- Sub MP: The orange MP bar. Remix versions are bugged, they might not load this.
- Spells that a party member can use.
- Leveling Curve and Path
- Magic levels
- Unlocked Summons
- Ansem's Report unlock flags
- Character and Heartless journal entries
- Heartless kill counts
- 99 Puppies unlock flags
- Everything Trinity related
- Mini Game records.
- Config menu options. It reflects the PS2 versions' options. Some of them are repurposed in Remix versions. PS3 and PC differs in that PC repurposes more options.
- World statuses and landing point flags
- Gummi Inventory including Final Mix exclusives
- Inventory and Ability dropdowns feature Final Mix exclusives in vanilla mode for modding reasons.
- The kh1.py file documents more known fields than the current app can edit. You can for example reset the Xemnas fight.

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
- Heartless and Nobody kill counts
- Reaction Command counters. The FM only ones aren't discovered yet but the vanilla ones are in FM too.
- Limit max scores
- Difficulty

## Documentation
For now, kh1_src/kh1.py and kh2_src/kh2.py double as save file documentations for the respective games. It's another long term goal to create user-friendly documentations.

## Known issues
- It's heavily work in progress so expect issues.
- Some fields aren't saved yet though the fields editable through the GUI should be.
- There are placeholder tabs that won't show anything. This isn't a bug, they just aren't implemented yet.
