#!/usr/bin/python

from string import *
from os import system
from copy import deepcopy
from random import randint
from os.path import exists

EXE_DIR = '/Users/rhiju/src/nupack3.0/bin/'
if not( exists(EXE_DIR) ): EXE_DIR = '/home/rhiju/src/nupack3.0/bin/'
assert( exists( EXE_DIR ) )

def get_base_pair_exposure( sequence ):

    (bpp, bpp_total ) = get_base_pair_probability( sequence )
    return bpp_total

def get_base_pair_probability( sequence ):
    v = []
    seqlength = 0
    pair_lines = run_nupack( sequence )

    bpp = []
    for line in pair_lines:
        if len( line )< 1: continue
        if line[0] == '%': continue
        cols = line.split()

        if len( cols ) == 1:
            seqlength = int( cols[0] )
            bpp_total = []
            bpp = []
            for i in range( seqlength ): bpp_total.append( 0.0 )
            for i in range( seqlength ): bpp.append( deepcopy(bpp_total) )

        if len( cols ) == 3:
            if int(cols[1]) ==  seqlength + 1:
                bpp_total[ int(cols[0])-1 ] = float( cols[2] )
            else:
                bpp[ int(cols[0])-1 ][ int(cols[1])-1 ] = float( cols[2] )
                bpp[ int(cols[1])-1 ][ int(cols[0])-1 ] = float( cols[2] )

    return (bpp, bpp_total)


def run_nupack( sequence ):
    tag = "%d" % randint( 0, 6553612312 )
    system( "echo %s > %s.in" % (sequence, tag) )
    system( "time " + EXE_DIR+"pairs -T 37 -material rna -cutoff 1e-12 %s" % tag )
    lines = open( tag+'.ppairs' ).readlines()
    system( "rm -rf %s.*" % tag )
    return lines


def base_pair_exposure_string( v ):
    s = ''
    for n in range( len( v ) ):
        d = int( v[n] * 10 )
        if (d > 9 ): d = 9
        s += '%d' % d
    if len( s) != len( v ): exit()
    return s
