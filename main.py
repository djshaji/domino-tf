from ui import UI
from models.object import ObjectDetect
import gi
import sys

import util

_x = util.have_x ()

if (_x):
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
    ui = UI ()
    
object_detect = ObjectDetect ()
path = util.download_and_resize_image (sys.argv [1])

img = object_detect.run_detector (path)
img = util.tf_to_image (img)
if _x:
    #img = ui.pillow_to_pixbuf (img)
    ui.set_image (img)
    util.ding ()
    Gtk.main ()
else:
    img.save('output.jpg')
    util.ding ()
