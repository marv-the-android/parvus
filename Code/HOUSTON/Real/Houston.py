import urwid
from time import sleep

class CommandCreate:
    def Main(self):
        self.initialise()
        loop = urwid.MainLoop(urwid.Columns(self.mainview), unhandled_input=self.exit_on_q)
        loop.run()

    def initialise(self):
        self.mainview = []
        self.input()
        self.output()

    def input(self):
        txt = urwid.Text("Hello", align="center")
        fill = urwid.Filler(txt)
        box = urwid.LineBox(fill)
        self.mainview.append(box)

    def output(self):
        txt = urwid.Text("World", align="center")
        fill = urwid.Filler(txt)
        box = urwid.LineBox(fill)
        self.mainview.append(box)

    def exit_on_q(self, key):
        if key in ["q", "Q"]:
            raise urwid.ExitMainLoop()


new = CommandCreate()
new.Main()