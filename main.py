from os import get_terminal_size
from colorama import Back, Fore, Style
from downloader import Download
from settings import readSetting, resource_path, editsettings

import json, os, subprocess, sys, time

"""
    ┌─  
    │
    ├─
    │
    └─
"""


printline = True
exit = False
while exit == False:
    # Cmd = input("Menu\n ├─ Create File(c) \n ├─ Do Multiply Folder (m)  \n ├─ Exit (e) \n └─ Setting (s) No t working \n~: ")
    if printline:
        print(
            "\n" * (os.get_terminal_size().lines - 7)
            + "Menu\n ├─ 1-Download \n ├─ 2-Load Settings \n ├─ 3-About \n └─ 4-Exit \n"
        )
    printline = True
    Cmd = input("~:")

    if Cmd == "1":
        Download()

    elif Cmd == "2":
        exitsetting = False
        while exitsetting == False:
            print("\nSettings ")
            settings = readSetting()
            for i in settings:
                print(
                    " ├─ "
                    + str(list(settings).index(i) + 1)
                    + "-"
                    + i
                    + ": "
                    + settings[i]
                )
            print(" └─ " + str(list(settings).__len__() + 1) + "-Back\n")
            inp = input("Settings:")
            if int(inp) <= len(settings):
                print(f"editing {list(settings.keys())[int(inp)-1]}")
                newval = input("Enter new value: ")
                editsettings(list(settings.keys())[int(inp) - 1], newval)
            else:
                exitsetting = True
    elif Cmd.lower() == "3":
        print(
            "\n" * (os.get_terminal_size().lines - 3)
            + """
maded with ♥
    2024    tank§man"""
        )
        input()
    elif Cmd.lower() == "4":
        exit = True
    else:
        print(Back.WHITE + Fore.BLACK + "-invalid-" + Style.RESET_ALL + "\n")
