from __future__ import print_function
from __future__ import absolute_import


class coreCLI(object):
    """ Interface for interactive server use. """
    
    def __init__(self):
        """ Define variables and kickstart the processes """
        
        self._commands = [
            {"input": "help", "output": "List of Commands:", "action": 1, "args": 0},
            {"input": "exit", "output": "Starting Exit Process", "action": 2, "args": 0},
            {"input": "clients", "output": "Connected Clients:", "action": 3, "args": 0},
        ]
    
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

    def _do_action(self, action, args):
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

