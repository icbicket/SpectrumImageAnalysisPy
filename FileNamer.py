from __future__ import print_function
import os
import glob

def NameFile(filepath):
	if os.path.exists(filepath):
		newname = FindLatestFilename(filepath)
	else:
		newname = filepath
	print('Saving file as...', newname)
	return newname

def FindLatestFilename(filepath):
	if len(filepath.rsplit('/', 1)) == 2:
		foldername = filepath.rsplit('/', 1)[0] # Split out folder path
		filename = filepath.rsplit('/', 1)[-1] # retrieve filename
		filelist = glob.glob((foldername + '/' + filename.rsplit('.', 1)[0] + '*.' + filename.rsplit('.')[-1])) # find list of files within folder
		nums = []
		lastfile = None
		for filen in filelist:
			if filen.rsplit('.', 1)[-2].rsplit('-', 1)[-1].isdigit(): # if the filename ends in -digit...
				nums.append(int(filen.rsplit('.', 1)[-2].rsplit('-', 1)[-1])) # append the number to the list
				lastnum = max(nums) # find maximum number
				lastfile = filen.rsplit('.', 1)[-2].rsplit('-', 1)[-2] + '-' + str(lastnum) + '.' + filen.rsplit('.', 1)[-1]
			elif lastfile is not None:
				lastfile = lastfile
			else:
				lastfile = filen.rsplit('.', 1)[-2] + '.' + filen.rsplit('.', 1)[-1]
		newfilename = NumberFileNames(lastfile)
	else:
		foldername = ''
		filename = filepath
		newfilename = NumberFileNames(filename)
	return newfilename
	

def NumberFileNames(filepath):
	if len(filepath.rsplit('/', 1)) == 2:
#		If the input filepath has a folder path included
		foldername = filepath.rsplit('/', 1)[0]
		filename = filepath.rsplit('/', 1)[-1]
	else:
		foldername = ''
		filename = filepath

	if filename.rsplit('-',1)[-1].rsplit('.', 1)[0].isdigit():
		filename = filename.rsplit('-', 1)[0] + '-' + str(1+int(filename.rsplit('-', 1)[-1].rsplit('.', 1)[0])) + '.' + filename.rsplit('.', 1)[-1]
	else:
		filename = filename.rsplit('.', 1)[-2] + '-1' + '.' + filename.rsplit('.', 1)[-1]
	filepath = os.path.join(foldername, filename)
	return filepath
