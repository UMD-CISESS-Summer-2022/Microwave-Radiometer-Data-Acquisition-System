import os
import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.filedialog as fd

from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from pyparsing import col

from scipy import signal
import scipy.io
import scipy.interpolate
import numpy as np
import math


from SerialCommunication import SerialCommunicator
from SerialTransferCommunication import SerialTransferCommunicator
from Recorder import Recorder

from threading import Thread

from serial_ports import serial_ports
from gaussfitter import gaussian, fitgaussian, moments


from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")


XLIM = 800


# add record button
def recordOnClick():
	param = {}
	try:

		if azimuth_angle.get():
			param["theta_azim"] = float(azimuth_angle.get())
		if elevation_angle.get():
			param["theta_elev"] = float(elevation_angle.get())
		if integration_time.get():
			param["integ_time"] = float(integration_time.get())
		param["duration"] = float(record_duration_s.get())
		if db.get():
			param["db"] = float(db.get())
		param["save_to"] = folder_button.cget("text")

	except:
		raise Exception("parameter Error")
	
	recordThread = Thread(target=lambda : stRecorder.start(param))
	recordThread.start()


# make connection on click
connected = False 
def connectOnClick():
	global connected
	global stc

	connected = True
	try:
		stc.stop()
		print("THREAD:", stc.is_alive())
	except:
		pass

	stc = SerialCommunicator(port=portName.get(), recorder=stRecorder)

	serialTransferThread = Thread(target=stc.start)
	serialTransferThread.start()

def folderOnClick():
	cwd = os.getcwd()
	dir = fd.askdirectory(initialdir=cwd) + "/"
	folder_button.configure(text=dir.replace(cwd,"."))
	



# fetching data from serical communicator
def animation_data():
	x = [i for i in range(XLIM)]
	y = [0 for _ in range(XLIM)]
	while True:
		if connected:
			try:
				demod = stc.read()
			except:
				demod = 0
			record_button.configure(fg="red" if stRecorder.on else "green")
			data_frequency.configure(text=str(stc.freq if stc else 0))
			input.configure(text=str(demod))
			y = y[1:] + [demod]
		yield x, y

# ploting 
def animation_frame(data):
	x, y = data[0], data[1]

	line.set_data(x, y)
	return line,



# plot selected recorded data
def print_plot2(data):
	plot2.clear()
	plot2.plot(data)
	canvas.draw_idle()

def open_file():
	file = fd.askopenfilenames(parent=root, title='Choose a File')
	mat = scipy.io.loadmat(file[0])
	print_plot2(mat["data"][0])



# plotting 2d map
def print_2d(data):
	x = data[:,0]
	y = data[:,1]
	a = -data[:,2]
	
	xi, yi = np.mgrid[x.min():x.max():500j, y.min():y.max():500j]
	grid_x, grid_y = np.mgrid[x.min():x.max():200j, y.min():y.max():200j]
	

	griddata = scipy.interpolate.griddata(np.array([x,y]).T, a, (grid_x, grid_y), method='linear')
	params = fitgaussian(griddata)
	fit = gaussian(*params)
	print(params)


	plot3.clear()
	plot3.scatter(data[:,0], data[:,1], a)

	plot4.clear()
	plot3.clear()
	plot3.imshow(griddata.T, cmap="jet", extent=[x.min(), x.max(), y.min(), y.max()])
	plot4.imshow(fit(*np.indices(griddata.shape)), cmap="jet", extent=[x.min(), x.max(), y.min(), y.max()])
	canvas2.draw_idle()
	

def print_calibration(data):
	plot3.clear()

	x = data[:,0]
	y = data[:,1]

	power = np.power(10, x / 10)

	plot3.scatter(x,y)
	plot4.scatter(power, y)

	canvas2.draw_idle()

def open_file_2():
	files = fd.askopenfilenames(parent=root, title='Choose a File')
	lst = []

	for file in files:
		mat = scipy.io.loadmat(file)
		
		az = float(mat["theta_azim"])
		el = float(mat["theta_elev"])

		# db = float(mat["db"])
		mean = np.round(np.mean(mat["data"][0]), 2)
		lst.append([az, el, mean])
		# lst.append([db, mean])

	print_2d(np.array(lst))
	# print_calibration(np.array(lst))




fig = plt.Figure(dpi=90)
plot1 = fig.add_subplot(211, xlim=(0,XLIM), ylim=(-50, 50))
plot2 = fig.add_subplot(212)
line, = plot1.plot([], [])


stRecorder = Recorder()
stc = None




# GUI #####################################
root = Tk()
root.title("CISESS Microwave Detector Interface")
root.geometry("960x540")

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Tab 1')
tabControl.add(tab2, text ='Tab 2')
tabControl.pack(expand = 1, fill ="both")

# conntection frame ########################
connectionFrame = LabelFrame(tab1, text="Connection", width=400, height=400)
connectionFrame.grid(row=0,column=0)

port_label = Label(connectionFrame, text="Port: ", font=("Helvatical", 20))
port_label.grid(row=0, column=0)
data_frequency_label = Label(connectionFrame, text="Frequency: ", font=("Helvatical", 20))
data_frequency_label.grid(row=1, column=0)
input_label = Label(connectionFrame, text="input: ", font=("Helvatical", 20))
input_label.grid(row=2, column=0)

portName = StringVar()

try:
	port = OptionMenu(connectionFrame, portName, *serial_ports())
	port.grid(row=0, column=1)
except:
	pass
data_frequency = Label(connectionFrame, text="0")
data_frequency.grid(row=1, column=1)
input = Label(connectionFrame, text="input")
input.grid(row=2, column=1)

connect_button = Button(connectionFrame, text="connect", command=connectOnClick)
connect_button.grid(row=3, column=0, columnspan=2)


# parameter frame ##########################
parameterFrame = LabelFrame(tab1, text="Parameters", width=400, height=400)
parameterFrame.grid(row=1, column=0)

azimuth_label = Label(parameterFrame, text="Azimuth angle", font=("Helvatical", 20))
azimuth_label.grid(row=0, column=0)
elevation_label = Label(parameterFrame, text="Elevation angle", font=("Helvatical", 20))
elevation_label.grid(row=1, column=0)
tau_label = Label(parameterFrame, text="Integration Time", font=("Helvatical", 20))
tau_label.grid(row=2, column=0)
duration_label = Label(parameterFrame, text="Record Duration (s)", font=("Helvatical", 20))
duration_label.grid(row=3, column=0)
save_to_label = Label(parameterFrame, text="Save to:", font=("Helvatical", 20))
save_to_label.grid(row=5, column=0)
db_label = Label(parameterFrame, text="db:", font=("Helvatical", 20))
db_label.grid(row=4, column=0)

azimuth_angle = Entry(parameterFrame, width=5)
azimuth_angle.grid(row=0, column=1)
elevation_angle = Entry(parameterFrame, width=5)
elevation_angle.grid(row=1, column=1)
integration_time = Entry(parameterFrame, width=5)
integration_time.grid(row=2, column=1)
record_duration_s = Entry(parameterFrame, width=5)
record_duration_s.grid(row=3, column=1)
db = Entry(parameterFrame, width=5)
record_duration_s.insert(0, 5)
db.grid(row=4, column=1)


folder_button = Button(parameterFrame, text="./", command=folderOnClick)
folder_button.grid(row=5,column=1)

record_button = Button(parameterFrame, text="Record", command=recordOnClick)
record_button.grid(row=6, column=0, columnspan=2)

# Graphing ####################################
canvas = FigureCanvasTkAgg(fig, master = tab1)
# canvas.draw_idle()
canvas.get_tk_widget().grid(row=0, column=1, rowspan=2)

ani	= animation.FuncAnimation(fig, animation_frame, animation_data, blit=True, interval = 1) # milliseconds
canvas.draw_idle()


file_button = Button(tab1, text="Select a File", command=open_file)
file_button.grid(row=2,column=0, columnspan=2)



# 2D graphing #################################
fig2 = plt.Figure(figsize=(16,6), dpi=60)
plot3 = fig2.add_subplot(121)
plot4 = fig2.add_subplot(122)
canvas2 = FigureCanvasTkAgg(fig2, master = tab2)
canvas2.get_tk_widget().grid(row=0, column=0)

file_button = Button(tab2, text="Select a File", command=open_file_2)
file_button.grid(row=1,column=0)




def on_closing():
	if messagebox.askokcancel("Quit", "Do you want to quit?"):
		try:
			stc.stop()
		except:
			pass
		root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()




'''
Graph:
	- matplotlib

Settings:
	- x range (time)
	- y range (amplitude)
	- frequency
	- signal simulator (real time)
		- sine wave
		- square wave
		- random wave
	
		
'''