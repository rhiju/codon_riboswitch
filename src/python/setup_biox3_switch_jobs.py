#!/usr/bin/python

from os import system, getcwd
from sys import argv
from os.path import exists, abspath

rundir = argv[1]

num_jobs = 50
if len( argv ) > 2:    num_jobs = int( argv[2] )

num_sequences = 100
if len( argv ) > 3:    num_sequences = int( argv[3] )

if not exists( 'qsub_files' ): system( 'mkdir qsub_files' )

EXE = '/scratch/users/rhiju/projects/anticodon_riboswitch/src/python/test_switches.py'
assert( exists( EXE ) )
EXE = abspath( EXE )
print EXE

job_file = 'qsubMINI'
fid_overall = open( job_file, 'w' )
for n in range( num_jobs ):
    fid = open( 'qsub_files/qsub%d.sh' % n ,'w' )

    fid.write( '#!/bin/bash\n' )
    fid.write( '#PBS -N test_switches_%d\n' % n )
    fid.write( '#PBS -o /dev/null\n' )
    fid.write( '#PBS -e /dev/null\n' )
    fid.write( '#PBS -l walltime=16:00:00\n' )
    fid.write( '\n' )
    pwd = getcwd()
    fid.write( 'cd %s\n' % pwd )
    fid.write( '\n' )
    fid.write( '%s %s/%d/ %d  > /dev/null 2> /dev/null \n' % (EXE,rundir,n,num_sequences) )

    fid_overall.write( 'qsub qsub_files/qsub%d.sh\n' % n )
fid_overall.close()

print 'Run jobs by typing:'
print ' source ',job_file

