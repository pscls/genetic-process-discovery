import os
import sys

assert len(sys.argv) == 4
sources = sys.argv[1]
sequences = sys.argv[2]
num_of_files = sys.argv[3]

for i in range (1, num_of_files+1):
    print(f"Generate file with overlapping: {i}/{num_of_files}")
    os.system(f"python3 ./data/generator.py {sources} {i} {sequences} output_{i}.txt")