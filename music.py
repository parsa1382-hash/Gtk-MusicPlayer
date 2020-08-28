#! /usr/bin/python3
# Parsa Amini, 2020
# Released by GPL3+

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GdkPixbuf
import os
import mpv

musics=[]
i = 0
c = 0

listbox = Gtk.ListBox()

player = mpv.MPV()

win = Gtk.Window()
win.set_title("Music")
scrolledwin = Gtk.ScrolledWindow()

def image_define(filename,w,h):
    return Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(filename=filename,width=w,height=h,preserve_aspect_ratio=True))

#imgplay = Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(filename='/home/parsa/icons/play.png',width=32,height=32,preserve_aspect_ratio=True))
#imgstop = Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(filename='/home/parsa/icons/stop.png',width=32,height=32,preserve_aspect_ratio=True))


imgplay = image_define('./icons/play.png',28,28)
imgstop = image_define('./icons/stop.png',28,28)
imgback = image_define('./icons/back.png',28,28)
imgnext = image_define('./icons/next.png',28,28)

playbutton = Gtk.Button(image = imgplay)
nextbutton = Gtk.Button(image = imgnext)
pervbutton = Gtk.Button(image = imgback)

a=''
g = 0
def play():
    global musics, i, c, playbutton, listbox, g, a
    if c == 0:
        player.play(musics[i])
        playbutton.set_image(imgstop)
        c += 1
    elif c%2 == 1:
        player.pause = True
        playbutton.set_image(imgplay)
        c += 1
    elif c%2 == 0:
        player.pause = False
        playbutton.set_image(imgstop)
        c += 1



def nex(button):
    global i, c
    i += 1
    c = 0
    listbox.unselect_all()
    row = listbox.get_row_at_index(i)
    listbox.select_row(row)
    play()
nextbutton.connect("clicked", nex)

def perv(button):
    global i, c
    i -= 1
    c = 0
    listbox.unselect_all()
    row = listbox.get_row_at_index(i)
    listbox.select_row(row)
    play()
pervbutton.connect("clicked", perv)

def b1(button):
    global c
    play()
playbutton.connect("clicked", b1)

def get_title(entry):
    return entry.name

def add_music(entry):
    musics.append(entry.path)
    title = get_title(entry)
    music_label = Gtk.Label(label=title)
    listbox.add(music_label)

def add_music_from(directory):
    for entry in os.scandir(directory):
        if entry.is_dir():
            add_music_from(entry.path)
        elif entry.is_file() and entry.path.endswith('.mp3'):
            add_music(entry)

music_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_MUSIC)
add_music_from(music_dir)


grid = Gtk.Grid()
grid.set_row_spacing(5)
grid.set_column_spacing(5)
win.add(grid)
grid.attach(scrolledwin,0,0,100,100)
scrolledwin.add(listbox)
grid.attach(playbutton,50,101,1,1)
grid.attach(nextbutton,51,101,1,1)
grid.attach(pervbutton,49,101,1,1)


def li(listbox, listboxrow):
    global musics, i, c, a, g
    c = 0
    i = listboxrow.get_index()
    if g==0:
        a = listboxrow
    g += 1
    play()

listbox.connect("row-activated", li)



win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
