ALLOWED_EXTENSIONS = ["bmp", "jpg", "jpeg", "png", "tiff", "webp", "svg"]


def allowed_file(filename):
    if "." in filename:
        ext = filename.rsplit(".", 1)[1]
        if ext.lower() in ALLOWED_EXTENSIONS:
            return True
    return False


from string import ascii_letters, digits
import os, random


def get_file_hash():
    while True:
        hash = "".join([random.choice(ascii_letters + digits) for n in range(10)])
        for i in os.listdir("/tmp"):
            if i.startswith(hash):
                continue
        return hash


from PIL import Image

def get_file_details(file):
    img = Image.open(file)
    width = img.width
    height = img.height 
    img.close()
    return width, height

def get_file_size(file):
    return os.path.getsize(file) # in bytes
