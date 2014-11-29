#!/usr/bin/env python

import numpy as np
import dyno_include as di
import ach
import curses
import time


d = ach.Channel(di.DYNO_REF_NAME)
dyno = di.DYNO_REF()
d.flush()

stdscr = curses.initscr()
dyno.LHR, dyno.LHP, dyno.LKP, dyno.LAP, dyno.CHR, dyno.CHP, dyno.CKP, dyno.CAP, dyno.RHR, dyno.RHP, dyno.RKP, dyno.RAP = 0,0,0,0,0,0,0,0,0,0,0,0


while True:

	[statuss, framesizes] = d.get(dyno, wait=True, last=True)
	stdscr.addstr(0, 0, "  LHR    LHP    LKP    LAP    CHR    CHP    CKP    CAP    RHR    RHP    RKP    RAP")
	stdscr.addstr(1, 0, "%1.3f  %1.3f  %1.3f  %1.3f  %1.3f  %1.3f  %1.3f  %1.3f  %1.3f  %1.3f  %1.3f  %1.3f" % (dyno.LHR, dyno.LHP, dyno.LKP, dyno.LAP, dyno.CHR, dyno.CHP, dyno.CKP, dyno.CAP, dyno.RHR, dyno.RHP, dyno.RKP, dyno.RAP))
	stdscr.refresh()
	time.sleep(1)
