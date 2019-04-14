from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv
import pickle
import os
import glob
import sys
import io

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def getLastName(instr):
	sindex = instr.find("^")
	eindex = instr.find("/")
	return instr[sindex + 1: eindex]

def updateHashmap(hashMap, name, umid):
	hashMap[umid] = [name,0]

def printHashMap(hashMap):
	for x in hashMap:
		print("UMID: " , x , " " , hashMap[x][0] , " " , hashMap[x][1])

def driveDownload(term):
	creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server()
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('drive', 'v3', credentials=creds)

	# Call the Drive v3 API
	results = service.files().list(fields="nextPageToken, files(id, name)", q="name='hashdoc_" + term + ".pickle'").execute()
	items = results.get('files', [])

	if items:
		print('Files:')
		for item in items:
			request = service.files().get_media(fileId=item['id'])
			fh = io.BytesIO()
			downloader = MediaIoBaseDownload(fh, request)
			done = False
			while done is False:
				status, done = downloader.next_chunk()
				print("Downloading hashmap %d%%." % int(status.progress() * 100))

def driveUpload(term):
	creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server()
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('drive', 'v3', credentials=creds)
	fileList = glob.glob('*.csv')
	for i in fileList:
		file_metadata = {'name': i}
		media = MediaFileUpload('files/' + i, mimetype='')
		file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
		print('File ID: %s' % file.get('id'))
		os.remove(i)
		
	file_metadata = {'name': "./hashdoc_"+termName+".pickle"}
	media = MediaFileUpload('files/' + "./hashdoc_"+termName+".pickle", mimetype='')
	file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
	print('File ID: %s' % file.get('id'))
	os.remove("./hashdoc_"+termName+".pickle")

#Obtain Input information
print("Welcome to the Schrader form automator!")
termName = input("Please enter the term (example w2019, f2018, etc.): ")

#download the hashmap file
driveDownload(term=termName)

perName = input("Please enter your name: ")
committee = input("Committee: ")
date = input("Event date (example 1-1-2019): ")
title = input("Event title: ")
p = input("Event point worth: ")
print("Swipe MCards or enter 'quit' to exit!")

points = int(p)
instr = ""
umid = ""
name = ""

#Open prebuilt hashMap
hashMap = None
if os.path.exists("./hashdoc_"+termName+".pickle"):
	hashMap = pickle.load(open("./hashdoc_"+termName+"pickle","rb"))

#open csv writer
with open("./"+ title + "_"+ date + ".csv", mode = 'w') as tallyFile:
	tallyFileWriter = csv.writer(tallyFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
	#write basic into to csv
	tallyFileWriter.writerow(["Name: ", perName])
	tallyFileWriter.writerow(["Committee: ", committee])
	tallyFileWriter.writerow(["Date:", date])
	tallyFileWriter.writerow(["Event name: ", title])
	tallyFileWriter.writerow(["Points for event: ", str(points)])
	tallyFileWriter.writerow(["Last Name", "UM ID", "Points"])

	#accept umid input
	while instr != "quit":
	    instr = input(umid + " ")

	    if instr != "quit":
	        umid = instr[8:16]

	        if umid not in hashMap:
	        	name = getLastName(instr)
	        	updateHashmap(hashMap, name, umid)

	        name = hashMap[umid][0] 

	        tallyFileWriter.writerow([name, umid, points])
	        #update running tally in hashMap
	        hashMap[umid][1] += int(points)
#update 
pickle.dump(hashMap, open("./hashdoc_"+termName+".pickle", "wb"))
driveUpload(term=termName)
printHashMap(hashMap)

#delete hashmap file from drive, and then upload local hashmap file

#delte hashmap after run inorder to prevent different local copies
#if os.path.exists("hashdoc.txt"):
#	os.remove("hashdoc.txt")

