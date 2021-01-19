import pandas as pd
pd.options.mode.chained_assignment = None 
import numpy as np
from pyproj import Transformer, Geod, CRS


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


def get_linelength_between_points(C1: list, C2: list) -> float:
    geod = Geod(ellps="WGS84")
    total_length = geod.line_length(C1, C2)
    return total_length


inputFile = "polylines_with_velocity_GK.csv"
outputFile = "transformed_" + inputFile
epsgIn = 'epsg:31467'  # DHDN GK zone 3
epsgOut = 'epsg:4326'  # WGS84
outputDims = 2

# C1 = Coords(9.198090266826734,48.78972385690148,265.2137686)
# C2 = Coords(9.193484399096668,48.78742827615106,279.9151045)
# get_linelength_between_points(C1, C2)


#
# usecols=[1,2,3,4,5,6,7,8,9])#, names=['x', 'y', 'z','R','G','B','ID','velocity','AverageVelocity'])
data = pd.read_csv(inputFile, header='infer')
# npd = data.to_numpy()

w = open(outputFile, "w", 16000000)
tmpString = ""
l = len(data.columns)
transformer = Transformer.from_crs(epsgIn, epsgOut)

convLon = []
convLat = []

for i in range(len(data)):
    # x and y are exchanged because DHDN uses Northing (y) and Easting (x)
    C = Coords(data.y[i], data.x[i], data.z[i])

    if outputDims == 3:
        c = transformer.transform(C.x, C.y, C.z)
    else:
        c = transformer.transform(C.x, C.y)

    convLon.append(c[1])
    convLat.append(c[0])


data['Lon'] = pd.Series(convLon)
data['Lat'] = pd.Series(convLat)
data['pt_to_pt_dist'] = pd.Series(pd.Series(data.velocity) * 0)
data['accum_stream_dist'] = pd.Series(pd.Series(data.velocity) * 0)

stream_ids = data.ID.unique()

for id in stream_ids:
    stream_parts = data.index[data['ID'] == id].tolist()
    stream_len = len(stream_parts)
    cnt = 0
    for i in stream_parts:
        if cnt > 0:
            dist = get_linelength_between_points(
                [data.Lon[i], data.Lon[i-1]],
                [data.Lat[i], data.Lat[i-1]])

            data.pt_to_pt_dist[i] = dist
            data.accum_stream_dist[i] = data.accum_stream_dist[i-1] + dist
        else:
            data.pt_to_pt_dist[i] = 0
            data.accum_stream_dist[i] = 0

        cnt += 1

data.to_csv(f'transformed_{inputFile}_all_fields', index=False)
data.to_csv(f'transformed_{inputFile}',
            index=False,
            columns=['Lon', 'Lat', 'z', 'R', 'G', 'B', 'ID', 'velocity', 'AverageVelocity', 'pt_to_pt_dist', 'accum_stream_dist'])


# if l == 9:
#     tmpString = str(c[1]) + "," + str(c[0]) + "," + str(C.z) + "," + str(npd[i][3]) + \
#         "," + str(npd[i][4]) + "," + str(npd[i][5]) + \
#         "," + str(npd[i][6]) + "," + str(npd[i][7]) + \
#         "," + str(npd[i][8]) + "\n"

# if l == 7:
#     tmpString = str(c[1]) + "," + str(c[0]) + "," + str(C.z) + "," + str(npd[i][3]) + \
#         "," + str(npd[i][4]) + "," + str(npd[i][5]) + \
#         "," + str(npd[i][6]) + "\n"
# elif l == 6:
#     tmpString = str(c[1]) + "," + str(c[0]) + "," + str(C.z) + "," + \
#         str(npd[i][3]) + "," + str(npd[i][4]) + "," + str(npd[i][5]) + "\n"
# elif l == 3:
#     tmpString = str(c[1]) + "," + str(c[0]) + "," + str(C.z) + "\n"

# if i % 100 == 0:
#     print(str(i) + ": " + tmpString)
# w.write(tmpString)


# w.close()
print("end reached!")
