# Illumina QC Summary Automation
The python script were created to automate the extraction of QC parameters from Illumina Miseq and Nextseq platforms. 2 scripts are available in this project to facilitate this purpose.

# export.py
This script will be useful if your sequencing runs were stored in servers. As the run-time of the actual script increases when accessing files over the server, the script will:
1) Locate folders with Illumina folder convention
2) Extract the necessary files
3) Export locally to selected location

## How to run
1) Execute the script export.py
2) Dialogue pop-up asks you to choose the **approximate location** of the sequencing runs
3) Script runs - will take awhile
4) Dialogue pop-up asks you to choose the **output location**.

Issue: If the script takes too long to run, change the 'glob_depth' variable. This controls how deep should the recursive 'glob.glob' function goes.

# summary_extraction
