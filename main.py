from __future__ import absolute_import
from __future__ import print_function
from core import server, cli
from device import device

if __name__ == "__main__":
    """ When the module is called directly it's __name__ will equal the 
        string "__main__", so this code will be excuted as well as all the indent 0
        code. 

        So this is our main entry point into the program. All functions from the other 
        modules should be called from here. 

    """
    #     ODO: Start scripting out the main program here. Calling individual functions from your
    #       different modules
    def send_dev_action(addr,device,action,authType,auth):
        return device.sendCommand(addr,action,authType,auth)
    def do_cli_action(action, args):
        """
        Does some type of action
        
        Keyword Arguments:
        action -- action associated with command; see commands list
        args -- arguments associated with command; see commands list
        
        """
        if action == "help":
            for cmd in commands: print (cmd['input'])

        elif action == "exit":
            server.clean()
            coreCli.clean()
            print("Press RETURN to exit.")

        elif action == "clients":
            for addr in server.addresses.values():
                print (addr)

    # Setting variables used by objects.
    commands = [
        {"input": "help", "args": 0},
        {"input": "exit", "args": 0},
        {"input": "clients", "args": 0},
    ]
    port = 38500
    version = "0.1"

    # Set up objects.
    # Device object handles communication between device drivers and Core.
    device = device.device
    # Server Object handles communication between Interface and Core.
    server = server.Server(version,port,device,send_dev_action)
    # CoreCLI is responsible for user input to the server.
    coreCli = cli.coreCLI(commands, do_cli_action)
