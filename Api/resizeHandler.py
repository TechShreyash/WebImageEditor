from PIL import Image


def resizeImage(max_height, max_width, hash):
    img = Image.open(f"/tmp/{hash}")
    width, height = img.size
    resize_ratio = min(max_width / width, max_height / height)
    new_width, new_height = int(width * resize_ratio), int(height * resize_ratio)
    img = img.resize((int(new_width), int(new_width)))
    img.save(f"/tmp/{hash}")
    return hash
