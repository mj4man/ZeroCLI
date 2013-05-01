from device.cisco import cat3560
device = cat3560.cat3560()
for action in device.action:
    print "%s: %s"%(action[0], action[1])
