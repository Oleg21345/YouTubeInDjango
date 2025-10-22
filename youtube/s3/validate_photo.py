from PIL import Image


def validate_image_size(photo_file, min_ratio=1.7, max_ratio=1.8):
    image = Image.open(photo_file)
    width, height = image.size
    ratio = width / height
    print(f"DEBUG image size: {width}x{height}, ratio={ratio}")
    if not (min_ratio <= ratio <= max_ratio):
        raise ValueError(f"The image must be approximately in 16:9 format (currently {width}x{height})")
