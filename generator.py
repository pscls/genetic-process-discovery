import sys
import base_files.mim as mim
import random

if len(sys.argv) < 6:
    print('Missing overlap value.')
    print(
        'Usage: {0} <no.instances> <overlap> <input-file> <output-file>'.format(sys.argv[0]))
    print('  \'no.instances\' specifies the number of instances to be created')
    print('  \'overlap\' specifies the number of overlapping instances')
    print('  \'input-file\' is the input file containing the sequences and their weigths')
    print('  \'output-file\' is the output file where the symbol sequence will be written')
    print('  \'number_of_generations\' how many sequences should be generated from the passed model')
    exit()


number_of_generations = int(sys.argv[5])

# read one sequence per line, together with a probability value

fin = open(sys.argv[3], 'r')

seqprobs = dict()

for line in fin:
    [z, p] = line.split()
    if len(z) > 0:
        seqprobs[z] = float(p)

fin.close()

mim.normalize(seqprobs)

# select instances to be used

ninstances = int(sys.argv[1])
if ninstances < 1:
    ninstances = 1
    print('using default no. instances = {0}'.format(ninstances))

overlap = int(sys.argv[2])
if overlap < 1:
    overlap = 1
    print('using default overlap = {0}'.format(overlap))

outputs = []

fout = open(sys.argv[4], 'w')

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

    # print(sequences)

    # printseqs()

    # write symbol sequence to output file


fout.close()

# main routine ends here
