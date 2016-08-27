# Addittional functions for downloading shit

# configuration
doDelay = True
doLog = True
downloadDir = "offline_download"

import sys, os, re
import time, datetime
import urllib
import downloadShit
from time import sleep
from random import randrange


# always set offset -1 then the filename number u want to start with
# Examples:
# downloadAbook("http://url.com/book1/", "book1_", 10, 12)   -> http://url.com/book1/10.mp3  .. http://url.com/book1/12.mp3
# downloadAbook("http://url.com/book2/", "book2_", 1, 50, 3) -> http://url.com/book2/001.mp3 .. http://url.com/book2/050.mp3
def downloadAbook(httpPrefix, localPrefix, startIndex, endIndex, zfillUrl=1):
	global downloadDir, doDelay, doLog
	# .... endIndex+1 to make it inclusive!
	for i in range(startIndex, endIndex+1):
		urlPath = httpPrefix + str(i).zfill(zfillUrl) + ".mp3";
		localPath = downloadDir + "/" + localPrefix + str(i).zfill(3) + ".mp3";
		print (urlPath)
		print ("    ===> {0}".format(localPath))
		# .... create download directory if not exists
		localPathDir = os.path.dirname(localPath)
		if not os.path.exists(localPathDir):
		    os.makedirs(localPathDir)
		# .... download the shit
		succeeded = False
		while not succeeded:
			try:
				downloadShit.downloadToFile(urlPath, localPath)
				#downloadShit.downloadWithProgress(urlPath, localPath)
				succeeded = True
			except IncompleteRead:
				# .... error during download
				succeeded = False
				if doLog:
					with open("zz_downloadShit.log", "a") as myfile:
						myfile.write("Failed to download " + urlPath + "... Will try again.\n")
				if doDelay:
					sleep([2, 3, 4, 11, 23, 34][randrange(3)])
		# .... append to log file
		if doLog:
			with open("zz_downloadShit.log", "a") as myfile:
				myfile.write("Successfully downloaded " + urlPath + " ---> " + localPath + "\n")
		# .... wait
		if doDelay:
			sleep([2, 3, 4, 11, 23, 34][randrange(3)])
