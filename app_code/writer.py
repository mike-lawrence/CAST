########
# Initialize debugger & check for expected variables
########
from file_forker import debug_class
debug = debug_class('writer')
debug.print('I am running')
debug.check_vars(['rx_dict', 'tx_dict'])

import sys
if sys.platform=='darwin':
	import appnope
	appnope.nope()

import os
import shutil
import sys
import time
import h5py

#get current time for data file name
if not os.path.exists('../data'):
	os.mkdir('../data')
writer_start_time_string = time.strftime('%Y_%m_%d_%H_%M_%S')

default_folder = '../data/_' + writer_start_time_string
if not os.path.exists(default_folder):
	os.mkdir(default_folder)

default_filebase = default_folder + '/_' + writer_start_time_string

new_file_prefix = None # might be updated by experiment
any_data_written = False
#debug.print('file ready')

dset_dict = {}
quit_when_queue_empty = False
file_sent = False
while len(rx_dict)>0:
	time.sleep(.01)
	#iterate over sources and deal with any new data
	for source,rxq in list(rx_dict.items()): #list() required for later pop
		if not rxq.empty():
			if quit_when_queue_empty:
				debug.print('still digesting items in queue from'+source)
			msg = rxq.get()
			if (msg.kind=='quit') & (source=='parent'):
				quit_when_queue_empty = True
				rx_dict.pop('parent')
				debug.print('quitting when queues are empty.')
			elif msg.kind=='new_file_prefix':
				new_file_prefix = msg.payload
			elif msg.kind=='attr':
				#we store the attributes in dset_dict until we have data, at which point they're written
				if(source not in dset_dict.keys()):
					dset_dict[source] = {'source':source}
				if('attr_dict' not in dset_dict[source].keys()):
					dset_dict[source]['attr_dict'] = {}
				dset_dict[source]['attr_dict'][msg.payload['name']] = msg.payload['value']
			elif msg.kind=='data':
				# msg.payload = np.append(msg.payload,msg.queue_time)
				# msg.payload = msg.payload.reshape(1,len(msg.payload))
				if len(msg.payload.shape)==1:
					msg.payload = msg.payload.reshape((1,msg.payload.shape[0]))
				if source not in dset_dict.keys() :
					dset_dict[source] = {'source':source}
				if 'handle' not in dset_dict[source].keys() :
					dset_dict[source]['file'] = default_filebase + '_' + source + '.hdf5'
					dset_dict[source]['handle'] = h5py.File( dset_dict[source]['file'] , 'w' , libver='latest' )
					dset_dict[source]['dset'] = dset_dict[source]['handle'].create_dataset(
						source
						, chunks = (msg.payload.shape[0],msg.payload.shape[1])
						, maxshape = (None,msg.payload.shape[1])
						, data = msg.payload
						# , shuffle = True
						# , fletcher32 = True
						# , compression = 'lzf'
					)
					#write attrs
					if 'attr_dict' in dset_dict[source].keys() :
						for attr_name,attr_value in dset_dict[source]['attr_dict'].items() :
							dset_dict[source]['dset'].attrs[attr_name] = attr_value
					any_data_written = True
					dset_dict[source]['handle'].swmr_mode = True
					for tx in tx_dict.values():
						tx.put(kind='file',payload={'source':source,'path':dset_dict[source]['file']})
				else: #this else occurs if we've already initialized the dset
					count_new_rows = msg.payload.shape[0]
					new_shape = (
						  dset_dict[source]['dset'].shape[0] + count_new_rows
						, dset_dict[source]['dset'].shape[1]
					)
					dset_dict[source]['dset'].resize( new_shape )
					dset_dict[source]['dset'][-count_new_rows:,] = msg.payload
					dset_dict[source]['dset'].flush()
			else:
				debug.print(f'Unrecognized message kind: {msg.kind}')
				# pass
		#queue is empty:
		elif quit_when_queue_empty:
			rx_dict.pop(source)
			if source in dset_dict.keys():
				if 'handle' in dset_dict[source].keys():
					dset_dict[source]['handle'].close()


if not any_data_written:
	shutil.rmtree(default_folder)
elif new_file_prefix is not None:
	new_file_base = new_file_prefix + '_' + writer_start_time_string
	new_folder = '../data/' + new_file_base
	os.mkdir(new_folder)
	for dset in dset_dict.values():
		old_file = dset['file']
		new_file = new_folder + '/' + new_file_base + '_' + dset['source'] + '.hdf5'
		os.rename( old_file , new_file )
	shutil.rmtree(default_folder)
debug.print('quitting')
sys.exit()
