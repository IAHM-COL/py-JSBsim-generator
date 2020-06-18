#!/usr/bin/python
# copyright 2020, Israel Hernandez - IAHM-COL
# copyright 2020, Simon 'Bomber' Marley
# License, GPL version 3 or later

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

#we can print the content of these airfoils to the terminal
#ie;

g535.print_airfoil()

# We can obtain a plot of the airfoil2D
# and then save it as a figure

myPlot = g535.plot_airfoil()
myPlot.savefig("output/g535.png")

# We can also save the airfoil in a new csv file
# (why this is useful is seen later)

g535.csvWriter(file="output/g535.csv")

# Finally, we can use an interpolation to smooth the airfoil
# (this is implicitly used on 3d extrapolations)
#
# The interpolation uses a parameter xdim which indicates
# the sampling lenght of the x-axis (span-wise)
# larger xdim produces larger airfoils more finely partitioned
# Note: in the absence of xdim, it assumes xdim = 25
#example

g535 = g535.interpolate(xdim=100)
g549 = g549.interpolate(xdim=100)
g535.csvWriter(file="output/g535_interpolated.csv")
myPlot = g535.plot_airfoil()
myPlot.savefig("output/g535_interpolated.png")


##STEP 2

## Here we construct an airfoil3D and extrapolate it
## so it contains information along the span

#To create an airfoil3D we can use the chord and tip information as such

gottingen = airfoil3D(chord=g535, tip=g549)

#indeed we can print the airfoil3D to the terminal, as well

gottingen.print_airfoil()

# we can produce plots for the Chord of the tip, like
tipPlot = gottingen.plot_airfoil_tip()
chordPlot = gottingen.plot_airfoil_chord()
tipPlot.savefig("output/gottingen_tip.png")
chordPlot.savefig("output/gottingen_chord.png")

##STEP 3

## Interpolation of the airfoil3D 
## This, just as the airfoil2D interpolation
## has the parameter xdim, indicating the level of smoothness on the
## airfoil section
## in addition it hast the parameter spandim
## which sets the locations at which you are intending to
## obtain sections of the airfoil
## like this
## spandim = [0, 0.5, 0.75, 1]
## Note, 0 and 1 are required indicating chord and tip respectively
## Note, the projection assumes lineal transformation
## of the wing shape
## Note, in the absence of spandim parameter, it presumes every 10%, such as
## spandim = [0,0.1,0.2......1.0]

gottingen = gottingen.interpolate(xdim=100, spandim=list(np.linspace(0,1,8)))

# in addition to the plot for chord and tip as above
# we can plot the projection at any segment requested, like so

#aplot=gottingen.plot_airfoil(segment=0.2)
#aplot.savefig("output/gottingen02.png")

## We can also export the interpolated airfoil3D
## as a series of CSV files

gottingen.csvWriter(path="output/")
