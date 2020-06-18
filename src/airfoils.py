#!/usr/bin/python
# copyright 2020, Israel Hernandez - IAHM-COL
# copyright 2020, Simon 'Bomber' Marley
# License, GPL version 3 or later

from scipy.interpolate import interp1d as interpolate
import matplotlib.pyplot as plt
import numpy as np
import csv

baseXdim = 25
baseSpandim = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

class airfoil2D:
    """Defines a class airfoil that manages specification of wing airfoil
    outline in 2D"""
    
    def __init__(self, name=None, upperlip=None, lowerlip=None):
        """Constructor for an airfoil"""
        self.name = name
        self.upperlip = {
            'x': np.linspace(1,0,15,endpoint=False),
            'y': np.zeros(15)
        }
        self.lowerlip = {
            'x': np.linspace(0,1,15),
            'y': np.zeros(15)
        }
        
        if upperlip is not None:
            self.upperlip = upperlip
            if lowerlip is not None:
                self.lowerlip = lowerlip

    def __repr__(self):
        return '<%s.%s object at %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self))
        )

    def set_upperlip(self,upperlip=None):
        if upperlip is None:
            self.upperlip = {
                'x': np.linspace(1,0,15,endpoint=False),
                'y': np.zeros(15)
            }
        self.upperlip=upperlip

    def set_lowerlip(self,lowerlip=None):
        if lowerlip is None:
            self.lowerlip = {
                'x': np.linspace(1,0,15,endpoint=False),
                'y': np.zeros(15)
            }
        self.lowerlip=lowerlip

    def flatten_upperlip(self):
        self.set_upperlip()

    def flatten_lowerlip(self):
        self.set_lowerlip()

    def flatten(self):
        self.flatten_upperlip()
        self.flatten_lowerlip()
        
    def interpolate(self, xdim=None):
        if xdim is None:
            xdim=baseXdim
            
        upperInterpolate = interpolate(self.upperlip['x'],
                                       self.upperlip['y'],
                                       kind='cubic',
                                       fill_value='extrapolate')
        lowerInterpolate = interpolate(self.lowerlip['x'],
                                       self.lowerlip['y'],
                                       kind='cubic',
                                       fill_value='extrapolate')
        xupper = np.linspace(1,0,xdim,endpoint=False)
        yupper = upperInterpolate(xupper)
        xlower =  np.linspace(0,1,xdim)
        ylower = lowerInterpolate(xlower)
        interpolated=airfoil2D()
        interpolated.upperlip = {'x':xupper,
                                   'y':yupper    }
        interpolated.lowerlip = {'x':xlower,
                                   'y':ylower    }
        interpolated.name = self.name
        return (interpolated)

    def print_airfoil(self):
        """prints an airfoil"""
        print (self.name)
        for elem in range(len(self.upperlip['x'])):
            print ("{:05f}".format(self.upperlip['x'][elem])
                   +
                   "\t" +
                   ("{:05f}".format(self.upperlip['y'][elem])))
        for elem in range(len(self.lowerlip['x'])):
            print ("{:05f}".format(self.lowerlip['x'][elem])
                   +
                   "\t" +
                   ("{:05f}".format(self.lowerlip['y'][elem])))


    def plot_airfoil(self, width=6.5, height=4):
        """Produces airfoil plot"""
        plt.figure(figsize=(width, height))
        plt.plot(np.append(self.upperlip['x'],0),
                 np.append(self.upperlip['y'],0),
                 label=self.name)
        plt.plot(self.lowerlip['x'],
                 self.lowerlip['y'])
        return (plt)

    def csvLoader(self, file=None):
        """Loads a 2D airfoil from a CSV"""
        newAirfoil=airfoil2D()
        if file is None:
            return (newAirfoil)

        x,y=[],[]
        with open(file, newline='') as csvfile:
            reader=csv.DictReader(csvfile, fieldnames=['x','y'])
            next(reader) #skip name
            for row in reader:
                x.append(row['x'])
                y.append(row['y'])

        x = [float(i) for i in x]
        y = [float(i) for i in y]
        lipboundary = x.index(0)
        xupper = x[0:lipboundary]
        yupper = y[0:lipboundary]
        xlower = x[lipboundary:len(x)]
        ylower = y[lipboundary:len(x)]
        newAirfoil.upperlip = {'x':xupper,
                                 'y':yupper    }
        newAirfoil.lowerlip = {'x':xlower,
                                 'y':ylower    }
        newAirfoil.name = file.replace('.csv', '')
        return (newAirfoil)

    def csvWriter(self, file=None):
        """Writes a 2D airfoil to new CS"""
        if file is None:
            file = self.name + ".csv"

        rowsupper = zip(self.upperlip['x'],
                        self.upperlip['y'])
        rowslower = zip(self.lowerlip['x'],
                        self.lowerlip['y'])
        with open(file, 'w', newline='') as csvfile:
            foilwriter = csv.writer (csvfile, delimiter=',')
            foilwriter.writerow([self.name,''])
            for row in rowsupper:
                foilwriter.writerow(row)
            for row in rowslower:
                foilwriter.writerow(row)

        return(file)

class airfoil3D:
    """Defines an airfoil with multiple airfoil2D sections
    and can do lineal extrapolation from chord (0) to tip (1) 
    at arbitrary relative segment locations (0,1]."""

    def __init__(self, chord=airfoil2D(), tip=None):
        if tip is None:
            tip = airfoil2D()
            tip.name = "Tip"
        if chord.name is None:
            chord.name = "Chord"
        self.airfoilSet = [chord,tip]
        self.segmentSet = [0,1]    

    def __repr__(self):
        return '<%s.%s object at %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self))
        )

    def setChord(self, chord=airfoil2D()):
        self.airfoilSet[0] = chord
        self.segmentSet[0] = 0

    def setTip(self, tip=airfoil2D()):
        self.airfoilSet[-1] = tip
        self.segmentSet[-1] = 1

    def flattenChord (self):
        self.setChord()

    def flattenTip (self):
        self.setTip()
        
    def print_airfoil(self):
        """Prints the airfoil 3D segments from chord to tip"""
        for elem in self.airfoilSet:
            elem.print_airfoil()

    def plot_airfoil(self, segment=0):
        """Plots the requested segment"""
        FoilIndex=self.segmentSet.index(segment)
        figure = self.airfoilSet[FoilIndex].plot_airfoil()
        return (figure)

    def plot_airfoil_chord(self):
        figure = self.plot_airfoil(0)
        return (figure)

    def plot_airfoil_tip(self):
        figure = self.plot_airfoil(1)
        return (figure)

    def csvWriter(self, path="./"):
        """Writes CSV files for each segmentation"""
        for elem in self.airfoilSet:
            if elem.name is not None:
                elem.csvWriter(file = path + elem.name + "_" + 
                               str(self.airfoilSet.index(elem)) +
                               ".csv")
            if elem.name is None:
                elem.csvWriter(file = path +
                               str(self.airfoilSet.index(elem)) +
                               ".csv")


    def interpolate(self, xdim=None, spandim=None):
        """Interpolates an airfoil3D on spandim segmentations"""
        if xdim is None:
            xdim = baseXdim
        if spandim is None:
            spandim =  baseSpandim

        """equalize xdims by interpolation"""
        chord = self.airfoilSet[0].interpolate(xdim=xdim)
        tip   = self.airfoilSet[1].interpolate(xdim=xdim)

        #create interpolation matrix of airfoils
        interpolated3D = airfoil3D()
        interpolated3D.segmentSet=spandim
        size = len(spandim)
        for i in range(size-1):
            interpolated3D.airfoilSet.append(airfoil2D())
        for idx, elem in enumerate(interpolated3D.airfoilSet):
            interpolated3D.airfoilSet[idx] = elem.interpolate(xdim=xdim)
            
        interpolated3D.setChord(chord)
        interpolated3D.setTip(tip)
        interpolated3D.airfoilSet[1].name = None

        """Set names of projectors"""
        for idx, elem in enumerate(interpolated3D.airfoilSet):
            if elem.name is None:
                elem.name = str(idx)

        def spanProjector(chordy,tipy,span=spandim):
            x=[spandim[0],spandim[-1]]
            y=[chordy, tipy]
            if (chordy - tipy == 0):
                return ([0 for i in spandim])
            spanInterpolate = interpolate(x,y, kind='linear',
                                          fill_value='extrapolate')
            spanExtrapolate = spanInterpolate(span)
            return(spanExtrapolate)

        """Interpolates shape"""
        for i in range(xdim):
            projectionUpper = spanProjector(interpolated3D.airfoilSet[0].upperlip['y'][i],
                                            interpolated3D.airfoilSet[-1].upperlip['y'][i],
                                            spandim)
            projectionLower = spanProjector(interpolated3D.airfoilSet[0].lowerlip['y'][i],
                                            interpolated3D.airfoilSet[-1].lowerlip['y'][i],
                                            spandim)

            for j in range(len(spandim)):
                interpolated3D.airfoilSet[j].upperlip['y'][i] = projectionUpper[j]
                interpolated3D.airfoilSet[j].lowerlip['y'][i] = projectionLower[j]
        
        return (interpolated3D)
