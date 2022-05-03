#when using file_forker, it's necessary to put all the code inside a 'if __name__ == '__main__':' check
if __name__ == '__main__':

	import sys
	from file_forker import debug_class, family_class #for easy multiprocessing
	import appnope
	appnope.nope()

	debug = debug_class('main')

	########
	#set up family
	########

	fam = family_class()
	fam.child(file='exp.py')
	fam.child(file='gamepad.py')
	fam.child(file='cpu.py')
	fam.child(file='writer.py') #writer must be last so it is the last to receive the quit command (might not be true anymore actually)

	fam.q_connect(tx_name_list=['gamepad'],rx_name_list=['exp'])
	fam.q_connect(tx_name_list=['exp'],rx_name_list=['writer'])
	fam.q_connect(tx_name_list=['cpu'],rx_name_list=['writer'])

	fam.start_and_monitor() #loops until all children self-terminate
	sys.exit()