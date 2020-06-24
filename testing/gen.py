import os

for i in range (1, 51):
    os.system(f"python3 ../generator.py 300 {i} ../sequences.txt ./output_{i}.txt 100")