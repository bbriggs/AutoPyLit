#imports
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
	global i, m, k
	while i <= numPages:
		m.click(421, 288) #click print
		#wait until the print window is open
		while str(os.system("wmctrl -l | grep 'kdm-virtual-machine Print'")) == "256":
			time.sleep(2)
			print "waiting"
		k.tap_key(k.tab_key) #select printer
		time.sleep(2)
		k.tap_key(k.tab_key) #enter into filename field
		time.sleep(.25)
		filenm = 'page' + str(i).zfill(5) + ".pdf"
		k.type_string(filenm) #enter filename
		time.sleep(.25)
		k.tap_key(k.enter_key) #press enter to print
		time.sleep(5)
		k.press_key(k.alt_key) #press alt+F4 to close the window
		k.tap_key(k.function_keys[4])
		k.release_key(k.alt_key)
		time.sleep(1)
		m.click(497, 385) #ensure focus is back in page
		if not os.path.isfile(startDir + filenm):
			print "File was NOT created, stopping loop"
			return False
			break
		#move file to other folder
		os.system("mv " + startDir + filenm + " " + finalFolder) #move file to desired folder
		time.sleep(.25)
		k.type_string('n') #press n for next page
		time.sleep(3)
		i +=1
	return True

def mergePDfs():
	#create one merged PDF of all files
	pdfCatCmd = "gs -dBATCH -dNOPAUSE -dSAFER -q -sDEVICE=pdfwrite -sOutputFile=" + finalFolder + "/" + \
		finalFileNm + " " + finalFolder + "/*.pdf "
	os.system(pdfCatCmd)

if __name__ == '__main__':
	print "Start Time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	if createPDFs():
		mergePDfs()
	else:
		print "a problem occurred"
	print "End Time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
		m.click(358.69140625, 282.88671875, 1) #click print
		time.sleep(.25) #wait
		app('System Events').key_code(76) #press enter
		time.sleep(.5) #wait
		m.click(570.97265625, 338.7890625, 1) #click PDF
		time.sleep(.5) #wait
		m.click(600.03125, 377.8515625, 1) #click PDF
		time.sleep(.25) #wait
		app('System Events').keystroke('page'+ str(i).zfill(5)) #type pdf name
		time.sleep(0.25) #wait
		app('System Events').key_code(76) #press enter
		time.sleep(1.25) #wait
		app('System Events').keystroke('n') #press n for next page
		time.sleep(4) #wait
		i += 1
>>>>>>> e83bf268bf80fbbab83bea148a1f077d47c0016b
