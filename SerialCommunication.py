# Importing Libraries
import time
import serial
from pySerialTransfer import pySerialTransfer as txfer
import numpy as np
from threading import Thread
import re

from Recorder import Recorder

MAX_RESULTS = 160

class SerialCommunicator:
	def __init__(self, port="/dev/cu.usbserial-210", baudrate=115200, timeout=1, recorder=Recorder()):
		# self.arduino = None

		self.port = port
		self.baudrate = baudrate
		self.recorder = recorder

		self.arduino = serial.Serial(self.port, self.baudrate)
		# self.Vspst = [0 for _ in range(MAX_RESULTS)]
		# self.Vdec = [0 for _ in range(MAX_RESULTS)]
		self.demod = 0
		self.freq = 0
		self.t_start = 0
		self.t_end = 0

	# def read():

	def start(self):
		# time.sleep(2)

		print("START SERIAL COMMUNICATION")
		while self.arduino.is_open:
			time.sleep(0.001)
			newline = self.arduino.readline()
			# print(newline)

			self.demod = int(newline)


			# print(self.demod)

			# execution time =====
			self.t_end = time.time()
			# print("{}".format((self.t_end - self.t_start)*1000))
			self.freq = round(1/(self.t_end - self.t_start), 3)
			self.t_start = self.t_end

			if self.recorder.on:
				# self.recorder.store((time.time(), self.demod))
				self.recorder.store(self.demod)


			# try:
			# 	match = re.search(r'(\d+)\s*(-?\d+(\.\d+)?)\s*(\d+(\.\d+)?)?', newline.decode("utf-8"))
			# 	# i, spst, dec = [s for s in newline.split()]
			# 	i = int(match.group(1))

			# 	if i == MAX_RESULTS:
			# 		self.demod = float(match.group(2))
			# 	else:
			# 		self.Vspst[i] = int(match.group(2))
			# 		self.Vdec[i] = int(match.group(4))
					
			# 	print("Update {} {} {}".format(i, match.group(2), match.group(4)))

			# except:
			# 	print("PARSE ERROR:", newline)
			# 	continue
			# print(self.arduino.is_open)


	def stop(self):
		self.arduino.close()
		


	def read(self):
		return self.demod

	# def getFreq(self):
	# 	return round(1/(self.t_end - self.t_start), 3)

# sc = SerialCommunicator(port="/dev/cu.usbserial-110")
# serialTransferThread = Thread(target=sc.start)
# serialTransferThread.start()

# while True:
# 	demod = sc.read()
# 	# print(demod)
# 	time.sleep(0.1)
			



# class SerialCommunicator:
# 	def __init__(self, port="/dev/cu.usbserial-210", baudrate=115200, timeout=1):
# 		self.link = txfer.SerialTransfer(port, baudrate, timeout = timeout)
# 		self.Vdec = [0 for _ in range(160)]
# 		self.Vspst = [0 for _ in range(160)]

# 	# def build(self, rx_vector, packet_id):
# 	# 	if packet_id == 0:
# 	# 		self.Vdec = rx_vector + self.Vdec[80:]
# 	# 	elif packet_id == 1:
# 	# 		self.Vspst = rx_vector + self.Vspst[80:]
# 	# 	elif packet_id == 2:
# 	# 		self.Vdec = self.Vdec[:80] + rx_vector
# 	# 	elif packet_id == 3:
# 	# 		self.Vspst = self.Vspst[:80] + rx_vector
# 	# 	else:
# 	# 		print('ERROR: No callback available for packet ID {}'.format(self.link.idByte))


# 	def update(self, idx, dec, spst):
# 		print("update {} {} {}".format(idx, dec, spst))
# 		self.Vdec[idx] = dec
# 		self.Vspst[idx] = spst

# 	def read(self):
# 		# while True:
# 		# 	time.sleep(0.1)
# 		# 	yield self.Vspst, self.Vdec
# 		return self.Vspst, self.Vdec
		
		
# 	def start(self):
# 		self.link.close()
# 		self.link.open()
# 		time.sleep(2)

# 		while True:
# 			if self.link.available():
# 				i = self.link.rx_obj(obj_type='h',
# 													obj_byte_size=2)

# 				dec = self.link.rx_obj(obj_type='h',
# 													obj_byte_size=2,
# 													start_pos=2)

# 				spst = self.link.rx_obj(obj_type='h',
# 													start_pos=4,
# 													obj_byte_size=2)
				
# 				self.update(i, dec, spst)
# 				# print('{} {} {} {}'.format(self.link.status, i, dec, spst))
# 			# 	continue


# 			# if self.link.available():
# 			# 	rx_vector = self.link.rx_obj(obj_type=list,
# 			# 														obj_byte_size=160,
# 			# 														list_format='h')

# 			# 	self.build(rx_vector, self.link.idByte)

# 			# 	print(rx_vector)

# 				# if self.link.idByte < len(self.callback_list):
# 				# 	self.callback_list[self.link.idByte](rx_vector)
# 				# elif self.link.debug:
# 				# 	print('ERROR: No callback available for packet ID {}'.format(self.link.idByte))
				
# 				# return True
        
# 			# elif self.link.debug and not self.link.status:
# 			# 	if self.link.status == txfer.CRC_ERROR:
# 			# 		err_str = 'CRC_ERROR'
# 			# 	elif self.link.status == txfer.PAYLOAD_ERROR:
# 			# 		err_str = 'PAYLOAD_ERROR'
# 			# 	elif self.link.status == txfer.STOP_BYTE_ERROR:
# 			# 		err_str = 'STOP_BYTE_ERROR'
# 			# 	else:
# 			# 		err_str = str(self.link.status)
						
# 			# 	print('ERROR: {}'.format(err_str))
			
# 			# return False

# 			# print(self.link.status)

# 			elif self.link.status < 0:
# 				if self.link.status == txfer.CRC_ERROR:
# 					print('ERROR: CRC_ERROR')
# 				elif self.link.status == txfer.PAYLOAD_ERROR:
# 					print('ERROR: PAYLOAD_ERROR')
# 				elif self.link.status == txfer.STOP_BYTE_ERROR:
# 					print('ERROR: STOP_BYTE_ERROR')
# 				else:
# 					print('ERROR: {}'.format(self.link.status))

# 			# print(self.link.status)
# 			time.sleep(0.001)


# sc = SerialCommunicator()
# # sc.start()
# serialTransferThread = Thread(target=sc.start)
# serialTransferThread.start()

# while True:
# 	Vspst, Vdec = sc.read()
# 	print("Vdec: {}".format(Vdec))
# 	print("Vspst: {}".format(Vspst))
# 	time.sleep(0.1)
