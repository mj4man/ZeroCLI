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
        print command
        print "Logging in using %s. Credentials are:\n  Username: %s\n  Password: %s" %(authtype,auth[0],auth[1])
