from PIL import Image, ImageChops
import os
import time


# config
# * set bg_color to RGB or None to use image default bg color
config = {
    'in_dir': 'csgCategory',
    'width': 90,
    'height': 90,
    'bg_color': (255, 255, 255),
    'quality': 100
}

# end config

# create out directory
out_dir = f'{config["in_dir"]}--completed'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)


# open directory and create image array
all_images = os.listdir(config['in_dir'])

# for each
for image_name in all_images:
    img = Image.open(f'{config["in_dir"]}/{image_name}')
    print(f'Processing -> {image_name}')

    # grab pixel 0,0 to discover base color of BG and calculate where to crop
    bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()

    # loop over images and crop them down to the edge of image
    if bbox:
        cropped_img = img.crop(bbox)
    else:
        cropped_img = img

    # resize (keep  ratio) -> in some cases this might actually scale the image UP
    wpercent = (config['width']/float(cropped_img.size[0]))
    hsize = int((float(cropped_img.size[1])*float(wpercent)))
    sized_img = cropped_img.resize(
        (config['width'], hsize), Image.ANTIALIAS)

    # add bg to make it a square
    x, y = sized_img.size
    if x != y:
        # get the bg color
        rgb_img = img.convert('RGB')
        r, g, b = config['bg_color'] if config['bg_color'] else rgb_img.getpixel(
            (0, 0))

        size = max(config['width'], x, y)
        final_img = Image.new('RGBA', (size, size), (r, g, b, 0))
        final_img.paste(
            sized_img, (int((size - x) / 2), int((size - y) / 2)))
    else:
        final_img = cropped_img

    # save
    if final_img.mode != 'RGB':
        final_img = final_img.convert('RGB')
    # one last final resize
    final_img = final_img.resize(
        (config['width'], config['height']), Image.ANTIALIAS)
    final_img.save(f'{out_dir}/{image_name}', quality=config['quality'])
    print(f'{image_name} saved to {out_dir}')
