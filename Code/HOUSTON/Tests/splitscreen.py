#Splitscreen.py is a test file for learning how urwid operates for the development of a UI for PARVUS command construction
#THIS IS TERRIBLY LAYED OUT AND IS NOT CONSISTENT WITH ITS USE OF CLASSES, LOCAL AND GLOBAL VARIABLES IT IS A TEST FILE AND I RANDOMLY ADDED THINGS

import urwid
#Urwid is console UI library for python using Curses (A lower level C library) as the base
#It operates with the use of "widgets" to allow construction of an organized interface
from time import sleep
#Sleep for pausing program
from datetime import datetime
#datetime for clock

#Decalares a colour palette that can be applied to urwid objects
palette = [
    ("banner", "black", "light gray"),
    ("streak", "black", "dark red"),
    ("bg", "black", "dark blue"),
]

#Glossary (sort of)
#text is the basic urwid object. Takes align command; align="center" would put the widget in the center of the screen).
#filler adds space to the top and bottom of a widget. Takes align command; align="middle" would put the widget in the middle of the screen).
#padding adds space to the left and right of a widget
#linebox draws a box around the perimeter of a widget
#listbox takes list of widgets and displays them as a list
#columns takes widgets and shows them in columns. Accepts "weights" to define width ratio between widgets
#pile takes widgets and shows them on top of each other (like a vertical version of column). Also, accepts "weights" to define height ratio between widgets
#attrmap assigns an attribute to a widget. Such as a entry from the colour palette.

top = urwid.Text(u"Hello world!\nThis is awesome", align="center")
#Declares text for top left of screen

def leftside(txt):
    fill = urwid.Filler(txt, "middle")
    pad = urwid.Padding(fill)
    box = urwid.LineBox(pad, title="Main")
    return box

#Test of a creating a class object to pass data to urwid mainloop
#In a final design all functions would likely be contained under one big class
#List iterator is test to continually update and cycle through a text element in a urwid box
class list_iterator:
    #Declares a list as each word in a string
    #.split() returns a list object of string seperated by spaces
    mainlist = u"Hello world this is a message to you!".split()
    #Decalare local variable count to keep track of what list entry urwid is showing
    count = 0
    #Function for screen refres for urwid alarm
    def refresh(self, loop=None, data=None):
        #self is an operator that references its own class
        #if list iterator is assigned to test then self would take on the propert of "test"
        #self.count would be test.count
        if self.count == len(self.mainlist):
            self.count = 0
        #Modifies the top text value and redraws the urwid screen to update values.
        top.set_text(self.mainlist[self.count])
        self.count = self.count + 1
        loop.draw_screen()
        #Alarm is a built in function of urwid that allows a user defined function to be run after a certain amount of time
        #Because this code is to indefinitely cycle through a list it sets an alarm to call itself once it has run
        loop.set_alarm_in(2, self.refresh)
#Declares an variable as the list_iterator class
test = list_iterator()

def rightside():
    #Split this string into list objects
    choices = u"This is pretty cool oh wait maybe it isnt".split()
    body = []
    
    #Convert each entry in choices and assign to new list as an urwid text widget
    for c in choices:
        body.append(urwid.Text(c, align="center"))

    txt = urwid.ListBox(body)
    map1 = urwid.AttrMap(txt, "banner")
    adapt = urwid.BoxAdapter(map1, len(body))
    fill = urwid.Filler(adapt, "top")
    pad = urwid.Padding(fill)
    map2 = urwid.AttrMap(pad, "bg")
    box = urwid.LineBox(map2, title="Details")

    return box

#Placeholder text for bottom left clock
bottomtext = urwid.Text(u"Hello world!\nThis is awesome", align="center")

def bottom(txt):
    fill = urwid.Filler(txt, "middle")
    pad = urwid.Padding(fill)
    box = urwid.LineBox(pad, title="Clock")
    return box

#Sets bottom left text to current time and redraws screen
def clock(loop=None, data=None):
    now = datetime.now()
    bottomtext.set_text(("banner", now.strftime(" %H:%M:%S ")))
    loop.draw_screen()
    loop.set_alarm_in(1, clock)

#Function that is run when a user presses an unexpected key.
def exit_on_q(key):
#Exits program if key press is Q or q
    if key in ["q", "Q"]:
        raise urwid.ExitMainLoop()

#Pile object with left widgets as inputs. Default weight is 1 so leftside(top) will appear twice as big as bottom(bottomtext).
pile = urwid.Pile([("weight", 2, leftside(top)), bottom(bottomtext)])

#Column object that takes pile widget and rightside text widget as inputs
#Size weighting can be seen again
column = urwid.Columns([("weight", 1, pile), ("weight", 3, rightside())])

#Finally define main loop object with column as the display variable
loop = urwid.MainLoop(column, palette=palette, unhandled_input=exit_on_q)
#Set alarms to run clock and test.refresh (the flashing text thing) as soon as mainloop is run
loop.set_alarm_in(0, clock)
loop.set_alarm_in(0, test.refresh)

#Finally run main loop and incorporate all defined widgets on one screen. Somehow actually runs!
loop.run()