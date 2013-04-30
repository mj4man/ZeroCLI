from __future__ import print_function
from __future__ import absolute_import


class coreCLI(object):
    """ Interface for interactive server use. """
    
    def __init__(self, commands, do_cli_action):
        """ Kickstart the processes """
        self._exit = 0
        self._commands = commands
        self.do_cli_action = do_cli_action
        self.cli_interface()

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
                    self.do_cli_action(command['input'],command['args'])
    def clean(self):
        self._exit = 0
