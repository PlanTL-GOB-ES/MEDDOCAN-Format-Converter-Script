# MEDDOCAN: Format Converter Script

## Digital Object Identifier (DOI)


## Introduction
------------

This script is distributed as apart of the Medical Document Anonymization (MEDDOCAN) 
task. It is intended to be used via command line:

<pre>
$> python converter.py -i input_folder/ -o output_folder/
</pre>

It converts files between `MEDDOCAN-Brat`, `MEDDOCAN-XML`, and `i2b2` formats. The mapping 
between the different formats is defined in the files in the `mappings/` folders. See 
below for further information.

Input and target directories, as well as source and target formats can be chosen 
via command line.


## Prerequisites
-------------

This software requires to have Python 3 installed on your system.


## Directory structure
-------------------

<pre>
input/
This directory contains sample input  files with annotations in `MEDDOCAN-Brat`, 
`MEDDOCAN-XML`, and `i2b2` annotation formats.

mapping/
This folder contains the files defining the mapping between the different formats.
Files ending with `map_categories.csv` define the mapping of the categories defined 
in the i2b2 2014 Personal Health-care Information (PHI) task, and files ending with 
`map_types.csv` define the mapping of the sub-categories defined in the same task.
This files are loaded into dictionaries to map the categories/sub-categories. If you
wish to change the mapping, do not change the script, just change the mapping in these
files.

output/
This directory contains sample output files with annotations in `MEDDOCAN-Brat`, 
`MEDDOCAN-XML`, and `i2b2` annotation formats.
</pre> 


## Usage
-----


It is possible to configure the behavior of this software using the different options.


  - The `-i/--input_dir` and `-o/--output_dir` options allow to select the input and
output directories.

  - The `-s/--source` option allows to select the source format of the input files.

  - The `-t/--target` option allows to select the target format of the output files.
  
  - `verbose` and `quiet` options allow to control the verbosity level.


The user can select the different options using the command line:

<pre>
usage: converter.py [-h] [-i INPUT_DIR] [-o OUTPUT_DIR] [-s {brat,xml,i2b2}]
                    [-t {brat,xml,i2b2}] [-v | -q]

Script to convert between MEDDOCAN-BRAT/MEDDOCAN-XML/i2b2 formats.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input_dir INPUT_DIR
                        Folder with the original input files
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Folder to store the output converted files
  -s {brat,xml,i2b2}, --source {brat,xml,i2b2}
                        Format of source files
  -t {brat,xml,i2b2}, --target {brat,xml,i2b2}
                        Format of target files
  -v, --verbose         Increase output verbosity
  -q, --quiet           Do not print anything
</pre>


## Examples

Basic Examples:

Convert all files in `input/brat/sample/` from `MEDDOCAN-Brat` format (default source 
format) into `MEDDOCAN-XML` (default target format) and store output files in 
`output/xml/sample/`:

<pre>
$> python converter.py -i input/brat/sample/ -o output/xml/sample/
</pre>


Convert all files in `input/xml/sample/` from `MEDDOCAN-XML` format into `i2b2`
formatand store output files in `output/i2b2/sample/`:

<pre>
$> python converter.py -i input/xml/sample/ -o output/i2b2/sample/ -s xml -t i2b2
</pre>



## Contact
------

Aitor Gonzalez-Agirre (aitor.gonzalez@bsc.es)


## License
-------

Copyright (c) 2019 Secretaría de Estado para el Avance Digital (SEAD)

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
THE SOFTWARE.

