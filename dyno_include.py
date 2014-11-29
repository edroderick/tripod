#!/usr/bin/env python

from ctypes import Structure,c_uint16,c_double,c_ubyte,c_uint32,c_int16


DYNO_REF_NAME 			=	'dyno-ref-chan'
LHR = 2
LHP = 3
LKP = 4
LAP = 5

CHR = 6
CHP = 7
CKP = 8
CAP = 9

RHR = 10
RHP = 11
RKP = 12
RAP = 13

class DYNO_REF(Structure):
    _pack_ = 1
    _fields_ = [("LHR",    c_double),
                ("LHP",    c_double),
                ("LKP",    c_double),
                ("LAP",    c_double),
                ("CHR",    c_double),
                ("CHP",    c_double),
                ("CKP",    c_double),
                ("CAP",    c_double),
                ("RHR",    c_double),
                ("RHP",    c_double),
                ("RKP",    c_double),
                ("RAP",    c_double) ]
                
