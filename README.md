# Kingdom Heart Save Editor
For now only KH1 and KH1FM are supported. Any other KH game is a very longterm goal.

The idea to write my own save editor came from the fact that Kingdom Save Editor is abandoned and it is very barebones in terms of knowledge and it can't be run on Android. For a university assignment I had to work with the ipywidgets Python package so I thought I could use it for my save editor. It turned out that it's not optimized for small screens so I was looking for GUI packages. I mostly stayed with Python since it can be easily used on Android. So after multiple restarts and a second university class influence I landed on Dash.

So I want to emphasize that the priority is to run the app on smartphones hence the overly vertical alignment.

# How to run
This is a Plotly Dash app written in Python so you need to have Python installed.
After then install the dash package via pip install dash.

Open a terminal in the repo's folder and run the command "python kh1se.py" alternatively if you have Jupyter Notebook installed you can run the 1st code cell in the ipynb file. I recommend the latter on Android.

Create a files and a saved folder in the repo's folder. Put your save files or even better save slot folders into the files folder. The app saves modified files into the saved folder. If it's a folder slot, the output will be a folder slot of course.

# Features
## What not to expect
- Don't expect support for the PC Remix PNG files, use Kingdom Save Editor for them. I have no reason to copy that functionality.
- No memory card file support. Use folder type memory card and put the save slot's folder into the repo's files folder that YOU need to create.
- PCSX2 attach.

## Features
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
- Gummi Inventory including Final Mix exclusives
- Inventory and Ability dropdowns feature Final Mix exclusives in vanilla mode for modding reasons.
- Config menu options. It reflects the PS2 versions' options. Some of them are repurposed in Remix versions. PS3 and PC differs in that PC repurposes more options.
- The kh1.py file documents more known fields than the current app can edit. You can for example reset the Xemnas fight.

## Documentation
For now, kh1_src/kh1.py doubles as a save file documentation. It's another long term goal to create a user-friendly documentation.

## Known issues
- It's heavily work in progress so expect issues.
- Some fields aren't saved yet but it doesn't affect the fields editible by the GUI so far.
- There are placeholder tabs that won't show anything. This isn't a bug, they just aren't implemented yet.
