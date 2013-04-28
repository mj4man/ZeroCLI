from __future__ import print_function
from __future__ import absolute_import

import time
import socket
import threading
import sys
import xml.etree.ElementTree as ET
from multiprocessing import Process, Queue


class Server(object):
    """ Orchestrates communication between all zeroCLI components """
    
    def __init__(self):
        """ Define variables and kickstart the processes """
        
        self._exit = 0
        self._clients = {}
        self._addresses= {}
        self._socketProcess = {}
        self._version = "0.1"
        self._port = 38500
        self._commands = [
            {"input": "help", "output": "List of Commands:", "action": 1, "args": 0},
            {"input": "exit", "output": "Starting Exit Process", "action": 2, "args": 0},
            {"input": "clients", "output": "Connected Clients:", "action": 3, "args": 0},
        ]
        
        self.queue = Queue()
        
        # When `sys.exit` is called clean() will be called
        
        print ("Starting service. Listening on port {0}.".format(self._port))
        
        # Creating a thread to wait for a new client or interface to start
        server = threading.Thread(target=self.__listen)
        server.start()
    
    def __clean(self):
        self._exit = 1
        timeout = 5
        try:
            client_socket = socket.socket()
            client_socket.connect(('localhost', self._port))
            time.sleep(1)
            client_socket.close()
        except:
            print("Couldn't connect to server")
        print ("Waiting for timeout")
        time.sleep(timeout)
        for process in self._socketProcess.values():
            process.terminate()
        sys.exit()
    
    def __listen(self):
        """ Listens for new client, then starts a new process """
        try:
            server_socket = socket.socket()
            server_socket.bind(('', self._port))
            server_socket.listen(5)
        except:
            print ("\nError binding server to port. Quiting...")
            self.__clean()
        i = 0 
        while True:
            if self._exit == 1:
                print("Main Socket Listener Shutdown.")
                server_socket.close()
                break
            else:
                # Creates a dict of {CLIENT: (<socket._socketobject at 0x1098900c0>, ('127.0.0.1', 53891))}
                self._clients[i], self._addresses[i] = server_socket.accept()
                self._socketProcess[i] = Process(target=self.__main, args = (self._clients[i],))
                self._socketProcess[i].start()
                i += 1    

    def cli_interface(self):
        """ The main CLI interface """

        def format_command(cmd):
            return cmd.strip().lower()
        
        print ('Server commands available. Type "help" for list of commands.')
        
        while True:
            if self._exit == 1:
                print ('Shut Down CLI')
                break

            # Making sure we have a consisent format of user inputted commands
            user_cmd = format_command(raw_input("# "))
            
            for command in self._commands:
                if user_cmd == command['input']:
                    print (command['output'])
                    if command['action'] is not 0:
                        #print ("Do action %i" %command['action'])
                        self.__do_action(command['action'],command['args'])

    def __do_action(self, action, args):
        """
        Does some type of action
        
        Keyword Arguments:
        action -- action number associated with command; see commands list
        args -- arguments associated with command; see commands list
        
        """
        if action == 1:
            for cmd in self._commands: print (cmd['input'])
        elif action == 2:
            for client in self._clients.values():
                client.close()
            print ("Closing down all services.")
            self.__clean()
        elif action == 3:
            for addr in self._addresses.values():
                print (addr)

    def helloRcv(self,thisVer):
        if thisVer == self._version:
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
        


    def __main(self, client):
        size = 1024
        hello = 0
        while True:
            if self._exit == 1:
                print ("Shut Down Client")
                break
            if hello == 0:
                client.send("<?xml version=\"1.0\"?><zeroCli><rpc callType=\"hello\"><ver>%s</ver></rpc></zeroCli>"% self._version)
                hello = client.recv(size)
                """Parse Welcome Message"""
                parseResponse = self.recieveData(hello)
                client.send(parseResponse)
                
            data = client.recv(size)
            if data:
                parseResponse = self.recieveData(data)
                client.send(parseResponse)
        client.close()
