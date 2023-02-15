import ctypes, enum

from subprocess import Popen
from os import path, mkdir, listdir
from json import dump
from sys import argv, executable

from utils import *

def getVersion() -> str:
    version = "0.0.1" # move me somewhere
    return f"Fox Package Manager v{version}"

# create persistent data file

# wip -> finish me!
persistentFile = mergePath(mainDir, "persistent.json")
if(not path.isfile(persistentFile)):
    persistent = {
        "permissions": {},
        "state": {
            "systemEnvironment": False,
            "version": getVersion()
        }
    }
    writeFile(persistent, persistentFile)
else: persistent = readFile(persistentFile)

"""

MOVE TO A SEPARATE FILE -- FOR BOOTSTRAPING OTHER PROGRAMS

in case other files need to be run as admin

"""
class SW(enum.IntEnum):
    HIDE = 0
    MAXIMIZE = 3
    MINIMIZE = 6
    RESTORE = 9
    SHOW = 5
    SHOWDEFAULT = 10
    SHOWMAXIMIZED = 3
    SHOWMINIMIZED = 2
    SHOWMINNOACTIVE = 7
    SHOWNA = 8
    SHOWNOACTIVATE = 4
    SHOWNORMAL = 1

class ERROR(enum.IntEnum):
    ZERO = 0
    FILE_NOT_FOUND = 2
    PATH_NOT_FOUND = 3
    BAD_FORMAT = 11
    ACCESS_DENIED = 5
    ASSOC_INCOMPLETE = 27
    DDE_BUSY = 30
    DDE_FAIL = 29
    DDE_TIMEOUT = 28
    DLL_NOT_FOUND = 32
    NO_ASSOC = 31
    OOM = 8
    SHARE = 26

""" use that function mapping you tested earlier -->
functionMap = {
    someFunctionName: theActualFunction,
    ...
}

for arg in argv: functionMap[arg]()

need a way to pass args

"""
def bootstrap() -> None:
    global persistent
    if(ctypes.windll.shell32.IsUserAnAdmin()):
        print("running main")
        main(persistent)
    else:
        print("not an admin --> changing permissions")
        hinstance = ctypes.windll.shell32.ShellExecuteW(None, 'runas', executable, argv[0], None, SW.SHOWNORMAL)
        if hinstance <= 32: raise RuntimeError(ERROR(hinstance))

# work in progress (low priority)
# debug = False
# if "-debug" in argv: debug = True

def copyFile(o: str, c: str) -> bool:
    # why does this exist? the EXACT function exists in utils, which is imported
    try:
       with open(o, "rb") as original, open(c, "wb") as copy: copy.write(original.read())
       return True
    except KeyboardInterrupt: exit()
    except Exception as e: print(e)
    return False

def main(persistent):
    print("in main")

    if(not path.isdir(mainDir)): mkdir(mainDir)

    # copy files to main dir (THIS IS A FLAT STRUCTURE -> WILL BE UPDATED)
    for file in listdir(getCwd()):
        if(file.endswith(".py") and not path.isdir(mergePath(mainDir, file)) or file == "commands.txt"): copyFile(file, mergePath(mainDir, file))

    # set up system variable
    print(persistent["state"]["systemEnvironment"])
    if(not persistent["state"]["systemEnvironment"]):
        if(windows()):
            print("Setting up system variable...")
            pout(f'setx fox \"{pycall} {mergePath(mainDir, "main.py")}\" /m')
        else:
            print("non-windows machines are currenly not supported")
            input("Press enter")
            ...
        persistent["state"]["systemEnvironment"] = True
        writeFile(persistent, persistentFile)

if(__name__ == "__main__"): bootstrap()