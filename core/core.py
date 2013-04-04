import time
import socket
import threading
import sys

def doAction(action,args):
        if action == 1:
                global commands
                listCommands(commands)
        if action == 2:
		global client
		global socketThread
		for c in client.values():
			c.close()
		for socket in socketThread.values():
			socket.stop()
		print "Exit"
                sys.exit()
        if action == 3:
		global address
                for addr in address.values():
			print addr


def listCommands(commands):
        for command in commands:
                print command['input']


def coreCli(commands):
	while True:
		usrcommand = raw_input("# ")
		output = 0
		for command in commands:
           	     if usrcommand == command['input']:
           	             output = 1
           	             print command['output']
           	             if command['action'] is not 0:
           	                     doAction(command['action'],command['args'])


def main(client):
	size = 1024
	while True:
		data = client.recv(size)
		if data:
			client.send(data)
	client.close()
	

commands = [
	{"input": "help", "output": "List of Commands:", "action": 1, "args": 0},
	{"input": "exit", "output": "Bye", "action": 2, "args": 0},
	{"input": "clients", "output": "Connected Clients:", "action": 3, "args": 0},
	]
client = {}
socketThread = {}
address = {}
i = 0
port = 38500
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind(('',port)) 
server.listen(5) 

print "Starting service. Listening on port %i. Server commands available. Type \"help\" for list of commands." %port

cliThread = threading.Thread(target = coreCli, args = (commands,))
cliThread.deamon = False
cliThread.start()

while True:
	client[i], address[i] = server.accept()
	socketThread[i] = threading.Thread(target=main, args = (client[i],))
	socketThread[i].daemon = False
	socketThread[i].start()	
	i += 1
