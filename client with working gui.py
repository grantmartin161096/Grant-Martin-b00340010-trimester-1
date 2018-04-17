# https://www.youtube.com/watch?v=gjU3Lx8XMS8
# https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter

import socket
import json
#The import JSON line of code will allow the client to receive and work with files sent to the client in this format.
from network_configuration import HOST, PORT
#The above line of code imports the localhost and port numbers (HOST, PORT = "127.0.0.1", 9997)
# into the client programme and the same import is present in the server code,
# so the client and server programmes can communicate with each other.
import tkinter
#Tkinter: Is a project interrupter
# that when uploaded into your Python programme will allow you to construct a graphical user interface
from tkinter import *
from functools import partial
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#matplotlib allows programmers to display information using 2 dimensional visual representation, like graphs
import time
#import time simply imports time in the graph being plotted on the GUI

def enum(**named_values):
    return type('Enum', (), named_values)
Buttons = enum(TEMP='temp', LOAD='load', POWER= 'power', CLOCK= 'clock')
#Enumerated type: Is a statement set-up for acceptances and is written in readable English,
# this detects change of state in the client GUI in this project.
# For example, if the user clicks ‘temperature’ on the GUI, the graph starts to plot,
# if the next button pressed is not temperature then the graph will reset.
class ClientGUI(tkinter.Frame):
#The class ‘ClientGUI ( )’  contains the functionality of the Graphical User Interface (GUI)
# and the ‘GET’ functions for receiving the temperature, load, clock and power values.
# This class is set-up as a parent – child relationship with the GUI as the parent and the ‘GET’ requests as the child.
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.starttime = (time.time())
        self.CreateWidgets()
#The above lines of code apply the measurement of time to the GUI which will be buit in the 'CreateWidgets' function

    def CreateWidgets(self):

        # dropdown menu bar
        menuBar = Menu(master=root)
        master=root.config(menu=menuBar)

        # creates left frame for labels and buttons
        leftFrame = Frame(master=root, width=50, height=50)
        leftFrame.grid(row=0, column=0, padx=10, pady=2)

        # creates right frame for graph
        rightFrame = Frame(master=root, width=50, height=50)
        rightFrame.grid(row=0, column=1, padx=10, pady=2)

        # 'File' menu
        fileMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=root.destroy)

        # buttons and commands
        # temperature button, which triggers 'GetTemp' when selected on the GUI
        self.temp_button = tkinter.Button(leftFrame, text="Temperature", width=15, command=self.GetTemp)
        self.temp_button.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        # load time button, which triggers 'GetLoad' when selected on the GUI
        self.load_button = tkinter.Button(leftFrame, text="Load Time", width=15, command=lambda: self.plot(canvas, ax))
        self.load_button.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        self.load_button = tkinter.Button(leftFrame, text="Load", width=15, command=self.GetLoad)
        self.load_button.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        # clock speed, which triggers 'GetClock' when selected on the GUI
        self.clock_button = tkinter.Button(leftFrame, text="Clock", width=15, command=self.GetClock)
        self.clock_button.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        # power button, which triggers 'GetPower' when selected on the GUI
        self.power_button = tkinter.Button(leftFrame, text="Power", width=15, command=self.GetPower)
        self.power_button.grid(row=4, column=0, padx=10, pady=5, sticky=W)
        # reset button, which resets the graph by clearing any data plotted so a new graph can be plotted by the user
        self.reset_button = tkinter.Button(master=root, text="Reset", width=15, command=lambda: self.reset())
        self.reset_button.grid(row=2, column=1, pady=20)

        # create canvas and graph in right frame
        mpl.rc('axes', edgecolor='b')
        fig=plt.figure(figsize=(8,6))
        self.ax0 = fig.add_axes([0.1,0.1,0.8,0.8], polar=False, label='axes 1')
        self.ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=False, label='axes 2')
        self.canvas = FigureCanvasTkAgg(fig, rightFrame)
        self.canvas.get_tk_widget().grid(row=0,column=1)
        self.canvas.draw()
#the above code creates the graph and the below code tells the graph what to plot and on what axis
        self.temp_c1_x = []
        self.temp_c1_y = []
        self.temp_c2_y = []
#the 3 lines above plots temperature
        self.load_c1_x = []
        self.load_c1_y = []
        self.load_c2_y = []
#the 3 lines above plots load
        self.clock_c1_x = []
        self.clock_c1_y = []
        self.clock_c2_y = []
#the 3 lines above plots clock
        self.power_c1_x = []
        self.power_c1_y = []
        self.power_c2_y = []
#the 3 lines above plots power
        self.prev_button_state = Buttons
        self.prev_button_state = Buttons.TEMP
#the above two lines of code make sure the previously pressed button matches the next button pressed

    def extract_value_message(self, message, key):
        # extract value by key from the string message
        print(message)
        data_json = json.loads(message)
        print(data_json[key])
        val = int(data_json[key])
        return val
#the above function extracts the value of the request data from the server and plots it on the graph

#The four ‘GET’ functions which follow all work the exact same,
# the only difference is they are calling different data information (temperature, load, clock and power)
#below is the 'GetTemp' function
    def GetTemp(self):
        if self.prev_button_state != Buttons.TEMP:
            self.reset()
            self.prev_button_state = Buttons.TEMP
#the above lines of code make sure the previously pressed button matches the next button pressed (temperature)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            print("connecting...")
            sock.connect((HOST, PORT))
#The first piece of code in the ‘GET’ function connects the client programme with the server programme
# using the HOST and PORT numbers imported from network_config and print ‘connecting…’ when this happens.
# request cpu temperature data from the server
            request = {"type": "request",
                       "param": "cpu_core_temp"}
            print(f"client sent: {request}")
            sock.sendall(bytes(json.dumps(request), "utf-8"))
            print("temp request sent...")
#The above line of code sends the request for the temperature in bytes to the server.
            response = str(sock.recv(1024), "utf-8")
            val1 = self.extract_value_message(response, "CPU Core #1")
            val2 = self.extract_value_message(response, "CPU Core #2")
#The above lines of code are used to receive the requested data from the server in strings.
# For each of the ‘Get’ requests ‘(socket.recv(????)’
#must be different sockets, because every socket must have a different number.
#'val1' is the value of 'CPU Core #1' and 'val2' is the value of 'CPU Core #2'

            x = time.time()
            x = x - self.starttime
            y1 = val1
            y2 = val2
#the above lines of code plot the time on the x-axis of the graph when the temperature button is pressed
#Showing the time which has past since the temperature button was pressed between the user pressing the temp button
            self.temp_c1_x.append(x)
            self.temp_c1_y.append(y1)
            self.temp_c2_y.append(y2)
#the above lines of code are retrieving the temperature value when the temperature data is requested
#The two lines of code below then plot the temperature value on the graph on the GUI

            self.plot(self.temp_c1_x, self.temp_c1_y, 0)
            self.plot(self.temp_c1_x, self.temp_c2_y, 1)

            #self.windowLog.insert(0.0, temp_response)
            #self.windowLog.insert(0.0, "\n")
#below is the 'GetLoad' function
    def GetLoad(self):
        if self.prev_button_state != Buttons.LOAD:
            self.reset()
            self.prev_button_state = Buttons.LOAD
# the above lines of code make sure the previously pressed button matches the next button pressed (load)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            #print("connecting again...")
            sock.connect((HOST, PORT))
# The first piece of code in the ‘GET’ function connects the client programme with the server programme
# using the HOST and PORT numbers imported from network_config and print ‘connecting…’ when this happens.
# request cpu load data from the server
            request = {"type": "request",
                       "param": "cpu_core_load"}
            #print(f"client sent: {request}")
            sock.sendall(bytes(json.dumps(request), "utf-8"))
            #print("load request sent...")
            # The above line of code sends the request for the temperature in bytes to the server.
            # Receive load data from the server
            response = str(sock.recv(2048), "utf-8")
            val1 = self.extract_value_message(response, "CPU Core #1")
            val2 = self.extract_value_message(response, "CPU Core #2")
# The above lines of code are used to receive the requested data from the server in strings.
# For each of the ‘Get’ requests ‘(socket.recv(????)’
# must be different sockets, because every socket must have a different number.
# 'val1' is the value of 'CPU Core #1' and 'val2' is the value of 'CPU Core #2'
            x = time.time()
            x = x - self.starttime
            y1 = val1
            y2 = val2
# the above lines of code plot the time on the x-axis of the graph when the load button is pressed
# Showing the time which has past since the load button was pressed between the user pressing the load button
            self.load_c1_x.append(x)
            self.load_c1_y.append(y1)
            self.load_c2_y.append(y2)
# the above lines of code are retrieving the load value when the load data is requested
# The two lines of code below then plot the load value on the graph on the GUI
            self.plot(self.load_c1_x, self.load_c1_y, 0)
            self.plot(self.load_c1_x, self.load_c2_y, 1)


            #self.windowLog.insert(0.0, load_response)
            #self.windowLog.insert(0.0, "\n")

#below is the 'GetClock' function
    def GetClock(self):
        if self.prev_button_state != Buttons.CLOCK:
            self.reset()
            self.prev_button_state = Buttons.CLOCK
# the above lines of code make sure the previously pressed button matches the next button pressed (clock)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            print("connecting again...")
            sock.connect((HOST, PORT))
# The first piece of code in the ‘GET’ function connects the client programme with the server programme
# using the HOST and PORT numbers imported from network_config and print ‘connecting…’ when this happens.
# request cpu clock data from the server
            request = {"type": "request",
                       "param": "cpu_core_clock"}
            print(f"client sent: {request}")
            sock.sendall(bytes(json.dumps(request), "utf-8"))
            print("clock request sent...")
            # The above line of code sends the request for the clock in bytes to the server.
            # Receive clock data from the server
            response = str(sock.recv(4096), "utf-8")
            val1 = self.extract_value_message(response, "CPU Core #1")
            val2 = self.extract_value_message(response, "CPU Core #2")
# The above lines of code are used to receive the requested data from the server in strings.
# For each of the ‘Get’ requests ‘(socket.recv(????)’
# must be different sockets, because every socket must have a different number.
# 'val1' is the value of 'CPU Core #1' and 'val2' is the value of 'CPU Core #2'
            x = time.time()
            x = x - self.starttime
            y1 = val1
            y2 = val2
# the above lines of code plot the time on the x-axis of the graph when the clock button is pressed
# Showing the time which has past since the clock button was pressed between the user pressing the clock button
            self.clock_c1_x.append(x)
            self.clock_c1_y.append(y1)
            self.clock_c2_y.append(y2)
# the above lines of code are retrieving the clock value when the clock data is requested
# The two lines of code below then plot the clock value on the graph on the GUI
            self.plot(self.clock_c1_x, self.clock_c1_y, 0)
            self.plot(self.clock_c1_x, self.clock_c2_y, 1)
#Below is the 'GetPower' function
    def GetPower(self):
        if self.prev_button_state != Buttons.POWER:
            self.reset()
            self.prev_button_state = Buttons.POWER
# the above lines of code make sure the previously pressed button matches the next button pressed (power)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            print("connecting again...")
            sock.connect((HOST, PORT))
# The first piece of code in the ‘GET’ function connects the client programme with the server programme
# using the HOST and PORT numbers imported from network_config and print ‘connecting…’ when this happens.
# request cpu clock data from the server
            request = {"type": "request",
                       "param": "cpu_core_power"}
            print(f"client sent: {request}")
            sock.sendall(bytes(json.dumps(request), "utf-8"))
            print("power request sent...")
            # The above line of code sends the request for the power in bytes to the server.
            # Receive power data from the server
            response = str(sock.recv(8192), "utf-8")
            val1 = self.extract_value_message(response, "CPU DRAM")
            val2 = self.extract_value_message(response, "CPU Package")
# The above lines of code are used to receive the requested data from the server in strings.
# For each of the ‘Get’ requests ‘(socket.recv(????)’
# must be different sockets, because every socket must have a different number.
# 'val1' is the value of 'CPU DRAM' and 'val2' is the value of 'CPU Package'
            x = time.time()
            x = x - self.starttime
            y1 = val1
            y2 = val2
# the above lines of code plot the time on the x-axis of the graph when the power button is pressed
# Showing the time which has past since the power button was pressed between the user pressing the power button
            self.power_c1_x.append(x)
            self.power_c1_y.append(y1)
            self.power_c2_y.append(y2)
# the above lines of code are retrieving the power value when the power data is requested
# The two lines of code below then plot the power value on the graph on the GUI
            self.plot(self.power_c1_x, self.power_c1_y, 0)
            self.plot(self.power_c1_x, self.power_c2_y, 1)


            #self.windowLog.insert(0.0, load_response)
            #self.windowLog.insert(0.0, "\n")
#the below 'plot' function describes the construction of the line which plots the graph on the GUI
    def plot(self, x, y, id):
        if id == 0:
            self.ax0.plot(x, y, color='blue', marker='o', linestyle='dashed', linewidth=1, markersize=3)
        elif id == 1:
            self.ax1.plot(x, y, color='red', marker='o', linestyle='dashed', linewidth=1, markersize=3)
        self.canvas.draw()
#the below 'reset' function is used to clear the 'temperature', 'load', 'clock' and 'power' data when pressed on the GUI
    def reset(self):
        self.ax0.clear()
        self.ax1.clear()
        self.starttime = (time.time())
        self.canvas.draw()

        self.temp_c1_x.clear()
        self.temp_c1_y.clear()
        self.temp_c2_y.clear()
#clears temperature data
        self.load_c1_x.clear()
        self.load_c1_y.clear()
        self.load_c2_y.clear()
#clears load data
        self.clock_c1_x.clear()
        self.clock_c1_y.clear()
        self.clock_c2_y.clear()
#clears clock data
        self.power_c1_x.clear()
        self.power_c1_y.clear()
        self.power_c2_y.clear()
#clears power data
if __name__ == '__main__':
    # tkinter gui
    # create root
    root = Tk()
    client = ClientGUI(master=root)
    client.mainloop()
    print("exiting...")