import wmi
#The first line of code imports Windows Management Instrumentation
#to allow our Python programme to access data from the Open Hardware Monitor.
debug = False
#when ‘debug = False’ when the code is run we only receive the CPU temperature,
#when ‘debug = True’ we receive temperature value and maximum temperatures of the devices identified (CPU, RAM and HDD).

#The next piece of code is contained within a class,
#the name of this class is ‘OHM’ and this class is called upon in the code for the server programme,
#when the server receives a ‘GET’ request from the client, the server will then pull this data from the ‘class OHM’.
class OHM:

    def __init__(self):
        self.hwmon = wmi.WMI(namespace="root\OpenHardwareMonitor")

    def get_core_temps(self):
        data = {}
        sensors_temp = self.hwmon.Sensor(["Name", "Parent", "Value", "Identifier", "SensorType", "Max"],
                                         SensorType="Temperature")
        if debug:
            print(sensors_temp)

        for temperature in sensors_temp:

            if debug:
                print("temperature object")
                print(temperature)

            if (temperature.Identifier.find("ram") == -1) and (temperature.Identifier.find("hdd") == -1) \
                    and (temperature.Name.find("Package") == -1):
                if debug:
                    print("cpu temperature values")
                    print(f"{temperature.value}, {temperature.max}, {temperature.name}")

                data['type'] = "cpu temperature"
                data[temperature.name] = temperature.value

        return data
#The above lines of code contain the ‘GET’ function for ‘temperature’ values from the OHM sensors
#and the ‘debug’ call which has already been explained.

    def get_core_loads(self):
        data = {}
        sensors_load = self.hwmon.Sensor(SensorType="Load")

        if debug:
            print(sensors_load)

        for load in sensors_load:
            if (load.Identifier.find("ram") == -1) and (load.Identifier.find("hdd") == -1) and \
                    (load.Name.find("Total") == -1):

                if debug:
                    print(f"{load.value}, {load.name}")

                data['type'] = "cpu load"
                data[load.name] = load.value

        return data
#The above lines of code contain the ‘GET’ function for the ‘load’ sensor from the OHM
#(‘def get_core_loads (self):’) in the above code the sensors are identified, the type of sensor is defined
#and when this function is called the data is returned to the server, which then relays this information to the client.

    def get_core_clocks(self):
        data = {}
        sensors_clock = self.hwmon.Sensor(SensorType="Clock")

        if debug:
            print(sensors_clock)

        for clock in sensors_clock:
            if (clock.Identifier.find("ram") == -1) and (clock.Identifier.find("hdd") == -1) and \
                    (clock.Name.find("Total") == -1):

                if debug:
                    print(f"{clock.value}, {clock.name}")

                data['type'] = "cpu clock"
                data[clock.name] = clock.value

        return data
#The above lines of code contain the ‘GET’ function for the ‘clock’ sensor from the OHM
#(‘def get_core_clocks (self):’) in the above code the sensors are identified, the type of sensor is defined
#and when this function is called the data is returned to the server, which then relays this information to the client.

    def get_core_powers(self):
        data = {}
        sensors_power = self.hwmon.Sensor(SensorType="Power")

        if debug:
            print(sensors_power)

        for power in sensors_power:
            if (power.Identifier.find("ram") == -1) and (power.Identifier.find("hdd") == -1) and \
                    (power.Name.find("Total") == -1):

                if debug:
                    print(f"{power.value}, {power.name}")

                data['type'] = "cpu power"
                data[power.name] = power.value

        return data
#The above lines of code contain the ‘GET’ function for the ‘power’ sensor from the OHM
#(‘def get_core_powers (self):’) in the above code the sensors are identified, the type of sensor is defined
#and when this function is called the data is returned to the server, which then relays this information to the client.

if __name__ == '__main__':

    my_ohm = OHM()
    core_temps = my_ohm.get_core_temps()
    print(core_temps)
    core_loads = my_ohm.get_core_loads()
    print(core_loads)
    core_clocks = my_ohm.get_core_clocks()
    print(core_clocks)
    core_powers = my_ohm.get_core_powers()
    print(core_powers)

#The final part of code for the OHM from ‘if __name__ == '__main__':’ down is called upon by the server,
#to return the data from the OHM class.