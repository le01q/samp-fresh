# setup.py
from cx_Freeze import setup, Executable
build_exe_options = {"includes": ["PyQt5"],
                     "packages": ["os"], "excludes": ["tkinter"]}
setup(name="SAMP Fresh",
      version="0.0.1",
      description="A custom launcher for SA:MP",
      author="ne0de",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", target_name="SAMP Fresh", icon="sampfresh.ico", base="Win32GUI")])
