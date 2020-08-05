# convertCoordinates
convert a list of coordinates from a txt file between different CRS using python and proj4 library

This short script was not thoroughly tested only on a few data sets on which it worked. It is a small tool to help me in may daily work to convert coordinates between differen Coordinate Reference Systems (CRS).

It requires the followint dependencies:
* pandas 1.0.3
* numpy 1.18.3
* pyproj 2.6.0

You need to change 4 lines (lines 35-39 in original commited file) of code to adapt it to your use-case. These lines are quite self- explanatory. Three output dimensions (line 39) has not been tested but in any way it only works with supported CRS.
```
35   inputFile = "streamlineData.txt"
36   outputFile = "transformed_" + inputFile
37   epsgIn = 'epsg:31467' # DHDN GK zone 3
38   epsgOut = 'epsg:4326' # WGS84
39   outputDims = 2
```


Lines 53 and 55 are for my special use-case. Here the additional data contained after the coordinates in the CSV or TXT file are also copied into the output file. This can be easily adapted to your need or even removed.

