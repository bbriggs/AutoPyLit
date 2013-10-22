
#imports
from Tkinter import *

#initialize Objects
master = Tk()

#global Vars
readyForMouseInput = False

#functions
def recMouseClick():
	#Fill text box with string "press m to grab mouse location"
	#set global var to something to signify that we are ready to use event when we hit m
	global tRecMouse, readyForMouseInput
	tRecMouse.delete(0, END)
	cCanvas.create_text(20, 30, anchor=W, text ="Press m to grab mouse location, or enter in textbox")
	readyForMouseInput = True

def keyEventForm():
	#if we are currently ready to grab mouse input, do it
	if readyForMouseInput:
		#get mouse coords
		readyForMouseInput = False

def saveAction():
	#saves the current action to the listbox
	pass

def loadConfig():
	#load a saved config
	pass

def saveConfig():
	#save current config, if currently saved, overwrite, if not, pop up dialog box
	pass

def saveConfigAs():
	#save as, always pop up dialog box
	pass

def moveItem(moveVal):
	#move selected item up/down
	pass

#create GUI buttons
lTitle = Label(master, text="Mouse / Keyboard Automation Tool",anchor = W, justify=LEFT)
lTitle2 = Label(master, text="",anchor = W, justify=LEFT)

fMouse = Frame(master)
lRecMouse = Label(fMouse, text="Click at Coordinates (x,y):", anchor = W, justify=LEFT, width=30)
tRecMouse = Entry(fMouse, width = 8)
bRecMouse = Button(fMouse, text="Get Coords", command=recMouseClick, width =8)

fEnterString = Frame(master)
lEnterString = Label(fEnterString, text="Pass Kestrokes:", anchor = W, justify=LEFT, width=30)
tEnterString = Entry(fEnterString)

fStartNum = Frame(master)
lStartNum = Label(fStartNum, text="Starting Num:", anchor = W, justify=LEFT, width=30)
tStartNum = Entry(fStartNum)

fEndNum = Frame(master)
lEndNum = Label(fEndNum, text="Ending Num (inclusive):", anchor = W, justify=LEFT, width=30)
tEndNum = Entry(fEndNum)

fWait = Frame(master)
lWait = Label(fWait, text="Wait Seconds:", anchor = W, justify=LEFT, width=30)
tWait = Entry(fWait)

fWaitScreen = Frame(master)
lWaitScreen = Label(fWaitScreen, text="Wait for window to open with name:", anchor = W, justify=LEFT, width=30)
tWaitScreen = Entry(fWaitScreen)

fComment = Frame(master)
lComment = Label(fComment, text="Enter a Comment with Action:", anchor = W, justify=LEFT, width=30)
tComment = Entry(fComment)

fSaveAction = Frame(master)
bSaveAction = Button(fSaveAction, text="Save Action", command=saveAction, width=30)

fMoveButtons = Frame(master)
bUp = Button(fMoveButtons, text=u"\u2191", command=moveItem(-1))
bDown = Button(fMoveButtons, text=u"\u2193", command=moveItem(1))

fActions = Frame(master)
lActions = Label(fActions, text="Action List:", anchor = W, justify=LEFT, width=30)
lbActions = Listbox(fActions, width = 50)

fSaves = Frame(master)
bLoad = Button(fSaves, text="Load Config", command=loadConfig)
bSave = Button(fSaves, text="Save Config", command=saveConfig)
bSaveAs = Button(fSaves, text="Save Config As...", command=saveConfigAs)

fCanvas = Frame(master)
lCanvas = Label(fCanvas, text="Messages:")
cCanvas = Canvas(fCanvas, height = 100, width = 400)
cCanvas.create_rectangle(5,5,390,100)

#paint everything
lTitle.pack()
lTitle2.pack()

"""
fMouse.pack_propagate(0)
fEnterString.pack_propagate(0)
fStartNum.pack_propagate(0)
fEndNum.pack_propagate(0)
fWait.pack_propagate(0)
fWaitScreen.pack_propagate(0)
fComment.pack_propagate(0)
fSaveAction.pack_propagate(0)
fMoveButtons.pack_propagate(0)
fActions.pack_propagate(0)
fSaves.pack_propagate(0)
fCanvas.pack_propagate(0)
"""

fMouse.pack()
fEnterString.pack()
fStartNum.pack()
fEndNum.pack()
fWait.pack()
fWaitScreen.pack()
fComment.pack()
fSaveAction.pack()
fMoveButtons.pack()
fActions.pack()
fSaves.pack()
fCanvas.pack()

lRecMouse.pack(side=LEFT)
tRecMouse.pack(side=LEFT)
bRecMouse.pack(side=LEFT)
lEnterString.pack(side=LEFT)
tEnterString.pack(side=LEFT)
lWait.pack(side=LEFT)
tWait.pack(side=LEFT)
lWaitScreen.pack(side=LEFT)
tWaitScreen.pack(side=LEFT)
tWait.pack(side=LEFT)
bSaveAction.pack(side=RIGHT)
bUp.pack(side=LEFT)
bDown.pack(side=LEFT)
lActions.pack()
lbActions.pack()
bLoad.pack(side=LEFT)
bSave.pack(side=LEFT)
bSaveAs.pack(side=LEFT)
lCanvas.pack()
cCanvas.pack()
lComment.pack(side=LEFT)
tComment.pack(side=LEFT)

master.mainloop()