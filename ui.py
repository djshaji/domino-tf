import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class UI ():
    window = None
    def create_window (self):
        self.window = Gtk.Window ()
        self.window.set
        self.window.show_all ()
        self.window.connect("destroy", Gtk.main_quit)
        
    def __init__ (self):

