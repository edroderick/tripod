#!/usr/bin/env python

import controller_include as ci
import ach
import sys
import time
import numpy as np
from ctypes import *

import curses
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)
stdscr.nodelay(1)

stdscr.addstr(0, 2,  "Hit 'q' to quit")
stdscr.addstr(1, 5,  "Use 'Arrow Keys' to move & 'Space Bar' to stop the robot!")
stdscr.addstr(3, 10, "   Forward")
stdscr.addstr(4, 10, "   Reverse")
stdscr.addstr(5, 10, "   Right")
stdscr.addstr(6, 10, "   Left")
stdscr.refresh()

c = ach.Channel(ci.CONTROLLER_REF_NAME)
controller = ci.KEY_REF()
c.flush()

controller.direction = ci.STOP
c.put(controller)


oldKey = ''
key    = ''
while key != ord('q'):
	key = stdscr.getch()
	
	if (key != oldKey):		
		if (key == curses.KEY_UP) | (key == ord('w')):
			stdscr.addstr(3, 10, ">> Forward")
			stdscr.addstr(4, 10, "   Reverse")
			stdscr.addstr(5, 10, "   Right")
			stdscr.addstr(6, 10, "   Left")
			controller.direction = ci.FORWARD
			c.put(controller)
			
		elif (key == curses.KEY_DOWN) | (key == ord('s')):
			stdscr.addstr(3, 10, "   Forward")
			stdscr.addstr(4, 10, ">> Reverse")
			stdscr.addstr(5, 10, "   Right")
			stdscr.addstr(6, 10, "   Left")
			controller.direction = ci.REVERSE
			c.put(controller)
			
		elif (key == curses.KEY_RIGHT) | (key == ord('d')): 
			stdscr.addstr(3, 10, "   Forward")
			stdscr.addstr(4, 10, "   Reverse")
			stdscr.addstr(5, 10, ">> Right")
			stdscr.addstr(6, 10, "   Left")
			controller.direction = ci.RIGHT
			c.put(controller)
		
		elif (key == curses.KEY_LEFT) | (key == ord('a')):
			stdscr.addstr(3, 10, "   Forward")
			stdscr.addstr(4, 10, "   Reverse")
			stdscr.addstr(5, 10, "   Right")
			stdscr.addstr(6, 10, ">> Left")
			controller.direction = ci.LEFT
			c.put(controller)
			
		elif (key == ord(' ')):	
			controller.direction = ci.STOP
			stdscr.addstr(3, 10, "   Forward")
			stdscr.addstr(4, 10, "   Reverse")
			stdscr.addstr(5, 10, "   Right")
			stdscr.addstr(6, 10, "   Left")
			c.put(controller)
		
	oldKey = key
	time.sleep(0.1)
	stdscr.refresh()

# Close the connection to the channels
c.close()


curses.endwin()
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
sys.exit("\n\nDone!\n")
