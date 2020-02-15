from PIL import Image, ImageChops
import os
import time


# config

config = {
    'in_dir': 'cg-images',
    'width': 90
}

# end config

# create directories and error log file
error_log = f'{config["in_dir"]}--{time.time()}.log'
out_dir = f'{config["in_dir"]}--completed'
failed_dir = f'{config["in_dir"]}--failed'
for directory in [out_dir, failed_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)


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

        # resize (keep  ratio) -> not sure if this step is needed
        wpercent = (config['width']/float(cropped_img.size[0]))
        hsize = int((float(cropped_img.size[1])*float(wpercent)))
        sized_img = cropped_img.resize(
            (config['width'], hsize), Image.ANTIALIAS)

        # add bg to make it a square
        x, y = sized_img.size
        if x != y:
            # get the bg color
            rgb_img = img.convert('RGB')
            r, g, b = rgb_img.getpixel((0, 0))

            size = max(config['width'], x, y)
            final_img = Image.new('RGBA', (size, size), (r, g, b, 0))
            final_img.paste(
                sized_img, (int((size - x) / 2), int((size - y) / 2)))
        else:
            final_img = cropped_img

        # save
        if final_img.mode != 'RGB':
            final_img = final_img.convert('RGB')

        final_img.save(f'{out_dir}/{image_name}')
        print(f'{image_name} saved to {out_dir}')
    else:
        # these are proably really bad :(
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(f'{failed_dir}/{image_name}')
        print(f'{image_name} possibly not cool, saving to {failed_dir}.')

        with open(error_log, 'a') as fp:
            fp.write(
                f'{image_name} possibly not cool, saving to {failed_dir}. \n')
