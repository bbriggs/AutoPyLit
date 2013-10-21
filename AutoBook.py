from appscript import app
from pymouse import PyMouse
import time

#print location: (358.69140625, 282.88671875)
#hit enter: app('System Events').key_code(76)
# click PDF: (569.25390625, 337.71484375)
# press s
# press enter
# pass "page" + x
# pass enter
#newpage = n
# sleep between each thing at least .01 seconds time.sleep(seconds)

m = PyMouse()

if True:
	numPages = 391 #pages in doc
	i = 197
	m.click(358.69140625, 282.88671875, 1) #activate sarfari
	while i <= numPages:
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
