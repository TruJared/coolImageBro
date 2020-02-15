from PIL import Image, ImageChops
from os import listdir

# todo allow for custom bg color

# config
config = {
    'in_dir': 'cg-images',
    'width': 90
}

# todo create out dir

# open directory and create image array
all_images = listdir(config['in_dir'])

# for each
for image_name in all_images:
    img = Image.open(f'{config["in_dir"]}/{image_name}')
    print(image_name)

    # grab pixel 0,0 to discover base color of BG and calculate where to crop
    # * in case nothing works we can just spit out the original image
    final_image = img
    # todo convert this bg to RGBA
    bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()

    # loop over images and crop them down to the edge of image
    if bbox:
        cropped_img = img.crop(bbox)

        # resize (keep  ratio) -> not sure if this step is needed
        wpercent = (90/float(cropped_img.size[0]))
        hsize = int((float(cropped_img.size[1])*float(wpercent)))
        sized_img = cropped_img.resize((90, hsize), Image.ANTIALIAS)

        # add bg to make it a square
        x, y = sized_img.size
        if x != y:
            size = max(90, x, y)
            final_img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
            final_img.paste(
                sized_img, (int((size - x) / 2), int((size - y) / 2)))
        else:
            final_img = cropped_img
            # todo create err log
    # save
    if final_img.mode != 'RGB':
        final_img = final_img.convert('RGB')

    final_img.save(f'{image_name}')
