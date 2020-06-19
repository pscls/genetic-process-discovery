# genetic-process-discovery

## generate sequence: 

e.g. for generate 100 sources with at most 5 overlapping from the defined model in sequences.txt

Run: `python3 mimgen.py 100 5 sequences.txt output.txt`


## run code with input sequence:
Run: `python3 mimmest.py output.txt`

If you want a validation of your model you need to append the sequence model as the second parameter: `python3 app.py output.txt sequences.txt`