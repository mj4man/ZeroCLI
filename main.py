from __future__ import absolute_import
from __future__ import print_function

import sys
from server import server

if __name__ == "__main__":
    """ When the module is called directly it's __name__ will equal the 
        string "__main__", so this code will be excuted as well as all the indent 0
        code. 

        So this is our main entry point into the program. All functions from the other 
        modules should be called from here. 

    """
    # TODO: Start scripting out the main program here. Calling individual functions from your
    #       different modules

    # Calling our main CLI interface
    zeroCli = server
    coreCli = zeroCli.cli_interface()

