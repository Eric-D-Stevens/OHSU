import os
import pathlib

os.chdir("ui_files")
os.system(r"pyuic5 Python_IEX_GUI.ui > Python_IEX_GUI.py")

os.system(r"python MainGUI.py")
