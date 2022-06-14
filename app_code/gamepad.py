
########
# Initialize debugger & check for expected variables
########
from file_forker import debug_class

debug = debug_class('experiment')
debug.print('I am running')
debug.check_vars(['rx_dict', 'tx_dict'])

#library imports

import sdl2 #for input and display
import sdl2.ext #for input and display
import sys
import time
import copy
import appnope
appnope.nope()

sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
sdl2.SDL_SetHint(sdl2.hints.SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS,b"1")

joystick = sdl2.SDL_JoystickOpen(0)
name = sdl2.joystick.SDL_JoystickName(joystick).decode("UTF-8")

col_info = {
	'trigger':{'col':1,'mapping':{ 'left':2, 'right':5},
	'time':{'col':2},
	'value':{'col':3},
}
tx_dict['writer'].put(kind='attr',payload={'name':'col_info','value':json.dumps(col_info)})

triggers = dict()
for side,index in {'left':2,'right':5}.items():
	triggers[side] = dict()
	triggers[side]['name'] = side
	triggers[side]['index'] = index
	triggers[side]['last_value'] = -(2**16)/2
	triggers[side]['last_time'] = time.perf_counter()
	triggers[side]['response_sent'] = False

while True:
	#check if there are any messages from the parent process
	if not rx_dict['parent'].empty():
		message = rx_dict['parent'].get()
		if message.kind == 'quit':
			sys.exit()
	#get the current time
	now = time.perf_counter()
	#check if there's any data from the gamepad
	sdl2.SDL_PumpEvents()
	for trigger in triggers.items():
		new_value = sdl2.SDL_JoystickGetAxis(joystick,trigger['index'])
		if new_value!=trigger['last_value']:
			trigger['last_time'] = time.perf_counter()
			trigger['last_value'] = new_value
			tx_dict['writer'].put(kind='data',payload=)
			to_write = np.array([[trigger['index'],trigger['last_time'],trigger['last_value']]],dtype=np.float64)
			tx_dict['writer'].put(kind='data',payload=copy.deepcopy(to_write))
			if new_value>trigger['last_value']:
				if new_value>0:
					if not trigger['response_sent']:
						tx_dict['exp'].put(kind=trigger['name'],payload=trigger['last_time'])
						trigger['response_sent'] = True
			else:
				if new_value<0:
					if trigger['response_sent']:
						trigger['response_sent'] = False
