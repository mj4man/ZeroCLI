import socket
from multiprocessing import Process, Queue
import threading
import sys
import atexit
import xml.etree.ElementTree as ET


class Core(object):
    """ Orchestrates communication between all zeroCLI components """
    
    def __init__(self):
        """ Define variables and kickstart the processes """
        
        self._i = 0 
        self._exit = 0
        self._client = {}
        self._socketProcess = {}
        self._address = {}
        self._version = "0.1"
        self._port = 38500
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self._commands = [
		{"input": "help", "output": "List of Commands:", "action": 1, "args": 0},
		{"input": "exit", "output": "Starting Exit Process", "action": 2, "args": 0},
		{"input": "clients", "output": "Connected Clients:", "action": 3, "args": 0},
		]

        queue = Queue()

        # When `sys.exit` is called clean() will be called
        atexit.register(self.clean)
		
		self.server.bind(('',self._port)) 
		self.server.listen(5) 
		
        print ("Starting service. Listening on port {0}.".format(self._port))
        
        # Creating a thread to wait for a new client or interface to start
		socketWait = threading.Thread(target = self.__socketStart__, args = ())
		socketWait.start()
        
    def __socketStart__(self):
	   	""" Listens for new client, then starts a new process """
        
        while True:
            i = self.i
			exit = self.exit
			if exit == 1:
				print "Main Socket Listener Shutdown."
				break
			self.client[i], self.address[i] = self.server.accept()
			self.socketProcess[i] = Process(target=self.main, args = (self.client[i],))
			self.socketProcess[i].start()
			self.i += 1    
	
    def doAction(self,action,args):
		if action == 1:
			commands = self.commands
			self.listCommands(commands)
		if action == 2:
			client = self.client
			socketProcess = self.socketProcess
			for c in client.values():
				c.close()
			print "Closing down all services."
			self.clean()
		if action == 3:
			address = self.address
			for addr in address.values():
				print addr


	def listCommands(self,commands):
		for command in commands:
			print command['input']


	def coreCli(self):
		print 'Server commands available. Type "help" for list of commands.'
		while True:
			if self.exit == 1:
				print "Shut Down CLI"
				break
			usrcommand = raw_input("# ")
			output = 0
			for command in self.commands:
			     if usrcommand == command['input']:
				     output = 1
				     print command['output']
				     if command['action'] is not 0:
						self.doAction(command['action'],command['args'])

	def clean(self):
		self.exit  = 1
		timeout = 5
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect(('localhost', self.port))
		time.sleep(1)
		client_socket.close()
		print "Waiting for timeout"
		time.sleep(timeout)
		for process in self.socketProcess.values():
			process.terminate()
		sys.exit()

	def helloRcv(self,ver):
		if ver == self.ver:
			return "Yes"
		else:
			return "No"

	def recieveData(self,data):
		try:
			tree = ET.fromstring(data)
			for child in tree.findall("rpc"):
				if child.get('callType') == 'hello':
					ver = child.find('ver').text
					returnValue = self.helloRcv(ver)
				
			return returnValue
		except Exception, e:
			return "<?xml version\"1.0\"?><zeroCli><error errorType=\"1\">%s</error></zeroCli>" % e
		


	def main(self,client):
		size = 1024
		hello = 0
		while True:
			exit = self.exit
			if exit == 1:
				print "Shut Down Client"
				return
			if hello == 0:
				client.send("<?xml version=\"1.0\"?><zeroCli><rpc callType=\"hello\"><ver>%s</ver></rpc></zeroCli>"% self.ver)
				hello = client.recv(size)
				"""Parse Welcome Message"""
				print hello
				parseResponse = self.recieveData(hello)
				client.send(parseResponse)
				
			data = client.recv(size)
			if data:
				parseResponse = self.recieveData(data)
				client.send(parseResponse)
		client.close()
		
	
