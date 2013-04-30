from action.network import network

class router(network):
    def __init__(self):
        network.__init__(self)
        self.action = self.action + (
                ['OSPFNetwork','Add OSPF network statement.', 'AREA', 'NETWORK', 'MASK'],
                ['OSPFPassiveInterface','Enable or disable passive interface for OSPF.', 'INTERFACE', 'BOOL']
        )
