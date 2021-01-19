import pandas as pd
import numpy as np
from pyproj import Transformer


class Coords():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def getCoords(self):
        return self.x, self.y, self.z

    def setCoords(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


inputFile = "polylines_with_velocity_GK.csv"
outputFile = "transformed_" + inputFile
epsgIn = 'epsg:31467'  # DHDN GK zone 3
epsgOut = 'epsg:4326'  # WGS84
outputDims = 2

data = pd.read_csv(inputFile)# , usecols=[1,2,3,4,5,6,7], names=['x', 'y', 'z','R','G','B','ID'])
npd = data.to_numpy()

w = open(outputFile, "w", 16000000)
tmpString = ""
l = len(npd[1])
transformer = Transformer.from_crs(epsgIn, epsgOut)

for i in range(len(npd)):
    # x and y are exchanged because DHDN uses Northing (y) and Easting (x)
    C = Coords(npd[i][1], npd[i][0], npd[i][2])
       
    if outputDims == 3:        
        c = transformer.transform(C.x,C.y,C.z)
    else:        
        c = transformer.transform(C.x,C.y)


    if l == 9:
        tmpString = str(c[1]) + "," + str(c[0]) + "," + str(C.z) + "," + str(npd[i][3]) + \
            "," + str(npd[i][4]) + "," + str(npd[i][5]) + \
            "," + str(npd[i][6]) + "," + str(npd[i][7]) + "," + str(npd[i][8]) + "\n"

    if l == 7:
        tmpString = str(c[1]) + "," + str(c[0]) + "," + str(C.z) + "," + str(npd[i][3]) + \
            "," + str(npd[i][4]) + "," + str(npd[i][5]) + \
            "," + str(npd[i][6]) + "\n"
    elif l == 6:
        tmpString = str(c[1]) + "," + str(c[0]) + "," + str(C.z) + "," + \
            str(npd[i][3]) + "," + str(npd[i][4]) + "," + str(npd[i][5]) + "\n"
    elif l == 3:
        tmpString = str(c[1]) + "," + str(c[0]) + "," + str(C.z) + "\n"

    if i % 100 == 0:
        print(str(i) + ": " + tmpString)
    w.write(tmpString)


w.close()
print("end reached!")
