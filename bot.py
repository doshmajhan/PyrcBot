import subprocess
import socket
import time

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



def echo():
    subprocess.call(['echo', 'hello'], shell=True)

def ping():
    subprocess.call(['ping', '127.0.0.1'])

if __name__ == '__main__':
    ircConnect()