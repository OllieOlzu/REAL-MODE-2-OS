# A simple way to turn real mode 16 bit boot sector ASM code into a operating system, either making a .BIN, .IMG, or .ISO.

This uses NASM, wich gets included in the python folder, and the EXE file also has it included meaning you can run the EXE stand alone.

______________________________________________________________________________

# HOW TO USE THE EXE FILE

Download it from the releases, then run it on a windows machine

______________________________________________________________________________

# HOW TO DO IT THE PYTHON WAY:

1: Download the python .zip folder from the releases

2: Extract it

3: Install the libraries (pip install winshell pywin32)

4: Make sure python is installed

3: Run the python file thats in the folder

______________________________________________________________________________

# TURN IT INTO THE EXE USING PYINSTALLER

1: Install pyinstaller (pip install pyinstaller)

2: Navigate to the python files folder in CMD

3: Run this to turn it into 1 EXE file with everything: 

    pyinstaller --onefile --noconsole --icon=icon.ico --add-data "nasm.exe;." --add-data "icon.ico;." REALMODE2OS.py
