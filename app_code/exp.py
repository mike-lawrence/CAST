########
# REMOVE THIS SECTION WHEN DONE DEVELOPING THE CORE EXPERIMENT
########

import multiprocessing
from collections import OrderedDict
from file_forker import q_class
this_ctx = multiprocessing.get_context('spawn')
rx_dict = {}
rx_dict['parent'] = q_class(name='parent_to_self',tx='parent',rx='self',ctx=this_ctx)
rx_dict['gamepad'] = q_class(name='parent_to_self',tx='parent',rx='self',ctx=this_ctx)
tx_dict = {}
tx_dict['parent'] = q_class(name='self_to_parent',tx='self',rx='parent',ctx=this_ctx)


########
# Initialize debugger & check for expected variables
########
from file_forker import debug_class
debug = debug_class('exp')
debug.print('I am running')
debug.check_vars(['rx_dict', 'tx_dict'])

import sys
if sys.platform=='darwin':
	import appnope
	appnope.nope()

# change wd (if in debugging mode)
import os
if os.getcwd().split('/')[-1]!='app_code':
	os.chdir('app_code')

########
#Important parameters
########

viewing_distance = 2.0 #units can be anything so long as they match those used in screen_width below
screen_width = 1.0 #units can be anything so long as they match those used in viewing_distance above
screen_size = (1920,1080) #pixel resolution of the screen
window_size = (1800,800) #pixel resolution of the screen

response_modality = 'trigger' # 'key' or 'button' or 'trigger'
left_key = 'z' #specify the key for the left-pointing target arrows
right_key = '/' #specify the key for the right-pointing target arrows
left_button = 4 #specify the button for the left-pointing target arrows
right_button = 5 #specify the button for the right-pointing target arrows
trigger_criterion_value = 0 #specify the trigger criterion

target_direction_list = ['left','right']
target_location_list = ['left','right']
flanker_list = ['neutral','congruent','incongruent'] #specify the types of flankers to employ. Options: neutral (no flankers), congruent, incongruent
warning_list = ['present','absent']
cue_validity_list = ['valid','invalid']
arrow_validity_ratio = 2 #2:1 valid:invalid trials
# warning_intensity_list = ['none','lo','hi']

warning_hi_volume = 1
warning_lo_volume = .1

warning_duration = 0.100
endo_warning_target_SOA = 1.000
exo_warning_target_SOA = 0.200

fixation_interval_min = 1.000 #specify a minimum fixation interval
fixation_interval_mean = 2.000 #specify the mean fixation interval, where each FI is randomly drawn from an exponential distribution with a minimum of fixation_interval_min
fixation_interval_max = 10.000 #specify a maximum fixation interval

response_timeout = 1.000 #how long to wait for response before terminating the trial
feedback_duration = 1.000 #specify the feedback_duration

trials_per_break = 24
number_of_blocks_per_task = 2 #specify the number of blocks

instruction_size_in_degrees = 1 #specify the size of the instruction text
feedback_size_in_degrees = 1 #specify the size of the feedback text (if used)
target_width_in_degrees = 2 #specify the width of the target arrows
offset_in_degrees = 5 #specify the vertical offset of the target from fixation
flanker_seperation_in_degrees = .2 #specify the size of the space between flankers

arrow_width_in_degrees = 1 #(when horizontal)
arrow_thickness = .15
arrow_height = .5
arrow_head = 1/3.0

text_width = .9 #specify the proportion of the screen to use when drawing instructions


########
# Import libraries
########
if sys.platform == "win32":
	import sdl2dll
import sdl2 #for input and display
import sdl2.ext #for input and display
import numpy #for image and display manipulation
from PIL import Image #for image manipulation
from PIL import Image
import soundfile as sf #for loading sounds
import sounddevice as sd #for playing sounds
import aggdraw
import math
import sys
import os
import random
import time
from collections import OrderedDict

########
# define trial class
########

def list_to_viDict(l):
	return({v:i for i,v in enumerate(l)})

class events_info_class:
	def __init__(self,**kwargs):
		self.od = OrderedDict()
		for key, value in kwargs.items():
			self.od[key] = {}
			if value is not None:
				self.od[key]['mapping'] = list_to_viDict(value)

events_info = events_info_class(
	block = None
	, trial = None
	, last_break_duration = None
	, fixation_interval = None
	, warning_intensity = ['none','lo','hi']
	, cue_validity = cue_validity_list
	, flankers = flankers_list
	, target_location = target_location_list
	, target_direction = target_direction_list
	, anticipation = None
	, response = target_direction_list
	, error = None
)
event_cols['block'] = {}
event_cols['trial'] = {}
event_cols['last_break_duration'] = {}
event_cols['fixation_interval'] = {}
event_cols['warning_intensity'] = {'mapping' = {}}
event_cols['cue_validity'] = {'mapping' = list_to_viDict(cue_validity_list)}
event_cols['cued_location'] = {'mapping' = list_to_viDict(target_location_list)}
event_cols['flankers'] = {'mapping' = list_to_viDict(flankers_list)}
event_cols['target_location'] = {'mapping' = list_to_viDict(target_location_list)}
event_cols['target_direction'] = {'mapping' = list_to_viDict(target_direction_list)}
event_cols['anticipation'] = {'mapping' = {'FALSE':0,'TRUE':1}}
event_cols['response'] = {'mapping' = list_to_viDict(target_direction_list)}
event_cols['error'] = {'mapping' = {'FALSE':0,'TRUE':1}}
event_cols['rt'] = {}
event_cols['feedback_response'] = {'mapping' = {'FALSE':0,'TRUE':1}}



class trial_info:
	def __init__(self,**kwargs):
		self.od = OrderedDict()
		for key, value in kwargs.items():
			self.od[key] = value
	def get(self,key):
		return self.od[key]
	def put(self,**kwargs):
		self.od[key] = value
	def 



event_cols = OrderedDict()
event_cols['block'] = {}
event_cols['trial'] = {}
event_cols['last_break_duration'] = {}
event_cols['fixation_interval'] = {}
event_cols['warning_intensity'] = {'mapping' = {}}
event_cols['cue_validity'] = {'mapping' = list_to_viDict(cue_validity_list)}
event_cols['cued_location'] = {'mapping' = list_to_viDict(target_location_list)}
event_cols['flankers'] = {'mapping' = list_to_viDict(flankers_list)}
event_cols['target_location'] = {'mapping' = list_to_viDict(target_location_list)}
event_cols['target_direction'] = {'mapping' = list_to_viDict(target_direction_list)}
event_cols['anticipation'] = {'mapping' = {'FALSE':0,'TRUE':1}}
event_cols['response'] = {'mapping' = list_to_viDict(target_direction_list)}
event_cols['error'] = {'mapping' = {'FALSE':0,'TRUE':1}}
event_cols['rt'] = {}
event_cols['feedback_response'] = {'mapping' = {'FALSE':0,'TRUE':1}}

#add column-number
for i in 1:length(event_cols):
	event_cols[i]['col'] = i

def make_trial_data_dict(
	block
	, trial
	, last_break_duration
	, fixation_interval
	, warning_intensity
	, cue_validity
	, cued_location
	, flankers
	, target_location
	, target_direction
	, 
)

def prep_data_for_writer(data_dict):
	array_for_writer = []
	for key,value in data_dict.item():
		array_for_writer.append(event_cols[key][value])



########
# Initialize the random number generator
########
random.seed()

########
# Initialize the window
########

exp_window = sdl2.ext.Window(
	'Experiment'
	, size = window_size
	, position = [
		  int((screen_size[0]/2)-(window_size[0]/2))
		, int((screen_size[1]/2)-(window_size[1]/2))
	]
	, flags = sdl2.SDL_WINDOW_SHOWN
)
exp_window_surf = sdl2.SDL_GetWindowSurface(exp_window.window).contents
#exp_window_array = sdl2.ext.pixels3d(exp_window_surf.contents)
sdl2.ext.fill(exp_window_surf,sdl2.pixels.SDL_Color(r=0, g=0, b=0, a=255))
exp_window.show()
exp_window.refresh()
sdl2.SDL_SetWindowResizable(exp_window.window,False)

window_x_center = window_size[0]/2 #store the location of the screen's x center
window_y_center = window_size[1]/2 #store the location of the screen's y center


########
# initialize the sound objects
########

warning_sound = sf.read('stimuli/pink_stereo.wav')
background_sound = sf.read('stimuli/pink_mono.wav')


########
#Perform some calculations to convert stimulus measurements in degrees to pixels
########
screen_width_in_degrees = math.degrees(math.atan((screen_width/2.0)/viewing_distance)*2)
PPD = screen_size[0]/screen_width_in_degrees #compute the pixels per degree (PPD)

instruction_font_size = int(instruction_size_in_degrees*PPD)
feedback_font_size = int(feedback_size_in_degrees*PPD)

offset = int(offset_in_degrees*PPD)

flanker_seperation = int(flanker_seperation_in_degrees*PPD)

target_width = int(round(target_width_in_degrees*PPD))

arrow_width = arrow_width_in_degrees*PPD
arrow_half_height = int(arrow_width*arrow_height/2.0)	
arrow_height = int(arrow_width*arrow_height)
arrow_head_width = int(arrow_width*arrow_head)
arrow_half_thickness = int(arrow_width*arrow_thickness/2)
arrow_width = int(arrow_width)


########
#Define some useful colors
########
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
grey = (127,127,127)
dark_grey = (63,63,63)
light_grey = (192, 192, 192)


########
#Initialize the fonts
########

print(feedback_font_size)
exp_font = sdl2.ext.ttf.FontTTF(
	font = 'stimuli/DejaVuSans.ttf'
	, size = str(feedback_font_size)+'px'
	, color = light_grey
	, height_chars = 'X'
)

exp_font.add_style(
	name = 'correct_feedback'
	, size = str(feedback_font_size)+'px'
	, color = light_grey
)
exp_font.add_style(
	name = 'incorrect_feedback'
	, size = str(feedback_font_size)+'px'
	, color = red
)

exp_font.add_style(
	name = 'instruction'
	, size = str(instruction_font_size)+'px'
	, color = light_grey
)

exp_font.add_style(
	name = 'caption'
	, size = str(int(instruction_font_size/2.0))+'px'
	, color = light_grey
)


# feedback_font.render_text(text, style='default', line_h=None, width=None, align='center')


########
# Create sprites for visual stimuli
########

arrow_points = ( 
    0 , arrow_half_height ,
    arrow_head_width , 0 , 
    arrow_head_width , arrow_half_height - arrow_half_thickness ,
    arrow_width , arrow_half_height - arrow_half_thickness ,
    arrow_width , arrow_half_height + arrow_half_thickness ,
    arrow_head_width , arrow_half_height + arrow_half_thickness ,
	arrow_head_width , arrow_height , 
	0 , arrow_half_height
)

grey_fill = aggdraw.Brush(grey)
arrow_left_im = Image.new('RGBA',[arrow_width,arrow_height],(0,0,0,0))
arrow_left_draw = aggdraw.Draw(arrow_left_im)
arrow_left_draw.polygon( arrow_points, grey_fill )
arrow_left_surf = sdl2.ext.image.pillow_to_surface(arrow_left_im)
arrow_right_surf = sdl2.ext.image.pillow_to_surface(arrow_left_im.transpose(Image.FLIP_LEFT_RIGHT))

black_pen = aggdraw.Pen(black,arrow_half_height)
square = aggdraw.Draw('RGBA',[arrow_width*2,arrow_width*2],(0,0,0,0))
square.rectangle([0+arrow_half_height,0+arrow_half_height,arrow_width*2-arrow_half_height,arrow_width*2-arrow_half_height],black_pen)
square_surf = sdl2.ext.image.pillow_to_surface(square)

circle = aggdraw.Draw('RGBA',[arrow_width*2,arrow_width*2],(0,0,0,0))
circle.ellipse([0+arrow_half_height,0+arrow_half_height,arrow_width*2-arrow_half_height,arrow_width*2-arrow_half_height],black_pen)
circle_surf = sdl2.ext.image.pillow_to_surface(circle)

black_fill = aggdraw.Brush(black)
dot = aggdraw.Draw('RGBA',[int(target_width/2),int(target_width/2)],(0,0,0,0))
dot.ellipse([0,0,target_width/2,target_width/2],black_fill)
dot_surf = sdl2.ext.image.pillow_to_surface(dot)


#define a function to read and resize an image, returing a pygame surface
def get_image(image_file):
	original_image = Image.open(image_file)
	start_width = original_image.size[0]
	start_height = original_image.size[1]
	aspect = start_width*1.0/start_height
	target_height = int(round(target_width/aspect))
	resized_image = original_image.resize((target_width , target_height), Image.ANTIALIAS)
	return resized_image

fish_files = [
	  'stimuli/fish_left_neutral.png'
	, 'stimuli/fish_left_sad.png'
	, 'stimuli/fish_left_happy.png'
	, 'stimuli/fish_left_happy2.png'
]

fish_surfs = {}
for file in fish_files:
	name = file.replace('stimuli/fish_left_','').replace('.png','')
	fish_surfs[name] = {'file':file,'name':name}
	fish_surfs[name]['image'] = get_image(file)
	fish_surfs[name]['left'] = sdl2.ext.image.pillow_to_surface(fish_surfs[name]['image'])
	fish_surfs[name]['right'] = sdl2.ext.image.pillow_to_surface(fish_surfs[name]['image'].transpose(Image.FLIP_LEFT_RIGHT))

target_height = fish_surfs['neutral']['image'].size[1]

def blit_surf(src,dest,loc):
	sdl2.SDL_BlitSurface(
		src
		, None
		, dest
		, sdl2.SDL_Rect(
			  int( dest.w/2 - src.w/2 + loc[0] )
			, int( dest.w/2 - src.w/2 + loc[1] )
			, src.w
			, src.h
		)
	)


def make_school_surf(center_surf,flanker_surf=None):
	school_surf = sdl2.ext.surface._create_surface(
		size = ( 3*target_width + 2*flanker_seperation , 3*target_height +2*flanker_seperation ) 
		, fill = black
	).contents
	#central fish
	blit_surf(
		src = center_surf
		, dest= school_surf
		, loc = (0,0)
	)
	if flanker_surf is not None:
		vert_offset = target_height + flanker_seperation
		#above center
		blit_surf(
			src = flanker_surf
			, dest= school_surf
			, loc = (0,-vert_offset)
		)
		#below center
		blit_surf(
			src = flanker_surf
			, dest= school_surf
			, loc = (0,vert_offset)
		)
		horiz_offset = target_width + flanker_seperation
		#left of center
		blit_surf(
			src = flanker_surf
			, dest= school_surf
			, loc = (-vert_offset,0)
		)
		#right of center
		blit_surf(
			src = flanker_surf
			, dest= school_surf
			, loc = (vert_offset,0)
		)
	return school_surf

school_surfs = {}
for target in ['left','right']:
	for flankers in ['left','right','neutral']:
		target_surf = fish_surfs['neutral'][target]
		if flankers=='neutral':
			kind = 'neutral'
			flankers_surf = None
		else:
			flankers_surf = fish_surfs['neutral'][flankers]
			if target==flankers:
				kind = 'congruent'
			else:
				kind = 'incongruent'
		school_surfs[target+'_'+kind] = make_school_surf(target_surf,flankers_surf)



########
# Drawing and helper functions
########

def exit_safely():
	tx_dict['parent'].put(kind='quit')
	sys.exit()

def check_triggers(exhaustive=False):
	found_triggers = None
	if exhaustive:
		while not rx_dict['gamepad'].empty():
			message = rx_dict['gamepad'].get()
			if message['type'] == 'trigger':
				found_triggers = message
	else:
		if not rx_dict['gamepad'].empty():
			message = rx_dict['gamepad'].get()
			if message['type'] == 'trigger':
				if message['value'] > trigger_criterion_value:
					found_triggers = message
	return found_triggers

#define a function that waits for a given duration to pass
def wait(duration=None,until=None,response_terminated=False):
	start = time.perf_counter()
	found_triggers = None
	while True:
		if duration is not None:
			if time.perf_counter() < (start + duration):
				break
		if until is not None:
			if time.perf_counter() < until:
				break
		if response_terminated:
			found_triggers = check_triggers()
			if found_triggers is not None:
				break
	return found_triggers

#define a function that will kill everything safely
def exit_safely():
	tx_dict['parent'].put(kind='quit')
	sys.exit()


#define a function to draw a pygame surface centered on a given offset from the center of the screen
def blit_to_screen(surf,x_offset=0,y_offset=0):
	blit_surf(surf,exp_window_surf,(x_offset,y_offset))


#define a function that draws a text at center
def draw_feedback(text,style='correct_feedback'):
	this_render = exp_font.render_text(text=text,style=style)
	blit_to_screen(this_render)


#define a function that draws an arrow
def draw_arrow(cued_location):
	if cued_location == 'left':
		blit_to_screen( arrow_left_surf )
	elif cued_location == 'right':
		blit_to_screen( arrow_right_surf )


#define a function that draws an arrow
def draw_dot(cued_location):
	if cued_location == 'left':
		blit_to_screen( dot_surf , -offset )
	elif cued_location == 'right':
		blit_to_screen( dot_surf, offset )



#define a function that draws a shape on the screen
def draw_shape(shape):
	if shape == 'circle':
		blit_to_screen( circle_surf )
	elif shape == 'square':
		blit_to_screen( square_surf )


#define a function that draws a target and, if necessary, flankers.
def draw_target(flankers,target_location,target_direction):
	if target_direction=='left':
		loc = -offset
	else:
		loc = offset
	blit_to_screen( school_surfs[target_direction+'_'+flankers] , loc )

#define a function that formats text for the screen
def draw_text(text,style):
	this_render = exp_font.render_text(text=text,style=style)
	if style=='caption':
		y_offset = exp_window_surf.h/2 - this_render.h/2
	else:
		y_offset = 0
	blit_to_screen(this_render,y_offset=y_offset)

#define a function that waits for a response
def wait_for_response():
	done = False
	while not done:
		sdl2.SDL_PumpEvents()
		if not rx_dict['parent'].empty():
			message = rx_dict['parent'].get()
			if message.kind == 'quit':
				sys.exit()
		for event in sdl2.ext.get_events():
			if event.type==sdl2.SDL_KEYDOWN:
				key = sdl2.keyboard.SDL_GetKeyName(event.key.keysym.sym).decode("utf-8").lower()
				if key=='escape':
					exit_safely()
				elif key=='return':
					done = True
		if not rx_dict['gamepad'].empty():
			message = rx_dict['gamepad'].get()
			if message['type'] == 'button':
				done = True

def screen_fill(color):
	sdl2.ext.fill(exp_window_surf,color)

#define a function that prints a message on the screen while looking for user input to continue. The function returns the total time it waited
def show_message(my_text):
	message_viewing_time_start = time.perf_counter()
	sdl2.SDL_PumpEvents()
	screen_fill(black)
	exp_window.refresh()
	screen_fill(black)
	draw_text(my_text, 'instruction')
	wait(.5)
	exp_window.refresh()
	screen_fill(black)
	wait_for_response()
	exp_window.refresh()
	screen_fill(black)
	wait(.5)
	message_viewing_time = time.perf_counter() - message_viewing_time_start
	return message_viewing_time


#define a function that requests user input
def get_input(get_what):
	get_what = get_what+'\n '
	text_input = ''
	screen_fill(black)
	exp_window.refresh()
	wait(.5)
	my_text = get_what+text_input
	screen_fill(black)
	draw_text(text=my_text,style='instruction')
	exp_window.refresh()
	screen_fill(black)
	done = False
	while not done:
		sdl2.SDL_PumpEvents()
		for event in sdl2.ext.get_events() :
			if event.type==sdl2.SDL_KEYDOWN:
				key = sdl2.keyboard.SDL_GetKeyName(event.key.keysym.sym).decode("utf-8").lower()
				if key=='escape':
					exit_safely()
				elif key=='return':
					done = True
				elif key == 'backspace':
					if text_input!='':
						text_input = text_input[0:(len(text_input)-1)]
						my_text = get_what+text_input
						screen_fill(black)
						draw_text(my_text, 'instruction')
						exp_window.refresh()
				else:
					text_input = text_input + key
					my_text = get_what+text_input
					screen_fill(black)
					draw_text(text=my_text,style='instruction')
					exp_window.refresh()
	screen_fill(black)
	exp_window.refresh()
	return text_input


#define a function to generate a fixation interval
def get_fixation_interval():
	fixation_interval = random.expovariate(1/(fixation_interval_mean-fixation_interval_min))+fixation_interval_min
	while fixation_interval>fixation_interval_max:
		fixation_interval = random.expovariate(1/(fixation_interval_mean-fixation_interval_min))+fixation_interval_min
	return fixation_interval


#define a function that generates a randomized list of trial-by-trial stimulus information representing a factorial combination of the independent variables.
def get_trials(task):
	trials=[]
	for flankers in flanker_list:
		for target_location in target_location_list:
			for target_direction in target_direction_list:
				if task=='n':
					warning_intensity_list = ['none','hi']
				else:
					warning_intensity_list = ['lo','hi']
				for warning_intensity in warning_intensity_list:
					for cue_validity in cue_validity_list:
						fixation_interval = get_fixation_interval()
						if cue_validity=='valid':
							cued_location = target_location
							trials.append([fixation_interval,warning_intensity,cue_validity,cued_location,flankers,target_location,target_direction])
							if task=='n':
								for i in range(arrow_validity_ratio-1):
									trials.append([fixation_interval,warning_intensity,cue_validity,cued_location,flankers,target_location,target_direction])
						elif cue_validity=='invalid':
							if target_location=='right':
								cued_location = 'left'
							else:
								cued_location = 'right'
							trials.append([fixation_interval,warning_intensity,cue_validity,cued_location,flankers,target_location,target_direction])
	random.shuffle(trials)
	return trials


#define a function to do stuff when Ss respond too soon
def too_soon(this_trial_info,trial_list):
	pre_target_response = 'TRUE'
	this_trial_info[0] = get_fixation_interval()
	trial_list.append(this_trial_info)
	random.shuffle(trial_list)
	#show feedback
	feedback_text = 'Too soon!'
	screen_fill(black)
	draw_feedback(feedback_text,'incorrect_feedback')
	exp_window.refresh()
	feedback_done_time = time.perf_counter()+feedback_duration
	return trial_list

#define a function to do stuff when Ss respond too soon
def process_feedback_response(this_trial_info,trial_list):
	pre_target_response = 'TRUE'
	this_trial_info[0] = get_fixation_interval()
	trial_list.append(this_trial_info)
	random.shuffle(trial_list)
	#show feedback
	feedback_text = 'Too soon!'
	screen_fill(black)
	draw_feedback(feedback_text,'incorrect_feedback')
	exp_window.refresh()
	feedback_done_time = time.perf_counter()+feedback_duration
	# return trial_list
	#process any responses from the feedback period
	if len(responses)>0:
		feedback_response = 'TRUE'
		#show feedback
		screen_fill(black)
		if feedback_text=='Miss!':
			draw_feedback('Too slow!','incorrect_feedback')
		else:
			draw_feedback('Respond only once!','incorrect_feedback')
		exp_window.refresh()
		feedback_done_time = time.perf_counter()+feedback_duration
		#wait until second feedback period is done
		wait(until=feedback_done_time,response_terminated=True)


def start_sounds():
	background_sound.set_volume(warning_lo_volume)
	background_sound.play(0)
	warning_sound.set_volume(0)
	warning_sound.play(0)

def stop_sounds():
	background_sound.stop()
	warning_sound.stop()


#define a function that runs a block of trials
def run_block(block,message_viewing_time):

	#start the sounds
	start_sounds()

	#get trials
	trial_list = get_trials(task)
	if block=='practice':
		trial_list = trial_list[0:trials_per_break]
	
	#run the trials
	trial_num = 0
	while len(trial_list)>0:
		#bump the trial number
		trial_num = trial_num + 1

		#break if necessary (at beginning rather than end so we can use `continue` below)
		if (trial_num>1) & (((trial_num-1)%trials_per_break)==0):
			stop_sounds()
			message_viewing_time = show_message('Take a break!\nWhen you are ready, press any button to continue the experiment.')
			start_sounds()

		#get the trial info
		trial_info = trial_list.pop(0)
		fixation_interval,warning_intensity,cue_validity,cued_location,flankers,target_location,target_direction = trial_info
		
		#start the trial by showing the fixation screen
		if task=='n':
			screen_fill(black)
			if warning_intensity!='none':
				draw_shape('circle')
			else:
				draw_shape('square')
			draw_arrow(cued_location)
		else:
			screen_fill(black)
			draw_feedback('+')
		exp_window.refresh()
		
		#get the trial start time and compute event times
		trial_start_time = time.perf_counter()
		warning_on_time = trial_start_time + fixation_interval
		warning_off_time = warning_on_time + warning_duration
		if task=='n':
			target_on_time = warning_on_time + endo_warning_target_SOA
		else:
			target_on_time = warning_on_time + exo_warning_target_SOA
		response_timeout_time = target_on_time + response_timeout
				
		if task=='n':
			#prep the target screen
			screen_fill(black)
			if warning_intensity!='none':
				draw_shape('circle')
			else:
				draw_shape('square')
			draw_arrow(cued_location)
			draw_target(flankers,target_location,target_direction)
		else:
			#prep the cue screen
			screen_fill(black)
			draw_feedback('+')
			draw_dot(cued_location)
				
		#wait until it's time to present the warning (and possibly cue)
		wait(until=warning_on_time)
		
		if task=='x':
			#show the cue
			exp_window.refresh()
		warning_on_time_delta1 = time.perf_counter() - warning_on_time

		#present the warning
		if warning_intensity!='none':
			if warning_intensity=='lo':
				warning_sound.set_volume(warning_hi_volume)
			else:
				warning_sound.set_volume(warning_hi_volume)
			background_sound.set_volume(0)
		warning_on_time_delta2 = time.perf_counter() - warning_on_time
		
		if check_triggers() is not None:
			trial_list = too_soon(trial_info,trial_list)
			continue

		if task=='x':
			#prep the post-cue screen
			screen_fill(black)
			draw_feedback('+')
		
		#wait until the warning period is done
		wait(until=warning_off_time)

		if task=='x':
			#turn off the cue
			exp_window.refresh()
			#prep the target screen
			screen_fill(black)
			draw_feedback('+')
			draw_target(flankers,target_location,target_direction)
		warning_off_time_delta1 = time.perf_counter() - warning_off_time

		#stop the warning
		background_sound.set_volume(warning_lo_volume)
		warning_sound.set_volume(0)
		warning_off_time_delta2 = time.perf_counter() - warning_off_time
		
		if check_triggers() is not None:
			trial_list = too_soon(trial_info,trial_list)
			continue

		#wait until it's time to present the target
		wait(until=target_on_time)

		#present the target
		exp_window.refresh() #this won't block bc too much time since last refresh has likely elapsed, but if we quickly draw and refresh again, the second refresh will block
		# draw & show a second target screen for more precise onset timing
		screen_fill(black)
		if task=='x':
			draw_feedback('+')
		else:
			if warning_intensity!='none':
				draw_shape('circle')
			else:
				draw_shape('square')
			draw_arrow(cued_location)
		draw_target(flankers,target_location,target_direction)
		exp_window.refresh() # this should block until actually shown, so time of prior refresh is 
		target_on_time2 = time.perf_counter() - 1.0/60.0
		target_on_time_delta = target_on_time2 - target_on_time

		if check_triggers() is not None:
			trial_list = too_soon(trial_info,trial_list)
			continue

		#wait until response
		response_event = wait(until=response_timeout_time,response_terminated=True)
	
		if response_event is None:
			response = -1
			error = -1
			rt = -1
			feedback_text = 'Miss!'
			feedback_style = 'incorrect_feedback'
			feedback_done_time = response_timeout_time + feedback_duration
		else:
			response = response_event['id']
			if response == target_direction:
				error = 0
			else:
				error = 1
			rt = response_event['time'] - target_on_time2
			feedback_style = 'correct_feedback'
			feedback_text = str(int(round(rt*1000)))
			feedback_done_time = response_event['time'] + feedback_duration

		#present the feedback screen
		screen_fill(black)
		draw_feedback(feedback_text,feedback_style)
		exp_window.refresh()

		#wait until feedback period is done
		wait(until=feedback_done_time,response_terminated=True)
		
		if check_triggers() is not None:
			trial_list = process_feedback_response(trial_info,trial_list)
			continue
		
		continue # just marking the end of the trial while loop
	stop_sounds() #make sure the sounds are stopped when done all trials


#
def do_tts(text):
	wait_for_response()

def do_auto_tts(text,to_eval=False):
	for sentence in text.split('.'):
		sentence = sentence+'.'
		screen_fill(black)
		if to_eval:
			eval(to_eval)
		draw_caption(sentence)
		exp_window.refresh()
		wait_for_response()


#define a function that demos the stimuli during instructions
def do_general_demo():

	text = "During this experiment, you should be sitting comfortably and facing the screen squarely. You should be sitting far enough away from the screen that the end of the piece of string in front of you comes to the point between your eyes. Please use the string now to check your distance and move your chair until the end comes to the point between your eyes. When you are ready to continue, press any button on the game controller in front of you."
	do_auto_tts(text)
	wait_for_response()

	text = "Throughout the experiment you'll be using the game controller to respond to images that will appear on the screen. The only buttons that you'll be using are the two large trigger buttons that you can press with your right and left index fingers."
	do_auto_tts(text)

	text = "Whenever you see a fish on the screen, press the button corresponding to the direction that the fish is pointing. So if a fish comes up on the screen pointing left like you see here, you'd press the left button."
	do_auto_tts(text,to_eval="draw_target('neutral','left','left')")

	text = "After you press the button, you'll see a number appear briefly at the center of the screen like this. This number shows how long it took you to press the button, in milliseconds. You want this number to be as small as possible, usually between 300 and 700, so try to press the buttons as fast as you can."
	do_auto_tts(text,to_eval="draw_feedback('538')")

	text = "Sometimes you may press the wrong button by mistake. Don't worry too much if this happens, it turns out that we learn almost as much from your mistakes as we do from your accurate answers, so going fast is what really matters. However, if you do make a mistake, don't bother trying to correct your response by pressing the other button."
	do_auto_tts(text)

	text = "You can only press the button once per fish, and if you press any other buttons a message like this will appear telling you to respond only once."
	screen_fill(black)
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "You can only press the button once per fish, and if you press any other buttons a message like this."
	do_tts(partial_text)
	screen_fill(black)
	draw_feedback('Respond only once!','incorrect_feedback')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "Will appear telling you to respond only once."
	do_tts(partial_text)

	text = "You only have about one second to press a button once the fish appears, and if you don't respond in time a message like this will appear telling you that you missed the fish."
	screen_fill(black)
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "You only have about one second to press a button once the fish appears, and if you don't respond in time a message like this"
	do_tts(partial_text)
	screen_fill(black)
	draw_feedback('Miss!','incorrect_feedback')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "will appear telling you that you missed the fish."
	do_tts(partial_text)

	text = "Finally, if you press a button before the fish appears a message like this will appear telling you that you pressed the button too soon."
	screen_fill(black)
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "Finally, if you press a button before the fish appears a message like this."
	do_tts(partial_text)
	screen_fill(black)
	draw_feedback('Too soon!','incorrect_feedback')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "will appear telling you that you pressed the button too soon."
	do_tts(partial_text)

	text = "The fish will appear pointing either left or right and they can appear on the left side of the screen as you've been seeing so far, but they can also appear on the right side of the screen, again pointing either left or right."
	screen_fill(black)
	draw_target('neutral','left','left')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "The fish will appear pointing either left"
	do_tts(partial_text)

	screen_fill(black)
	draw_target('neutral','left','right')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "or right and they can appear on the left side of the screen as you've been seeing so far"
	do_tts(partial_text)

	screen_fill(black)
	draw_target('neutral','right','left')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "but they can also appear on the right side of the screen, again pointing either left"
	do_tts(partial_text)

	screen_fill(black)
	draw_target('neutral','right','right')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "or right"
	do_tts(partial_text)

	text = "Where each fish appears and what direction it's pointing are both completely random, so there won't be any pattern to where the fish will appear, and there also won't be any pattern to the direction the fish is pointing. Remember your job is to indicate what direction the fish is pointing no matter where it appears."
	do_auto_tts(text)

	text = "Sometimes there will only be one fish as you've been seeing so far, but other times there will be a whole school of fish like this."
	screen_fill(black)
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "Sometimes there will only be one fish as you've been seeing so far"
	do_tts(partial_text)

	screen_fill(black)
	draw_target('congruent','left','left')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "but other times there will be a whole school of fish like this."
	do_tts(partial_text)

	text = "When you see a school of fish, your job is to press the button corresponding to the direction of the center fish and ignore the buddy fish on either side."
	screen_fill(black)
	draw_target('congruent','left','left')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	do_tts(text)

	text = "Sometimes the buddy fish will be pointing in the same direction as the center fish, as you see here, and sometimes the buddy fish will be pointing in the opposite direction as the center fish."
	screen_fill(black)
	draw_target('congruent','left','left')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "Sometimes the buddy fish will be pointing in the same direction as the center fish, as you see here"
	do_tts(partial_text)

	screen_fill(black)
	draw_target('incongruent','right','left')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "and sometimes the buddy fish will be pointing in the opposite direction as the center fish."
	do_tts(partial_text)


def do_generic_pre_practice_instructions():
	text = "The first few minutes of this part of the experiment will be a practice period designed to help you get a feel for how this part of the experiment works. At the end of practice, the computer will give you a break, after which the experiment proper will begin. This part of the experiment should take about ten to fifteen minutes, and the computer will give you opportunities to take breaks every few minutes. At the end of this part of the experiment, you will be given instructions for the next part of the experiment."
	do_auto_tts(text)

	text = "Please check that you are sitting the appropriate distance from the screen and when you are ready to begin practice, press any button."
	screen_fill(black)
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	do_tts(text)
	wait_for_response()


#define a function that demos the target stimuli during instructions
def do_n_demo():

	text = "During this part of the experiment, you will see an arrow at the center of the screen that will help you guess where the next fish is going to appear."
	screen_fill(black)
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "During this part of the experiment"
	do_tts(partial_text)

	screen_fill(black)
	draw_arrow('left')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "you will see an arrow at the center of the screen that will help you guess where the next fish is going to appear."
	do_tts(partial_text)

	text = "Most of the time the fish will appear where the arrow is pointing, but sometimes the fish will appear opposite to where the arrow is pointing. However, even though the arrow will be wrong sometimes, it will be right most of the time so it makes sense to always pay attention to the side to which the arrow is pointing. To help you anticipate when the fish is going to appear, the computer will play a sound through the headphones and whenever you hear this sound, the fish will appear one second later. The headphones will actually play a constant fuzz throughout this part of the experiment, and it's this fuzz sound that will change slightly to let you know that the fish is going to appear soon. To give you an example of what this sounds like, in a moment the computer will play the fuzz for two seconds, then the fuzz will change briefly then one second will pass after which the fish will appear."
	do_auto_tts(text)
	trial_start_time = time.perf_counter()
	warning_on_time = trial_start_time + 1
	warning_off_time = warning_on_time + warning_duration
	target_on_time = warning_on_time + endo_warning_target_SOA

	wait(2)
	start_sounds()
	wait(until=warning_on_time)
	warning_sound.set_volume(warning_lo_volume)
	background_sound.set_volume(0)
	wait(until=warning_off_time)
	background_sound.set_volume(warning_lo_volume)
	warning_sound.set_volume(0)
	wait(until=target_on_time)
	screen_fill(black)
	draw_target('neutral','left','left')
	exp_window.refresh()
	wait(1)
	screen_fill(black)
	exp_window.refresh()

	text = "Not all fish will be preceded by the fuzz change, so sometimes you will be uncertain as to when the fish are going to appear. To let you know if the next fish is going to be preceded by a fuzz change, a shape will appear surrounding the arrow."
	do_auto_tts(text)

	text = "If the arrow is surrounded by a circle, the fuzz change will happen."
	screen_fill(black)
	draw_arrow('left')
	draw_shape('circle')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	do_tts(text)

	text = "If the arrow is surrounded by a square, the fuzz change won't happen."
	screen_fill(black)
	draw_arrow('left')
	draw_shape('square')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	do_tts(text)


#define a function that demos the target stimuli during instructions
def do_x_demo():

	text = "During this part of the experiment, a dot will flicker briefly before the fish appears, either on the left like this, or on the right like this."
	screen_fill(black)
	draw_feedback('+')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "During this part of the experiment, a dot will flicker briefly before the fish appears, either on the left like this"
	do_tts(partial_text)

	screen_fill(black)
	draw_feedback('+')
	draw_dot('left')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	wait(warning_duration)

	screen_fill(black)
	draw_feedback('+')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	partial_text = "or on the right like this."
	do_tts(partial_text)

	screen_fill(black)
	draw_feedback('+')
	draw_dot('right')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	wait(warning_duration)

	screen_fill(black)
	draw_feedback('+')
	draw_caption(text=text,style='caption')
	exp_window.refresh()
	wait(1)

	text = "The location of this flicker is completely random and doesn't have anything to do with where the fish is going to appear. Throughout this part of the experiment, the headphones will play a fuzz sound. This fuzz sound will change slightly before the fish appears. To give you an example of what this fuzz change sounds like, in a moment the computer will play the fuzz for two seconds, then the fuzz will change briefly, after which a fish will appear."
	do_auto_tts(text)

	wait(2)
	# warning_sound.set_volume(warning_hi_volume)
	wait(2)
	# warning_sound.play(0)
	wait(exo_warning_target_SOA)
	screen_fill(black)
	draw_target('neutral','left','left')
	exp_window.refresh()
	wait(1)
	screen_fill(black)
	exp_window.refresh()

	text = "Sometimes the fuzz change will be quiet like you just heard, but other times the fuzz change will be louder. The fish will always appear immediately after the fuzz change."
	do_auto_tts(text)


########
# Start the experiment
########

#get subject info
sid = get_input('SID ("test" to demo):')
first_task = get_input('First task (\'n\' or \'x\'):')
if sid != 'test':
	sex = get_input('Sex (m or f):')
	age = get_input('Age (2-digit number):')
	handedness = get_input('Handedness (r or l):')
else:
	sex = 'test'
	age = 'test'
	handedness = 'test'


inputs = {
	'sid':sid,
	'first_task':first_task,
	'sex':sex,
	'age':age,
	'handedness':handedness,
}

{
	'fixation_interval':{'col':1},
	'warning_intensity':{'col':2,'mapping':{}},
	'':{'col':3,'mapping':{}},
	'':{'col':4,'mapping':{}},
	'':{'col':5,'mapping':{}},


	'block':{'col':1,'mapping':{ value['exercise']:key for key,value in block_dict.items()}},
	'set':{'col':2},
	'time':{'col':3},
	'side':{'col':5,'mapping':{}},
}

#encode & send header to writer
header = json.dumps({'inputs':inputs,'event_cols':event_cols})
tx_dict['writer'].put(kind='attr',payload={'name':'header','value':header})

if first_task=='n':
	task_order = ['n','x']
else:
	task_order = ['x','n']


#show some demo screens
# show_message('Press any button to begin general instrunctions.')
# do_general_demo()
# show_message('Press any button to begin instructions specific to first part of the experiment.')



block = 0
for repetition in range(2):
	for task in task_order:
		# if task=='n':
		# 	do_n_demo()
		# else:
		# 	do_x_demo()
		# do_generic_pre_practice_instructions()
		show_message('Press any button to begin.')
		run_block('practice',0)
		message_viewing_time = show_message('Practice is complete.\nPress any button to begin the experiment.')
		for i in range(number_of_blocks_per_task):
			block = block + 1
			run_block(block,message_viewing_time)
			if i<(number_of_blocks_per_task-1):
				# message_viewing_time = show_message('Take a break!\nYou\'re about '+str(block)+'/'+str(number_of_blocks_per_task*4)+' done.\nWhen you are ready, press any button to continue the experiment.')
				message_viewing_time = show_message('Take a break!\nPlease use the string now to check that you are still sitting the appropriate distance from the screen.\nWhen you are ready, press any button to continue the experiment.')
			elif block<(number_of_blocks_per_task*4):
				show_message('You\'re all done the this part of this experiment. Press any button to begin instructions for the next part of the experiment.')
			else:
				show_message('You\'re all done!\nPlease alert the person conducting this experiment that you have finished.')

exit_safely()
