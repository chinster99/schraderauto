print("Welcome to the Schrader form automator!")
perName = input("Please enter your name: ")
committee = input("Committee: ")
date = input("Event date: ")
title = input("Event title: ")
points = input("Event point worth: ")

instr = ""
umid = ""

while instr != "quit":
    instr = input(umid + " ")
    if instr != "quit":
        umid = instr[8:16]
