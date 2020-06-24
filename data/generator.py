# DISCLAIMER:
#
# This file contains code and is based one the mimgen.py from Diogo R. Ferreira and Daniel Gillblad
# Code Package URL: http://web.ist.utl.pt/diogo.ferreira/mimcode/
# Code File URL: http://web.ist.utl.pt/diogo.ferreira/mimcode/mimgen.py
#
#
#
# Multiple Instance Model (MIM)
# (Sequence generator)
#
# Copyright (c) 2009, Daniel Gillblad and Diogo Ferreira
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#     * Redistributions of source code must retain the above
#       copyright notice, this list of conditions and the following
#       disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials
#       provided with the distribution.
#     * All published materials that made use of of this software
#       during its preparation must acknowledge this software and
#       its copyright holders within the material.
#     * Neither the name of the copyright holder nor the names of
#       other contributors may be used to endorse or promote products
#       derived from this software without specific prior written
#       permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

# ======================================================================================================================

import sys
import random

if len(sys.argv) < 5:
    print('Missing overlap value.')
    print(
        'Usage: {0} <no.instances> <overlap> <input-file> <output-file>'.format(sys.argv[0]))
    print('  \'no.instances\' specifies the number of instances to be created')
    print('  \'overlap\' specifies the number of overlapping instances')
    print('  \'number_of_generations\' how many sequences should be generated from the passed model')
    print('  \'output-file-name\' is the output file where the symbol sequence will be written')
    exit()


fin = open("MODEL_DEFINTION.txt")

seqprobs = dict()

for line in fin:
    [z, p] = line.split()
    if len(z) > 0:
        seqprobs[z] = float(p)

fin.close()

def normalize(d):
    rowsum = 0.0
    for k in d.keys():
        rowsum = rowsum + d[k]
    if rowsum > 0.0:
        for k in d.keys():
            d[k] = d[k] / rowsum

normalize(seqprobs)

ninstances = int(sys.argv[1])
if ninstances < 1:
    ninstances = 1
    print('using default no. instances = {0}'.format(ninstances))

overlap = int(sys.argv[2])
if overlap < 1:
    overlap = 1
    print('using default overlap = {0}'.format(overlap))

outputs = []

fout = open("./data/generated_data/" + sys.argv[4], 'w')

number_of_generations = int(sys.argv[3])
while number_of_generations > 0:
    random.seed()

    sequences = dict()

    for k in range(0, ninstances):
        psum = 0.0
        p = random.random()
        for z in seqprobs.keys():
            psum += seqprobs[z]
            if p < psum:
                sequences[k+1] = z[:]
                break

    # generate symbol sequence

    symbolseq = []
    sourceseq = []

    upperbound = 0

    while len(sequences) > 0:
        sources = sequences.keys()
        selected = random.randint(
            0, min(overlap-1, len(sources)-1, upperbound))
        if selected >= upperbound:
            upperbound += 1
        sources = list(sources)
        source = sources[selected]
        symbol = sequences[source][0]
        symbolseq.append(symbol)
        sourceseq.append(source)
        if len(sequences[source]) <= 1:
            del sequences[source]
            upperbound -= 1
        else:
            sequences[source] = sequences[source][1:]

    fout.write(",".join(symbolseq))
    fout.write("\n")
    number_of_generations -= 1

fout.close()
