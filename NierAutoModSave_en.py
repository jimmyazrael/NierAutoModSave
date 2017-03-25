# -*- coding: utf-8 -*-
"""
NieR:AutoModSave v0.1 by jimmyazrael
This script will guide and help you to import Nier:A's saves shared by others.

Requirement:
1. Preferably you should have received the whole save folder,
or at least you should have the following files:
    GameData.bat, one or more than one of the SlotData files
    and probably SystemData.dat. Although the use of SystemData.dat
    is still unknown.
2. Please make sure you back up your own save folder, as using other's 
save file will make yours unreadable. If you would like to use your save files 
again, simply treat your own backup save folder as the one shared by someone else
and repeat the very same steps stated below.

Steps:
1. Back up your WHOLE save folder, which is likely located at Documents\My Games\NieR_Automata ;
2. Remove everything except Graphic.ini in that folder;
3. Put the files (except Graphic.ini) you received from another player in the folder;
if you prefer exe:
    4. Put NierAutoModSave.exe in the same folder, run it, follow it, done.
else if you prefer .py script and you have Python installed:
    4. Put NierAutoModSave.py in the same folder and run it, follow it, done.
"""

import os
import glob

msg = dict()
# English messages
msg['gd_not_found'] = '''
    GameData.bat not found in this directory, please find and put it here.
    Press Enter to continue when the file is ready.'''
msg['gen_msg'] = '''
    A new GameData.dat is currently needed to continue the process.
    It can be generated by the game.
    Please start the game.
    You may exit the game after the title screen shows up.
    Do not close this window and come back after it is done.
    Shall we continue? (press Enter to confirm)'''
msg['modsv'] = 'Modifying %s...'
msg['modgd'] = 'Modifying GameData.dat...'
msg['end'] = '\nFinished. Glory to mankind!\n'

# Rename the GameData file
while not glob.glob('GameData.dat'):
    print msg['gd_not_found'] # Have to use print, raw_input just hates Chinese
    raw_input()
if glob.glob('savemod_GameData.dat'):
    os.remove('savemod_GameData.dat')
os.rename('GameData.dat', 'savemod_GameData.dat')

# Extract signature string
sig = ''  # Signature string
while True:
    try:
        with open('GameData.dat', 'rb') as f:
            sig = f.read(15)
            break
    except IOError:
        print msg['gen_msg']
        raw_input()
        pass

# We have the sig, the new GameData.dat just outlives its usefulness
os.remove('GameData.dat')

# Modify save slot(s) data header with the sig str
for fname in glob.glob('SlotData_?.dat'):
    print msg['modsv'] % fname
    with open(fname, 'r+b') as f:
        content = f.read()  # small file, read it all
        content = content[:4] + sig + content[19:]
        f.seek(0)  # Reset head position
        f.write(content)

# Modify original shared GameData.dat
print msg['modgd']
os.rename('savemod_GameData.dat', 'GameData.dat')
with open('GameData.dat', 'r+b') as f:
    content = f.read()
    content = sig + content[15:]
    f.seek(0)
    f.write(content)

print msg['end']
os.system('pause')  # I don't think anybody will use this on linux so it's fine
