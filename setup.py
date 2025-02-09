import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

# This script creates exutable file.
cx_Freeze.setup(
    name="Tetris",
    options={"build_exe": {"packages": ["pygame", "pygame_menu"],
                           "include_files": ["assets"]}},
    executables=executables
)
