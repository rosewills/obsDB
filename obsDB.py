#!/usr/bin/env python
'''
Obsidian Database Helper

Version: 0.0.0
Created: 2024-02-20 (by Rose Wills)
Status: not finished

Takes a CSV file and creates files for each entry (based on optional criteria).

conda activate obsdb

'''

# symlink: mklink data C:\Users\Rose\Sync\career\notes\js2024\obs-data

# IMPORTS #
###########
# Basic Functions
import re				# regex support
import pandas as pd		# reading in and working with csv data
import os
from datetime import datetime
import shutil

# Pretty Colors for Terminal Output (Bash-specific)
class colors:
	red = '\033[91m'
	green = '\033[92m'
	yellow = '\033[93m'
	blue = '\033[94m'
	purple = '\033[95m'
	cyan = '\033[96m'
	bold = '\033[1m'
	underline = '\033[4m'
	endc = '\033[0m'


jobTable = pd.read_csv("C:/Users/Rose/Sync/coding/projects/obsDB/data/posting-table-demo.csv",	# csv file
					sep=",",					# character used to delimit columns
					quotechar='"',				# character used to quote strings
					skipinitialspace=True,		# True if a space is added after each column delimiter
					index_col="Filename")		# Name of column to be used as row labels


timeNow = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')


def updatemeta(fileName, searchField, valNew, sizeCheck=True, dryrun=True, v=False, report=False):
	ignore = dryrun
	fileMod = os.stat(fileName).st_mtime
	if v == True:
		print("UPDATING YAML METADATA FOR", fileName)

	# findRegex = re.escape(field)+": .*"
	# replRegex = re.escape(field)+": "+re.escape(valNew)
	newFile = fileName+"-tmp"

	with open(fileName, "r", encoding='utf-8') as file:
		try:
			lines = file.readlines()
		except Exception as e:
			# print("Error!")
			print("(updatemeta1) ERROR: ",e)
			lines = [""]
			ignore = True
		
	with open(newFile, "wb") as file:
		metaBlock = 0
		try:
			firstline = lines[0].strip()
			if firstline == "---":
				for line in lines:
					sline = line.strip()
					if metaBlock < 2:
						if sline == "---":
							metaBlock += 1
						else:
							try:
								match = re.match('^(.*?): (.*)', sline)
								field = match.group(1)
								value = match.group(2)
								# print("FIELD:", "["+field+"]\t"+"VALUE:", "["+value+"]")
								try:
									if field == searchField:
										valOld = value
										if valOld == valNew:
											result = "match"
											ignore = True
											print(colors.green+"metadata matches:"+colors.endc, fileName)
											if v == True:
												print("\tvalOld:", valOld)
												print("\tvalNew:", valNew)
										else:
											result = "diff"
											if dryrun == False:
												print(colors.yellow+"updating ["+field+"] in",fileName+colors.endc)
												print("from ["+valOld+"] to ["+valNew+"]...")
												# line = re.sub(findRegex, replRegex, line)
												line = re.sub(rf"^{field}: {valOld}", rf"{field}: {valNew}", line)
											else:
												print(colors.yellow+"metadata does mot match:"+colors.endc, fileName)
												print("\tvalOld:", valOld)
												print("\tvalNew:", valNew)

								except Exception as e:
									print("(updatemeta2) ERROR: ",e)
							except:
								if v == True:
									print("cannot parse metadata line: ["+sline+"]")
							field = ""
					file.write(bytes(line, "UTF-8"))
					# file.write(line)

			else:
				print("(updatemeta3) ERROR: no YAML metadata block detected!")
				print("                     first line: ["+firstline+"]")
				print("                     (metadata block must must begin & end with \"---\"), and start on the first line of the file.")
				ignore = True
		except Exception as e:
			# print("(updatemeta4) ERROR: file appears to be empty.")
			print("(updatemeta4) ERROR: ",e)
			ignore = True
			
	# os.utime(newFile, (fileMod,fileMod))
	origSize = os.stat(fileName).st_size
	# print("origSize:", origSize)
	newSize = os.stat(newFile).st_size
	# print("newSize:", newSize)

	if sizeCheck == True:
		print("SIZE CHECK:",origSize," (original file) ->",newSize,"(updated file)")
		if origSize == newSize:
			print(colors.green+"no errors detected."+colors.endc)
		else:
			print(colors.red+"(updatemeta5) ERROR: new file is not the same size as original file. (",origSize,"->",newSize,")"+colors.endc)
			ignore = True
	
	if ignore == True:
		if v == True:
			print("original file untouched.")
	else:
		print("updating original file...")
		shutil.copyfile(newFile, fileName)
		os.utime(fileName, (fileMod,fileMod))
		chngNum += 1

	try:
		if v == True:
			print("cleaning up...")
		shutil.copy(os.path.join(os.getcwd(),newFile),"C:/Users/Rose/Sync/coding/projects/obsDB/bkp-tmp/")
		os.remove(os.path.join(os.getcwd(),newFile))
	except Exception as e:
		print("(updatemeta6) ERROR: ",e)
		os.remove(os.path.join(os.getcwd(),newFile))
	
	if report == True:
		return result


def matchCheck(df, dfField, yamlField, v=False):
	matchCount = 0
	diffCount = 0
	notFound = []

	for fileName, info in df.iterrows():
		wpCode = df.at[fileName, 'WP Code']
		file = wpCode+"-"+fileName+".md"

		value = df.at[fileName, dfField]

		if os.path.isfile(file) == True:
			count = updatemeta(file, yamlField, value, sizeCheck=False, report=True)
			if count == "match":
				matchCount += 1
			elif count == "diff":
				diffCount += 1
		else:
			notFound.append(file)

	print(colors.green+str(matchCount), "matches"+colors.endc)
	print(colors.yellow+str(diffCount), "differences"+colors.endc)
	print(colors.red+str(len(notFound)), "files do not exist"+colors.endc)

	if v == True:
		for entry in notFound:
			print(colors.red+"\t"+entry+colors.endc)



matchCheck(jobTable, 'Job Type', "job-type", v=True)