#!/usr/bin/env python
##############################################################
# PRF (SPACE precipitation profile) reader.
# 
#
#
#
##############################################################

def prfline(prf):
	'''prfline(filehandle prf)
	Return an array of strings corresponding to a record from a prf.
	Record fields (in order): 
	 (1-15):
	Facility, Date, Time, Sprinkler, Model, Nozzle, PSI, Riser, Flow, 
	 Spacing, Radius, Arc, Min/Revol, Set Screw, Rec #,

	 Duration, Comment'''
	l	=prf.read(500)
	# Here I must apologize for the mess.
	# This assigns all values in one pass, and does so in an ugly way
	larray	=[l[0:20],l[21:28],l[30:34],l[36:55],l[57:62],l[63:82],l[84:92],
			l[94:98],l[99:106],l[107:109],l[110:113],l[115:119],
			l[120:124],l[125:129],l[130:140],l[141:145],l[146:186],
			int(l[187:189]),int(l[190:193]),
			l[194:499]]
	return larray
