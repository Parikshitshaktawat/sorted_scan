from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might miss some required modules.
# Dependencies are automatically detected, but it might miss some modules.
build_exe_options = {
    "packages": ["os", "tkinter", "logging", "threading"],
    "excludes": [],
    "include_files": []
}

# Base setting for Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # This hides the console window.

# Define the setup for the application
setup(
    name="Sort Files",
    version="1.0",
    description="File sorting on the basic of size app",
    options={"build_exe": build_exe_options},
    executables=[Executable("sorted_scanning.py", base=base)]  # Replace "your_script.py" with the main script filename.
)
