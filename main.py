from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload
from apiclient import errors
import csv
import pickle
import os
import glob
import sys
import io

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

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
		for item in items:
			request = service.files().get_media(fileId=item['id'])
			fh = io.FileIO('hashdoc_' + term + '.pickle', 'wb')
			downloader = MediaIoBaseDownload(fh, request)
			done = False
			while done is False:
				status, done = downloader.next_chunk()
				print("Downloading hashmap %d%%." % int(status.progress() * 100))

def driveUpload(term, title, date):
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

	results = service.files().list(fields="nextPageToken, files(id, name)", q="name='hashdoc_" + term + ".pickle'").execute()
	items = results.get('files', [])
	for i in items:
		try:
			service.files().delete(fileId=i['id']).execute()
		except errors.HttpError:
			print('Cannot delete old hashmap from drive')
	
	results = service.files().list(fields="nextPageToken, files(id, name)", q="name='FinalPointsTally_"+term+".csv'").execute()
	items = results.get('files', [])
	for i in items:
		try:
			service.files().delete(fileId=i['id']).execute()
		except errors.HttpError:
			print('Cannot delete old hashmap from drive')

	file_metadata = {'name': 'FinalPointsTally_'+term+'.csv'}
	media = MediaFileUpload('./FinalPointsTally_'+term+'.csv', mimetype='text/csv')
	file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
	os.remove('./FinalPointsTally_'+term+'.csv')

	file_metadata = {'name': "hashdoc_"+termName+".pickle"}
	media = MediaFileUpload("./hashdoc_"+termName+".pickle", mimetype='text/pickle')
	file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
	os.remove("./hashdoc_"+termName+".pickle")

	file_metadata = {'name': title + "_"+ date + ".csv"}
	media = MediaFileUpload("./"+ title + "_"+ date + ".csv", mimetype='text/csv')
	file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
	os.remove("./"+ title + "_"+ date + ".csv")
	

#Obtain Input information
print("Welcome to the Schrader form automator!")
termName = input("Please enter the term (example w2019, f2018, etc.): ")

#download the hashMap file
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
hashMap = {}
if os.path.exists("./hashdoc_"+termName+".pickle"):
	hashMap = pickle.load(open("./hashdoc_"+termName+".pickle","rb"))

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

with open("FinalPointsTally_"+termName+".csv", mode = 'w') as finalFile:
	finalFileWriter = csv.writer(finalFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	finalFileWriter.writerow(["Last Name", "UM ID", "Points"])
	for michID, v in hashMap.items():
		finalFileWriter.writerow([michID, v[0], v[1]])

driveUpload(term=termName, title=title, date=date)

#delete hashMap file from drive, and then upload local hashMap file

#delte hashMap after run inorder to prevent different local copies
#if os.path.exists("hashdoc.txt"):
#	os.remove("hashdoc.txt")

