#imports
#requires lib pyUserInput
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time
import os

#init objects
m = PyMouse()
k = PyKeyboard()

#global vars, need to check before EVERY RUN
finalFileNm = "WholeBook.pdf"
startDir = "/home/kdm/"
finalFolder = "/home/kdm/RippedBooks"
numPages = 348 #pages in Doc
i = 1 #starting page number

def createPDFs():
	#while loop loops through all pages and creates a pdf, 
	#also moves those pdfs into a dedicated folder
	#returns Boolean True/False for whether code executed successfully
	global i, m, k
	while i <= numPages:
		#click print
		m.click(421, 288) 
		
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
		m.click(497, 385)
		
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
	startTime = "Start Time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	if createPDFs():
		mergePDfs()
	else:
		print "a problem occurred"
	print startTime
	print "End Time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
