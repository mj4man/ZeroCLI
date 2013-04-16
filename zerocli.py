import sys
sys.path.append('core')
sys.path.append('interfaces')
sys.path.append('interpreter')
sys.path.append('actions')
sys.path.append('devices')
import core

zeroCli = core.core()
coreCli = zeroCli.coreCli()
