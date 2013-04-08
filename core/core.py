import time
import socket
from multiprocessing import Process, Queue
import threading
import sys
import atexit


def doAction(action,args):
        if action == 1:
                global commands
                listCommands(commands)
        if action == 2:
		global client
		global socketProcess
		for c in client.values():
			c.close()
		print "Closing down all services."
		clean()
                sys.exit()
        if action == 3:
		global address
                for addr in address.values():
			print addr


def listCommands(commands):
        for command in commands:
		print command['input']


def coreCli(commands,q):
	while True:
		global exit
		if exit == 1:
			print "Shut Down CLI"
			return
		usrcommand = raw_input("# ")
		output = 0
		for command in commands:
           	     if usrcommand == command['input']:
           	             output = 1
           	             print command['output']
           	             if command['action'] is not 0:
           	                     doAction(command['action'],command['args'])

def clean():
	global port
	global exit
	exit  = 1
	timeout = 5
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect(('localhost', port))
	client_socket.close()
	global socketProcess
	time.sleep(timeout)
	for process in socketProcess.values():
		process.terminate()


def main(client):
	size = 1024
	hello = 0
	while True:
		global exit
		if exit == 1:
			print "Shut Down Client"
			return
		if hello == 0:
			client.send("<zeroCli>\n <hello>\n  <type>server</type>\n  <ver>1.0</ver>\n  <capabilities>\n   <test ver=\"1.0\" />\n   <actions ver=\"1.0\">\n  </capabilities>\n </hello>\n</zeroCli>")
			hello = client.recv(size)
			client.send("Welcome")
			
		data = client.recv(size)
		if data:
			client.send(data)
	client.close()
	
def socketStart(server, client, i, address, socketProcess):
	while True:
		global exit
		if exit == 1:
			print "Main Socket Listener Shutdown."
			return
		client[i], address[i] = server.accept()
		socketProcess[i] = Process(target=main, args = (client[i],))
		socketProcess[i].start()
		i += 1

commands = [
	{"input": "help", "output": "List of Commands:", "action": 1, "args": 0},
	{"input": "exit", "output": "Starting Exit Process", "action": 2, "args": 0},
	{"input": "clients", "output": "Connected Clients:", "action": 3, "args": 0},
	]
client = {}
socketProcess = {}
address = {}
exit = 0
i = 0
port = 38500
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind(('',port)) 
server.listen(5) 
q = Queue()
atexit.register(clean)
print "Starting service. Listening on port %i. Server commands available. Type \"help\" for list of commands." %port

cliProcess = threading.Thread(target = coreCli, args = (commands,q))
cliProcess.start()
socketWait = threading.Thread(target = socketStart, args = (server, client, i, address, socketProcess))
socketWait.start()
