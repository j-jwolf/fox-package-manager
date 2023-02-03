# Fox Python Package Manager
## John Wolf

## This package manager currently requires at least Python 3.10

## Contents
1. Installation
2. Usage
3. Troubleshooting
4. Notes

## 1. Installation
To install, run the installer.py and give the program permission to add the fox system variable.
To do this, open the CMD or terminal in the folder that contains install.py and run the following:
```
python installer.py
```

This will copy the source code to C:\Users\your-profile\Fox-Package-Manager

## 2. Usage
This package manager attempts to make managing Python imports easier by handling them for you

You may run the following for a list of instructions:
```
%fox% help
```

Open a terminal in the folder you would like to contain the package and run the following:
```
%fox% new your_package_name
```

This will create a new package with whatever you name it. You can pass additional, optional arguments after the package name. The manager will assume that these are required packages and will treat them as such:
```
%fox% new your_package_name your dependencies go here
```

Running this will create a package that starts with 3 dependencies. These can be changed later.

You will find a new directory that shares a name with the package. This is where your source code will be kept. You can build the package, which will ensure that all dependencies are installed in the virtual environment. This step is optional.
```
%fox% build
```

You can also run the package by the following command. You can add arguments to the command that will be passed to the target file.
```
%fox% run optional arguments here
```

## 3. Troubleshooting

### The program has an error involving the match operator
Match is a Python feature that was released in 3.10. This program was developed on 3.11 and is not yet backwards compatible with older Python releases. This is currently being addressed.

### I didn't add a dependency when I created the package. Can I add it now?
Yes, you can add it to the config.json file. In the file, you will file package.dependencies. Add each item in separated by commas.
```js
{
    "dependencies": [
        "igraph",
        "keyboard"
    ]
}
```

## 4. Notes

### Planned Future Development (in order of planned release)
1. Backwards compatiblity (> Python 3.10)
2. Change the system variable %fox% to a path variable fox
3. Cleaned up stdout
4. Package information command
5. C integration for i/o and other areas that would benefit from the speed of C