from gtk3 import Gtk3
#from models.object import ObjectDetect
from models.movienet import MoviNet
import gi
import sys

import util

_x = util.have_x ()

if (_x):
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
    gtk3 = Gtk3 ()
    Gtk.main_iteration_do (False)
    
#object_detect = ObjectDetect ()
#path = util.download_and_resize_image (sys.argv [1])

movi = MoviNet ()
movi.load_file (sys.argv [1])
#img = object_detect.run_detector (path)
#img = util.tf_to_image (img)
if _x:
#    gtk3.models ["object"] = object_detect
    #img = ui.pillow_to_pixbuf (img)
#    gtk3.set_image (img)
    Gtk.main_iteration_do (False)
    movi.detect (gtk3)
    util.ding ()
    Gtk.main ()
else:
#    img.save('output.jpg')
    util.ding ()
