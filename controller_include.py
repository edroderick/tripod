#!/usr/bin/env python

from ctypes import Structure,c_uint16,c_double,c_ubyte,c_uint32,c_int16


CONTROLLER_REF_NAME    =	'controller-ref-chan'
STOP 	= 0
FORWARD = 1
REVERSE = 2
RIGHT 	= 3
LEFT 	= 4

class KEY_REF(Structure):
    _pack_ = 1
    _fields_ = [("direction",   c_int16) ]
