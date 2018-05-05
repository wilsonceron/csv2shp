#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* 

											"csv2shp.py"
											************

		Developed by: Wilson  Seron		e-mail: wilsonseron@gmail.com 		Date: 01/04/18
	
	

-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* 
'''
import sys, os, getopt
import csv
import unicodedata
import argparse
from osgeo import ogr
from argparse import RawTextHelpFormatter


def	readOptions():

	status = False

	parser = argparse.ArgumentParser(description = "Basic Usage",formatter_class=RawTextHelpFormatter)
	parser.add_argument("-i", "--input", help = "CSV input File\nFirst line: Header\nSecond line: Data type{integer, real or String}\nothers lines: Your data: \nExample:\n\tx,y,type,id\n\treal,real,string,integer\n\t-23.163353,-45.794501,'Rain gauge',9320 ", required = True, default = "")
	parser.add_argument("-o", "--output", help = "Output file name", required = True, default = "")
	parser.add_argument("-t", "--type", type=str, choices=["points", "lines"],  help = "Shape type: points or lines", required = True, default = "")

	argument = parser.parse_args()

	if argument.input and argument.output and argument.type:
		status = True

	if not status:
		print("Maybe you want to use -h for help")
		status = False 
		
	return {"success":status, "input":argument.input, "output":argument.output, "type":argument.type }


def	createLines(data,outputFileName,shapeType):
	path = os.getcwd()

	header		=	data.pop(0)
	dataType	=	data.pop(0)
	csvFile		=	path+"/"+outputFileName+"_lines.csv"

	if len(data[0]) < 3:
			return False

	f = open(csvFile, "w") 
	
	temp = header[4:]
	temp.insert(0,"Lines")
	f.write(";".join(str(x) for x in temp))
	f.write("\n")

	for line in data:
		f.write("LINESTRING (" + line[0]+ " " + line[1] + "," + line[2]+ " " + line[3] + ")"  ) 		

		for i in  range(4,len(line)):
			f.write(";"+line[i])
		f.write("\n")

	f.close()

	vrt= path+"/"+outputFileName+"_lines.vrt"

	f = open(vrt,'w')
	f.write('<OGRVRTDataSource><OGRVRTLayer name="lines">'+'\n')
	f.write("<SrcDataSource>" + csvFile + "</SrcDataSource>" + "\n"+ "<SrcLayer>"+outputFileName+"_lines</SrcLayer>" +"\n")
	f.write("<GeometryType>wkbLineString</GeometryType>"+"\n")
	f.write('<GeometryField encoding="WKT" field="Lines"/>'+"\n")			

	header=header[4:]
	dataType=dataType[4:]

	for i in range (0, len(header) ):
		f.write("<Field name='" + header[i] + "' src='"+header[i] + "' type='" + dataType[i] + "' width='45'/>\n")	


	f.write("</OGRVRTLayer>\n</OGRVRTDataSource>"+"\n")
	f.close()



	in_ds = ogr.Open(vrt)
	lyr = in_ds.GetLayer('lines')
	for feat in lyr:
		geom = feat.GetGeometryRef()
		print (geom.ExportToWkt())

	ogr.GetDriverByName("ESRI Shapefile").CopyDataSource(in_ds, path+"/"+outputFileName+"_lines.shp")





	return True

def createPoints(data,outputFileName,shapeType):
	
	path = os.getcwd()
	dataType	=	data.pop(1)
	header		=	data[0]
	csvFile		=	path+"/"+outputFileName+"_points.csv"

	f = open(csvFile, "w") 

	for line in data:
		for i in  range(0,len(line)):
			f.write(line[i]+",")			
		f.write("\n")
	f.close()

	vrt= path+"/"+outputFileName+"_points.vrt"


	f = open(vrt,'w')
	f.write('<OGRVRTDataSource>\n<OGRVRTLayer name="points">'+'\n')
	f.write("<SrcDataSource>" +csvFile + "</SrcDataSource>" + "\n"+ "<SrcLayer>"+outputFileName+"_points</SrcLayer>" +"\n")
	f.write("<GeometryType>wkbPoint</GeometryType>"+"\n"+"<GeometryField encoding=\'PointFromColumns\' x=\'X\' y=\'Y\'/>"+"\n")

	header=header[2:]
	dataType=dataType[2:]

	for i in range (0, len(header) ):
		f.write("<Field name='" + header[i] + "' src='"+header[i] + "' type='" + dataType[i] + "' width='45'/>\n")	


	f.write("</OGRVRTLayer>\n</OGRVRTDataSource>"+"\n")
	f.close()


	in_ds = ogr.Open(vrt)
	lyr = in_ds.GetLayer('points')
	for feat in lyr:
		geom = feat.GetGeometryRef()
		print (geom.ExportToWkt())

	ogr.GetDriverByName("ESRI Shapefile").CopyDataSource(in_ds, path+"/"+outputFileName+"_points.shp")


	return True


if __name__ == '__main__':
	
	result = readOptions()

	if	not result.get("success"):
		exit(1)

	csvFile 		=	result.get("input")
	outputFileName	=	result.get("output")
	shapeType		=	result.get("type")

	with open(csvFile, 'r') as f:
	  reader = csv.reader(f)
	  data = list(reader)

	if	shapeType == "lines":
		createLines(data,outputFileName,shapeType)
	else:
		createPoints(data,outputFileName,shapeType)
		 

