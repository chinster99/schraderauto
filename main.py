import csv
import pickle
import os

def getLastName(instr):
	sindex = instr.find("^")
	eindex = instr.find("/")
	return instr[sindex + 1: eindex]

def updateHashmap(hashMap, name, umid):
	hashMap[umid] = [name,0]

def printHashMap(hashMap):
	for x in hashMap:
		print("UMID: " , x , " " , hashMap[x][0] , " " , hashMap[x][1])


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
hashMap = pickle.load(open("hashdoc.txt","rb"))

#open csv writer
with open(title + ".csv", mode = 'w') as tallyFile:
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
pickle.dump(hashMap, open("hashdoc.txt", "wb"))
printHashMap(hashMap)

#delete hashmap file from drive, and then upload local hashmap file

#delte hashmap after run inorder to prevent different local copies
#if os.path.exists("hashdoc.txt"):
#	os.remove("hashdoc.txt")

