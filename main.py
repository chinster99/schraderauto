from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv
import pickle
import os
import glob

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

def driveDownload():
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
	results = service.files().list(fields="nextPageToken, files(id, name)").execute()
	items = results.get('files', [])

	if not items:
		print('No files found.')
	else:
		print('Files:')
		for item in items:
			print(u'{0} ({1})'.format(item['name'], item['id']))

def driveUpload():
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
	fileList = glob.glob('./*.csv')
	for i in fileList:
		file_metadata = {'name': i}
		media = MediaFileUpload()

#download the hashmap file

#Obtain Input information
print("Welcome to the Schrader form automator!")

perName = input("Please enter your name: ")
committee = input("Committee: ")
date = input("Event date: ")
title = input("Event title: ")
p = input("Event point worth: ")

points = int(p)
instr = ""
umid = ""
name = ""

#Open prebuilt hashMap
hashMap = None
if os.path.exists("./hashdoc.pickle"):
	hashMap = pickle.load(open("hashdoc.pickle","rb"))

#open csv writer
with open(title + "_"+ date + ".csv", mode = 'w') as tallyFile:
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
pickle.dump(hashMap, open("hashdoc.pickle", "wb"))
printHashMap(hashMap)

#delete hashmap file from drive, and then upload local hashmap file

#delte hashmap after run inorder to prevent different local copies
#if os.path.exists("hashdoc.txt"):
#	os.remove("hashdoc.txt")

