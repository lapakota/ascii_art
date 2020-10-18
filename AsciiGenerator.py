import argparse
import sys
import Viewer
import tkinter as tk

from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

GRAYSCALE_40 = r"B@&#MZWO0QbdpqwmoazunxrctiI1?l!+~;:-_,`."
GRAYSCALE_10 = '@%#J+=-:.'
GRAYSCALE_DOUBLE = '01'
SYMBOL_WIDTH, SYMBOL_HEIGHT = 11, 17
FONT = ImageFont.truetype('Lucon.ttf', 19)


def create_ascii_txt(image, new_width, new_height, symbols):
    image = image.resize((new_width, new_height))
    image = image.convert('L')
    pixels = image.getdata()
    interval = int(256 / len(symbols)) + 1
    new_pixels = ''.join([symbols[pixel // interval] for pixel in pixels])
    new_pixels_count = len(new_pixels)
    ascii_text = [new_pixels[index:index + new_width]
                  for index in range(0, new_pixels_count, new_width)]
    ascii_text = "\n".join(ascii_text)

    return ascii_text


def create_ascii_image(image, new_width, new_height, symbols):
    image = image.resize((new_width, new_height),
                         Image.NEAREST, reducing_gap=1.5)
    pixels = image.load()
    symbols = list(symbols[::-1])
    interval = len(symbols[::-1]) / 256
    ascii_image = Image.new(mode='RGB',
                            size=(new_width * SYMBOL_WIDTH,
                                  new_height * SYMBOL_HEIGHT),
                            color=(30, 30, 30))  # dark grey
    draw = ImageDraw.Draw(ascii_image)
    for i in range(new_height):
        for j in range(new_width):
            r, g, b = pixels[j, i]
            shade_of_gray = int(r / 3 + g / 3 + b / 3)
            draw.text((j * SYMBOL_WIDTH, i * SYMBOL_HEIGHT),
                      (symbols[int(shade_of_gray * interval)]),
                      font=FONT, fill=(r, g, b))
    return ascii_image


def check_width_and_height(width, height):
    return width > 0 and height > 0

def check_mode(args):
    if args.mode:
        if args.mode == "10":
            return GRAYSCALE_10
        if args.mode == "40":
            return GRAYSCALE_40
        if args.mode == "double":
            return GRAYSCALE_DOUBLE
        else:
            return False


def check_ansi_file(args):
    if Path(args.image).suffix == ".ansi":
        return True


def parse_args(args):
    parser = argparse.ArgumentParser(description='Convert image to ascii art')
    parser.add_argument('--image', dest='image',
                        help='Input image name', required=True)
    parser.add_argument('--width', dest='width',
                        help='Input width of ascii art in symbols',
                        required=False)
    parser.add_argument('--height', dest='height',
                        help='Input height of ascii art in symbols',
                        required=False)
    parser.add_argument('--scale', dest='scale',
                        help="Input scale (max scale = 1)",
                        default=0.2, required=False)
    parser.add_argument('--mode', dest='mode',
                        help='Input mode name [10],[40],[double]',
                        default="40", required=False)
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    if check_ansi_file(args):
        with open(args.image) as f:
            print(f.read())
            sys.exit(1)
    image = Image.open(args.image)
    width, height = image.size
    scale = float(args.scale)
    new_width = int(width * scale)
    new_height = int(scale * height * (SYMBOL_WIDTH / SYMBOL_HEIGHT))
    if args.width:
        new_width = int(args.width)
        new_height = int((SYMBOL_WIDTH / SYMBOL_HEIGHT)
                         * (new_width * height) / width)
    if args.height:
        new_height = int(args.height)
        new_width = int((SYMBOL_HEIGHT / SYMBOL_WIDTH)
                        * (new_height * width) / height)
    if args.width and args.height:
        new_width = int(args.width)
        new_height = int(args.height)
    if not check_width_and_height(new_width, new_height):
        print("Width must be > 0 and Height must be > 0")
        sys.exit(1)
    if not check_mode(args):
        print("Wrong mode")
        sys.exit(1)
    mode = check_mode(args)
    out_file_name = "ascii_string.txt"
    ascii_art = create_ascii_txt(image, new_width, new_height, mode)
    with open(out_file_name, "w") as f:
        f.write(ascii_art)
    out_image = create_ascii_image(image, new_width, new_height, mode)
    out_image.save("ascii_photo.png")
    print("Converting done.", "Ascii art was saved to: " + out_file_name,
          "Please wait, soon you will see generated image.", sep="\n")
    window = tk.Tk()
    window.geometry(str(int(out_image.width / 2))
                    + 'x'
                    + str(int(out_image.height / 2)))
    Viewer.Zoomer(window, path='ascii_photo.png')
    window.mainloop()


if __name__ == '__main__':
    main()
