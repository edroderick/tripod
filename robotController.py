import os
import dynamixel
import time
import random
import sys
import subprocess
import optparse
import yaml
import numpy as np
import ach
import math as m


import controller_include as ci
import dyno_include as di



UL = 5.0
LL = 5.0

def zero():
	dyno.LHP = 0
	dyno.LKP = 0
	dyno.LAP = 0
	dyno.CHP = 0
	dyno.CKP = 0
	dyno.CAP = 0
	dyno.RHP = 0
	dyno.RKP = 0
	dyno.RAP = 0
	d.put(dyno)

def dH(H):
	thetah = -m.acos((H/2.0)/UL)
	thetak = m.pi - 2.0*(m.pi/2.0 - thetah)
	thetaa = 0 + thetah - thetak
	
	A = [thetah , thetak , thetaa]
	
	return A

def rotHip(thetah, thetak, dT):
	thetah = thetah - dT
	thetaa = 0 + thetah - thetak
	
	A = [thetah , thetak , thetaa]
	
	return A

def lean(legs, direction):
	for i in range(1,9):	
		if legs == 'center':
			dyno.CKP = dyno.CKP + direction*1.0/10.0
		if legs == 'outer':
			dyno.LKP = dyno.LKP + direction*1.0/10.0
			dyno.RKP = dyno.RKP + direction*1.0/10.0
	
		d.put(dyno)
		time.sleep(.075)	

def squatAll():
	dyno.CHP = squat[0]
	dyno.CKP = squat[1]
	dyno.CAP = squat[2]
	dyno.RHP = squat[0]
	dyno.RKP = squat[1]
	dyno.RAP = squat[2]
	dyno.LHP = squat[0]
	dyno.LKP = squat[1]
	dyno.LAP = squat[2]
	d.put(dyno)

def stepForward():	
	#RAISE INNER LEG
	B = dH(7)

	dyno.CHP = B[0]
	dyno.CKP = B[1]
	dyno.CAP = B[2]
	d.put(dyno)
	time.sleep(1)

	#STEP LEG FORWARD
	C = rotHip(dyno.CHP, dyno.CKP, .5)
	dyno.CHP = C[0]
	dyno.CAP = C[2]
	d.put(dyno)
	time.sleep(1)
	
	#PUT ALL FEET DOWN
	A = dH(6)

	dyno.RHP = A[0]
	dyno.RKP = A[1]
	dyno.RAP = A[2]

	dyno.LHP = A[0]
	dyno.LKP = A[1]
	dyno.LAP = A[2]
	d.put(dyno)
	time.sleep(1)
	
	#SHIFT COG FORWARD
	lean('center',1)
	time.sleep(1)

	
	#STAND ON CENTER LEG
	dyno.CHP = squat[0]
	dyno.CKP = squat[1]
	dyno.CAP = squat[2]
	d.put(dyno)
	#stime.sleep(1)

	#STEP LEGS FORWARD
	C = rotHip(dyno.RHP, dyno.RKP, .5)
	#Stime.sleep(1)

	dyno.RHP = C[0]
	dyno.RAP = C[2]
	dyno.LHP = C[0]
	dyno.LAP = C[2]
	d.put(dyno)
	#time.sleep(1)

	#BOTH FEET DOWN
	A = dH(5)

	dyno.CHP = A[0]
	dyno.CKP = A[1]
	dyno.CAP = A[2]
	d.put(dyno)
	time.sleep(1)

	lean('outer',1.0)

	dyno.LHP = squat[0]
	dyno.LKP = squat[1]
	dyno.LAP = squat[2]
	dyno.RHP = squat[0]
	dyno.RKP = squat[1]
	dyno.RAP = squat[2]
	d.put(dyno)
	time.sleep(.5)

	dyno.CHP = squat[0]
	dyno.CKP = squat[1]
	dyno.CAP = squat[2]

	d.put(dyno)
	time.sleep(1)
	
def turn(direction):
	#RAISE INNER LEG
	B = dH(7)
	
	dyno.CHP = B[0]
	dyno.CKP = B[1]
	dyno.CAP = B[2]
	d.put(dyno)
	time.sleep(.5)
	
	dyno.CHR = direction*.5
	d.put(dyno)
	time.sleep(.5)

	dyno.CHP = squat[0]
	dyno.CKP = squat[1]
	dyno.CAP = squat[2]
	dyno.RHP = B[0]
	dyno.RKP = B[1]
	dyno.RAP = B[2]

	dyno.LHP = B[0]
	dyno.LKP = B[1]
	dyno.LAP = B[2]
	d.put(dyno)
	time.sleep(.5)

	dyno.CHR = 0
	d.put(dyno)
	time.sleep(.5)
	squatAll()

def stepBack():
	B = dH(7)

	dyno.CHP = B[0]
	dyno.CKP = B[1]
	dyno.CAP = B[2]
	d.put(dyno)
	time.sleep(.5)

	#STEP LEG BACK
	C = rotHip(dyno.CHP, dyno.CKP, -.75)
	dyno.CHP = C[0]
	dyno.CAP = C[2]
	d.put(dyno)
	time.sleep(.5)
	dyno.CKP = dyno.CKP + .5
	dyno.CAP = dyno.CAP - .5
	#dyno.LHP = C[0]
	d.put(dyno)
	time.sleep(.5)
	
	
	print 'start'
	dT = .05
	for i in range(1, 7):
		dyno.RKP = dyno.RKP - dT
		dyno.LKP = dyno.LKP - dT
		dyno.RHP = dyno.RHP - dT/2
		dyno.LHP = dyno.LHP - dT/2
		dyno.LAP = dyno.LAP - dT/2
		dyno.RAP = dyno.RAP - dT/2
		dyno.CAP = dyno.CAP - dT/2
		d.put(dyno)
		time.sleep(.085)
		
	time.sleep(.5)
	
	print 'step2'
	dT = .25
	dyno.CKP = dyno.CKP - 3*dT
	dyno.LKP = dyno.LKP - 2*dT
	dyno.RKP = dyno.RKP - 2*dT
	d.put(dyno)
	time.sleep(.5)
	
	print 'stand up'
	for i in range (1,10):
		dyno.CHP = dyno.CHP + .5/10.0
		dyno.CKP = dyno.CKP + 1.0/10.0
		dyno.CAP = dyno.CAP - .5/10.0
		d.put(dyno)
		time.sleep(.05)
	
	dyno.CHP = squat[0]
	dyno.CKP = squat[1]
	dyno.CAP = squat[2]
	C = rotHip(dyno.RHP, dyno.RKP, -.75)
	
	dyno.RHP = C[0]
	dyno.RAP = C[2]
	dyno.LHP = C[0]
	dyno.LAP = C[2]
	d.put(dyno)
	time.sleep(.5)
	
	dyno.LKP = dyno.LKP + .75
	dyno.RKP = dyno.RKP + .75
	dyno.LAP = dyno.LHP - dyno.LKP
	dyno.RAP = dyno.RHP - dyno.RKP
	d.put(dyno)
	time.sleep(.5)
	
	dT = .05
	for i in range(1,7):
		dyno.CKP = dyno.CKP - 1.5*dT
		dyno.LKP = dyno.LKP - 3*dT
		dyno.RKP = dyno.RKP - 3*dT
		dyno.CAP = dyno.CAP - 1.5*dT
		d.put(dyno)
		time.sleep(.1)
	time.sleep(.5)
	
	dyno.CHP = dyno.CHP - .2
	dyno.CKP = dyno.CKP - 1.2
	dyno.CAP = dyno.CAP + 1.5
	d.put(dyno)
	time.sleep(.5)
	
	squatAll()



c = ach.Channel(ci.CONTROLLER_REF_NAME)
controller 	= ci.KEY_REF()
c.flush()

d = ach.Channel(di.DYNO_REF_NAME)
dyno 		= di.DYNO_REF()
d.flush()

squat = dH(9)

dyno.LHP = -.1
dyno.LKP = -.2
dyno.LAP = .1

dyno.CHP = -.1
dyno.CKP = -.2
dyno.CAP = .1

dyno.RHP = -.1
dyno.RKP = -.2
dyno.RAP = .1

d.put(dyno)
time.sleep(2)


while(1):
	
	[statuss, framesizes] = c.get(controller, wait=True, last=True)
	
	if (controller.direction == ci.FORWARD):
		print '\nMoving Fowrad ...'
		stepForward()		
			
	elif (controller.direction == ci.REVERSE):
		print '\nMoving Backward ...'
		stepBack()

	elif (controller.direction == ci.RIGHT):
		print '\nTurning Right ...'
		turn(1)

	elif (controller.direction == ci.LEFT):
		print '\nTurning Left ...'
		turn(-1)

	elif (controller.direction == ci.STOP):
		print '\nStopped'
		zero()
	
