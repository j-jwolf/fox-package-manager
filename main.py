"""
Fox Package Manager
"""

# imports
import os, sys
from json import load, dump
from datetime import date, datetime

"""
THIS ENTIRE PROJECT NEEDS TO BE CLEANED UP. THIS IS A MESS

to do
    add linux/mac functionality
    change system to path variable (%fox% to fox)
    remove print statements that arent needed anymore
    please add a way to redirect stdout on a process and >> output when running commands like pip upgrade & such
    please fix the main
    UPDATE THE COMMANDS FILE

"""

# local files
from utils import *

# check that this machine can run the package manager 
minimumVersion = "3.10" # this python version is required for match case and type unions (return str | dict)
try: assert(getPythonVersion() >= minimumVersion and windows())
except KeyboardInterrupt: exit()
except AssertionError as e:
    if(getPythonVersion() >= minimumVersion): print("This package manager currently requires {minimumVersion} of Python to run")
    else: print("This package manager currently requires windows to run")
    exit()

# builds project by creating venv if needed and installing any missing dependencies
def buildProject() -> None:
    # check app-env exists
    if(not path.isdir(venv)):
        print("Setting up package virtual environment...")
        Popen(f"{pycall} -m venv {venv}").wait()
    # check dependencies
    Popen(f"{venvCall} && {pycall} {mergePath(mainDir, 'verification.py')}").wait()
    return

def removeDependency(depen: str) -> bool:
    try:
        pout(f"{venvCall} && pip uninstall {depen}")
        return True
    except KeyboardInterrupt: exit()
    except Exception as e: print(e) # log this in the future
    return False

# main function
"""
main function needs a rework

new project:
    dynamic questions about the package (get user input)
    better layout
    CLEAN UP THE CODE

"""
def main() -> None:
    configFile = "config.json"
    assert(len(sys.argv) != 1)
    if(sys.argv[1] == "help"):
        # if help is command, prints commands.txt for more information
        print("List of commands:")
        data = "\t"+"\n\t".join(readFile(mergePath(mainDir, "commands.txt")).split("\n"))
        print(data)
        exit()
    # match command user passed as arg
    # maybe move this to its own file. its getting kind of cramped here
    match sys.argv[1]:
        case "new":
            # create a new project
            assert(len(sys.argv) > 2)
            project = sys.argv[2]
            os.mkdir(project)
            assert(not os.path.isfile(project))
            dependencies = [arg for arg in sys.argv]
            for _ in range(3): dependencies.pop(0) # add dependencies
            data = {
                "package": {
                    "projectName": project,
                    "authors": [],
                    "packageVersion": "0.0.1", # change?
                    "pythonVersion": getPythonVersion(),
                    "description": "",
                    "keywords": []
                },
                "library": {
                    "dependencies": dependencies,
                    "entry": mergePath("src", "main.py"),
                    "packageArgs": [] # args for the target file/entry point. these are optional and they are placed after called args. for more information, read commands.txt or run fox help
                }
            }
            assert(writeFile(data, mergePath(project, configFile)))
            mkdir(mergePath(project, "src"))
            assert(writeFile("def main() -> int:\n\tprint('Hello, world!')\n\treturn 0\n\nif(__name__ == '__main__'):\n\tres = main()", mergePath(project, "src", "main.py")))
        case "run":
            # run project (build and run)
            assert(len(sys.argv) >= 2)
            config = readFile(configFile)
            args = " ".join(config["library"]["packageArgs"])
            if(len(sys.argv) > 2):
                dynamicArgs = " ".join([sys.argv[i] for i in range(2, len(sys.argv))])
                args = f"{dynamicArgs} {args}"
            buildProject()
            print("\n\n")
            entry = config['library']['entry']
            pout(f"{venvCall} && {pycall} {entry} {args}")
        case "build": buildProject() # builds project
        case "entry":
            # change the entry/target file in config.library.entry (what file the package manager runs to start your package)
            assert(len(sys.argv) >= 3 and sys.argv[2].endswith(".py")) # may include other files?
            config = readFile(configFile)
            config["library"]["entry"] = sys.argv[2]
            if(not sys.argv[2].startswith("src") and not "-no_src" in sys.argv): config["library"]["entry"] = f"{mergePath('src', config['library']['entry'])}"
            # elif(sys.argv[3] == "no_src" and not sys.argv[2].startswith("src")): pass
            writeFile(config, configFile)
            print(f"Updated entry file to {sys.argv[2]}")
        case "add-depen":
            # add a new dependency (can be multiple)
            assert(len(sys.argv) >= 3)
            config = readFile(configFile)
            for i in range(2, len(sys.argv)):
                if(sys.argv[i] not in config["library"]["dependencies"]): config["library"]["dependencies"].append(sys.argv[i])
            print("Added dependencies")
            writeFile(config, configFile)
        case "drop-depen":
            # remove a dependency (can be multiple)
            assert(len(sys.argv) >= 3)
            config = readFile(configFile)
            for i in range(2, len(sys.argv)):
                if(sys.argv[i] in config["library"]["dependencies"]):
                    """
                    need a better solution. if the package is not in the app-env but is in the config file, it will not be removed
                    find a way to check the app-env's working set and see if sys.argv[i] is in it. if not, safe to remove from the config file
                    """
                    if(removeDependency(sys.argv[i])): config["library"]["dependencies"].remove(sys.argv[i])
            writeFile(config, configFile)
            print("Dropped dependencies")
        case "add-keyword":
            """
            is this really so useful that it would have its own fox command?
            """
            assert(len(sys.argv) >= 3)
            try:
                config = readFile(configFile)
                for i in range(2, len(sys.argv)):
                    if(sys.argv[i] not in config["package"]["keywords"]): config["package"]["keywords"].append(sys.argv[i])
                writeFile(config, configFile)
                print("Added keywords")
            except KeyboardInterrupt: exit()
            except Exception as e: print(e)
        case "drop-keyword":
            """
            same with above, is this so useful?
            """
            assert(len(sys.argv) >= 3)
            try:
                config = readFile(configFile)
                for i in range(2, len(sys.argv)):
                    if(sys.argv[i] in config["package"]["keywords"]): config["package"]["keywords"].remove(sys.argv[i])
                writeFile(config, configFile)
                print("Removed keywords")
            except KeyboardInterrupt: exit()
            except Exception as e: print(e)
        case "set-args":
            """
            sets args that can be reused. these are overwritten by args entered at run
            
            ie.
                command: %fox% run these would be args
                config: {
                    library: {
                        packageArgs: [
                            from,
                            config
                        ]
                    }
                }
                these would be args would be passed as args [0:4] and any args in the config file would be passed AFTER the dynamic args
                your program's argv would be the following:
                    [__file__, these, would, be, args, from, config]"""
            assert(len(sys.argv) >= 3)
            try:
                config = readFile(configFile)
                for i in range(2, len(sys.argv)): config["library"]["packageArgs"].append(sys.argv[i])
                writeFile(config, configFile)
                print("Set package arguments")
            except KeyboardInterrupt: exit()
            except Exception as e: print(e)
        case "clear-args":
            # clears the current args in config file
            config = readFile(configFile)
            config["library"]["packageArgs"] = []
            writeFile(config, configFile)
            print("Cleared package arguments")
        case other: print(f"Failed on match - case passed: {sys.argv[1]}")
    return

# driver code

"""
not implemented fully!

persistentFile = "data.json"
if(os.path.isfile(persistentFile)): persistent = readFile(persistentFile)
"""

main() # run main