# Importing Libraries
import time
import serial
from pySerialTransfer import pySerialTransfer as txfer
import numpy as np
from threading import Thread
import re

from Recorder import Recorder

MAX_RESULTS = 160


class SerialTransferCommunicator:
	def __init__(self, port="/dev/cu.usbserial-210", baudrate=115200, timeout=1, recorder=Recorder()):
		self.link = txfer.SerialTransfer(port, baudrate, timeout = timeout)
		self.recorder = recorder

		self.demod = 0
		self.t_start = 0
		self.t_end = 0
		# self.Vdec = [0 for _ in range(160)]
		# self.Vspst = [0 for _ in range(160)]


	# def update(self, idx, dec, spst):
	# 	print("update {} {} {}".format(idx, dec, spst))
	# 	self.Vdec[idx] = dec
	# 	self.Vspst[idx] = spst

	def read(self):
		# while True:
		# 	time.sleep(0.1)
		# 	yield self.Vspst, self.Vdec
		# return self.Vspst, self.Vdec
		return self.demod
		
		
	def start(self):
		self.link.close()
		self.link.open()
		print("START SERIAL COMMUNICATION")
		reconnect_cnt = 0

		time.sleep(2)


		while self.link.connection.is_open:
			time.sleep(0.001)

			if self.link.available():
				self.demod = self.link.rx_obj(obj_type='h')

				# dec = self.link.rx_obj(obj_type='h',
				# 						obj_byte_size=2,
				# 						start_pos=2)

				# spst = self.link.rx_obj(obj_type='h',
				# 						start_pos=4,
				# 						obj_byte_size=2)

				print(self.demod)

				# execution time =====
				self.t_end = time.time()
				print("{}".format((self.t_end - self.t_start)*1000))
				self.t_start = self.t_end

				if self.recorder.on:
					self.recorder.store(self.demod)

				reconnect_cnt = 0


				continue
				
				# self.update(i, dec, spst)
				# print('{} {} {} {}'.format(self.link.status, i, dec, spst))
			# 	continue


			# if self.link.available():
			# 	rx_vector = self.link.rx_obj(obj_type=list,
			# 								obj_byte_size=160,
			# 								list_format='h')

			# 	self.build(rx_vector, self.link.idByte)

			# 	print(rx_vector)

				# if self.link.idByte < len(self.callback_list):
				# 	self.callback_list[self.link.idByte](rx_vector)
				# elif self.link.debug:
				# 	print('ERROR: No callback available for packet ID {}'.format(self.link.idByte))
				
				# return True
        
			
			# return False

			# print(self.link.status)

			elif self.link.status < 0:
				if self.link.status == txfer.CRC_ERROR:
					print('ERROR: CRC_ERROR')
				elif self.link.status == txfer.PAYLOAD_ERROR:
					print('ERROR: PAYLOAD_ERROR')
				elif self.link.status == txfer.STOP_BYTE_ERROR:
					print('ERROR: STOP_BYTE_ERROR')
				else:
					print('ERROR: {}'.format(self.link.status))

			else:
				reconnect_cnt += 1
				# print(reconnect_cnt)
				if reconnect_cnt > 1000:
					reconnect_cnt = 0
					print("RECONNECTING...")
					self.link.close()
					self.link.open()
					time.sleep(1)

				

			
			# if reconnect_cnt > 1000:
			# 	reconnect_cnt = 0
			# 	i = 0
			# 	print("RECONNECTING...")
			# 	# self.link.close()
			# 	# self.link.open()
			# 	time.sleep(2)




			# print(self.link.status)
	def stop(self):
		print("CLOSEE")
		self.link.close()



# sc = SerialCommunicator()
# # sc.start()
# serialTransferThread = Thread(target=sc.start)
# serialTransferThread.start()

# while True:
# 	Vspst, Vdec = sc.read()
# 	print("Vdec: {}".format(Vdec))
# 	print("Vspst: {}".format(Vspst))
# 	time.sleep(0.1)
