from ui import UI
from models.object import ObjectDetect
import gi
import sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

ui = UI ()
object_detect = ObjectDetect ()
path = ui.download_and_resize_image (sys.argv [1])
img = object_detect.run_detector (path)
ui.set_image (img)

Gtk.main ()
