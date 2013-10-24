
#imports
from Tkinter import *
from pykeyboard import PyKeyboard
import tkFileDialog, tkMessageBox

#initialize Objects
master = Tk()
master.wm_title("pyScraper")
k = PyKeyboard()

#global Vars
readyForMouseInput = False
specialkeys= {"Ctrl" : "control_l_key", "Alt" : "alt_l_key", "Del" : "delete_key", "Insert":"insert_key","Esc":"escape_key","Special Keys":""}
headerLst = ["Order","Action Type", "Value", "Comment"]
delimChars = "<~>"

#functions
def recMouseClick():
    #Fill text box with string "press m to grab mouse location"
    #set global var to something to signify that we are ready to use event when we hit m
    global tRecMouse
    tRecMouse.delete(0, END)
    sendMessage("Press m to grab mouse location, or enter in textbox")
    master.bind("m",getMouseInput)
    master.focus()

def sendMessage(txt):
	cCanvas.delete(ALL)
	cCanvas.create_text(20, 30, anchor=W, text =txt)
	cCanvas.create_rectangle(5,5,390,100)

def getMouseInput(event):
    tRecMouse.insert(0, str(master.winfo_pointerxy()))
    master.unbind("<Key>")
    sendMessage("")
    
def specialKeyInsert():
    """
    Special key menu options and corresponding values are stored in this dict
    Event is passed to this function
    The call to tEnterString.insert() looks up corresponding value from Menu and
    inserts it in text box on click
    
    Special key cheatsheet:
    Menu Option     pyKeyboard Value
    Ctrl            control_r_key control_l_key
    Alt             alt_key alt_l_key alt_r_key
    Delete          delete_key
    Insert          insert_key
    Escape          escape_key
    """
    #We're going to do the conversion later on, when we read the action list. For now, let's keep it human readable. 
    if mEnterString.get() != "Special Keys":
		if len(tEnterString.get()) == 0:
			tEnterString.insert(0,mEnterString.get())
			mEnterString.set("Special Keys")
		else:
			tEnterString.insert(len(tEnterString.get()),"+"+mEnterString.get())
			mEnterString.set("Special Keys")

def saveAction():
	#saves the current action to the listbox
	#ensure only one textbox is filled out
	total = int(tRecMouse.get().strip() != "")
	total += int(tEnterString.get().strip() != "")
	total += int(tWait.get().strip() != "")
	total += int(tWaitScreen.get().strip() != "")
	
	print tRecMouse.get().strip()
	
	#false is zero
	#true is one
	
	print total
	
	if total == 1:
		#exactly 1 input
		#save action to masterListbox then refresh listbox
		orderNum = lb
		
	elif total == 0:
		#no inputs
		tkMessageBox.showwarning("Wrong number of inputs!", "You must have at least one action filled out!")
	else:
		#more than one input
		tkMessageBox.showwarning("Wrong number of inputs!", "Entering more than one action at a time is not allowed, please only select a Mouse, Keyboard, Wait or Window action")
		
		
def delAction():
	#deletes selected action
	if len(lbActions.curselection()) == 0 or int(lbActions.curselection()[0]) == 0:
		pass
		#We will not allow you to delete the header, also if nothing is selected, do nothing
	else:
		lbActionsBackend.delete(lbActions.curselection())
		repaintActionLb()

def loadConfig():
	#load a saved config
	#ask user to choose file:
	loadFile = tkFileDialog.askopenfile()
	
	i = 0
	lines = loadFile.readlines()
	#get each line in file
	lbActionsBackend.delete(0,END)
	addLBItem(headerLst)
	for line in lines:
		#loop through line for args
		fileArgs = []
		currLine = line.replace("\n","")
		fileArgs = currLine.split(delimChars)
		if int(fileArgs[0]) == -1:
			#End num
			tStartNum.delete(0,END)
			tStartNum.insert(0,fileArgs[2])
		elif int(fileArgs[0]) == -2:
			#start num
			tEndNum.delete(0,END)
			tEndNum.insert(0,fileArgs[2])
		else:
			addLBItem(fileArgs)
		i += 1
		currline = str(loadFile.readline(1))
	repaintActionLb()

def clearInputs():
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

#add an item to master listbox, repaint listbox user sees
def addLBItem(argLst):
	#order, action type, value, comment are column headers
	lbActionsBackend.insert(END, argLst[0] + "<~>" + argLst[1] + \
		"<~>" + argLst[2] + "<~>" + argLst[3])
	repaintActionLb()

#Pull all data from master listbox and repaint what the user sees
def repaintActionLb():
	#Clear list and add header
	lbActionsBackend.delete(0,END)
	lbActions.insert(END, "Order".ljust(8) + "|" + "Action Type".ljust(20) + \
		"|" + "Value".ljust(25) + "|" + "Comment".ljust(25))
	
	i = 0
	#loop through backend listbox and display values in user friendly way, will truncate chars if necessary
	for i in range(lbActionsBackend.size()-1):
		lineStr = str(lbActionsBackend.get(i))
		argLst = lineStr.split(delimChars)
		lbActions.insert(END, argLst[0][0:8].ljust(8) + "|" + argLst[1][0:20].ljust(20) + \
			"|" + argLst[2][0:25].ljust(25) + "|" + argLst[3][0:25].ljust(25))

#create GUI buttons
lTitle = Label(master, text="Mouse / Keyboard Automation Tool",anchor = W, justify=LEFT)
lTitle2 = Label(master, text="",anchor = W, justify=LEFT)

fMouse = Frame(master)
lRecMouse = Label(fMouse, text="Click at Coordinates (x,y):", anchor = W, justify=LEFT, width=30)
tRecMouse = Entry(fMouse, width = 8)
bRecMouse = Button(fMouse, text="Get Coords", command=recMouseClick, width =8)

fEnterString = Frame(master)
lEnterString = Label(fEnterString, text="Pass Keystrokes:", anchor = W, justify=LEFT, width=30)
tEnterString = Entry(fEnterString)
mEnterString = StringVar(fEnterString)
mEnterString.set("Special Keys")
##TO DO: Add support for F keys, Windows/Function/Mac key, Home/End, Page Up/Down
mEnterStringOptions = OptionMenu(fEnterString, mEnterString, "Special Keys","Ctrl","Alt","Del","Insert","Esc")
#mEnterStringOptions.bind("<ButtonRelease-1>",specialKeyInsert)
bEnterString = Button(fEnterString, text="Add", command=specialKeyInsert, width=8)

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
bSaveAction = Button(fSaveAction, text="Save Action", command=saveAction, width=15)
bDelAction = Button(fSaveAction, text="Delete Action", command=delAction, width=15)

fMoveButtons = Frame(master)
bUp = Button(fMoveButtons, text=u"\u2191", command=moveItem(-1))
bDown = Button(fMoveButtons, text=u"\u2193", command=moveItem(1))

fActions = Frame(master)
lActions = Label(fActions, text="Action List:", anchor = W, justify=LEFT, width=30)
lbActions = Listbox(fActions, width = 100, font=("Courier",12))
lbActionsBackend = Listbox(fActions, width=1, height =1)
repaintActionLb()


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
mEnterStringOptions.pack(side=LEFT)
bEnterString.pack(side=LEFT)
lWait.pack(side=LEFT)
tWait.pack(side=LEFT)
lWaitScreen.pack(side=LEFT)
tWaitScreen.pack(side=LEFT)
tWait.pack(side=LEFT)
bSaveAction.pack(side=RIGHT)
bDelAction.pack(side=RIGHT)
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
lStartNum.pack(side=LEFT)
tStartNum.pack(side=LEFT)
lEndNum.pack(side=LEFT)
tEndNum.pack(side=LEFT)


master.mainloop()
