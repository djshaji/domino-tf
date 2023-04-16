import gi
import array
import os
import tempfile
from six.moves.urllib.request import urlopen
from six import BytesIO
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
import io
import util

# For measuring the inference time.
import time

from ui import UI

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gio, GLib

class Gtk3 (UI):
    window = None
    keymap = dict ()
    models = dict ()
    
    def detect (self, path):
        print (path)
        vector = path.split ("|")
        if vector [0] in self.models:
            object_detect = self.models [vector [0]]
            path = util.download_and_resize_image (vector [1])
            img = object_detect.run_detector (path)
            img = util.tf_to_image (img)
            self.set_image (img)
            util.ding ()
            
        
    def hotkeys (self, widget, event):
        print (f'{event.keyval}')
        if event.keyval == 65293:
            text = widget.get_text ()
            if "#" in text:
                cmd = text.split ("#")
                if cmd [0] in self.keymap:
                    self.keymap [cmd [0]](cmd[1])
        
        
    def create_window (self):
        self.window = Gtk.Window ()
        self.window.resize (800, 600)
        self.box = Gtk.VBox ()
        self.window.add (self.box)
        self.img = Gtk.Image ()
        self.img.set_from_pixbuf (GdkPixbuf.Pixbuf.new_from_file (os.getcwd () + "/logo.png"))
        self.box.pack_start (self.img, True, True, 10)
        self.entry = Gtk.Entry ()
        self.entry.connect ("key-press-event", self.hotkeys)
        self.box.pack_start (self.entry, False, False, 10)
        self.window.show_all ()
        self.window.connect("destroy", Gtk.main_quit)
        self.keymap ["detect"] = self.detect
        
    def __init__ (self):
        self.create_window ()

    def download_and_resize_image(self, url, new_width=256, new_height=256):
        _, filename = tempfile.mkstemp(suffix=".jpg")
        response = urlopen(url)
        image_data = response.read()
        image_data = BytesIO(image_data)
        pil_image = Image.open(image_data)
        pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
        pil_image_rgb = pil_image.convert("RGB")
        pil_image_rgb.save(filename, format="JPEG", quality=90)
        print("Image downloaded to %s." % filename)
        return filename

    def pillow_to_pixbuf (self, image):
        contents = None
        with io.BytesIO() as output:
            image.save(output, format="JPEG")
            contents = output.getvalue()
        _b = GLib.Bytes.new (contents)
        stream = Gio.MemoryInputStream.new_from_bytes(_b)
        pixbuf = GdkPixbuf.Pixbuf.new_from_stream(stream, None)
        return pixbuf

    def set_image (self, img):
        pixbuf = self.pillow_to_pixbuf (img)
        self.img.set_from_pixbuf (pixbuf)
