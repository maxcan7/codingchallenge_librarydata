# codingchallenge_librarydata
This coding challenge uses Brooklyn library data (not provided).

The purpose of this pipeline is to read a json file into python, do some cleaning, transform it into a specific format, and output it to a csv file.

I have a windows PC and git bash has been finicky for unix terminal operations for me so I chose to write this pipeline almost exclusively in python, run through Spyder / Ipython. With more time, I would like to test this dataset in an Ubuntu virtualmachine and run it through a unix terminal.

Additionally, with more time I would like to write a test suite for unit testing.

## Requirements
This pipeline requires python3 

**The following python packages are required for librarydata_preprocess.py**:  
configparser  
json
csv
time

## Config
You will need to create a .ini file as a config with the following sections:

**[config]**
header=comma-separated list of the variables (column names)
datapath=path for the json input file
subset=if the json file has a key embedding all of the data, this is to subset the values of that key out
outputpath=path for the csv output file
rowkey=if the individual rows have a key embedding the data, this is to subset the values of that key out
rename_from=names of variables to be renamed from json to csv, comma-separated
rename_to=the new variable names in the same order as above, comma-separated
split_from=variables that need to be split e.g. splitting begin and end times, comma-separated
split_to=the new variables from the split, comma-separated within split variables and semicolon-separated between split variables e.g. monday, tuesday in split_from might look like monday_start, monday_end; tuesday_start, tuesday_end
splitter=the separator e.g. blank, - , (an actual comma) , ; , etc.

**configpath.py**  
A python script that only contains a string with the path for the .ini file. My .ini file is in the main directory but it should be flexible.

example:  
'your preferred python shebang'  
configpath = "path/configname.ini"  

## Preprocess (librarydata_preprocess.py)
This python pipeline loads a configuration file, loads a json input file, creates a writer to a csv output file, and cleans and transforms the data.

Within the library_clean function, variables are renamed, split, removed, a processing date stamp is added, and the transformed data are written to a csv.