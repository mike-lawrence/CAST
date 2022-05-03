
########
# Initialize debugger & check for expected variables
########
from file_forker import debug_class

debug = debug_class('experiment')
debug.print('I am running')
debug.check_vars(['rx_dict', 'tx_dict'])

#library imports

import usb
import sys
import time
import copy
import appnope
appnope.nope()

#find, claim & configure the gamepad
dev = usb.core.find(idVendor=1118, idProduct=654) #wired 360 gamepad
if dev.is_kernel_driver_active(0):
	dev.detach_kernel_driver(0)
dev.set_configuration()
usb.util.claim_interface(dev, 0)
read_endpoint = dev[0][(0,0)][0] #endpoint to read from
write_endpoint = dev[0][(0,0)][1] #endpoint to write to

#turn the LED off
dev.write(write_endpoint,"\x01\x03\x00",0)
last_data = None

button_names = {\
	'2': {\
		'1':'dpad-up'\
		, '2':'dpad-down'\
		, '4':'dpad-left'\
		, '8':'dpad-right'\
		, '16':'start'\
		, '32':'back'\
		, '64':'left-stick'\
		, '128':'right-stick'\
	}\
	, '3': {\
		'1':'LB'\
		, '2':'RB'\
		, '4':'xbox'\
		, '8':''\
		, '16':'A'\
		, '32':'B'\
		, '64':'X'\
		, '128':'Y'\
	}\
}

last_buttons_down = {\
	'2': {\
		'1':False\
		, '2':False\
		, '4':False\
		, '8':False\
		, '16':False\
		, '32':False\
		, '64':False\
		, '128':False\
	}\
	, '3': {\
		'1':False\
		, '2':False\
		, '4':False\
		, '8':False\
		, '16':False\
		, '32':False\
		, '64':False\
		, '128':False\
	}\
}

#define a useful function for processing button input
def process_buttons(button_set,now,data,last_buttons_down):
	buttons_down = copy.deepcopy(last_buttons_down)
	state = data[button_set]
	events = []
	for i in [128,64,32,16,8,4,2,1]:
		if state>=i:
			buttons_down[str(button_set)][str(i)] = True
			state = state - i
		else:
			buttons_down[str(button_set)][str(i)] = False
		# for i in [128,64,32,16,8,4,2,1]:
		#print [i,buttons_down[str(button_set)][str(i)],last_buttons_down[str(button_set)][str(i)]]
		if buttons_down[str(button_set)][str(i)]!=last_buttons_down[str(button_set)][str(i)]:
			message = {}
			message['time'] = now
			if buttons_down[str(button_set)][str(i)]:
				message['type'] = 'buttonDown'
			else:
				message['type'] = 'buttonUp'
			message['name'] = button_names[str(button_set)][str(i)]
			events.append(message)
	return [events,buttons_down]

def send_event(message):
	tx_dict['exp'].put(kind='event',payload=message)
	tx_dict['writer'].put(kind='event',payload=message)


while True:
	#check if there are any messages from the parent process
	if not rx_dict['parent'].empty():
		message = rx_dict['parent'].get()
		if message.kind == 'quit':
			usb.util.release_interface(dev, 0)
			sys.exit()
	#get the current time
	now = time.perf_counter()
	#check if there's any data from the gamepad
	try:
		data = dev.read(read_endpoint.bEndpointAddress,read_endpoint.wMaxPacketSize,0)
	except usb.core.USBError as e:
		data = None
		if e.args == ('Operation timed out',):
			continue
	#process the data from the gamepad
	if data is not None:
		if len(data)==20: #getting some button/axis state data
			if last_data is not None:
				for button_set in [2,3]: #check both button sets
					if last_data[button_set]!=data[button_set]: #check buttons associated with state 2
						button_events,last_buttons_down = process_buttons(button_set=button_set,now=now,data=data,last_buttons_down=last_buttons_down)
						for this_button_event in button_events:
							message = {}
							message['type'] = 'button'
							message['id'] = this_button_event
							message['time'] = now
							send_event(message)
				for trigger in [4,5]:
					if last_data[trigger]!=data[trigger]:
						message = {}
						message['type'] = 'trigger'
						if trigger==4:
							message['id'] = 'left'
						else:
							message['id'] = 'right'
						message['time'] = now
						message['value'] = data[trigger]
						send_event(message)
			#write/overwrite last_data with current data
			last_data = data
