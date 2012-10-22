from __future__ import division
from grapefruit import Color
from PIL import Image

def color_to_ints(color):
    # Gray out illegal colors.
    if not color.isLegal:
        color = Color.NewFromHtml('gray')
    return color.intTuple

def interpolate(start, end, amount):
    return start + (end - start) * amount

for size in (16, 128, 512, 1024):
    img = Image.new('RGB', (size, size), 'white')
    pixels = img.load()

    for l in range(5, 100, 5):
        for x in range(size):
            a = interpolate(-1.0, 1.0, x / size)
            for y in range(size):
                b = interpolate(-1.0, 1.0, y / size)
                color = Color.NewFromLab(l, a, b)
                pixels[x,y] = color_to_ints(color)

        name = 'CIELAB_{}_L{:02d}.png'.format(size, int(l))
        print(name)
        img.save(name)

    for a_index in range(1, 19 + 1):
        a = interpolate(-1.0, 1.0, a_index / 20)
        for x in range(size):
            b = interpolate(-1.0, 1.0, x / size)
            for y in range(size):
                l = interpolate(100.0, 0.0, y / size)
                color = Color.NewFromLab(l, a, b)
                pixels[x,y] = color_to_ints(color)

        name = 'CIELAB_{}_a{:02d}.png'.format(size, a_index)
        print(name)
        img.save(name)

    for b_index in range(1, 19 + 1):
        b = interpolate(-1.0, 1.0, b_index / 20)
        for x in range(size):
            a = interpolate(-1.0, 1.0, x / size)
            for y in range(size):
                l = interpolate(100.0, 0.0, y / size)
                color = Color.NewFromLab(l, a, b)
                pixels[x,y] = color_to_ints(color)

        name = 'CIELAB_{}_b{:02d}.png'.format(size, b_index)
        print(name)
        img.save(name)
