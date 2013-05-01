from action.network.router.router import router

class cisco(router):
    def __init__(self):
        router.__init__(self)
        self.action = self.action + (
                ['EIGRPNetwork','Add EIGRP network statement.', 'NETWORK', 'MASK'],
                ['EIGRPAuto_Summary','Enable or disable EIGRP auto-summary.', 'BOOL']
        )
