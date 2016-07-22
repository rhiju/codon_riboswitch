#!/usr/bin/python

from sys import argv
from glob import glob
from os.path import exists
from os.path import dirname

alldirname = argv[1]

globfiles = glob( alldirname + '/*/sequences.txt' )

globfiles.sort()

files = ['sequences.txt','exposure_free.txt','exposure_closed.txt','aptamer_bpp.txt']

fid = {}
for file in files:    fid[ file ] = open( file, 'w' )

for globfile in globfiles:
    indir = dirname( globfile )
    for file in files:
        infile = indir + '/' + file
        assert( exists( infile ) )
        for line in open( infile ): fid[file].write( line )

for file in files:
    fid[ file ].close()
    print 'Created: ', file
