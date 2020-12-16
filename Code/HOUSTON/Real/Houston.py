import urwid
import string
from time import sleep

class CommandCreate:
    screen = urwid.raw_display.Screen()
    _,rows = screen.get_cols_rows()

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
        self.content = urwid.SimpleFocusListWalker([urwid.Text("Hello world")])
        listbox = urwid.ListBox(self.content)
        adapt = urwid.BoxAdapter(listbox, height=self.rows)
        fill = urwid.Filler(adapt)
        line = urwid.LineBox(fill)
        self.mainview.append(line)

    def exit_on_q(self, key):
        if key in ["q", "Q"]:
            raise urwid.ExitMainLoop()
        elif key in string.ascii_lowercase:
            self.content.append(urwid.Text(key, align="center"))
        elif key in ["R"]:
            self.content.clear()

new = CommandCreate()
new.Main()