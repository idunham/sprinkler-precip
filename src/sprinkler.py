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



