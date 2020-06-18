#!/usr/bin/python
# copyright 2020, Israel Hernandez - IAHM-COL
# copyright 2020, Simon 'Bomber' Marley
# License, GPL version 3 or later

##This is a minimal example to produce the 3D projection of airfoils on
#CSV files given chord and tip specifications an presuming linear
#decay from chord to tip.

## For more detailed example of usage check
## wingTest.py

from airfoils import airfoil2D, airfoil3D
import numpy as np

# After importing the airfoil2D and airfoil3D above
#
# STEP 1
#
# Read the CSV files,
# as new instances of airfoil2D()

g535 = airfoil2D().csvLoader(file="G535.csv")
g549 = airfoil2D().csvLoader(file="G549.csv")

##STEP 2

## Here we construct an airfoil3D and extrapolate it
## so it contains information along the span

#Create an airfoil3D: we can use the chord and tip information as such

gottingen = airfoil3D(chord=g535, tip=g549)

##STEP 3

## Interpolation of the airfoil3D 

gottingen = gottingen.interpolate(xdim=100, spandim=list(np.linspace(0,1,8)))

##STEP 4: write the result to a desired path

gottingen.csvWriter(path="output/")
