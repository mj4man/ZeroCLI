"""

Expect Device Driver for Cisco 3560.

"""

from interpreter.ciscoIOS import ciscoIOS

class cat3560(ciscoIOS):
    def __init__(self):
        """
        Start driver by setting some variables and making it child of the IOS
        interpreter.
        """
        ciscoIOS.__init__(self)
        self.action = self.action
        self.authMethod = "userpass"
        self.capabilities = self.action

    def sendCommand(self,host,action,authtype,auth):
        # Filler for command send.
        command = self.convertAction(action)
        try:
            #Filler for connecting to device.
            filler = 0
        except:
            otype = 1
            output = "Error contacting device."
        return [otype,output]
