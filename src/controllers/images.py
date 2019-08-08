import random

from flask import Blueprint, send_file, request
from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO

images = Blueprint('images', __name__)

SCALE = 500
QUALITY = 75
BOX_HEIGHT = 32
BOX_WIDTH = 32

FILLS = (
    (129, 252, 237),
    (255, 202, 88),
    (111, 255, 176)
)

def create_image(drawer, height, width):
    drawer.rectangle([(0, 0), (width, height)], fill=(255, 255, 255))

    for y in range(0, height):
        for x in range(0, width):
            if (x % BOX_WIDTH == 0) and (y % BOX_WIDTH == 0):
                if random.choice([False, True]):
                    fill = random.choice(FILLS)
                    drawer.rectangle([(x, y), (x + BOX_WIDTH, y + BOX_HEIGHT)], fill=fill)

def add_filter(image, height, width):
    return image.filter(ImageFilter.GaussianBlur(radius=6))

@images.route('/repo')
@images.route('/repo/<int:height>')
@images.route('/repo/<int:height>/<int:width>')
def get_repo_image(height=256, width=1024):
    buffer = BytesIO()
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    create_image(draw, height, width)

    if request.args.get('filter', 'false').lower() == 'true':
        image = add_filter(image, height, width)

    image.save(buffer, 'JPEG', quality=QUALITY)
    buffer.seek(0)

    return send_file(buffer, mimetype="image/jpeg")
