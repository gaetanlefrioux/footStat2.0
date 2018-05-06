import os
import data_loader as dl
import numpy as np

''' Files cleaning methods '''
loader = dl.DataLoader()

''' Clean sell content '''
def stripAll(line):
	newLine = []
	for e in line:
		newLine.append(e.strip())
	return newLine

''' check if a line is empty '''
def isEmptyLine(line):
	for e in line:
		if e != '' and e != None and e != '#REF!' and e != '\r\n':
			return False
	return True

''' Clean the given file '''
def cleanFile(competition, file):
	tmpPath = '../tmp.csv'
	if(not competition in loader.getAvailableCompetitions() or not file in loader.getAvailableSeasons(competition)):
		raise IOError()
	requestedFile = open(loader.directory+competition+'/'+file, 'r')
	tmpFile = open(tmpPath, 'w')
	tmpFile.write('')
	tmpContent = ''
	requestedLines = requestedFile.readlines()
	tmpContent += requestedLines[0]
	if "\r\n" not in requestedLines[0]:
		tmpContent += "\r\n"
	ncol = len(requestedLines[0].split(","))
	for i in range(1, len(requestedLines)):
		splitLine = requestedLines[i].split(",")
		splitLine = splitLine[:ncol]
		if not isEmptyLine(splitLine):
			splitLine = stripAll(splitLine)
			contentToAdd = ','.join(splitLine)
			tmpContent += contentToAdd
			if "\r\n" not in contentToAdd:
				tmpContent += "\r\n"
	tmpFile.write(tmpContent)
	tmpFile.close()
	requestedFile.close()
	data = loader.loadStandAloneFile(tmpPath)
	newData = np.sort(data, axis=0, order="Date")
	# format the date like in other files
	for i in range(newData.size):
		newData[i]["Date"] = newData[i]["Date"].strftime("%d/%m/%y")
	loader.write(loader.directory+competition+'/'+file, newData)
	os.remove(tmpPath)
