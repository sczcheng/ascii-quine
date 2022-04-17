"""
find the brightness of the given ascii character
"""
import string

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

mono = PIL.ImageFont.truetype("Courier New Bold.ttf", 20)

def filterallow(c):
    if c == ' ':
        return True
    if c.isspace():
        return False
    if c in "%%\'\"\\{}@":
        return False
    return True

allowed = list(filter(filterallow, string.printable))

def brightness(c: str) -> int:
    img = PIL.Image.new('RGB', (40, 40))
    d = PIL.ImageDraw.Draw(img)
    d.text((10, 10), c, fill=(255, 255, 255), font=mono)
    data = img.getdata(1) # get red data
    brightnessc = sum(data)
    return brightnessc

def createdict() -> dict[str, float]:
    maxb = max([ brightness(c) for c in allowed ])
    brightnessdict = { c: brightness(c)/maxb for c in allowed }
    return brightnessdict

if __name__ == '__main__':
    d = list(createdict().items())
    print(createdict())
    d.sort(key=lambda t: t[1])
    for key, val in d:
        print(key, val)
