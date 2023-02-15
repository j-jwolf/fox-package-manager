from json import dump, load
from os import path, mkdir, getcwd
from sys import platform, version
from ast import literal_eval
from subprocess import Popen

# initialize venv vars
venv = "app-env"
venvCall = "app-env\\Scripts\\activate.bat"
pycall = "python"
if not platform in {'win32', "msys", "cygwin"}:
    # not windows, change the above
    venvCall = "source app-env/bin/activate"
    pycall = "python3"

# i/o
def readFile(fn: str, binary: bool = None) -> str | dict:
    # reads the file based on its extension, json files are read as dictionaries
    assert(path.isfile(fn))
    if not binary in {True, False}: binary = False # default to text
    data = None
    mode = "r"
    if(binary): mode = "rb"
    try:
        with open(fn, mode) as file:
            match fn.split(".")[1]:
                # match by file extension
                case "json": data = load(file)
                case other: data = file.read()
    except KeyboardInterrupt: exit()
    except Exception as e: print(e)
    return data
def writeFile(data: str | dict, fn: str, mode: str = None) -> bool:
    if mode not in {"w", "a", "rb", "wb"} or fn.split(".")[1] == "json" and mode != "w": mode = "w" # default to write
    try:
        with open(fn, mode) as file:
            match fn.split(".")[1]:
                case "json": dump(data, file, indent = 4)
                case other: file.write(data)
        return True
    except KeyboardInterrupt: exit()
    except Exception as e: print(e)
    return False
def copyFile(o: str, c: str) -> bool: return writeFile(readFile(o), c)

# system
def pout(command: str, **kwargs): Popen(command, shell = True).wait()
def windows() -> bool: return platform in {"msys", "win32", "cygwin"}
def getPythonVersion() -> str: return version.split(" ")[0]
def meetsVersion(ver: str) -> bool: return getPythonVersion() >= ver

# path
def mergePath(*args: str) -> str: return path.sep.join(args)
def getCwd() -> str: return getcwd()

# make main directory
if(windows()): mainDir = mergePath(path.expanduser("~"), "Fox-Package-Manager")
else: exit()

# set up backwards compatibility --> what is able to run on the current version?
backwardsCompitable = {
    "match": meetsVersion("3.10.0"),
    "unionType": meetsVersion("3.10.0"),
    "typing": meetsVersion("3.5.0")
}