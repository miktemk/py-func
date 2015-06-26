import sys, os, re
from sys import stdout
import time, datetime
from urllib.request import urlopen
import ftplib

def download(url):
	"""Copy the contents of a file from a given URL
	and returns the result
	"""
	webFile = urlopen(url)
	result = webFile.read()
	webFile.close()
	return result

def downloadToFile(url, localFile=None):
	"""Copy the contents of a file from a given URL
	to a local file.
	"""
	if localFile == None:
		localFile = url.split('/')[-1]
	localFile = open(localFile, 'wb')
	localFile.write(download(url))
	localFile.close()

# from http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
def downloadWithProgress(url, file_name=None):
	if file_name == None:
		file_name = url.split('/')[-1]
	u = urlopen(url)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(u.headers["Content-Length"])
	print("Downloading: %s Bytes: %s" % (file_name, file_size))

	file_size_dl = 0
	block_sz = 8192
	while True:
		buffer = u.read(block_sz)
		if not buffer:
			break

		file_size_dl += len(buffer)
		f.write(buffer)
		status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
		status += ' [' + ('x'*(int(file_size_dl * 20. / file_size)+1)).ljust(20, '-') + ']'
		stdout.write("\r%s" % status)
		stdout.flush()
	print("")
	f.close()

#uploads the file to some domain
def uploadToFtp(filenameLocal, pathUpThere, domain, username, password):
	session = ftplib.FTP(domain, username, password)
	# file to send
	file = open(filenameLocal,'rb')
	head, tail = os.path.split(filenameLocal)
	# send the file
	finalPath = 'public_html/' + pathUpThere + '/' + tail
	print('uploading', filenameLocal, 'to', finalPath)
	session.storbinary('STOR ' + finalPath, file)
	# close file and FTP
	file.close()
	session.quit()
