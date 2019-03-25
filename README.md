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

    Copyright 2019 Secretaría de Estado para el Avance Digital (SEAD)

Licensed under the Apache License, Version 2.0 (the "License"); you may 
not use this file except in compliance with the License. You may obtain a 
copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

