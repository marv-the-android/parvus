import urwid
from time import sleep

class CommandCreate:
    def Main(self):
        self.initialise()
        self.loop = urwid.MainLoop(urwid.Columns(self.mainview), unhandled_input=self.exit_on_q)
        self.loop.run()

    def initialise(self):
        self.mainview = []
        self.input()
        self.output()

    def input(self):
        txt = urwid.Text("Hello World", align="center")
        fill = urwid.Filler(txt)
        box = urwid.LineBox(fill)
        self.mainview.append(box)

    def output(self):
        self.list1 = []
        content = urwid.SimpleFocusListWalker(self.list1)
        listbox = urwid.ListBox(content)
        adapt = urwid.BoxAdapter(listbox, len(self.list1))
        fill = urwid.Filler(adapt)
        box = urwid.LineBox(fill)
        self.mainview.append(box)

    def exit_on_q(self, key):
        if key in ["q", "Q"]:
            raise urwid.ExitMainLoop()
        elif key in ["rR"]:
            self.list1.append(urwid.Text(key))
            self.loop.draw_screen()


new = CommandCreate()
new.Main()