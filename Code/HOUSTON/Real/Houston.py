import urwid
import string
from time import sleep

class CommandCreate:
    screen = urwid.raw_display.Screen()
    _,rows = screen.get_cols_rows()

    def Main(self):
        self.initialise()
        self.loop = urwid.MainLoop(urwid.Columns(self.mainview), unhandled_input=self.keypress, palette=[("reversed", "standout", "")])
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
        self.content = urwid.SimpleFocusListWalker([urwid.Text("Hello world")])
        listbox = urwid.ListBox(self.content)
        adapt = urwid.BoxAdapter(listbox, height=self.rows)
        fill = urwid.Filler(adapt)
        line = urwid.LineBox(fill)
        self.mainview.append(line)

    def keypress(self, key):
        if key in ["Q"]:
            raise urwid.ExitMainLoop()
        elif key in string.ascii_lowercase:
            test = urwid.Button(key)
            pad = urwid.Padding(test, align="center", width=("relative", 25))
            self.content.append(urwid.AttrMap(pad, None, focus_map="reversed"))
        elif key in ["R"]:
            self.content.clear()

new = CommandCreate()
new.Main()