# Illumina QC Summary Automation
The python script were created to automate the extraction of QC parameters from Illumina Miseq and Nextseq platforms. 2 scripts are available in this project to facilitate this purpose.

Original script (v1) is available if the latest version does not work on your device.
v2 - Adds prompt for selection of QC paramters, revamped the code
v2.1 - Convert global variables to functions

# export.py
This script will be useful if your sequencing runs were stored in servers. Not necessary for actual script.
As the run-time of the actual script increases when accessing files over the server, the script will:
1) Locate folders with Illumina folder convention
2) Extract the necessary files
3) Export locally to selected location

## How to run
1) Execute the script export.py
2) Dialogue pop-up asks you to choose the **approximate location** of the sequencing runs
3) Script runs - will take awhile
4) Dialogue pop-up asks you to choose the **output location**.

Issue: If the script takes too long to run, change the 'glob_depth' variable. This controls how deep should the recursive 'glob.glob' function goes.

# summary_extraction.py v2
Main script for QC summary metrics extraction.
1) Locate folders with Illumina folder convention
2) For each runs, access the relevant files
3) Extract relevant run parameters

```
Prompt 1: Summary QC paramaters
'Cluster Count', 'Cluster Count Pf', 'Error Rate', 
'First Cycle Intensity', '% Aligned', '% >= Q30',
'Projected Yield G', 'Yield G'

Prompt 2: Lane QC (only lane 1)
'% >= Q30', '% Aligned', '% Occupied', '% Pf', 'Cluster Count', 
'Cluster Count Pf', 'Density', 'Density Pf', 'Error Rate', 
'Error Rate 100', 'Error Rate 35', 'Error Rate 50', 
'Error Rate 75', 'First Cycle Intensity', 'Phasing', 
'Phasing Offset', 'Phasing Slope', 'Prephasing', 
'Prephasing Offset', 'Prephasing Slope', 'Projected Yield G', 
'Reads', 'Reads Pf', 'Tile Count', 'Yield G'

Prompt 3: Index QC
'Mapped Reads Cv', 'Max Mapped Reads', 'Min Mapped Reads',
'Total Fraction Mapped Reads', 'Total Pf Reads', 'Total Reads'
```

4) Loop and concat
5) Export

## How to run
1) Execute the script summary_extraction.py
2) Dialogue pop-up asks you to choose the **approximate location** of the sequencing runs
3) 3 prompts will appear for selection of QC paramaters
4) Script runs - will take awhile. Logs will be printed on the console while the script is running
5) Database in .xlsx format is exported

# Bugs
The script has only been tested on Miseq and Nextseq 500 data. If you encounter any issues, do reach out and send me a sample of the offending data files.
