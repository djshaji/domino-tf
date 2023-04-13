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

# For measuring the inference time.
import time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gio, GLib

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
