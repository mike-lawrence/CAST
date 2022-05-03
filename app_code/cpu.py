########
# Initialize debugger & check for expected variables
########
from file_forker import debug_class

debug = debug_class('experiment')
debug.print('I am running')
debug.check_vars(['rx_dict', 'tx_dict'])

#library imports
import sys
import psutil
import numpy as np
import time
import json
import appnope
appnope.nope()

#encode & send header to writer
sys_info = {
	'num_physical_cores':psutil.cpu_count(logical=False)
	, 'num_logical_cores':psutil.cpu_count(logical=True)
	#, 'num_available_cores':len(psutil.Process().cpu_affinity())
	, 'core_max_frequency':psutil.cpu_freq().max
	, 'power_plugged':psutil.sensors_battery().power_plugged
}
tx_dict['writer'].put(kind='attr',payload={'name':'sys_info','value':json.dumps(sys_info)})

# col_names = 'time,mem,'+','.join(['cpu'+str(i) for i in range(psutil.cpu_count())])
col_names = 'time,mem,cpu'
print(col_names)
tx_dict['writer'].put(kind='attr',payload={'name':'col_names','value':col_names})


while True:
	if not rx_dict['parent'].empty():
		message = rx_dict['parent'].get()
		if message.kind == 'quit':
			sys.exit()
	time.sleep(.1)
	tx_dict['writer'].put(kind='data',payload=np.array([time.perf_counter(),psutil.virtual_memory().percent,psutil.cpu_percent()],dtype=np.float64))
