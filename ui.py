import gi
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

class UI ():
    window = None
    def create_window (self):
        self.window = Gtk.Window ()
        self.window.resize (800, 600)
        self.box = Gtk.VBox ()
        self.window.add (self.box)
        self.img = Gtk.Image ()
        self.img.set_from_pixbuf (GdkPixbuf.Pixbuf.new_from_file (os.getcwd () + "/logo.png"))
        self.box.pack_start (self.img, True, True, 10)
        self.entry = Gtk.Entry ()
        self.box.pack_start (self.entry, False, False, 10)
        self.window.show_all ()
        self.window.connect("destroy", Gtk.main_quit)
        
    def __init__ (self):
        self.create_window ()
