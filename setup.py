application_title = "resizer" #what you want to application to be called
main_python_file = "resizer.py" #the name of the python file you use to run the program

import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

includes = ["atexit","re"]

setup(
        name = application_title,
        version = "0.0.1",
        description = "Simple image resizer tool by Ciacco Davide",
        options = {"build_exe" : {"includes" : includes }},
        executables = [Executable(main_python_file, base = base)])