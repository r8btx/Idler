import subprocess
import time

# Code from macok @https://stackoverflow.com/questions/34514644/in-python-3-how-can-i-tell-if-windows-is-locked/57258754#57258754

time.sleep(5)
process_name='LogonUI.exe'
callall='TASKLIST'
outputall=subprocess.check_output(callall)
outputstringall=str(outputall)
if process_name in outputstringall:
    print("Locked.")
else: 
    print("Unlocked.")