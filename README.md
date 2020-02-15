# Cool Image Bro 📷

A Python script to assist transforming not square images into square images. It _should_ work reasonably well to scale images both up and down. It works _reasonably_ well with poorly compressed and noisy images.

## What I Need? 🤷‍♂

1. [Python 3. X](https://www.python.org/downloads/) - I used 3.8.1, so I'd suggest that version; but hey, you do you.

1. Lots of images that aren't square.

1. A little knowledge of working with code/CLI -> there's no GUI. 😢

## How 'Dis Work 🧙‍♂️

1. Put your image directory in the same directory as this script.

1. switch to the Python env (unless you want to install, or already have, the necessary libraries installed).

   1. Mac/Linux type `source ./Scripts/activate`
   1. Windows ([sorry](https://docs.python.org/3/library/venv.html))

1. Open `crop_n_resize.py` in any text or code editor. And change the `config` settings at the top of the file and save.

1. From command line simply run the script with `python crop_n_resize.py` (or whatever command you use for python).

1. Chill

## Output 💩

1. There will be two folders a `xxxx--completed` and a `xxxx--failed` directory as well as a timestamped log file.

1. Everything in the `xxxx--completed` directory _should_ be correct (see gotchas below).

1. Everything in the `xxx--failed` folder will be an image that for one reason or antother was unable to be processed correctly.

## Gotchas 🦀

1. Images that don't have a solid border color won't work properly (basically this script uses the top left pixel to define the background color that is needed to crop AND to figure out what color to use to complete the square).

1. Images that have multiple background colors won't work as good as those with one solid background color (see above).

1. You'll still have to visually inspect the `xxxx--completed` folder as images will not 'fail' if the background color is unusual (as explained above)

1. I recommend removing any images that don't have a solid border color before running the script.
