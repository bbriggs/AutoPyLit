#imports
#requires lib pyUserInput
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time
import os
import Tkinter as tk

#instantiate objects
m = PyMouse()
k = PyKeyboard()

#global vars, need to check before EVERY RUN
finalFileNm = "WholeBook.pdf"
startDir = "/home/kdm/"
finalFolder = "/home/kdm/RippedBooks"
numPages = 3 #pages in Doc
i = 1 #starting page number

#Grab mouse location and return
def calibrate_location(txt):
	#create the instance
	root = tk.Tk()
	
	#hides that silly window
	root.withdraw()
    
	#asks user to move mouse to proper location and hit enter
	raw_input("Move your mouse to the desired position for mouse for " + txt + \
		" and press enter")
    
	#winfo_pointerxy() returns a tuple with x and y. 
	#pointerxy[0] is the x and and pointerxy[1] is the y. 
	#We store the tuple in pointer_loc and return it. 
	pointer_loc = root.winfo_pointerxy()
	
	#return result
	return pointer_loc

def createPDFs(mouseTuple1, mouseTuple2):
	#while loop loops through all pages and creates a pdf, 
	#also moves those pdfs into a dedicated folder
	#returns Boolean True/False for whether code executed successfully
	global i, m, k
	while i <= numPages:
		#click print
		m.click(mouseTuple1[0], mouseTuple1[1]) 
		
		#wait until the print window is open
		while str(os.system("wmctrl -l | grep 'kdm-virtual-machine Print'")) == "256":
			time.sleep(2)
			print "waiting"
		
		#select printer
		k.tap_key(k.tab_key)
		time.sleep(2)
		
		#enter into filename field
		k.tap_key(k.tab_key) 
		time.sleep(.25)
		filenm = 'page' + str(i).zfill(5) + ".pdf"
		k.type_string(filenm)
		time.sleep(.25)
		
		#press enter to print
		k.tap_key(k.enter_key)
		time.sleep(5)
		
		#press alt+F4 to close the window
		k.press_key(k.alt_key)
		k.tap_key(k.function_keys[4])
		k.release_key(k.alt_key)
		time.sleep(1)
		
		#ensure focus is back in page
		m.click(mouseTuple2[0], mouseTuple2[1])
		
		#Check to see if file was created
		if not os.path.isfile(startDir + filenm):
			print "File was NOT created, stopping loop"
			return False
			break
			
		#move file to final folder
		os.system("mv " + startDir + filenm + " " + finalFolder) #move file to desired folder
		time.sleep(.25)
		
		#press n for next page
		k.type_string('n')
		time.sleep(3)
		
		#increment counter
		i +=1
	return True

def mergePDfs():
	#create one merged PDF of all files
	pdfCatCmd = "gs -dBATCH -dNOPAUSE -dSAFER -q -sDEVICE=pdfwrite -sOutputFile=" + \
		 finalFolder + "/" + finalFileNm + " " + finalFolder + "/*.pdf "
	os.system(pdfCatCmd)

#if block so we can turn code on/off easier
if __name__ == '__main__':
	#main code execution
	
	#Get first mouse tuple
	firstTuple = calibrate_location("the print icon")
	
	#get second mouse tuple
	secondTuple = calibrate_location("the page body")
	
	#get start time for loop execution
	startTime = "Start Time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	if createPDFs(firstTuple, secondTuple):
		mergePDfs()
	else:
		print "a problem occurred"
	print startTime
	print "End Time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
