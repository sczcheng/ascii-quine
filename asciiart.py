"""
python3 asciiart.py [-h] [--reverse] [--quine] imgpath width
generate ascii art that looks like image at imgpath to standard output
"""

from brightness import createdict

import PIL.Image
import PIL.ImageEnhance

asciidict = createdict()

def resize(image: PIL.Image.Image, new_width: int):
    width, height = image.size
    new_height = round(height * new_width / (2 * width))
    return image.resize((new_width, new_height))

def to_greyscale(image: PIL.Image.Image):
    return image.convert("L")

def asciifrompixel(v: int, reverse: bool):
    expectedval = v/255
    if reverse:
        expectedval = 1 - expectedval
    mindiff = 1
    minchar = None
    for c, val in asciidict.items():
        if abs(val-expectedval) < mindiff:
            mindiff = abs(val-expectedval)
            minchar = c
    return minchar

def pixel_to_ascii(image: PIL.Image.Image, reverse: bool):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += asciifrompixel(pixel, reverse)
    return ascii_str

def asciiart(path: str, width: int, reverse: bool) -> str:
    image = PIL.Image.open(path)

    image = resize(image, width).convert("RGBA")
    image = to_greyscale(image)

    enhancer = PIL.ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.4)

    ascii_str = pixel_to_ascii(image, reverse)

    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img_list=[]

    for i in range(0, ascii_str_len, img_width):
        ascii_img_list.append(ascii_str[i:i+img_width])
    
    ascii_img = '\n'.join(ascii_img_list)
    
    return ascii_img

def asciiquine(path: str, space: int, reverse: bool) -> str:
    if space <= 70:
        return asciiquine2(path, space, reverse)

    originalquinegen = """a='a=%r;print(a%%a);x=lambda s:print(f"x({s!r})")';print(a%a);x=lambda s:print(f"x({s!r})")"""
    if space < len(originalquinegen):
        space = len(originalquinegen)
    spaces_to_add = (space - len(originalquinegen)) // 2
    quinegen="""a='a=%r;""" + ' ' * spaces_to_add + """print(a%%a);x=lambda s:print(f"x({s!r})")';""" + ' ' * spaces_to_add + """print(a%a);x=lambda s:print(f"x({s!r})")"""
    innerwidth = len(quinegen) - 5

    ascii_inner = asciiart(path, innerwidth, reverse)

    ascii_img_list = []
    ascii_img_list.append(quinegen)
    for line in ascii_inner.split('\n'):
        ascii_img_list.append(f"x('{line}')")
    ascii_img = '\n'.join(ascii_img_list)

    return ascii_img

def asciiquine2(path: str, space: int, reverse: bool) -> str:
    smallquine = """a='a=%r\\nprint(a%%a);x=lambda s:print(f"x({s!r})")'
print(a%a);x=lambda s:print(f"x({s!r})")"""
    quinelines = smallquine.split('\n')
    innerwidth = len(quinelines[0])-5

    ascii_inner = asciiart(path, innerwidth, reverse)

    ascii_img_list = []
    ascii_img_list.extend(quinelines)
    for line in ascii_inner.split('\n'):
        ascii_img_list.append(f"x('{line}')")
    ascii_img = '\n'.join(ascii_img_list)

    return ascii_img


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="generate ascii art that looks like image at imgpath to standard output")
    parser.add_argument('imgpath', help="generate an ascii art that looks like the image located here")
    parser.add_argument('--width', type=int, default=100, help="resulting ascii art line width (best effort)")
    parser.add_argument('--reverse', action='store_true', help="reverse the color of the input image")
    parser.add_argument('--quine', action='store_true', help="generated ascii art is a quine, this flag ignores width")
    args = parser.parse_args()

    imgpath = args.imgpath
    width = args.width
    reverse =  args.reverse
    quine = args.quine

    if quine:
        result = asciiquine(imgpath, width, reverse)
    else:
        result = asciiart(imgpath, width, reverse)

    print(result)
