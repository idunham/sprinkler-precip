#!/usr/bin/env python
##############################################################
# Sprinkler array code...
# Currently assumes frequency=1 (spacing of catchments)
# Hardcoded MaxDist (radius of spray area)
# Uses linear interpolation
# 
#
#
#
##############################################################

from numpy import *
from scipy import interpolate
import math
import matplotlib.pyplot as plt



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


def MapSprinkler(Sprinkler,SprinklerPrecip,MaxDist):
	for x in range(0,(MaxDist+1)):
		for y in range(0,(MaxDist+1)):
			# We'll allow mapping onto a filled map
			r=(x**2 + y**2)**.5
			CellPrecip = PolInterp(r,SprinklerPrecip,MaxDist)
		 	Sprinkler[(MaxDist-x,MaxDist-y)] += CellPrecip
			Sprinkler[(MaxDist+x,MaxDist-y)] += CellPrecip
			Sprinkler[(MaxDist+x,MaxDist+y)] += CellPrecip
			Sprinkler[(MaxDist-x,MaxDist+y)] += CellPrecip


Sprinkler = zeros( ((2*MaxDist+1),(2*MaxDist+1)) )

SprinklerDist = [0,1,2,3,4,5,6,7,8,9,10]
SprinklerData = [0,1.4,1.2,1,1,1,.9,.9,.8,.4,0]
MaxDist       = int(math.ceil(SprinklerDist[SprinklerDist.shape[0]-1]))

SprinklerSpace= int(8)

SprinklerPrecip=interpolate.splrep(SprinklerDist,SprinklerData)
MapSprinkler(Sprinkler,SprinklerData,MaxDist)

# Now to add the sprinkler maps up correctly...
AllSprinklers=zeros( (MaxDist * 4 + 1, MaxDist * 4 + 1))

CurrX = int(MaxDist + 1 - SprinklerSpace*(math.floor( (MaxDist+1)/SprinklerSpace)/2 ))
CurrY = CurrX
SprinklerNum=int( math.ceil( (4 * MaxDist + 1 - CurrX)/SprinklerSpace ) )
# Fill block of sprinkler positions
# Basic theory:
# Sprinkler.shape=(2*MaxDist+1,2*MaxDist+1)
# Sprinkler[ceil(Breadth)]  is the center.
# Sprinkler[1,1] is the corner of the data, but we'll use [0,0]
# We need X & Y = the starting corners.
#

X = CurrX - int( math.ceil(Sprinkler.shape[0])/2 )
#  print (4 * MaxDist), CurrX, SprinklerSpace, SprinklerNum
for x in range(0,SprinklerNum):
	Y = CurrY -  int( math.ceil( Sprinkler.shape[0] )/2 )
	for y in range(0,SprinklerNum):
		#  SprinklerPos[x,y,0]=X
		#  SprinklerPos[x,y,1]=Y
		AddArray2D(AllSprinklers,Sprinkler,X,Y)
		#  print X, Y, x, y
		Y=Y+SprinklerSpace
	X=X+SprinklerSpace


SprinklerPlot=plt.contourf(AllSprinklers[(MaxDist+1):(MaxDist+SprinklerSpace+2),(MaxDist+1):(MaxDist+SprinklerSpace+2)])
Plot2=plt.contourf(AllSprinklers)
plt.colorbar()
plt.show()

