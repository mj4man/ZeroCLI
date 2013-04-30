"""

Expect Device Driver for Cisco 3560.

"""

from interpreter.ciscoIOS import ciscoIOS

class cat3560(ciscoIOS):
    def __init__(self):
        ciscoIOS.__init__(self)
        self.action = self.action
    
    def sendCommand(host,command,username,password):
        # Filler for command send.
        filler = 1

    def capabilities(self):
        return self.action
