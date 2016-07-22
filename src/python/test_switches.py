#!/usr/bin/python

from nupack_wrappers import base_pair_exposure_string, get_base_pair_probability
from copy import deepcopy
from os.path import exists
from os import system
from sys import argv
import random

outdir = './'
if len( argv ) > 1:
    outdir = argv[1]
if not exists( outdir ): system( 'mkdir -p '+outdir )
num_sequences = 10
if len( argv ) > 2:
    num_sequences = int( argv[2] )

N = 100

aptamer_sequence = 'CGAGGACCGGUACGGCCGCCACUCG'
secstruct_mut    = '((((...(((.....)))...))))'
nt_mut           = '..........NNN.N..........'
closed_sequence  = '...CGCCCGCGAGUAGCGGGCG...'

sequence_file = outdir+'/sequences.txt'
fid_sequences = open( sequence_file, 'w' )
exposure_free_file = outdir+'/exposure_free.txt'
fid_free      = open( exposure_free_file, 'w' )
exposure_closed_file = outdir+'/exposure_closed.txt'
fid_closed    = open( exposure_closed_file, 'w' )
aptamer_bpp_file = outdir+'/aptamer_bpp.txt'
fid_aptamer_bpp  = open( aptamer_bpp_file, 'w' )

RNA_char = 'ACGU'
rna_WC = ['AU','UA','GC','CG']
#rna_WC = ['AU','UA','GC','CG','GU','UG']
def get_random_sequence( N ):
    sequence = ''
    for n in range( N ): sequence += random.choice( RNA_char )
    return sequence

def parse_pairs( secstruct ):
    pairs = []
    right_parens = []
    for i in range( len( secstruct ) ):
        if secstruct[ i ] == '(':
            right_parens.append(i)
        elif secstruct[ i ] == ')':
            pairs.append( (right_parens[-1],i) )
            del( right_parens[-1] )
    return pairs

def mutate_secstruct( sequence, secstruct ):
    pairs = parse_pairs( secstruct )
    sequence_out = deepcopy( sequence )
    for pair in pairs:
        WC = random.choice( rna_WC )
        sequence_out = sequence_out[:pair[0]] + WC[0] + sequence_out[(pair[0]+1):pair[1] ] + WC[1] + sequence_out[ (pair[1]+1):]
    return sequence_out

def mutate_nt( sequence, nt_mut):
    sequence_out = deepcopy( sequence )
    for i in range( len( nt_mut ) ):
        if nt_mut[i] == 'N':
            sequence_out = sequence_out[:i] + random.choice( RNA_char ) + sequence_out[ (i+1):]
    return sequence_out

aptamer_bp_idx = ( N + 2, N + len( aptamer_sequence ) - 3 )

for i in range( num_sequences ):
    print 'Doing sequence number: %d of %d' % ( i+1 , num_sequences )
    rand_sequence1 = get_random_sequence( N )
    rand_sequence2 = get_random_sequence( N )

    aptamer_sequence_mutated = mutate_secstruct( aptamer_sequence, secstruct_mut )
    aptamer_sequence_mutated = mutate_nt( aptamer_sequence_mutated, nt_mut)


    sequence_free   = rand_sequence1 + aptamer_sequence_mutated + rand_sequence2
    ( bpp_free, exposure_free )  = get_base_pair_probability( sequence_free )
    aptamer_bpp_free = bpp_free[ aptamer_bp_idx[0] ][ aptamer_bp_idx[1] ]

    closed_sequence_mutated = ''
    for m in range( len( aptamer_sequence_mutated ) ):
        if closed_sequence[m] == '.':
            closed_sequence_mutated += aptamer_sequence_mutated[m]
        else:
            closed_sequence_mutated += closed_sequence[m]

    #print aptamer_sequence_mutated
    #print closed_sequence_mutated

    sequence_closed = rand_sequence1 + closed_sequence_mutated + rand_sequence2
    ( bpp_closed, exposure_closed ) = get_base_pair_probability( sequence_closed )
    aptamer_bpp_closed = bpp_closed[ aptamer_bp_idx[0] ][ aptamer_bp_idx[1] ]

    fid_sequences.write( sequence_free + '\n' )

    for m in exposure_free: fid_free.write( ' %f' % m )
    fid_free.write('\n')

    for m in exposure_closed: fid_closed.write( ' %f' % m )
    fid_closed.write('\n')

    fid_aptamer_bpp.write( '%f %f\n' % (aptamer_bpp_free, aptamer_bpp_closed ) )
    if False:
        fid = open( 'bpp.txt', 'w' )
        for i in range( len( bpp_free ) ):
            for j in range( len( bpp_free[i] ) ): fid.write( ' %f' % bpp_free[i][j] )
            fid.write( '\n' )
        fid.close()

fid_sequences.close()
fid_free.close()
fid_closed.close()
fid_aptamer_bpp.close()

print 'Created: ', sequence_file
print 'Created: ', exposure_free_file
print 'Created: ', exposure_closed_file
print 'Created: ', aptamer_bpp_file
