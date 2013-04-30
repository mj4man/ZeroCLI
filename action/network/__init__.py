from action import action

class network(action):
    def __init__(self):
        action.__init__(self)
        self.action = self.action + (
                ['setMacAddress','Set the MAC address of a(n) (sub)interface.'],
                ['getMacAddress','Request the MAC address of a(n) (sub)interface.']
        )
