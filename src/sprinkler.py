#!/usr/bin/env python
##############################################################
# Sprinkler array code...
# 
#
#
#
##############################################################

from numpy import *
from Tkinter import *
from scipy import interpolate
import matplotlib.pyplot as plt
import tkFileDialog as tkf
import csv
import math


def AddArray2D(Target,From,CornerX=0,CornerY=0):
	TgtX=Target.shape[0]
	TgtY=Target.shape[1]
	FromX=From.shape[0]
	FromY=From.shape[1]
	TMinX=int(CornerX)
	TMinY=int(CornerY)
	TMaxX=FromX+TMinX
	TMaxY=FromY+TMinY
	# We need to get the window for From, also
	FMinX=0
	FMinY=0
	FMaxX=FromX
	FMaxY=FromY
	# Fix the edge/corner cases	
	if TMinX < 0:
		FMinX -= TMinX
		TMinX = 0
	if TMinY < 0:
		FMinY -= TMinY
		TMinY = 0
	if TMaxX > TgtX:
		FMaxX -= (TMaxX - TgtX)
		TMaxX = TgtX
	if TMaxY > TgtY:
		FMaxY -= (TMaxY - TgtY)
		TMaxY = TgtY
	Target[TMinX:TMaxX,TMinY:TMaxY] += From[FMinX:FMaxX,FMinY:FMaxY]

def PolInterp(r,SprinklerPrecip,MaxDist=10,freq=1):
	# SprinklerPrecip should always be whatever holds precipitation data;
	# this function was split out to provide a single point of failure
	# when it gets redefined.
	# freq is unimplemented, MaxDist should be unneeded
	if r < MaxDist:		# Don't touch anything otherwise
		low=math.floor(r)
		up=math.ceil(r)
		if int(low) == int(up):
			return SprinklerPrecip[int(low)]
		else:
			return (((r-low)/(up-low)) * (SprinklerPrecip[int(up)] - SprinklerPrecip[int(low)]) + SprinklerPrecip[int(low)])
	else:
		return 0

def Interpolate(r,SprinklerPrecip,MaxDist=10):
	if r < MaxDist:
		return interpolate.splev(r, SprinklerPrecip)
	else:
		return 0

def PlotSprinkler(Sprinkler):
	Plot1=plt.contourf(Sprinkler)
	plt.colorbar()
	plt.show()



def MapSprinkler(Sprinkler,SprinklerPrecip,MaxDist):
	for x in range(0,(MaxDist+1)):
		for y in range(0,(MaxDist+1)):
			# We'll allow mapping onto a filled map
			r=(x**2 + y**2)**.5
			CellPrecip = Interpolate(r,SprinklerPrecip,MaxDist)
		 	Sprinkler[(MaxDist-x,MaxDist-y)] = CellPrecip
			Sprinkler[(MaxDist+x,MaxDist-y)] = CellPrecip
			Sprinkler[(MaxDist+x,MaxDist+y)] = CellPrecip
			Sprinkler[(MaxDist-x,MaxDist+y)] = CellPrecip

def getCSV(mode='rb'):
	root = Tk()
	root.withdraw()
	file_opt = options = {}
	options['filetypes'] = [('All files', '.*'), ('CSV data', '.csv')]
	datacsv = tkf.askopenfile(mode=mode, parent=root, **file_opt)
	root.destroy()
	dialect = csv.Sniffer().sniff(datacsv.read(1024))
	datacsv.seek(0)
	Data=csv.reader(datacsv,dialect)
	SprinklerDist = array(Data.next())
	SprinklerData = array(Data.next())
	MoreData = array(Data.next())
	datacsv.close()
	return (SprinklerDist,SprinklerData,MoreData)

if __name__=='__main__':
	Profile=getCSV('rb')
	SprinklerDist = Profile[0]
	SprinklerData = Profile[1]
	MoreData = Profile[2]

	MaxDist       = int(math.ceil(float(SprinklerDist[SprinklerDist.shape[0]-1])))

	Sprinkler = zeros( ((2*MaxDist+1),(2*MaxDist+1)) )
	SprinklerX= int(float(MoreData[0]))
	SprinklerY= int(float(MoreData[1]))
	PlotX     = 1 + 3 * SprinklerX
	PlotY     = 1 + 3 * SprinklerY

	SprinklerPrecip=interpolate.splrep(SprinklerDist,SprinklerData)
	MapSprinkler(Sprinkler,SprinklerPrecip,MaxDist)

	AllSprinklers=zeros( (PlotX,PlotY))
	SprinklerNum=int(4)

	# Fill block of sprinkler positions
	# Basic theory:
	# Sprinkler.shape=(2*MaxDist+1,2*MaxDist+1)
	# Sprinkler[ceil(Breadth)]  is the center.
	# Sprinkler[1,1] is the corner of the data, but we'll use [0,0]
	# We need X & Y = the starting corners.

	X = 0 - int( math.floor( Sprinkler.shape[0]/2 ) )
	Y = 0 - int( math.floor( Sprinkler.shape[1]/2 ) )
	for x in range(0,SprinklerNum):
		Y = 0 -  int( math.ceil( Sprinkler.shape[0] )/2 )
		for y in range(0,SprinklerNum):
			AddArray2D(AllSprinklers,Sprinkler,X,Y)
			Y=Y+SprinklerY
		X=X + SprinklerX
	
	PlotSprinkler(AllSprinklers[SprinklerX:2*SprinklerX+1,SprinklerY:2*SprinklerY+1])

