import urwid, urwid.numedit
#Urwid is an module python that allows the creation of command line user interfaces
#Urwid interfaces are built by setting up and arrange "widgets

import board, busio, digitalio, adafruit_rfm69
from time import sleep
#Board, busio, digitalio and adafruit_rfm69 are modules for interfacing the with adafruit 433MHz radio transceiver
#Sleep is to perform pauses in the code

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D22)
reset = digitalio.DigitalInOut(board.D27)
rfm69 = adafruit_rfm69.RFM69(spi, cs, reset, 433.0)
#Defining control and data pins for the transceiver

def resend(packet):
#Resend is a custom function that makes sure a packet has been received before transitioning to the next
    ackpack = None
    while ackpack == None:
        rfm69.send(packet)
        #Send a data packet
        for i in range(30):
            #Check every tenth of a second for 3 seconds for an acknowledgement
            ackpack = rfm69.receive()
            if ackpack is not None:
                #If a packet has been recieved then break from for loop
                break
            sleep(0.1)
            #If a packet hasn't been receieved than rfm69.receive() is None and the data packet will be retransmitted

#Common urwid commands rather than write the same thing ewvery time they appear
#AttrMap assigns a palette attribute such as foreground and background colour to an obejct
#Filler puts space either side of a widget and aligns vertically
#Padding puts space above and below a widget and aligns horizontally
#Linebox surrounds a widget with a box. Simple as

class MainScreen:
    def Main(self):
        loop = urwid.MainLoop(self.Setup(), unhandled_input=self.keypress, palette=[("reversed", "standout", "")])
        #Configures main loop
        #Run self.Setup and takes the output as the widget
        #Unhandled keypress tells urwid what function to run when a key is pressed
        #Defines the colour palette to use with the program. In this case its a very simple and just inverts a selected button
        loop.run()

    def Setup(self):
    #Builds main widget to pass to urwid.MainLoop
        top = urwid.Columns([("weight", 1, self.Info()), ("weight", 3, self.CommandList())])
        #Columns is a widget that takes two widgets and puts them in columns
        #The Info widget is on the left and CommandList is on the right
        #The weight defines what relative size they take up. 1 and 3 would mean 25% and 75%
        mainview = urwid.Pile([("weight", 3, top), ("weight", 1, self.Config())])
        #Pile places two widgets on top of the other
        #Info and ColumnList are on the top and Config runs along the bottom
        mainview = urwid.LineBox(mainview)
        #Put entire widget into an outlined box
        return mainview

    def Config(self):
    #Config is a widget displayed at the bottom of the interface and lets a user change the values of commands
    #Change distance for drive and reverse
    #Change rotation degrees for clockwise and anticlockwise
        values = (("Drive", "1"), ("Reverse", "1"), ("Clockwise", "90"), ("Anticlockwise", "90"))
        self.configvalues = urwid.SimpleFocusListWalker([])
        #A FocusListWalker takes widgets as an argument such as buttons and makes them scrollable
        for v in values:
            temp = urwid.numedit.FloatEdit(("{}: ".format(v[0])), v[1])
            #FloatEdit is an extended library from urwid for editing of float values
            temp = urwid.AttrMap(temp, None, focus_map="reversed")
            #Assigns the reversed/inverted colour scheme to an object when it is the focus of a list
            self.configvalues.append(temp)
        config = urwid.Columns(self.configvalues)
        config = urwid.Filler(config)
        config = urwid.LineBox(config)
        return config

    def CommandList(self):
    #Walkable list of user defined PARVUS instructions
        self.commands = urwid.SimpleFocusListWalker([])
        commandbox = urwid.ListBox(self.commands)
        commandbox = urwid.LineBox(commandbox)
        return commandbox

    def Info(self):
    #Info box on what user interface keyboard controls
        intro = "Welcome to the PARVUS Instruction set development environment!"
        commandlist = [
            intro,
            "Drive : 1",
            "Reverse : 2",
            "Clockwise : 3",
            "Anticlockwise : 4",
            "Capture : 5",
            "Exit : F12"
        ]
        #Just a simple list with text to display
        info = []
        for c in commandlist:
            info.append(urwid.Text(c))
            info.append(urwid.Divider(u" "))
        #Iterates through the commandlist and assigns them as a text variable with a divider to be displayed
        info = urwid.Pile(info)
        info = urwid.Filler(info, valign="top")
        info = urwid.LineBox(info)
        return info

    def keypress(self, key):
        #Function that is called to handle MainLoop keypresses
        if key in ["f12"]:
            raise urwid.ExitMainLoop()
            #Exits program cleanly
            
        elif key in "1 2 3 4".split():
            #Add new PARVUS command based on keypress with parameters defined in config
            numkey = int(key)-1
            commandparam = ["drive", "reverse", "clockwise", "anticlockwise"]
            newcommand = "{0} {1}".format(commandparam[numkey], self.configvalues[numkey].original_widget.value())
            newcommand = urwid.Button(newcommand)
            newcommand = urwid.Padding(newcommand, align="left", width=("relative", 50))
            newcommand = urwid.AttrMap(newcommand, None, focus_map="reversed")
            self.commands.append(newcommand)
            
        elif key in ["5"]:
            newcommand = urwid.Button("Capture")
            newcommand = urwid.Padding(newcommand, align="left", width=("relative", 50))
            newcommand = urwid.AttrMap(newcommand, None, focus_map="reversed")
            self.commands.append(newcommand)
            
        elif key == "delete" and self.commands.get_focus()[1] is not None:
            #Delete the currently highlighted object from the PARVUS command list
            #If the list is empty nothing happens
            temp = self.commands.get_focus()[1]
            del self.commands[temp]
            
        elif key == "f1":
            #Saves the current PARVUS commands to a text file
            #Todo: Maybe pickle data instead
            with open("test.txt", "w") as f:
                for c in self.commands:
                    temp = c.original_widget.original_widget.get_label()
                    f.write("{}\n".format(temp))
                    #Writes list to each line of the text file

        elif key == "f2":
            #Transmits current instructions to PARVUS
            resend(bytes("start {0}".format(len(self.commands)), "utf-8"))
            sleep(1)
            for c in self.commands:
                temp = c.original_widget.original_widget.get_label()
                #Gets plain text value from PARVUS command list as they are initially urwid widgets
                #Could also have two lists. Urwid list and plain list
                txpacket = bytes(temp.strip(), "utf-8")
                resend(txpacket)
                sleep(1)
            resend(bytes("end", "utf-8"))
            sleep(1)

main = MainScreen()
main.Main()


