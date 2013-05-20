"""

Expect Device Driver for Cisco 3560.

"""
import pexpect
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

    def sendCommand(self,addr,action,authtype,auth):
        # Filler for command send.
        command = self.convertAction(action)
        try:
            session = pexpect.spawn("telnet %s"%addr, timeout=20)
            session.expect(":")
            session.sendline(auth[0])
            session.expect(":")
            session.sendline(auth[1])
            session.expect('([a-zA-Z0-9])*(#)')
            session.sendline(command)
            session.expect('([a-zA-Z0-9])*(#)')
            output = session.before
            output = output.replace(command,'',1)
            otype = 0
        except:
            otype = 1
            output = "Error contacting device."
        return [otype,output]
