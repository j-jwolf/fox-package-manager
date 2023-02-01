import os, sys
from json import load, dump
from datetime import date, datetime

from utils import *

"""
to do
    remove launcher.py
    remove print statements that arent needed anymore
    please add a way to redirect stdout on a process and >> output when running commands like pip upgrade & such
"""

def buildProject() -> None:
    # check app-env exists
    if(not path.isdir(venv)):
        print("Installing virtual environment...")
        Popen(f"{pycall} -m venv {venv}").wait()
    # check dependencies
    Popen(f"{venvCall} && {pycall} {mergePath(mainDir, 'verification.py')}").wait()
    return

def main():
    configFile = "config.json"
    assert(len(sys.argv) != 1)
    if(len(sys.argv) == 2 and sys.argv[1] == "help"):
        print("List of commands:")
        data = "\t"+"\n\t".join(readFile(mergePath(mainDir, "commands.txt")).split("\n"))
        print(data)
        exit()
    match sys.argv[1]:
        case "new":
            assert(len(sys.argv) > 2)
            project = sys.argv[2]
            os.mkdir(project)
            assert(not os.path.isfile(project))
            dependencies = [arg for arg in sys.argv]
            for i in range(3): dependencies.pop(0)
            data = {
                "meta": {
                    "projectName": project,
                    "authors": [],
                    "packageVersion": "0.0.1", # change?
                    "pythonVersion": getPythonVersion()
                },
                "package": {
                    "dependencies": dependencies,
                    "entry": "main.py"
                }
            }
            assert(writeFile(data, mergePath(project, configFile)))
            assert(writeFile("def main():\n\tprint('Hello, world!')\n\treturn\n\nif(__name__ == '__main__'):\n\tmain()", mergePath(project, "main.py")))
        case "run":
            args = [arg for arg in sys.argv]
            for i in range(2): args.pop(0)
            args = " ".join(args)
            config = readFile(configFile)
            buildProject()
            # run at entry point
            # Popen(f"{venvCall} && {pycall} {config['package']['entry']}").wait()
            # print(f"Venv: {venv}\nVenv call: {venvCall}\npycall: {pycall}")
            # exit()
            print("\n\n")
            pout(f"{venvCall} && {pycall} {config['package']['entry']} {args}")
        case "build": buildProject()
        case other: print("ahhh!")
    return

# not implemented
persistentFile = "data.json"
if(os.path.isfile(persistentFile)): persistent = readFile(persistentFile)

main()