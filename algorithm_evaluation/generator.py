import os
num_of_files = 50
for i in range (1, num_of_files+1):
    print(f"Generate file with overlapping: {i}/{num_of_files}")
    os.system(f"python3 ./data/generator.py 30 {i} 1000 output_{i}.txt")