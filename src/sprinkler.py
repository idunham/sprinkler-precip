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
import math

MaxDist=10
Sprinkler = zeros( ((2*MaxDist+1),(2*MaxDist+1)) )
SprinklerPrecip=[0,1.4,1.2,1,1,1,.9,.9,.8,.4,0]

SprinklerSpace=12

def AddArray2D(Target,From,CornerX=0,CornerY=0):
	# Target currently must be >= From.Breadth +CornerY x From.Height+CornerX
	pass
	TgtX=Target.shape[0]
	TgtY=Target.shape[1]
	FromX=From.shape[0]
	FromY=From.shape[1]
	TMinX=int(CornerX)
	TMinY=int(CornerY)
	TMaxX=TgtX - (TMinX+FromX)
	TMaxY=TgtY - (TMinY+FromY)
	Target[TMinX:TMaxX,TMinY:TMaxY] += From


for x in range(0,(MaxDist+1)):
	for y in range(0,(MaxDist+1)):
		OUT=0
		r=(x**2 + y**2)**.5
		if r > MaxDist:
			OUT=0
		elif r == MaxDist:
			OUT=0
		else:
			low=math.floor(r)
			up=math.ceil(r)
			if int(low) == int(up):
				OUT=SprinklerPrecip[int(low)]
			else:
				OUT=(((r-low)/(up-low)) * (SprinklerPrecip[int(up)] - SprinklerPrecip[int(low)]) + SprinklerPrecip[int(low)])
		Sprinkler[(MaxDist-x,MaxDist-y)]=OUT
		Sprinkler[(MaxDist+x,MaxDist-y)]=OUT
		Sprinkler[(MaxDist+x,MaxDist+y)]=OUT
		Sprinkler[(MaxDist-x,MaxDist+y)]=OUT

#print Sprinkler


# If you append, be sure to specify an axis (0 or 1)
# An array appended to axis 0 goes below the starting array
# and it must have the same breadth as the first array
# This means a shape of (foo,array1.breadth)
# Similarly, axis 1 needs a shape of (array1.height,foo), 
# and will expand array1 by breadth foo.
# Example:
# append(Sprinkler,zeros( (MaxDist*2+1,MaxDist*2) ),axis=1)

CurrX = int(MaxDist + 1 - SprinklerSpace*(math.floor( (MaxDist+1)/SprinklerSpace) ))
SprinklerNum=int( math.ceil( (4 * MaxDist + 1 - CurrX)/SprinklerSpace ) )

SprinklerPos=zeros( (SprinklerNum,SprinklerNum,2), dtype=int )
# First Sprinkler position: Curr{X,Y}
# Assuming square layout
CurrY = CurrX
# Fill block of sprinkler positions
X=CurrX
for x in range(0,SprinklerNum):
	Y=CurrY
	for y in range(0,SprinklerNum):
		SprinklerPos[x,y,0]=X
		SprinklerPos[x,y,1]=Y
		Y=Y+SprinklerSpace
	X=X+SprinklerSpace



# Now to add the sprinkler maps up correctly...
AllSprinklers=zeros( (MaxDist * 4 + 1, MaxDist * 4 + 1)
for x in range(0,SprinklerNum):
	for y in range(0,SprinklerNum):
		
