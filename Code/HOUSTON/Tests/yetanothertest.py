import urwid

screen = urwid.raw_display.Screen()
_,rows = screen.get_cols_rows()


contentlist = [urwid.Text("Hello world!")]

def keypress(key):
    content.append(urwid.Text(key))
    loop.draw_screen()

content = urwid.SimpleFocusListWalker(contentlist)
listbox = urwid.ListBox(content)
adapt = urwid.BoxAdapter(listbox, rows)
fill = urwid.Filler(adapt)
linebox = urwid.LineBox(fill)

loop = urwid.MainLoop(linebox, unhandled_input=keypress)
loop.run()