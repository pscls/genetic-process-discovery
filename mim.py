# Multiple Instance Model (MIM)
# (Main package)
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


from operator import itemgetter
import math
import pprint
pp = pprint.PrettyPrinter(indent=4)


# general routine for normalizing probability distributions


def normalize(d):
    rowsum = 0.0
    for k in d.keys():
        rowsum = rowsum + d[k]
    if rowsum > 0.0:
        for k in d.keys():
            d[k] = d[k] / rowsum


# general routine for converting a sequence to string
def seq2str(seq):
    string = ''
    for elem in seq:
        string += str(elem)
    return string


# general routine for sorting a dictionary by values
def sortbyvalue(d):
    result = []
    for d_instance in d:
        result.append(sorted(d_instance.items(),
                             key=itemgetter(1), reverse=True))
    return result


# routine for computing the G-metric between two MIM models
def gmetric(m1, m2):
    pz = m1.seqprobs()
    qz = m2.seqprobs()
    g = 0.0
    for z in pz.keys():
        if z in qz:
            g += math.sqrt(pz[z]*qz[z])
    return g


class model_manager:
    inactive_models = []  # array of all models that are successfully estimated
    active_models = []  # number of all currently used models
    intital_models = 5  # number of initially created models

    def __init__(self, x):
        for i in range(self.intital_models):
            # TODO: Initaialize the matrices differently
            new_model = model(x)
            self.active_models.append(new_model)

    def estimate(self):
        results = []

        while len(self.active_models) > 0:
            # Do one iteration for all models
            for model in self.active_models:
                results.append(model.estimate())

            # abortion critera for estimation loop
            for model in self.active_models:
                if model.s in model.prevsseqs:
                    self.active_models.remove(model)
                    self.inactive_models.append(model)

        return results

    def seqprobs(self):
        results = []
        for model in self.inactive_models:
            results.append(model.seqprobs())
        return results


class model:

    BEGIN = 'o'

    END = 'x'

    x = []  # the symbol sequence

    N = 0  # the length of x

    D = []  # the set of symbols in x

    gM = dict()  # the global model used to initialize M (M^{+} in the paper)

    M = dict()  # the transition matrix M

    s = []  # the source sequence s (to be determined)

    y = dict()  # the separate source sequences (y^{(k)} in the paper)

    its = 0  # number of executed estimation loops

    prevsseqs = []  # all sequences of the last estimation

    # class constructor initializes the global model gM
    def __init__(self, x):
        self.x = x
        self.N = len(self.x)
        self.D = [self.BEGIN] + sorted(set(self.x)) + [self.END]
        self.initial_estimation()

    # initially estimate gM and s
    def initial_estimation(self):
        for a in self.D:
            self.gM[a] = dict()
            for b in self.D:
                self.gM[a][b] = 0.0
        for n in range(0, self.N-1):
            a = self.x[n]
            b = self.x[n+1]
            self.gM[a][b] += 1.0
        for a in self.D:
            normalize(self.gM[a])

        self.estsources(self.gM)

    # print given transition matrix T

    def printmodel(self, T):
        for a in self.D:
            print(a.ljust(5))
        print("")
        for a in self.D:
            print(a.ljust(5),)
            for b in self.D:
                if T[a][b] == 0.0:
                    print('-'.ljust(5))
                else:
                    print('{0:.2f}'.format(T[a][b]).ljust(5))

    # estimate the source sequence s from a given transition matrix T (algorithm 1 in the paper)

    def estsources(self, T):
        self.s = []
        self.y = dict()
        active = set()
        for n in range(0, self.N):
            xn = self.x[n]
            pmax = 0.0
            sn = -1
            for k in active:
                if xn in self.y[k]:
                    continue
                a = self.y[k][-1]
                b = xn
                p = T[a][b]
                if p > pmax:
                    sn = k
                    pmax = p
            if sn == -1 or T[self.BEGIN][xn] > pmax:
                sn = len(self.y) + 1
                active.add(sn)
                self.y[sn] = []
            self.s.append(sn)
            self.y[sn].append(xn)
            pnext = 0.0
            bnext = self.BEGIN
            for b in self.D:
                if T[xn][b] > pnext:
                    pnext = T[xn][b]
                    bnext = b
            if bnext == self.END:
                active.remove(sn)

    # update the transition matrix M based on the current separate source sequences y
    def estparams(self):
        self.M = dict()
        for a in self.D:
            self.M[a] = dict()
            for b in self.D:
                self.M[a][b] = 0.0
        for k in self.y.keys():
            a = self.BEGIN
            b = self.y[k][0]
            self.M[a][b] += 1.0
            for r in range(0, len(self.y[k])-1):
                a = self.y[k][r]
                b = self.y[k][r+1]
                self.M[a][b] += 1.0
            a = self.y[k][-1]
            b = self.END
            self.M[a][b] += 1.0
        for a in self.D:
            normalize(self.M[a])

    # expectation-maximization procedure to estimate s and M iteratively (algorithm 2 in the paper)
    def estimate(self):
        print('Initializing source sequence...')
        # start with an estimate of s computed from the global model gM

        # CHANGE: abort iteration when probabilities do not change anymore
        # while self.s not in prevsseqs:
        self.its += 1
        print('#{0}: Estimating parameters...'.format(self.its))
        self.estparams()  # update transition matrix M
        self.prevsseqs.append(self.s[:])
        print('#{0}: Computing source sequence...'.format(self.its))
        self.estsources(self.M)  # use current M to re-estimate s
        # pp.pprint(self.M)
        return len(set(self.s))

    # computes the probability distribution for the different sequences produced by this model (p(z) or q(z) in the paper)
    def seqprobs(self):
        probs = dict()
        for k in self.y.keys():
            z = seq2str(self.y[k])
            if z in probs:
                probs[z] += 1.0
            else:
                probs[z] = 1.0
        normalize(probs)
        return probs

    # checks that it is possible to recover the symbol sequence x from the separate sequences y (sanity check)
    def checkmodel(self):
        x2 = []
        pos = dict()
        for k in self.y:
            pos[k] = -1
        for n in range(len(self.s)):
            sn = self.s[n]
            pos[sn] += 1
            xn = self.y[sn][pos[sn]]
            x2.append(xn)
        return x2 == self.x
