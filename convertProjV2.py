import pandas as pd
import numpy as np
from pyproj import Proj, transform


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


def transf(epsgIn, epsgOut, coor, dims):
    # inProj = Proj(init='epsg:3857')
    inProj = Proj(epsgIn)
    outProj = Proj(epsgOut)
    # outProj = Proj(init='epsg:4326')
    x, y, z = coor.getCoords()
    if dims == 3:
        out = transform(inProj, outProj, x, y, z)
    else:
        out = transform(inProj, outProj, x, y)

    
    return out

inputFile = "myData.txt"
outputFile = "transformed_" + inputFile
epsgIn = 'epsg:31467' # DHDN GK zone 3
epsgOut = 'epsg:4326' # WGS84
outputDims = 2

data = pd.read_csv(inputFile) #, usecols=[1,2,3], names=['x', 'y', 'z'])
npd = data.to_numpy()

w = open(outputFile, "w", 16000000)
tmpString = ""
l = len(npd[1])
for i in range(len(npd)):
    # x and y are exchanged because DHDN uses Northing (y) and Easting (x)
    C = Coords(npd[i][1], npd[i][0] , npd[i][2] )
    c = transf(epsgIn,epsgOut,C , outputDims)
    # tmpString = str(c[0]) + " " + str(c[1]) + "\n"
    if l==7:
        tmpString = str(c[1]) + " " + str(c[0]) + " " + str(C.z) + " " + str(npd[i][3]) + str(npd[i][4]) + str(npd[i][5]) +  str(npd[i][6]) + "\n"
    else:
        tmpString = str(c[1]) + " " + str(c[0]) + " " + str(C.z) + " " + str(npd[i][3]) + str(npd[i][4]) + str(npd[i][5]) + "\n"
    if i % 100==0:
        print(str(i) + ": " + tmpString)
    w.write(tmpString)


w.close()
print("end reached!")
