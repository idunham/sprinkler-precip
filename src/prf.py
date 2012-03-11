#!/usr/bin/env python
##############################################################
# PRF (SPACE precipitation profile) reader.
# Provides functions to read a single entry (prfline),
# convert all entries from f.tell() to the end into a 2-d ndarray
# (readprf), and parse a given sprinkler's data from string to an
# array of usable values (NOT YET IMPLEMENTED: parsedata)
# NOTE: use f.seek(0) before reading more.
#
# Doing this as an object with methods and safety checking would 
# be much better. 
# Eventually I hope to implement write support as well.
# This will allow sharing data with SPACE.
#
# Calculations based on spacing and other readily accessed 
# information belong outside this library--alternate formats
# should be supported.
##############################################################
import numpy as np

def prfline(prf):
	'''prfline(filehandle prf)
	Return an array of strings corresponding to a record from a prf.
	Record fields (in order): 
	 (1-15):
	Facility, Date, Time, Sprinkler, Model, Nozzle, PSI, Riser, Flow, 
	 Spacing, Radius, Arc, Min/Revol, Set Screw, Rec #,

	 Duration, Comment
	 Data'''
	l	=prf.read(500)
	# Here I must apologize for the mess.
	# This assigns all values in one pass.
	larray	=[l[0:20],l[21:28],l[30:34],l[36:55],l[57:62],l[63:82],l[84:92],
			l[94:98],l[99:106],l[107:109],l[110:113],l[115:119],
			l[120:124],l[125:129],l[130:140],l[141:145],l[146:186],
			int(l[187:189]),int(l[190:193]),
			l[193:499]]
	return larray

def readprf(File):
	'''readprf(File) -> 2-d array of strings'''
	parr=np.zeros((20,0),dtype='|S305')
	try:
		line=prf.prfline(File)	#Initialize
		while line != "":
			parr=np.append(parr,numpy.array(line).reshape((1,20),0),0)
			line=prf.prfline(File)
	except:
		pass
	finally:
		return parr

def parsedata(Type,DataString,As):
	'''parsedata(Type,String,As)->1-d array of catchment readings
	There's a 305-byte string containing about 61 readings.
	This should return those readings.
	In order to make it meaningful, we need the format selector 
	(which should be 1-5, if I remember right).
	The format selectors tell whether we need to transform the data.
	'''
	# There are 61 fields; the first is 3 chars + \r
	# The rest are 4 chars + \r
	# We need to start at the right index (DataString[3], usually)
	# If \r is not found, error! The file isn't a valid PRF.	
	start=DataString.index('\r')
	DataList=np.zeros(61)
	DataList[0]=float(DataString[0:start])
	for i in range(60):
		DataList[i]=float(DataString[start+1+(5*i):start+5*(i+1)])
	
	return DataList

