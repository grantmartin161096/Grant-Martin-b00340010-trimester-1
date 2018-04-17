import socketserver
import time
from network_configuration import HOST, PORT
#The above line of code imports the localhost and port numbers (HOST, PORT = "127.0.0.1", 9997) in the server programme
#And the same import is present in the client code, so the client and server programmes can communicate with each other.
from OHM import OHM
#The above line of code is importing the OHM class set-up in the OHM Python file, to import data from the OHM.
import json
#The above line of code imports JSON files into the programme,
#this is important as the data from the OHM will be entering the programme in this format
#and data being sent from the server to the client will be in this file format.


class TCPRequestHandler(socketserver.BaseRequestHandler):
    #This class sets up how the server will deal with requests from the client.
    """
    The request handler receives the response data from the client
    """

    def __init__(self, request, client_address, server):

        print("initialising. . . ")
        #When a request is made from the client the server will print ‘initialising. . .’
        # Init the base class
        super(TCPRequestHandler, self).__init__(request, client_address, server)
#The below function will define how the server will handle the request made from the client.
    def handle(self):
        #time.sleep(1)
#The above line of code ‘time.sleep(1)’ will pause the client GUI request button pressed for 1 second
#(there are 4 request buttons on the GUI : Temperature, Load, Clock and Power)
        """
        The request handler class.
        """
        print("client data incoming...")
        #  self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip().decode("utf-8")  # NB bytes to string
        #In the above lines of code, the server decodes the received data from the OHM class from bytes
        #(ones and zeros) to strings (readable figures/information)
        print(f"data received: {self.data}")

        # request OHM data
        requested_data = {}
        my_ohm = OHM()
        request = json.loads(self.data)
        if request['type'] == 'request':
            if request['param'] == 'cpu_core_temp':
                requested_data = my_ohm.get_core_temps()
            elif request['param'] == "cpu_core_load":
                requested_data = my_ohm.get_core_loads()
            elif request['param'] == "cpu_core_clock":
                requested_data = my_ohm.get_core_clocks()
            elif request['param'] == "cpu_core_power":
                requested_data = my_ohm.get_core_powers()
#The above code is used to retrieve the requested data from the OHM class set-up in the OHM.py file,
#by using if and elif statements and calling ‘my_ohm = OHM()’ function.
        print(requested_data)
        # return the data to the client
        response = json.dumps(requested_data)
        self.request.sendall(response.encode('utf-8'))
#The above two lines of code are used to send the data requested by the client, back to the client from the server.
#This data is sent to the client in bytes (ones and zeros)
#so we need to encode the strings (readable figures/information) into bytes.

def main():
    with socketserver.TCPServer((HOST, PORT), TCPRequestHandler) as server:
        print("starting server")
        server.serve_forever()
#The above function ‘def main():’
#Is setting the server to run forever on the TCP network established and using the set-up localhost and port.

if __name__ == '__main__':
    main()
    print("exiting...")
#The server programme will print ‘exiting…’ if the programme is stopped.