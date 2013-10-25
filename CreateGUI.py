"""To do:
	1. Save As button
	2. Figure out why extra lines are going into saved files
"""
#imports
from Tkinter import *
from pykeyboard import PyKeyboard
from pymouse import PyMouse
import tkFileDialog, tkMessageBox

#initialize Objects
master = Tk()
master.wm_title("pyScraper")
k = PyKeyboard()
m = PyMouse()

#global Vars
readyForMouseInput = False
specialkeys= {"Ctrl" : "control_l_key", "Alt" : "alt_l_key", "Del" : "delete_key", "Insert":"insert_key","Esc":"escape_key","Special Keys":""}
headerLst = ["Order","Action Type", "Value", "Comment"]
delimChars = "<~>"
loadedFileName = ""
beenSaved = True
#note in createWidgets(), we create globals as well

#functions
def recMouseClick():
    #Fill text box with string "press m to grab mouse location"
    #set global var to something to signify that we are ready to use event when we hit m
    tRecMouse.delete(0, END)
    sendMessage("Press m to grab mouse location, or enter in textbox")
    master.bind("m",getMouseInput)
    master.focus()

def sendMessage(txt):
	cCanvas.delete(ALL)
	cCanvas.create_text(20, 30, anchor=W, text =txt)
	cCanvas.create_rectangle(5,5,610,100)

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
	global beenSaved
	#ensure only one textbox is filled out
	total = int(tRecMouse.get().strip() != "")
	total += int(tEnterString.get().strip() != "")
	total += int(tWait.get().strip() != "")
	total += int(tWaitScreen.get().strip() != "")
	
	if total == 1:
		#exactly 1 input
		#save action to masterListbox then refresh listbox
		orderNum = lbActionsBackend.size() + 1
		
		#get action specific values
		if tRecMouse.get().strip() != "":
			actionType = "Click Mouse"
			actionVal = tRecMouse.get()
			
		elif tEnterString.get().strip() != "":
			actionType = "Pass Keys"
			actionVal = tEnterString.get()
			
		elif tWait.get().strip() != "":
			actionType = "Wait Seconds"
			actionVal = tWait.get()
			
		elif tWaitScreen.get().strip() != "":
			actionType = "Wait for Screen"
			actionVal = tWaitScreen.get()

		Comment = tComment.get()
		addLBItem([orderNum, actionType, actionVal, Comment])
		beenSaved = False
		clearInputs()
		
	elif total == 0:
		#no inputs
		tkMessageBox.showwarning("Wrong number of inputs!", "You must have at least one action filled out!")
	else:
		#more than one input
		tkMessageBox.showwarning("Wrong number of inputs!", "Entering more than one action at a time is not allowed, please only select a Mouse, Keyboard, Wait or Window action")
		
def delAction():
	#deletes selected action
	global beenSaved
	if len(lbActions.curselection()) == 0 or int(lbActions.curselection()[0]) == 0:
		pass
		#We will not allow you to delete the header, also if nothing is selected, do nothing
	else:
		lbActionsBackend.delete(str(int(lbActions.curselection()[0]) - 1)) #have to account for header row
		repaintActionLb()
		beenSaved = False

def loadConfig():
	#load a saved config
	#ask user to choose file:
	global beenSaved, loadedFileName
	
	#determine if user gets option to save, provide if necessary
	if not(beenSaved):
		#ask user if they want to save
		if tkMessageBox.askyesno("Save?","Would you like to save your current list?"):
			if len(loadedFile) > 0:
				saveConfig()
			else:
				saveAsConfig()
	
	loadFile = tkFileDialog.askopenfile(filetypes=[("workflow files",".fecn")])
	
	i = 0
	
	if loadFile == None:
		#no file returned
		print "No File Returned"
		return
		
	lines = loadFile.readlines()
	
	#Clear existing file
	lbActionsBackend.delete(0,END)
		
	for line in lines:
		#loop through line for args
		fileArgs = []
		currLine = line#.strip("\n") <-need for saving
		fileArgs = currLine.split(delimChars)
		if int(fileArgs[0]) == -1:
			#Populate End num textbox
			tStartNum.delete(0,END)
			tStartNum.insert(0,fileArgs[2])
		elif int(fileArgs[0]) == -2:
			#Populate start num textbox
			tEndNum.delete(0,END)
			tEndNum.insert(0,fileArgs[2])
		else:
			#Add row to lbActionsBackend
			addLBItem(fileArgs)
		i += 1
	loadedFileName = loadFile.name
	loadFile.close()
	beenSaved = True
	
def clearInputs():
	tRecMouse.delete(0, END)
	tEnterString.delete(0, END)
	tWait.delete(0, END)
	tWaitScreen.delete(0, END)
	sendMessage("")

#clear screen and vars for new sequence
def newActionSet():
	#ask user if they want to save first
	global beenSaved
	
	#determine if user needs option to save, provide if necessary
	if not(beenSaved):
		if tkMessageBox.askyesno("Save?","Would you like to save your current list?"):
			if loadeFileName != "":
				saveConfig()
			else:
				saveConfigAs()
	
	#clear everything and reinitialize screen
	clearInputs()
	tStartNum.delete(0, END)
	tEndNum.delete(0, END)
	lbActions.delete(0, END)
	lbActionsBackend.delete(0, END)
	lbActions.insert(END, "Order".ljust(8) + "|" + "Action Type".ljust(20) + \
		"|" + "Value".ljust(25) + "|" + "Comment".ljust(25))
	beenSaved = True	

def saveConfig():
	#save current config, if currently saved, overwrite, if not, pop up dialog box
	#determine if we already have a file loaded, if so, proceed, if not, open dialog
	#loop through lbActionsBackend to get data
	#write data to file
	global beenSaved
	saveFile = tkFileDialog.asksaveasfile(mode='w',defaultextension=".fecn")
	#ensure filetype is fecn
	if saveFile.name[len(saveFile.name)-5:len(saveFile.name)] == ".fecn":
		#file is good continue with save
		#first need to save start num / end num
		saveFile.write("-1<~>StartNum<~>%s<~>\n" % tStartNum.get())
		saveFile.write("-2<~>EndNum<~>%s<~>\n" % tEndNum.get())
		saveFile.writelines(lbActionsBackend.get(0,END))
		saveFile.close()
	else:
		#wrong filename
		pass
		
	beenSaved = True
	pass

def saveConfigAs():
	#save as, always pop up dialog box
	global beenSaved
	beenSaved = True
	pass

def moveItemUp():
	moveItem(-1)
	
def moveItemDwn():
	moveItem(1)
	
def moveItem(moveDir):
	#move selected item up/down, moveDir should be 1 (move down) or -1 (move up)
	global beenSaved

	#check that an item is selected
	if len(lbActions.curselection()) > 0:
		#get selected item index and value
		lstindex = int(lbActions.curselection()[0])
		curItm = lbActionsBackend.get((str(lstindex - 1)))
		
		#ensure movement is allowed
		print lbActions.size()
		if (lstindex + moveDir > 0) and (lstindex + moveDir < lbActions.size()) and \
				(lstindex !=0):
			#delete item
			lbActionsBackend.delete(lstindex - 1)
		
			#reinsert item at proper position
			lbActionsBackend.insert(lstindex - 1 + moveDir, curItm)
	
			repaintActionLb()
			lbActions.activate(lstindex + moveDir)
			lbActions.selection_set(lstindex + moveDir)
			beenSaved = False
		else:
			print "not allowed"
	pass

#add an item to master listbox, repaint listbox user sees
def addLBItem(argLst):
	#order, action type, value, comment are column headers
	lbActionsBackend.insert(END, str(argLst[0]) + "<~>" + str(argLst[1]) + \
		"<~>" + str(argLst[2]) + "<~>" + str(argLst[3]) + "\n")
	repaintActionLb()

#Pull all data from master listbox and repaint what the user sees
def repaintActionLb():
	#Clear list and add header
	lbActions.delete(0,END)
	lbActions.insert(END, "Order".ljust(8) + "|" + "Action Type".ljust(20) + \
		"|" + "Value".ljust(25) + "|" + "Comment".ljust(25))
	
	i = 0
	#loop through backend listbox and display values in user friendly way, will truncate chars if necessary
	while i < lbActionsBackend.size():
		lineStr = str(lbActionsBackend.get(i))
		argLst = lineStr.split(delimChars)
		lbActions.insert(END, argLst[0][0:8].ljust(8) + "|" + argLst[1][0:20].ljust(20) + \
			"|" + argLst[2][0:25].ljust(25) + "|" + argLst[3][0:25].ljust(25))
		i += 1

def goGetEmTiger():
	i = 0
	while i < lbActionsBackend.size():
		lineStr = str(lbActionsBackend.get(i))
		argLst = lineStr.split(delimChars)
		if argLst[1] == "Click Mouse":
			#To do: Sanitize inputs
			#Mouse coords need to come in as (X, " "Y)
			loc_string = argLst[2]
			loc_string = loc_string[1:-1].strip()
			loc_string = loc_string.replace(" ","")
			m.click(int(loc_string.split(",")[0]), int(loc_string.split(",")[1]))
		elif argLst[1] == "Pass Keys":
			pass
		elif argLst[1] == "Wait Seconds":
			pass
		elif argLst[1] == "Wait for Screen":
			pass
		else:
			pass
		i += 1

def createWidgets():
	#create GUI buttons
	global lTitle, lTitle2, fMouse, lRecMouse, tRecMouse, bRecMouse, fEnterString, \
		lEnterString, tEnterString, mEnterString, mEnterStringOptions, bEnterString, \
		fStartNum, lStartNum, tStartNum, fEndNum, lEndNum, tEndNum, fWait, lWait, tWait, \
		fWaitScreen, lWaitScreen, tWaitScreen, fComment, lComment, tComment, fSaveAction, \
		bSaveAction, bDelAction, fMoveButtons, bUp, bDown, fActions, lActions, lbActions, \
		lbActionsBackend, fSaves, bLoad, bSave, bSaveAs, fCanvas, lCanvas, cCanvas, bClear, bGo
		
	
	lTitle = Label(master, text="Mouse / Keyboard Automation Tool",anchor = W, justify=LEFT)
	lTitle2 = Label(master, text="",anchor = W, justify=LEFT)

	fMouse = Frame(master)
	lRecMouse = Label(master, text="Click at Coordinates (x,y):", anchor = W, justify=LEFT)
	tRecMouse = Entry(master)
	bRecMouse = Button(master, text="Get Coordinates", command=recMouseClick, width = 14)

	fEnterString = Frame(master)
	lEnterString = Label(master, text="Pass Keystrokes:", anchor = W, justify=LEFT)
	tEnterString = Entry(master)
	mEnterString = StringVar(master)
	mEnterString.set("Special Keys")
	##TO DO: Add support for F keys, Windows/Function/Mac key, Home/End, Page Up/Down
	mEnterStringOptions = OptionMenu(master, mEnterString, "Special Keys","Ctrl", \
		"Alt","Del","Insert","Esc")
	#mEnterStringOptions.bind("<ButtonRelease-1>",specialKeyInsert)
	bEnterString = Button(master, text="Add", command=specialKeyInsert)

	fStartNum = Frame(master)
	lStartNum = Label(master, text="Starting Num:", anchor = W, justify=LEFT)
	tStartNum = Entry(master)

	fEndNum = Frame(master)
	lEndNum = Label(master, text="Ending Num (inclusive):", anchor = W, justify=LEFT)
	tEndNum = Entry(master)

	fWait = Frame(master)
	lWait = Label(master, text="Wait Seconds:", anchor = W, justify=LEFT)
	tWait = Entry(master)

	fWaitScreen = Frame(master)
	lWaitScreen = Label(master, text="Wait for window to open with name:", anchor = W, justify=LEFT)
	tWaitScreen = Entry(master)

	fComment = Frame(master)
	lComment = Label(master, text="Enter a Comment with Action:", anchor = W, justify=LEFT)
	tComment = Entry(master)

	fSaveAction = Frame(master)
	bSaveAction = Button(master, text="Save Action", command=saveAction, width =10)
	bDelAction = Button(master, text="Delete Action", command=delAction, width =10)

	fActions = Frame(master)
	lActions = Label(master, text="Action List:", anchor = W, justify=LEFT)
	lbActions = Listbox(master, width = 86, font=("Courier",12))
	lbActionsBackend = Listbox(master)
	repaintActionLb()

	fMoveButtons = Frame(master)
	bUp = Button(master, text=u"\u2191", command=moveItemUp)
	bDown = Button(master, text=u"\u2193", command=moveItemDwn)

	fSaves = Frame(master)
	bLoad = Button(fSaves, text="Load Config", command=loadConfig, width = 15)
	bSave = Button(fSaves, text="Save Config", command=saveConfig, width = 15)
	bSaveAs = Button(fSaves, text="Save Config As...", command=saveConfigAs, width = 15)
	bClear = Button(fSaves, text="Clear Screen", command=newActionSet, width = 15)

	fCanvas = Frame(master)
	lCanvas = Label(master, text="Messages:")
	cCanvas = Canvas(master, height = 100, width = 655)
	cCanvas.create_rectangle(5,5,610,100)

	bGo = Button(master, text="GO!", command=goGetEmTiger, height = 5)

def paintWidgets():
	#paint everything
	
	#titles
	lTitle.grid(row = 0, column = 0, columnspan=4)
	lTitle2.grid(row = 1, column = 0, columnspan=4)
	
	#Action Labels
	lRecMouse.grid(row = 2, column = 0, sticky=W)
	lEnterString.grid(row = 3, column = 0, sticky=W)
	lWait.grid(row = 4, column = 0, sticky=W)
	lWaitScreen.grid(row = 5, column = 0, sticky=W)
	lComment.grid(row = 6, column = 0, sticky=W)
	
	#Action Controls
	tRecMouse.grid(row = 2, column = 1, sticky=W)
	tEnterString.grid(row = 3, column = 1, sticky=W)
	tWait.grid(row = 4, column = 1, sticky=W)
	tWaitScreen.grid(row = 5, column = 1, sticky=W)
	tComment.grid(row = 6, column = 1, sticky=W+E, columnspan = 3)
	
	#Action Control Buttons
	bRecMouse.grid(row = 2, column = 2, sticky=W+E, padx=3)
	mEnterStringOptions.grid(row=3, column = 2, sticky=W+E)
	bEnterString.grid(row=3, column = 3, sticky=W+E)
	
	#Action buttons
	bDelAction.grid(row=7, column = 2, columnspan=2, sticky = E, padx = 3)
	bSaveAction.grid(row = 7, column = 2, columnspan=2, sticky = W)
	
	#action listbox
	lActions.grid(row=8, column = 0, sticky=W)
	lbActions.grid(row = 9, column = 0, sticky=W, columnspan = 4, padx=10)

	#Up / Down buttons
	bUp.grid(row = 9, column = 0, columnspan = 4, sticky=NE, pady = 10)
	bDown.grid(row = 9, column = 0, columnspan = 4, sticky=SE, pady = 10)

	#Start / End Num
	lStartNum.grid(row = 10, column = 0, sticky=W)
	lEndNum.grid(row = 11, column = 0, sticky=W)
	tStartNum.grid(row = 10, column = 1, sticky=W)
	tEndNum.grid(row = 11, column = 1, sticky=W)

	#Save Buttons
	fSaves.grid(row = 12, column = 0, columnspan = 4)
	bLoad.grid(row = 0, column = 0)
	bSave.grid(row = 0, column = 1)
	bSaveAs.grid(row = 0, column = 2)
	bClear.grid(row = 0, column = 3)

	#Canvas
	lCanvas.grid(row=13, column = 0, sticky=W)
	cCanvas.grid(row=14, column = 0, columnspan = 4, sticky=W)
	
	#Go Button
	bGo.grid(row = 15, column = 0, columnspan = 4, sticky=NSEW)
	master.grid_rowconfigure(15, minsize=100)
	
createWidgets()
paintWidgets()

master.mainloop()
