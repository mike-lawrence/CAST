import sys
import time
import inspect
import multiprocessing
import multiprocessing.queues


########
# Define a class that facilitates multi-child print messages
########
class debug_class():
	def __init__(self,process_name):
		self.print_num = 0
		self.process_name = process_name
	def print(self,message,critical=False):
		if critical:
			prefix = '!!'
		else:
			prefix = '  '
		print(prefix+'{'+self.process_name+'}'+'['+str(self.print_num)+'] '+message)
		self.print_num += 1
	def check_vars(self,vars_expected):
		for var in vars_expected:
			if not (var in inspect.currentframe().f_back.f_locals):
				self.print('missing '+var,critical=True)

########
# Define a class for structured messages
########
class message_class:
	def __init__(self,kind,payload):
		self.kind = kind
		self.payload = payload
		self.put_time = time.perf_counter()
		self.get_time = None
	def compute_queue_time(self):
		self.get_time = time.perf_counter()
		self.queue_time = self.get_time - self.put_time

########
# Subclass multiprocessing.queue.Queue to add some useful features
########

class q_class():
	def __init__(self,name,tx,rx,ctx):
		self.name = name
		self.tx = tx
		self.rx = rx
		self.ctx = ctx
		self.report_bottlenecks = True
		self.bottleneck_time = 1.0 #in seconds
		self.debug = debug_class(self.name)
		self.q = ctx.Queue()
		return None
	def empty(self):
		return self.q.empty()
	def put(self,kind,payload=None):
		message = message_class(kind,payload)
		self.q.put(message)
		return None
	def get(self):
		message = self.q.get(block=False)
		message.compute_queue_time()
		if self.report_bottlenecks:
			if message.queue_time>self.bottleneck_time:
				self.debug.print('Queue bottleneck: '+str(int(1000*message.queue_time))+'ms')
		return(message)

########
# Define a class that spawns a new process
########
class child_class:
	def __init__(self,ctx,file,name,debug):
		self.ctx = ctx
		self.file = file
		self.name = name
		self.debug = debug
		self.debug.process_name = self.name + ' (in main)'
		self.rx_dict = {}
		self.rx_dict['parent'] = q_class(name='parent_to_'+self.name,tx='parent',rx=self.name,ctx=self.ctx)
		self.tx_dict = {}
		self.tx_dict['parent'] = q_class(name=self.name+'_to_parent',tx=self.name,rx='parent',ctx=self.ctx)
		self.init_dict = {}
		self.started = False
	def f(self,file,init_dict):
		globals().update(init_dict)
		exec(open(file).read(),globals(),globals())
		import sys
		sys.exit()
	def start(self):
		self.init_dict['rx_dict'] = self.rx_dict
		self.init_dict['tx_dict'] = self.tx_dict
		if self.started:
			self.debug.print('Oops! Already started this child.')
		else:
			self.process = self.ctx.Process( target=self.f , args=(self.file,self.init_dict,) )
			self.process.start()
			self.started = True
	def is_alive(self):
		return self.process.is_alive()
	def stop(self):
		if not self.started:
			self.debug.print('Oops! Not started yet!')
		else:
			self.rx_dict['parent'].put(kind='quit')
		return None

class family_class:
	def __init__(self):
		self.ctx = multiprocessing.get_context('spawn')
		self.q_dict = {}
		self.child_dict = {}
		self.debug = debug_class('main')
	def child(self,file,name=None):
		if name is None:
			name = file.replace('.py','')
		self.child_dict[name] = child_class(ctx=self.ctx,file=file,name=name,debug=self.debug)
	def q_connect(self,tx_name_list=None,rx_name_list=None):
		if(tx_name_list is None):
			tx_name_list = [key for key in self.child_dict.keys()]
		if(rx_name_list is None):
			rx_name_list = [key for key in self.child_dict.keys()]
		for tx_name in tx_name_list :
			for rx_name in rx_name_list :
				if tx_name!=rx_name:
					q_name = tx_name+'_to_'+rx_name
					self.q_dict[q_name] = q_class(name=q_name,tx=tx_name,rx=rx_name,ctx=self.ctx)
					self.child_dict[tx_name].tx_dict[rx_name] = self.q_dict[q_name]
					self.child_dict[rx_name].rx_dict[tx_name] = self.q_dict[q_name]
	def start(self):
		for child in self.child_dict.values():
			child.start()
	def stop(self):
		for child in self.child_dict.values():
			child.stop()
	def monitor_for_quit(self):
		done = False
		while not done:
			time.sleep(.1)
			for child in self.child_dict.values():
				if not child.tx_dict['parent'].empty() :
					if child.tx_dict['parent'].get().kind=='quit':
						done = True #breaks out of the while loop
						break #breaking out of the for loop over children
	def monitor_for_all_stopped(self):
		while len(self.child_dict)!=0:
			time.sleep(.1)
			for child in list(self.child_dict.values()): #list() required for later pop
				if not child.process.is_alive():
					self.child_dict.pop(child.name)
				else:
					child.debug.print('Still running.')
		debug.print('All stopped.')
	def start_and_monitor(self):
		self.start()
		self.monitor_for_quit()
		self.stop()
