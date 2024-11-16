# This code is used to get data from the Arduino and save it to a csv file

import serial
import csv
ser = serial.Serial('/dev/cu.usbserial-1110', 115200) # Change this to the port your Arduino is connected to
t = 0
with open("k0c0_15.csv", mode="w") as dataFile: #Change file name here
    dataWriter = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    while t < 250:
        f = str(ser.readline()).strip("b'").split("\\t")[0:5]
        t += 1
        print(f)
        dataWriter.writerow(f)
