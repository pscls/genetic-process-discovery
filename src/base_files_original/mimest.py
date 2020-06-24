# Multiple Instance Model (MIM)
# (Usage example)
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


import sys
import mim

# read symbol sequence x from stdin, with one symbol per line
x = []
for line in sys.stdin:
	symbol = line.strip()
	if len(symbol) > 0:
		x += [symbol]

# print the sequence as string
#print "Symbol sequence: ", mim.seq2str(x)

#print "({0} symbols)".format(len(x))

# create to be estimated from sequence x
m = mim.model(x)

# estimate model
K = m.estimate()

# print model
m.printmodel(m.M)

# show the probability distribution of the different sequences in the model
pz = mim.sortbyvalue(m.seqprobs())
# for z, p in pz:
# 	print '{0:.3f} : {1}'.format(p, z)	

# print 'Total number of sources: {0}'.format(K)	