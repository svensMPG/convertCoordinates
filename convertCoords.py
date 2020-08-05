import pandas as pd
import numpy as np
from pyproj import Proj, transform
import sys
import getopt


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



################ Starting the console parameter parseing ###################
###########################################################################
# this block is only used for calling the python script from console with parameters.
# if parameters are hard coded this block can be avoided. It is not part of the actuall data processing

if len(sys.argv) < 2:
    sys.exit("ERROR: not enough arguments. At least an input file is required. Use " +
             sys.argv[0] + " -f or --file INPUT.file")

# define a help text
helpText = "-h or --help:\t\tshows this help.\n-f or --file=[FILE]:\twhere FILE is the input file. This is mandatory\n"
helpText += "-v or --verbose:\tprint some info during processing\n"
helpText += "-i or --inputEPSG:\tdefine the EPSG code of the intput data in the format 'EPSG:31467'\n"
helpText += "-o or --outpttEPSG:\tdefine the EPSG code of the result, same format as inputEPSG.\n"
helpText += "-d or --inDim:\t\tinput Dimensions 2 or 3 accepted, i.e. x,y or x,y,z = height\n-D or --outDim:\t\toutput Dimensions, see input Dimensions.\n"
helpText += "-c or --coordsOnly:\tif set only the transformed coordinates are written to output file. Otherwise, \n\t\t\tthe rest of the columns of the input file will be appended after the last coordinate columnt."


# define valid arguments for command line arguments
short_options = "f:hi:o:vd:D:c"
long_options = ["file=", "help", "inputEPSG=",
                "outputEPSG=", "verbose", "inDim=", "outDim=", "coordsOnly"]

# Get full command-line arguments
full_cmd_arguments = sys.argv

# Keep all but the first
argument_list = full_cmd_arguments[1:]

# try to read arguments
try:
    arguments, values = getopt.getopt(
        argument_list, short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    print(str(err))
    sys.exit(2)

hasESPG_in = False
hasESPG_out = False
verbose = False
hasInputFile = False
inDim = 2
outDim = 2
coordsOnly = False

# Evaluate given options
for current_argument, current_value in arguments:
    if current_argument in ("-v", "--verbose"):
        verbose = True
    elif current_argument in ("-h", "--help"):
        sys.exit(helpText)
    elif current_argument in ("-i", "--inputEPSG"):
        epsgIn = current_value
        hasESPG_in = True
    elif current_argument in ("-o", "--outputEPSG"):
        epsgOut = current_value
        hasESPG_out = True
    elif current_argument in ("-c", "--coordsOnly"):
        coordsOnly = True
    elif current_argument in ("-f", "--file"):
        inputFile = current_value
        hasInputFile = True
    if current_argument in ("-d", "--inDim"):
        inDim = current_value
    if current_argument in ("-D", "--outDim"):
        outDim = current_value

if not hasInputFile:
    sys.exit("ERROR: no input file given. use " +
             sys.argv[0] + " --file=input.file or -f input.file [OPTIONS]\nFor OPTIONS, see --help")

if not(hasESPG_in and hasESPG_out):
    print("WARNING: not enough arguments.\n Input file and input and output EPSG code is needed.\n Applying standard transform from DHDN GKz3 to WGS84")
    epsgIn = 'epsg:31467'  # DHDN GK zone 3
    epsgOut = 'epsg:4326'  # WGS84


outputFile = "transformed_" + inputFile
################ end of console parameter parseing ###################

####################################################################################################
############### actual processing of data starts here and function definitions above ###############
####################################################################################################

data = pd.read_csv(inputFile)  # , usecols=[1,2,3], names=['x', 'y', 'z'])
npd = data.to_numpy()

w = open(outputFile, "w", 16000000)
tmpString = ""

s = npd.shape[1]

for i in range(len(npd)):
    # x and y are exchanged because DHDN uses Northing (y) and Easting (x)
    C = Coords(npd[i][1], npd[i][0], npd[i][2])
    c = transf(epsgIn, epsgOut, C, outDim)
    # tmpString = str(c[0]) + " " + str(c[1]) + "\n"

    if coordsOnly:
        tmpString = str(c[1]) + " " + str(c[0]) + " " + str(int(npd[i][3])) + "\n"
    else:
        tmpString = str(c[1]) + " " + str(c[0]) + " " + \
            str(int(npd[i][3])) + " " + \
            str(npd[i][inDim:]).strip("[").strip("]") + "\n"
    if verbose:
        if i % 10 == 0:
            print(str(i) + ": converting " + epsgIn + " --> " + epsgOut + ": " + str(npd[i][1]) + ", " + str(
                npd[i][0]) + ", " + str(npd[i][2]) + " --> " + tmpString)
    w.write(tmpString)


w.close()
print("end reached!")
