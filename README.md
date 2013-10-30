AutoPyLit
=================  
A keyboard and mouse automation tool  
------------------------------------  
   

###FAQ
  
####**What does this do?**
Have you ever had to click here, then there, then here again over and over?  
Ever wish you could just have the keyboard and/or mouse just do something for you?  
This might not be for you. Then again, it might. I'm not here to tell you what you should and shouldn't be using, this is just a fun project for us.  

####**How do I use it?**
Install python and the one non-standard library we use, pyUserInput. 
Python downloads can be found [here](http://www.python.org/download/)  
The pyUserInput library and instructions for installing it can be found [here](https://github.com/SavinaRoja/PyUserInput)  
Once that is done, run the pyScrape.py file by executing it from command line or just clicking on it. Your preference.  
If you choose command line, your command will look something like this:  
**Windows**  
`C:\Users\username\Desktop\pyScrape.py`  
**Linux**  
`./pyScrape.py`  
This command takes no arguments.  
  
####**I made some actions and I want to save them.**
Click save. Pick a spot for the file to go, then save it.  
The file will save as a .FECN file type.  

####**It doesn't work.**
Try troubleshooting it by doing some very simple tasks first, such as clicking on a target or passing a Ctrl+Shift+Esc, then gradually make them more complex. 
Also be aware that because of the limitation of pyUserInput, the keyboard automation does not work in Mac.  
Yeah, you read that right. Something works better in Windows than it does in Mac. It's crazy, we know.  
One last note about things you can and cannot do: Ctrl+Alt+Delete isn't working so well right now.  

####**It still doesn't work.**
Have you tried turning it off and on again?  

####**Yes.**
Email us. Bren@brenbriggs.com or kevin.daniel.mccabe@gmail.com
  
####**Will you update this?**
Probably, but we don't know when.  

####**Are there any planned updates or features?** 
We would like to add a feature to pass shell commands from the action list.  
If you have a feature you'd like to request, shoot us an e-mail at bren@brenbriggs.com or kevin.daniel.mccabe@gmail.com  

####**Your GUI is ugly. Why isn't that a planned update?**
Thanks for noticing. 
  
####**Libraries we use (in case you get a dependency error)**  
*    Tkinter
*    pyUserInput (specifically, pykeyboard and pymouse)
*    os
*    time
*    ctypes
*    platform
*    Some windows installs need win32api

####**What python version are you using?**
2.7.5  
There is allegedly a bug with Tkinter in Mac Mavericks that is slated to be fixed in Python 2.7.6. 

####**I wrote my own FECN File. Can I use that? 
Go get 'em, Tiger. 

####**Can I share/modify/steal this code?**
This programs' code is licensed under the GNU GPL, which can be found [here](http://www.gnu.org/copyleft/gpl.txt).
And the README (what you're reading) is copywritten under [this](http://www.gnu.org/copyleft/fdl.txt) license.
  
##Required input formats for the GUI
###This is a box by box breakdown of the input format required for each field.
###Note: **Only fill out one input field per action.**
####"Click at Coordinates (x,y)"
If you choose to manually include the mouse coordinates, they must be in the following format:  
`(100, 100)`
That is, open paren then integer, comma, space, integer, close paren. **You may not use a decimal**
####"Pass Keystrokes"
There are two kinds of keystrokes that can be passed here: literal (like a string) and special keys. 
A special key is entered without quotes, and a literal string is entered with quotes. 
Plus symbols go between keystrokes
If you are passing a literal string, it is always the last item. 
F-keys populate as `F[x]`. Fill in the space between brackets with the specific F-key you want to use. 

*    `Ctrl` is interpreted as the control key
*    `"Ctrl"` is interpreted as sending a string that contains the characters 'Ctrl' (as though you typed them instead of pressed the Ctrl key)

#####More examples:

*    `Ctrl+Shift+Esc`
*    `"Hello world!"`
*    `Ctrl+"a"`
*    `Alt+F[4]`

####"Wait seconds"
Does exactly what it sounds like. It waits the number of seconds you tell it to. 
**Note:** You _can_ put a float/decimal in this field. 

####"Wait for window"
This field scans all visible (minimized and otherwise) windows and fires the next action only if a window has in its name the string you passed in. 
Example: 
"Manager" will execute if "Windows Task Manager" appears. **This is case sensitive.**

####"Enter Comment with Action"
This is for your own personal reference. Put anything you want here. It's not included in the mandatory fields, nor does it count against your one entry field maximum. 

####Staring Num/Ending Num
This is in case you want to output for a certain number of times and include that counter in your output. 
If you don't care, just start at 1 and end on the number of times you would like to iterate. 
Example:
Starting Num: 1
Ending Num:   100
**or**
Starting Num: 50
Ending Num:   60

##Buttons
###Starting from the top down:
####Get Coordinates
This button learns the position of your mouse. Upon clicking, move the mouse to the desired click location for the action. Press 'm' and viola! 
The coordinates populate in text box to the left. **Note: This is the recommended method.**
Click "Save Action to see it populate in the Action List. 

####Special keys
This is a dropdown menu for selecting special keys to pass. 
**Note: the only special keys supported are the ones in this list.**
**Note: Doesn't work on Mac.**
Once you have the special key selected, click it, then click the Add button. Lather, rinse, and repeat until you have the desired key combination. 
Click "Save Action to see it populate in the Action List. 

####Delete Action/Save Action
Save action takes any actions listed in the fields above and sends it to the action list. Delete action deletes the currently highlighted action from the action list. 

####Up and down arrows (to the right of the action box)
Moves the highlighted event up or down in the order of occurrence in the action list. 

####Load/Save/Save Config As
*    Load config loads a configuration
*    Save config saves your config if you already have a file name
     *  If you have not loaded a file or saved a file already, you will be prompted to give the file a name at this time
*    Save Config As prompts you to name the file as you save it. 

####Clear Screen
Clears the action list and any input in the text boxes

####GO!
Take a wild guess.