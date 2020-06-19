# genetic-process-discovery

## generate sequence:

Run: `python3 base_files/mimgen.py <#traces> <#max_overlappings> <sequence_file> <output_file>`

## generate multiple sequence:

Run: `python3 generator.py <#traces> <#max_overlappings> <sequence_file> <output_file> <number_of_sequences>`

## run code with input sequence:

Run: `python3 app.py output.txt`

If you want a validation of your model you need to append the sequence model as the second parameter: `python3 app.py output.txt sequences.txt`
