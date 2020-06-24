# genetic-process-discovery

## generate multiple sequence:
Run: `python3 gen_data/generator.py <#traces> <#max_overlappings> <number_of_sequences> <output_file_name>`

## run code with input sequence:
Run: `python3 app.py <symbol_sequence_file_name>`

FYI: you do not have to care about file paths, the code taks care of it.


# Testing

1. Run `python3 algorithm_evaluation/generator.py` to create output files with symbol sequencess (edit of the file could be necessary) -> output_<#overlappingSources>.txt
2. Run `python3 algorithm_evaluation/analysis_<base|genetic>.py` to train models and generate gscore for each -> gscores.json
3. Run `python3 algorithm_evaluation/viz.py` to visualize the exported gscore metrics