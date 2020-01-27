import subprocess, os, ctypes, time
import win32gui, win32con
from threading import Timer

# Preventing sleep from mishsx @https://stackoverflow.com/questions/57647034/prevent-sleep-mode-python-wakelock-on-python/57647169#57647169
# Detecting unlock from macok @https://stackoverflow.com/questions/34514644/in-python-3-how-can-i-tell-if-windows-is-locked/57258754#57258754
# Set display off  from arjun024 @https://github.com/arjun024/turn-off-screen/blob/master/turnoff.py

'''
For macs:
https://apple.stackexchange.com/questions/76107/how-can-i-keep-my-mac-awake-and-locked
'''

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
        import ctypes
        print("Preventing Windows from going to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS | \
            WindowsInhibitor.ES_SYSTEM_REQUIRED)

    def uninhibit(self):
        import ctypes
        print("Allowing Windows to go to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(
            WindowsInhibitor.ES_CONTINUOUS)

# Terminate screen off command once executed
def force_exit():
	pid = os.getpid()
	os.system('taskkill /pid %s /f' % pid)

t = Timer(1, force_exit)
osSleep = None

# If not Windows, stop running
if os.name != 'nt':
    raise(OSError("OS not compatible!"))

osSleep = WindowsInhibitor()

osSleep.inhibit() # Prevent sleep

ctypes.windll.user32.LockWorkStation() # Lock Windows

# Set screen off
t.start()
SC_MONITORPOWER = 0xF170
win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, SC_MONITORPOWER, 2)
t.cancel()

# Check if the Windows is unlocked
while True:
    outputall=subprocess.check_output('TASKLIST')
    outputstringall=str(outputall)
    if 'LogonUI.exe' in outputstringall:
        time.sleep (2)
    else:
        print(time.asctime (), "[Unlocked]")
        break

# Allow sleep again
if osSleep:
    osSleep.uninhibit()