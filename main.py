from os import get_terminal_size
from colorama import Back, Fore, Style
from downloader import Download
from functions import download_image, get_header
from settings import readSetting, resource_path, editsettings
import json, os

"""
    ┌─  
    │
    ├─
    │
    └─
"""


printline = True
exit = False
if __name__ == "__main__":
    is_main= True    
else:
    is_main = False


while exit == False and is_main:
    if printline:
        print(
            "\n" * (os.get_terminal_size().lines - 8)
            + "Menu\n ├─ 1-Download Gallery \n ├─ 2-Download single image \n ├─ 3-Settings \n ├─ 4-About \n └─ 5-Exit \n"
        )
    printline = True
    Cmd = input("~:")

    if Cmd == "1":
        Download()

    if Cmd == "2":
        imageurl = input("E-Hentai Page URL: ")
        try:
            get_header()
            download_image(imageurl)
        except FileExistsError:
            print("already exesits")

    elif Cmd == "3":
        exitsetting = False
        while exitsetting == False:
            print("\n" * (os.get_terminal_size().lines - 9) + "\nSettings ")
            settings = json.loads(os.environ["userdata"])
            for i in settings:
                print(
                    " ├─ "
                    + str(list(settings).index(i) + 1)
                    + "- "
                    + i
                    + " : "
                    + str(settings[i])
                )
            print(" └─ " + str(list(settings).__len__() + 1) + "- Back\n")
            inp = int(input("Settings:"))
            if int(inp) <= len(settings):
                print(f"editing {list(settings.keys())[inp-1]}")
                newval = input("Enter new value: ")
                editsettings(list(settings.keys())[inp-1], newval)
            else:
                exitsetting = True
    elif Cmd.lower() == "4":
        print(
            "\n" * (os.get_terminal_size().lines - 3)
            + """
maded with ♥
    2024    tank§man"""
        )
        input()
    elif Cmd.lower() == "5":
        exit = True
    else:
        print(Back.WHITE + Fore.BLACK + "-invalid-" + Style.RESET_ALL)
