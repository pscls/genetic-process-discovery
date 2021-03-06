# Genetic Correlation Discoveryfor Unlabeled Event Logs

This repository contains a genetic extension as well as an generation, visualization and algorithm-test scripts to the core approach of Diogo R. Ferreira and Daniel Gillblad which can be found [here](https://github.com/pscls/genetic-process-discovery/tree/master/src/base_files_original).


## Structure
1. `src` - contains all algorithm files
2. `algorithm_evaluation` - provides generation, visuzalisation and algorithm testing files
3. `data` - stores generated files and the Process Model Definition
4. `docs` - presentation slides, blog and paper

## 1. Generator
Will generator multiple files with the required input 
```python algorithm_evaluation/generator.py <number of sources per symbol sequence> <number of sequences per file> <number of files (1 to X)>```

e.g. `python algorithm_evaluation/generator.py 300 100 50`

## 2. Algorithm Execution
Both algorithm will produce a gscore.json which can then be passed to the visualization script.

### 2.1 Base Algorithm
`python algorithm_evaluation/analysis_base.py`

### 2.2 Genetic Algorithm
`python algorithm_evaluation/analysis_genetic.py`

## 3. G-score Visualization
Visualization of the g-score output file from one of the analysis files.
`python algorithm_evaluation/viz_gscore.py <file name>`

e.g. `python algorithm_evaluation/viz_gscore.py gscore.json`

## 4. [Optional] Fitness Function Visualization
Visualization of the fitness function result (the export needs to be activated first to produce the required file).
`python algorithm_evaluation/viz_wight_functions_gscores.py`
