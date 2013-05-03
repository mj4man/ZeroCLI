"""
    ZeroCLI's CLI - Possible the Dummest thing ever, right? Nope.
    OneCLI is a very basic CLI into the ZeroCLI framework. It is meant
    to be lightweight and somewhat barebones. It is in no way intended
    to be fully featured, but is here for testing and raw/barebones
    access into pushing actions to devices.

"""
import os
commands = [
    {"input": "help", "output": "List of Commands:", "action": 1, "args": 0},
    {"input": "exit", "output": "Bye", "action": 2, "args": 0},
    {"input": "actions", "output": "All Action modules currently installed:", "action": 3, "args": ["Device Name"]},
    {"input": "devices", "output": "All Device drivers currently installed:", "action": 4, "args": 0},
    {"input": "send action", "output": "Not done", "action": 5, "args": [" Which Action:", " Which Device Type:", " IP/Hostname:"]},
    ]

def sendAction(args):
    print "Opening Socket."
    print "Sending Action."
    print "Action Queued."

def getActions(device):
    print "Device is %s" %device[0]
    print "Acton"

def getDevices():
    print "Device"

def listCommands(commands):
    for command in commands:
        print command['input']

def doAction(action,args):
    if action == 1:
        global commands
        listCommands(commands)
    if action == 2:
        quit()
    if action == 3:
        getActions(args)
    if action == 4:
        getDevices()
    if action == 5:
        sendAction(args)


def oneCLI(commands):
    usrcommand = raw_input("# ")
    output = 0
    for command in commands:
        if usrcommand == command['input']:
            output = 1
            print command['output']
            if command['action'] is not 0:
                if command['args'] != 0:
                    args = []
                    for arg in command['args']:
                        args.append(raw_input("%s :"%arg))
                else:
                    args = 0
                doAction(command['action'],args)
    if output != 1:
        print "Command not found. Type \"help\" for a list of commands."

print "Wellcome to ZeroCLI's CLI. Try that one on...yeah..."

while True:
    oneCLI(commands)
