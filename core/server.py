from __future__ import print_function
from __future__ import absolute_import

import socket
import threading
import sys
import xml.etree.ElementTree as E    
from multiprocessing import Process, Queue


class Server(object):
    """ Orchestrates communication between all zeroCLI components """
    
    def __init__(self,version,port):
        """ Define variables and kickstart the processes """
        
        self._exit = 0
        self._clients = {}
        self.addresses= {}
        self._socketProcess = {}
        self._version = version
        self._port = port
        self.queue = Queue()
        
        print ("Starting service. Listening on port {0}.".format(self._port))
        
        # Creating a thread to wait for a new client or interface to start
        server = threading.Thread(target=self._listen)
        server.start()
    
    def clean(self):
        # Cleanup function. Called by main.py when ready to exit.
        self._exit = 1
        timeout = 5
        for client in self._clients.values():
            client.close()
        try:
            client_socket = socket.socket()
            client_socket.connect(('localhost', self._port))
            time.sleep(1)
            client_socket.close()
        except:
            print("Couldn't connect to server")
        for process in self._socketProcess.values():
            process.terminate()
        sys.exit()
    
    def _listen(self):
        """ Listens for new client, then starts a new process """
        try:
            server_socket = socket.socket()
            server_socket.bind(('', self._port))
            server_socket.listen(5)
        except:
            print ("\nError binding server to port. Server dying. Type 'exit' to quit...")
            self.clean()
        i = 0 
        while True:
            if self._exit == 1:
                print("Main Socket Listener Shutdown.")
                server_socket.close()
                break
            else:
                self._clients[i], self.addresses[i] = server_socket.accept()
                self._socketProcess[i] = Process(target=self._clientHandle, args = (self._clients[i],))
                self._socketProcess[i].start()
                i += 1    

    def helloRcv(self,thisVer):
        # Place holder for future hello check and return.
        if thisVer == self._version:
            return "Yes"
        else:
            return "No"

    def recieveData(self,data):
        """
        Recieve data from client and parce the response. This function contains all the actions for RPC calls.
        """
        try:
            tree = E    .fromstring(data)
            for child in tree.findall("rpc"):
                if child.get('callType') == 'hello':
                    # Handle hello from Client and establish connection.
                    ver = child.find('ver').text
                    returnValue = self.helloRcv(ver)
                
            return returnValue
        except Exception, e:
            return "<?xml version\"1.0\"?><zeroCli><error errorType=\"1\">%s</error></zeroCli>" % e
        


    def _clientHandle(self, client):
        """
        This functon handles the client's communication. Recieves XML and sends to parcer. Sends return XML.
        """
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
