import device

class network(device.device):
	macaddress = "none"
	def macAddr(self,address):
		self.macaddress = address
