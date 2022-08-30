import time
from scipy.io import savemat


class Recorder():
	def __init__(self):
		self.on = False
		self.data = []

	def store(self, datum):
		self.data.append(datum)


	def start(self, param):
		if self.on:
			raise Exception("Recorder already on")

		self.on = True
		time.sleep(param["duration"])
		self.end(param)
		return

	def end(self, param):
		self.on = False
		self.save(param)
		return

	def save(self, param):
		param["data"] = self.data
		print(param)
		timestr = time.strftime("%Y%m%d-%H%M%S")
		filename = "MiRES_{}".format(timestr)
		filename += "_az_{}".format(param["theta_azim"]) if "theta_azim" in param else ""
		filename += "_el_{}".format(param["theta_elev"]) if "theta_elev" in param else ""
		filename += "_db_{}".format(param["db"]) if "db" in param else ""

		print(filename)

		savemat("{}/{}.mat".format(param["save_to"], filename), param)

		print("saved {}".format(param))

		self.data = []
		return

