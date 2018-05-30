from tkinter import *
import time
import subprocess
import threading


#-----------------------------------Fields--------------------------------------#
#this method is only used as a place holder for the object t
def temp():
    pass
BPM = 100
subDivBPM = 100
timeBefore = 0.0 #time of the previous click
timeNow = 0.0 #variable to hold the current time
numTap = 0 #variable to keep track of number of taps done
retrievedTime = 0.0
actualDifference = 0.0
recordingTaps = False #is set to True when recording the intervals between clicks
metronomeOn = False #is set to True when beeps start
t = threading.Timer(60.0/BPM, temp) #this object is the object that helps run code after a certain time
subDivideT = threading.Timer(60.0/BPM, temp) #this object is the object that helps run code after a certain time (for subdividing)
subDivideCount = 1 #this helps keep track of which subdivided beats to play
subDivideType = "quarter" #this helps the compiler know which subdivision is being used currently

#-----------------------------------Overall--------------------------------------#

window = Tk()


window.title("Metronome")
window.configure(background = "light blue")

#-----------------------------------Title--------------------------------------#
topFrame = Frame(window, bg = "gray")
topFrame.pack(side = "top", padx=20, pady = 10)

title = Label (topFrame, text="METRONOME", bg="light blue", fg="darkslategray", font = "none 60 bold")
title.pack(side = "top")
title.pack(side = "top")


#-----------------------------------Click and Other Functions--------------------------------------#
def recalculateSubDiv(): #this function helps recalculate the subdivision BPM everytime the tempo is adjusted
    global BPM
    global subDivBPM
    global subDivideType
    if subDivideType == "quarter":
        subDivBPM = BPM
    elif subDivideType == "eighth":
        subDivBPM = BPM*2
    elif subDivideType == "sixteenth":
        subDivBPM = BPM*4
    elif subDivideType == "triplet":
        subDivBPM = BPM*3

#minus BPM by one
def click1(event):
    global BPM
    BPM -= 1
    BPMLabel.config(text=BPM)
    recalculateSubDiv()

#add BPM by one
def click2(event):
    global BPM
    BPM += 1
    BPMLabel.config(text=BPM)
    recalculateSubDiv()

#tapper function
def click3(event):
    global BPM
    global numTap
    global timeNow
    global timeBefore
    global retrievedTime
    global actualDifference
    retrievedTime = time.time()#gets
    numTap += 1

    if numTap > 1: #run only after the second tap
        timeBefore = timeNow #put the old time back
        timeNow = retrievedTime #make timeNow the new retrieved time
        actualDifference = timeNow - timeBefore #difference in time between the click that just happened and the click before that
        newBPM = 60.0/actualDifference #format into beats per minute
        newBPM += 0.5 #add 0.5 to make it so it rounds up or down a number
        BPM = int(newBPM)
        recalculateSubDiv()


    else:#skip the first tap
        timeNow = retrievedTime #temporarily set timeNow to base time

    BPMLabel.config(text=BPM)

#function that gets the tempo from the input box
def setTempo(input):
    global BPM
    BPM = int(input)
    BPMLabel.config(text=BPM)
    recalculateSubDiv()


def playMetronome(): #this function is repeatedly ran when the metronome beaper is turned on
    global BPM
    global t #this object is the object that helps run code after a certain time
    global subDivideCount #this variable keeps track of which offbeat the computer is currently on
    global subDivBPM
    t = threading.Timer(60.0/subDivBPM, playMetronome) #instantiate the timer. setting it so it calls playMetronome to play the sound
    t.start() #starts the timer that runs in the background.

    if subDivideCount is 1 or subDivideType == "quarter":
        print(subDivideType)
        subprocess.call(["afplay", "dit2.wav"]) #plays sound
        if (subDivideType == "eighth" or subDivideType == "sixteenth" or subDivideType == "triplet"):
            subDivideCount += 1

    elif subDivideCount > 1 and subDivideType is not "quarter": #plays sound if subdividing and on off beat
        subprocess.call(["afplay", "dah2.wav"])
        subDivideCount += 1

    #resetting back to 1 after every two beeps
    if subDivideType == "eighth" and subDivideCount == 3:
        subDivideCount = 1

    #resetting back to 1 after every three beeps
    elif subDivideType == "triplet" and subDivideCount == 4:
        subDivideCount = 1

    #resetting back to 1 after every 4 beeps
    elif subDivideType == "sixteenth" and subDivideCount == 5:
        subDivideCount = 1
    print(subDivideCount)


#------------------Functions for Subdividing------------------#

#all functions in this section are activated when a subdivision button is pressed
def quarterClick(event):
    global BPM
    global subDivBPM
    global subDivideType
    global subDivideCount

    #setting all variables to match with quarter notes
    subDivBPM = BPM
    subDivideType = "quarter"
    subDivideCount = 1

def eighthClick(event):
    global BPM
    global subDivBPM
    global subDivideType
    global subDivideCount

    #setting all variables to match with eighth notes
    subDivBPM = BPM
    subDivBPM = subDivBPM*2
    subDivideType = "eighth"
    subDivideCount = 1

def sixteenthClick(event):
    global BPM
    global subDivBPM
    global subDivideType
    global subDivideCount

    #setting all variables to match with sixteenth notes
    subDivBPM = BPM
    subDivBPM = subDivBPM*4
    subDivideType = "sixteenth"
    subDivideCount = 1

def tripletClick(event):
    global BPM
    global subDivBPM
    global subDivideType
    global subDivideCount

    #setting all variables to match with triplet notes
    subDivBPM = BPM
    subDivBPM = subDivBPM*3
    subDivideType = "triplet"
    subDivideCount = 1



#-----------------------------------Main Frame--------------------------------------#

#setting up the main frame
mainFrame = Frame(window, bg = "light blue", height=800, width=720)
mainFrame.pack(side="bottom")
mainFrame.pack_propagate(0)

#label and functions for BPM widget
Label(mainFrame, text = "BPM", bg ="light blue", fg="darkslategray", font = "none 18 bold").pack()
BPMLabel = Label(mainFrame, text = BPM, bg ="light blue", fg="darkslategray", font = "none 40 bold")
BPMLabel.pack()

startCanvas = Canvas(mainFrame, width=250, height=25, bg="green")
startCanvas.pack()
textId = startCanvas.create_text(125,13, fill="darkslategray", font = "none 11 bold", text="START")

#click function for turning on the metronome
def click5(event):
    global metronomeOn
    metronomeOn = not metronomeOn

    if metronomeOn == True:
        startCanvas.config(bg="red")
        startCanvas.itemconfig(textId, text="STOP")
        playMetronome() #runs function for metronome

    else:
        startCanvas.config(bg="green")
        startCanvas.itemconfig(textId, text="START")
        t.cancel() #stops metronome

startCanvas.bind("<Button-1>", click5)




Label(mainFrame, text = "Press the right button to raise the tempo by one and the left to lower by one!", bg = "light blue",fg="darkslategray", font = "none 11 bold").pack()



#-----------------------------------Tempo Buttons Widgets and Frames--------------------------------------#
#frame within the main frame so the two buttons can go next to eachother
frame2 = Frame(mainFrame, bg = "light blue", height="150", width="500")
frame2.pack(side="top")
frame2.pack_propagate()

#canvas for left button
canvas = Canvas(frame2, width=75, height=150, bg="light blue")
canvas.pack(side="left")
canvas.bind("<Button-1>", click1)
canvas.create_rectangle(0,0,75,150,fill="gray")
canvas.create_text(37,75, fill="darkslategray", font = "none 40 bold", text="-")

#canvas for right button
canvas2 = Canvas(frame2, width=75, height=150, bg="light blue")
canvas2.pack(side="right")
canvas2.bind("<Button-1>", click2)
canvas2.create_rectangle(0,0,75,150,fill="gray")
canvas2.create_text(37,75, fill="darkslategray", font = "none 40 bold", text="+")


e1 = Entry(mainFrame)
e1.pack()

submit = Button(mainFrame, text = "submit", command = lambda: setTempo(e1.get()))
submit.pack()


#-----------------------------------Subdivision Frames and Widgets--------------------------------------#

subdivFrame = Frame(mainFrame, bg="blue", height="80", width="400")
subdivFrame.pack()
subdivFrame.pack_propagate()

quarterCanvas = Canvas(subdivFrame, width=100, height=80, bg ="light steel blue")
quarterCanvas.pack(side="left")
quarterCanvas.create_text(50,40, fill="darkslategray", font = "none 15 bold", text="QUARTER")
quarterCanvas.bind("<Button-1>", quarterClick)

eighthCanvas = Canvas(subdivFrame, width=100, height=80, bg ="LightCyan2")
eighthCanvas.pack(side="left")
eighthCanvas.create_text(50,40, fill="darkslategray", font = "none 15 bold", text="EIGHTH")
eighthCanvas.bind("<Button-1>", eighthClick)

sixteenthCanvas = Canvas(subdivFrame, width=100, height=80, bg ="LightCyan3")
sixteenthCanvas.pack(side="left")
sixteenthCanvas.create_text(50,40, fill="darkslategray", font = "none 15 bold", text="SIXTEENTH")
sixteenthCanvas.bind("<Button-1>", sixteenthClick)

tripletCanvas = Canvas(subdivFrame, width=100, height=80, bg ="LightCyan4")
tripletCanvas.pack(side="left")
tripletCanvas.create_text(50,40, fill="darkslategray", font = "none 15 bold", text="TRIPLET")
tripletCanvas.bind("<Button-1>", tripletClick)




#-----------------------------------Tapper Frames and Widgets--------------------------------------#

#frame for tapper
frame3 = Frame(mainFrame, bg="light blue", height = "62", width ="125")
frame3.pack()
frame3.pack_propagate()

Label(frame3, text = "Press the gray button to tap the tempo. Press the green button below to start recording and red to stop.", bg = "light blue",fg="darkslategray", font = "none 11 bold").pack(side="top")

tapCanvas = Canvas(frame3, width=250, height=62, bg ="gray")
tapCanvas.pack()
tapCanvas.pack_propagate()
tapCanvas.create_rectangle(0,0,250,62,fill="gray")
tapCanvas.bind("<Button-1>", click3)


#frame for tapper
frame4 = Frame(mainFrame, bg="light blue", height = "31", width ="125")
frame4.pack()
frame4.pack_propagate()

tapStopCanvas = Canvas(frame4, width=250, height=31, bg ="green")

#tapper function to start/stop recording taps
def click4(event):
    global recordingTaps
    global numTap
    global timeNow
    global timeBefore

    recordingTaps = not recordingTaps
    if recordingTaps == True: #begin recording
        tapStopCanvas.config(bg="red")

    elif recordingTaps == False: #stop recording taps
        tapStopCanvas.config(bg="green")
        timeNow = 0.0 #resetting everything
        timeBefore = 0.0 #resetting everything
        numTap = 0 #resetting everything


tapStopCanvas.pack()
tapStopCanvas.pack_propagate()
tapStopCanvas.bind("<Button-1>", click4)




window.mainloop()
