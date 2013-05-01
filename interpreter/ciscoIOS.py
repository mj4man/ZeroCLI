"""

Cisco's Traditional IOS Interpreter.
This interpreter converts actions into IOS commands and sends result to device driver.

"""
import string
from action.network.router.cisco.cisco import cisco

class ciscoIOS(cisco):
    def __init__(self):
        cisco.__init__(self)
        self.action = self.action
    
    def convertAction(self,action):
        command = "Error"
        if action == "getHostName":
            command = "show run | inc hostname"
        return command
