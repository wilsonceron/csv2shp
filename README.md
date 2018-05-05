# csv2shp
A simple tool to conver csv files to shape files

This is a simple python command-line script.
YOU NEED PYTHON3 TO RUN IT!

usage: csv2shp.py [-h] -i INPUT -o OUTPUT -t {points,lines}

Basic Usage

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        CSV input File
                        First line: Header
                        Second line: Data type{integer, real or String}
                        others lines: Your data: 
                        Example:
                        	x,y,type,id
                        	real,real,string,integer
                        	-23.163353,-45.794501,'Rain gauge',9320 
  -o OUTPUT, --output OUTPUT
                        Output file name
  -t {points,lines}, --type {points,lines}
                        Shape type: points or lines

