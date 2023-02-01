from sys import executable
from subprocess import check_call, DEVNULL
from pkg_resources import working_set
from json import load

from utils import readFile, pout, pycall

print("Updating virtual environment's pip...")
pout(f"{pycall} -m pip install --upgrade pip")

print("checking all dependencies are installed...")

# read config data
config = readFile("config.json")

# finding missing packages
dependencies = set(config["package"]["dependencies"])
missing = dependencies - {pkg.key for pkg in working_set}

# install missing packages
if(missing):
    print(f"installing {len(missing)} missing dependencies...")
    check_call([executable, "-m", "pip", "install", *missing], stdout = DEVNULL)

match len(missing):
    case 0: print("All dependencies installed")
    case other: print(f"Installed {len(missing)} missing dependencies")