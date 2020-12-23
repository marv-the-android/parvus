import urwid
import string
from time import sleep

class CommandCreate:
    screen = urwid.raw_display.Screen()
    _,rows = screen.get_cols_rows()

    def Main(self):
        self.initialise()
        self.loop = urwid.MainLoop(urwid.Columns(self.mainview), unhandled_input=self.keypress, palette=[("reversed", "light gray", "dark red")])
        self.loop.run()

    def initialise(self):
        self.mainview = []
        self.input()
        self.output()

    def input(self):
        buttonlist = u"Drive Reverse Clockwise".split()
        buttons = urwid.SimpleFocusListWalker([])
        for b in buttonlist:
            temp = urwid.Button(b)
            urwid.connect_signal(temp, "click", self.MenuEntry, b)
            buttons.append(urwid.AttrMap(temp, None, focus_map="reversed"))
        listbox = urwid.ListBox(buttons)
        adapt = urwid.BoxAdapter(listbox, height=self.rows)
        fill = urwid.Filler(adapt)
        line = urwid.LineBox(fill)
        self.mainview.append(line)

    def output(self):
        self.content = urwid.SimpleFocusListWalker([])
        listbox = urwid.ListBox(self.content)
        adapt = urwid.BoxAdapter(listbox, height=self.rows)
        fill = urwid.Filler(adapt)
        line = urwid.LineBox(fill)
        self.mainview.append(line)

    def MenuEntry(self, button, choice):
        selected = urwid.Button(choice)
        self.content.append(urwid.AttrMap(selected, None, focus_map="reversed"))

    def keypress(self, key):
        if key in ["Q"]:
            raise urwid.ExitMainLoop()
        elif key in ["R"]:
            self.content.clear()

new = CommandCreate()
new.Main()