import time
import socket
from multiprocessing import Process, Queue
import threading
import sys
import atexit
import xml.etree.ElementTree as ET


class core():
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
		print "Server commands available. Type \"help\" for list of commands."
		while True:
			exit = self.exit
			if exit == 1:
				print "Shut Down CLI"
				return
			usrcommand = raw_input("# ")
			output = 0
			for command in self.commands:
			     if usrcommand == command['input']:
				     output = 1
				     print command['output']
				     if command['action'] is not 0:
						self.doAction(command['action'],command['args'])

	def clean(self):
		port = self.port
		self.exit  = 1
		timeout = 5
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect(('localhost', port))
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
		tree = ET.fromstring(data)
		for child in tree.findall("rpc"):
			if child.get('callType') == 'hello':
				ver = child.find('ver').text
				returnValue = self.helloRcv(ver)
				
		return returnValue
		


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
		
	def socketStart(self):
		while True:
			i = self.i
			exit = self.exit
			if exit == 1:
				print "Main Socket Listener Shutdown."
				return
			self.client[i], self.address[i] = self.server.accept()
			self.socketProcess[i] = Process(target=self.main, args = (self.client[i],))
			self.socketProcess[i].start()
			self.i += 1

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
	ver = "0.1"
	port = 38500
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	q = Queue()
	def __init__(self):
		atexit.register(self.clean)
		client = self.client
		socketProcess = self.socketProcess
		address = self.address
		exit = self.exit
		i = self.i
		port = self.port
		server = self.server
		commands = self.commands
		q = self.q
		self.server.bind(('',port)) 
		self.server.listen(5) 
		print "Starting service. Listening on port %i." %port
		self.socketWait = threading.Thread(target = self.socketStart, args = ())
		self.socketWait.start()
