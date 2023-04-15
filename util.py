import playsound
from six.moves.urllib.request import urlopen
from six import BytesIO
import os
import tempfile
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
from time import gmtime, strftime

def timestamp ():
    return strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

def have_x ():
    if "DISPLAY" in os.environ:
        return True
    return False
def download_and_resize_image(url, new_width=256, new_height=256):
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

def tf_to_image (data):
    img = Image.fromarray(data, 'RGB')
    return img

def ding ():
    playsound.playsound ("/usr/share/sounds/freedesktop/stereo/complete.oga")
