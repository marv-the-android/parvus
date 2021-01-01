import urwid, urwid.numedit

import board, busio, digitalio, adafruit_rfm69
from time import sleep

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D22)
reset = digitalio.DigitalInOut(board.D27)
rfm69 = adafruit_rfm69.RFM69(spi, cs, reset, 433.0)

def ackwait():
	ackpack = None
	while ackpack == None:
		ackpack = rfm69.receive()
		sleep(0.1)

class MainScreen:
    def Main(self):
        loop = urwid.MainLoop(self.Setup(), unhandled_input=self.keypress, palette=[("reversed", "standout", "")])
        loop.run()

    def Setup(self):
        top = urwid.Columns([("weight", 1, self.Info()), ("weight", 3, self.CommandList())])
        mainview = urwid.Pile([("weight", 3, top), ("weight", 1, self.Config())])
        mainview = urwid.LineBox(mainview)
        return mainview

    def Config(self):
        values = (("Drive", "1"), ("Reverse", "1"), ("Clockwise", "90"), ("Anticlockwise", "90"))
        self.configvalues = urwid.SimpleFocusListWalker([])
        for v in values:
            temp = urwid.numedit.FloatEdit(("{}: ".format(v[0])), v[1])
            temp = urwid.AttrMap(temp, None, focus_map="reversed")
            self.configvalues.append(temp)
        config = urwid.Columns(self.configvalues)
        config = urwid.Filler(config)
        config = urwid.LineBox(config)
        return config

    def CommandList(self):
        self.commands = urwid.SimpleFocusListWalker([])
        commandbox = urwid.ListBox(self.commands)
        commandbox = urwid.LineBox(commandbox)
        return commandbox
    
    def Info(self):
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
        info = []
        for c in commandlist:
            info.append(urwid.Text(c))
            info.append(urwid.Divider(u" "))
        info = urwid.Pile(info)
        info = urwid.Filler(info, valign="top")
        info = urwid.LineBox(info)
        return info
    
    def keypress(self, key):
        if key in ["f12"]:
            raise urwid.ExitMainLoop()
        elif key in "1 2 3 4".split():
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
            temp = self.commands.get_focus()[1]
            del self.commands[temp]
        elif key == "f1":
            with open("test.txt", "w") as f:
                for c in self.commands:
                    temp = c.original_widget.original_widget.get_label()
                    f.write("{}\n".format(temp))
					
        elif key == "f2":
            rfm69.send(bytes("start", "utf-8"))
            ackwait()
            sleep(1)
            for c in self.commands:
                temp = c.original_widget.original_widget.get_label()
                txpacket = bytes(line.strip(), "utf-8")
                print(txpacket)
                rfm69.send(txpacket)
                ackwait()
                sleep(1)
            rfm69.send(bytes("end", "utf-8"))
            sleep(1)

main = MainScreen()
main.Main()
