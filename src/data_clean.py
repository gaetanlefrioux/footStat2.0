import os

''' Cleaning those .csv files '''
''' Truncate too long lines '''
''' Remove empty lines '''
''' Clean cells content '''
''' Write the new content in the tmp/ directory to avoid loosing file content if an error occur '''

''' Clean sell content '''
def stripAll(line):
	newLine = []
	for e in line:
		newLine.append(e.strip())
	return newLine

''' check a line is empty '''
def isEmptyLine(line):
	for e in line:
		if e != '' and e != None and e != '#REF!' and e != '\r\n':
			return False
	return True

''' Remove the content of all csv in tmp directory '''
def removeTmpFileContent():
	competitions = os.listdir('../tmp/')
	for c in competitions:
		seasons = os.listdir('../tmp/'+c)
		for s in seasons:
			print('Removing content of file ../tmp/%s/%s'%(c,s))
			f = open('../tmp/'+c+'/'+s, 'w')
			f.write('')
			f.close()

''' Populate the content of the /tmp .csv with the content of /data .csv cleaned'''
def createCleanTmp():
	currentDirectory = '../data/'
	newDirectory = '../tmp/'
	competitions = os.listdir(currentDirectory)
	for competition in competitions:
		seasons = os.listdir(currentDirectory+competition)
		for season in seasons:
			print('Cleaning content for file %s/%s ...'%(competition, season))
			currentFilename = currentDirectory+competition+'/'+season
			newFilename = newDirectory+competition+'/'+season
			currentFile = open(currentFilename, 'r')
			newFile = open(newFilename, 'w')
			currentLines = currentFile.readlines()
			newFileContent = ''
			newFileContent += currentLines[0]
			if "\r\n" not in currentLines[0]:
				newFileContent += "\r\n"
			ncol = len(currentLines[0].split(","))
			for i in range(1, len(currentLines)):
				splitLine = currentLines[i].split(",")
				splitLine = splitLine[:ncol]
				if not isEmptyLine(splitLine):
					splitLine = stripAll(splitLine)
					contentToAdd = ','.join(splitLine)
					newFileContent += contentToAdd
					if "\r\n" not in contentToAdd:
						newFileContent += "\r\n"
			newFile.write(newFileContent)
			newFile.close()			
			currentFile.close()

removeTmpFileContent()
createCleanTmp()
