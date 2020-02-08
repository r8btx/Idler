import subprocess, win32con, os, ctypes, time

# Preventing sleep from mishsx @https://stackoverflow.com/questions/57647034/prevent-sleep-mode-python-wakelock-on-python/57647169#57647169
# Detecting unlock from macok @https://stackoverflow.com/questions/34514644/in-python-3-how-can-i-tell-if-windows-is-locked/57258754#57258754

'''
For macs:
https://apple.stackexchange.com/questions/76107/how-can-i-keep-my-mac-awake-and-locked
'''

# If not Windows, stop running
if os.name != 'nt':
    raise(OSError("OS not compatible!"))

class WindowsInhibitor:
    '''Prevent OS sleep/hibernate in windows; code from:
    https://github.com/h3llrais3r/Deluge-PreventSuspendPlus/blob/master/preventsuspendplus/core.py
    API documentation:
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa373208(v=vs.85).aspx'''
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    
    def __init__(self):
        pass

    def inhibit(self):
        print("Preventing Windows from going to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS | \
            WindowsInhibitor.ES_SYSTEM_REQUIRED)

    def uninhibit(self):
        print("Allowing Windows to go to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS)

osSleep = None

osSleep = WindowsInhibitor()

osSleep.inhibit() # Prevent sleep

ctypes.windll.user32.LockWorkStation() # Lock Windows

# Set screen off
# Documentation: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendmessagew
SC_MONITORPOWER = 0xF170
ctypes.windll.User32.SendMessageW(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, SC_MONITORPOWER, 2)

# Check if the Windows is unlocked
while True:
    outputall=subprocess.check_output('TASKLIST')
    outputstringall=str(outputall)
    if 'LogonUI.exe' in outputstringall:
        time.sleep(3)
    else:
        print(time.asctime(), "[Unlocked]")
        break

# Allow sleep again
if osSleep:
    osSleep.uninhibit()