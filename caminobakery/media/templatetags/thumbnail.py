import os.path
from PIL import Image
from django.template import Library

register = Library()

SCALE_WIDTH = 'w'
SCALE_HEIGHT = 'h'
SCALE_BOTH = 'both'


def scale(max_x, pair):
    x, y = pair
    new_y = (float(max_x) / x) * y
    return (int(max_x), int(new_y))


@register.filter
def thumbnail(file, size='200w'):
    """
    Allows for thumbnailing photos based on width, height or both. You can also default to 200 width.

    Examples:

        <img src="{{ object.image.url }}" alt="original image">

        <img src="{{ object.image|thumbnail:"250w" }}" alt="image resized to 250w x (calculated/scaled)h ">

        <img src="{{ object.image|thumbnail:"250h" }}" alt="image resized to (calculated/scaled)w x 250h h ">

        <img src="{{ object.image|thumbnail:"250x200" }}" alt="image resized to 250wx200h ">

        <img src="{{ object.image|thumbnail }}" alt="image resized to default 200w (or whatever you default it to) format">

    """
    # defining the size
    if (size.lower().endswith('h')):
        mode = 'h'
        size = size[:-1]
        max_size = int(size.strip())
    elif (size.lower().endswith('w')):
        mode = 'w'
        size = size[:-1]
        max_size = int(size.strip())
    else:
        mode = 'both'

    # defining the filename and the miniature filename
    filehead, filetail = os.path.split(file.path)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
    filename = file.path
    miniature_filename = os.path.join(filehead, miniature)
    filehead, filetail = os.path.split(file.url)
    miniature_url = filehead + '/' + miniature
    if (os.path.exists(miniature_filename) and
       os.path.getmtime(filename) > os.path.getmtime(miniature_filename)):
            os.unlink(miniature_filename)
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        image = Image.open(filename)
        image_x, image_y = image.size

        if mode == SCALE_HEIGHT:
            image_y, image_x = scale(max_size, (image_y, image_x))
        elif mode == SCALE_WIDTH:
            image_x, image_y = scale(max_size, (image_x, image_y))
        elif mode == SCALE_BOTH:
            image_x, image_y = [int(x) for x in size.split('x')]
        else:
            raise Exception("Thumbnail size is ##w, ##h, or ##x## format.")

        image.thumbnail([image_x, image_y], Image.ANTIALIAS)
        try:
            image.save(
                miniature_filename, image.format, quality=90, optimize=1)
        except:
            image.save(miniature_filename, image.format, quality=90)

    return miniature_url
