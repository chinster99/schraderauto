import csv
import pickle

print("Welcome to the Schrader form automator!")
perName = input("Please enter your name: ")
committee = input("Committee: ")
date = input("Event date: ")
title = input("Event title: ")
p = input("Event point worth: ")

points = int(p);

instr = ""
umid = ""
name = ""

hashMap = pickle.load(open("hashdoc.txt","rb"))

with open(title + ".csv", mode = 'w') as tallyFile:
	tallyFileWritter = csv.writer(tallyFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	tallyFileWritter.writerow(["Name: ", perName])
	tallyFileWritter.writerow(["Committee: ", committee])
	tallyFileWritter.writerow(["Date:", date])
	tallyFileWritter.writerow(["Event name: ", title])
	tallyFileWritter.writerow(["Points for event: ", str(points)])
	tallyFileWritter.writerow(["Name", "UM ID", "Points"])
	while instr != "quit":
	    instr = input(umid + " ")
	    if instr != "quit":
	        umid = instr[8:16]
	        name = hashMap[umid][0]
	        tallyFileWritter.writerow([name, umid, points])
	        hashMap[umid][1] += points

pickle.dump(hashmap, open("hashdoc.txt", "wb"))

