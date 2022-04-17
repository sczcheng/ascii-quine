"""
python3 asciiart.py [-h] [--reverse] [--quine] imgpath width
generate ascii art that looks like image at imgpath to standard output
"""

from brightness import createdict

import PIL.Image
import PIL.ImageEnhance

asciidict = {'0': 0.6219938508191888, '1': 0.476772101250895, '2': 0.6084319588931475, '3': 0.5928484184812366, '4': 0.6567409341700712, '5': 0.6452006907298994, '6': 0.6619214084151118, '7': 0.44880596386303334, '8': 0.7336478119866908, '9': 0.6606578781114434, 'a': 0.6128121972791981, 'b': 0.7433769953249378, 'c': 0.4944615255022533, 'd': 0.7417344059301689, 'e': 0.6488649286105378, 'f': 0.6376195089078887, 'g': 0.7836414943351725, 'h': 0.6906456639851746, 'i': 0.45878785326201404, 'j': 0.5300930800657035, 'k': 0.693551783683612, 'l': 0.4925662300467506, 'm': 0.7727330160468349, 'n': 0.5824453523143663, 'o': 0.5181316598576422, 'p': 0.7914753822179169, 'q': 0.793033736259108, 'r': 0.4995156467169271, 's': 0.5544792149265046, 't': 0.5105504780356316, 'u': 0.5586909826053995, 'v': 0.5139620098555364, 'w': 0.67560965337152, 'x': 0.6426736301225624, 'y': 0.6786000084235354, 'z': 0.5544792149265046, 'A': 0.8106389251568884, 'B': 0.861390725687571, 'C': 0.5834561765573011, 'D': 0.7199174493534937, 'E': 0.8154403403108285, 'F': 0.6989007286358084, 'G': 0.71966474329276, 'H': 0.8324979994103525, 'I': 0.5320304931979952, 'J': 0.5631133386682391, 'K': 0.8073958640441393, 'L': 0.6049783093964537, 'M': 1.0, 'N': 0.8872930969127742, 'O': 0.6465484563871456, 'P': 0.7067767341953418, 'Q': 0.8717516741776523, 'R': 0.8120288084909236, 'S': 0.6679442361959315, 'T': 0.6678178831655646, 'U': 0.6898454281261845, 'V': 0.6464642210335678, 'W': 0.9337488944109843, 'X': 0.7809880806974687, 'Y': 0.6198458493029525, 'Z': 0.6743461230678516, '!': 0.27843996125173737, '#': 0.8661921408415112, '$': 0.6957419028766373, '&': 0.6015667775765489, '(': 0.3794381501916354, ')': 0.37926967948447965, '*': 0.4007075769700543, '+': 0.3754369708966853, ',': 0.12235185107189488, '-': 0.17958977382807564, '.': 0.07640146569515226, '/': 0.3609063724044982, ':': 0.15284504906709345, ';': 0.1697763551362507, '<': 0.4309480689045192, '=': 0.46034620730320513, '>': 0.43183254011708716, '?': 0.38722992039759085, '[': 0.44623678557890745, ']': 0.44615255022532957, '^': 0.22035968495977762, '_': 0.28286231731457695, '`': 0.05172050709682854, '|': 0.3324348228951691, '~': 0.21736932990776228, ' ': 0.0}

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
