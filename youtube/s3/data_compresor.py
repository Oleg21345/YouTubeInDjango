import PIL
from PIL import Image, ImageOps
from django.contrib import messages
import io


def compress_photo(photo):
    base_width = 360
    image = Image.open(photo)
    image = ImageOps.exif_transpose(image)
    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")
    MAX_SIZE = (8000, 8000)
    if image.size[0] > MAX_SIZE[0] or image.size[1] > MAX_SIZE[1]:
        raise ValueError("Photo is too big!")

    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    image = image_without_exif
    width_persernt = (base_width / float(image.size[0]))
    hsize = int(float(image.size[1] * float(width_persernt)))
    image = image.resize((base_width, hsize), PIL.Image.Resampling.LANCZOS)

    buffer = io.BytesIO()
    image.save(buffer, format="WEBP", quality=80)
    buffer.seek(0)
    print(f"Image composed {buffer}")
    return buffer






