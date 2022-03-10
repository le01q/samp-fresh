from cx_Freeze import setup, Executable
build_exe_options = {"includes": ["colorama"],
                     "packages": ["os"], "excludes": [""]}
setup(name="SAMP Fresh CLI",
      version="0.0.1",
      description="A custom launcher for SA:MP",
      author="le01q",
      options={"build_exe": build_exe_options},
      executables=[Executable("samp-fresh-cli.py", target_name="SAMP Fresh CLI", icon="sampfresh_cli.png", base="Win32GUI")])
