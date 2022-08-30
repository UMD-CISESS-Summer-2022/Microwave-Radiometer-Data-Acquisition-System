import enum
from time import time, sleep
import math
import numpy as np
import threading
from scipy import signal
from SignalType import SignalType

class SignalGenerator:
	def __init__(self, signalType = SignalType['zero'], f = 1, t = 0, fs = 1000):
		self.signalType = signalType
		self.f = f
		self.fs = fs
		self.t = t
		self.val = 0

	def start(self):
		print("start signal")

		startTime = time()

		while True:
			self.t = time() - startTime
			self.val = self.signalType(self.f, self.t)
			sleep(1/self.fs)
			# yield self.val

	def sample(self):
		return self.t, self.val




# def main():
# 	a = SignalGenerator(SignalType['sine'])
# 	global sample

# 	def sample():
# 		sleep(2)
# 		while True:
# 			# print(a.sample())
# 			print(a.t, a.val)
# 			sleep(0.1)

# 	p1 = threading.Thread(target=a.start)
# 	# p2 = threading.Thread(target=sample)

# 	if __name__ == "__main__":
# 		p1.start()
# 		sample()
# 		# p2.start()



# main()