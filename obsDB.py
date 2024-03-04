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
import sys
import metautils as mu



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

# syncFields = {
# 	"WP Code": "workplace",
# 	"Position": "",
# 	"Job Type": "job-type",
# 	"Posted Date": "",
# 	"Status": "",
# 	"Link": "",

# }
dbPath = "C:/Users/Rose/Sync/coding/projects/obsDB/jobs/"
dbTable = pd.read_csv("C:/Users/Rose/Sync/coding/projects/obsDB/data/posting-table-demo.csv",	# csv file
					sep=",",					# character used to delimit columns
					quotechar='"',				# character used to quote strings
					skipinitialspace=True,		# True if a space is added after each column delimiter
					index_col="Filename")		# Name of column to be used as row labels


timeNow = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')



def matchCheck(df, dfField, yamlField, v=False, dryrun=True, listVals=False):
	matchCount = 0
	diffCount = 0
	notFound = []

	for fileName, info in df.iterrows():
		wpCode = df.at[fileName, 'WP Code']
		file = wpCode+"-"+fileName+".md"
		filePath = os.path.join(dbPath, file)

		value = df.at[fileName, dfField]

		# if os.path.isfile(filePath) == True:
		umout = mu.updatemeta(filePath, yamlField, value, sizeCheck=False, insert=True, report=True, dryrun=dryrun, v=v, listVals=listVals)
		if umout == "match":
			matchCount += 1
		elif umout == "diff":
			diffCount += 1
				# if dryrun == False:
				# 	mu.fixmeta(filePath)
		# else:
		# 	notFound.append(file)

	print(colors.green+str(matchCount), "matches"+colors.endc)
	print(colors.yellow+str(diffCount), "differences"+colors.endc)
	# print(colors.red+str(len(notFound)), "files do not exist"+colors.endc)

	if v == True:
		for entry in notFound:
			print(colors.red+"\t"+entry+colors.endc)



matchCheck(dbTable, 'Position', "aliases", v=False, dryrun=False, listVals=True)
# matchCheck(dbTable, 'WP Code', "workplace", v=False, dryrun=False)
# matchCheck(dbTable, 'Job Type', "job-type", v=False, dryrun=False)
# matchCheck(dbTable, 'Posted Date', "posted", v=False, dryrun=False)
# matchCheck(dbTable, 'Status', "status", v=False, dryrun=False)
# matchCheck(dbTable, 'Link', "link", v=False, dryrun=False)