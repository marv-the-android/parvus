import urwid
from time import sleep

text = urwid.Text("WOW")
listbox = urwid.ListBox([text])
fill = urwid.Filler(listbox)

loop = urwid.MainLoop(fill)
loop.run()