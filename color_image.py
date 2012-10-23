from __future__ import division
import math
from grapefruit import Color
from PIL import Image

def color_to_ints(color):
    # Gray out illegal colors.
    if not color.isLegal:
        color = Color.NewFromHtml('gray')
    return color.intTuple

def interpolate(start, end, amount):
    return start + (end - start) * amount

def draw_lab_l_slice(image, l):
    width, height = image.size
    pixels = image.load()
    for x in range(width):
        a = interpolate(-1.0, 1.0, x / width)
        for y in range(height):
            b = interpolate(-1.0, 1.0, y / height)
            color = Color.NewFromLab(l, a, b)
            pixels[x,y] = color_to_ints(color)

def draw_lab_a_slice(image, a):
    width, height = image.size
    pixels = image.load()
    for x in range(width):
        b = interpolate(-1.0, 1.0, x / width)
        for y in range(height):
            l = interpolate(100.0, 0.0, y / height)
            color = Color.NewFromLab(l, a, b)
            pixels[x,y] = color_to_ints(color)

def draw_lab_b_slice(image, b):
    width, height = image.size
    pixels = image.load()
    for x in range(width):
        a = interpolate(-1.0, 1.0, x / width)
        for y in range(height):
            l = interpolate(100.0, 0.0, y / height)
            color = Color.NewFromLab(l, a, b)
            pixels[x,y] = color_to_ints(color)

def draw_lab_l_cylinder(image, l):
    width, height = image.size
    pixels = image.load()
    for x in range(width):
        hue = interpolate(0, 360, x / width)
        for y in range(height):
            chroma = interpolate(1.0, 0.0, y / height)
            a = math.sin(math.radians(hue)) * chroma * math.sqrt(2)
            b = math.cos(math.radians(hue)) * chroma * math.sqrt(2)
            color = Color.NewFromLab(l, a, b)
            pixels[x,y] = color_to_ints(color)

def draw_lab_hue_cylinder(image, hue):
    width, height = image.size
    pixels = image.load()
    for x in range(width):
        chroma = interpolate(0.0, 1.0, x / width)
        for y in range(height):
            l = interpolate(100.0, 0.0, y / height)
            a = math.sin(math.radians(hue)) * chroma * math.sqrt(2)
            b = math.cos(math.radians(hue)) * chroma * math.sqrt(2)
            color = Color.NewFromLab(l, a, b)
            pixels[x,y] = color_to_ints(color)

def make_lab_slices():
    for size in (16, 128, 512, 1024):
        img = Image.new('RGB', (size, size), 'white')

        for l in range(5, 100, 5):
            draw_lab_l_slice(img, l)
            name = 'CIELAB_{}_L{:02d}.png'.format(size, int(l))
            print(name)
            img.save(name)

        for a_index in range(1, 19 + 1):
            a = interpolate(-1.0, 1.0, a_index / 20)
            draw_lab_a_slice(img, a)
            name = 'CIELAB_{}_a{:02d}.png'.format(size, a_index)
            print(name)
            img.save(name)

        for b_index in range(1, 19 + 1):
            b = interpolate(-1.0, 1.0, b_index / 20)
            draw_lab_b_slice(img, b)
            name = 'CIELAB_{}_b{:02d}.png'.format(size, b_index)
            print(name)
            img.save(name)

def make_lab_cylinders():
    for width, height in [(360, 100), (360*4, 100*4)]:
        for l in range(5, 100, 5):
            img = Image.new('RGB', (width, height), 'white')
            draw_lab_l_cylinder(img, l)
            name = 'CIELAB_CYLINDER_{}x{}_L{:02d}.png'.format(width, height, int(l))
            print(name)
            img.save(name)

def make_lab_spokes():
    for width, height in [(128, 128), (512, 512)]:
        for hue in range(0, 360, 5):
            img = Image.new('RGB', (width, height), 'white')
            draw_lab_hue_cylinder(img, hue)
            name = 'CIELAB_CYLINDER_{}x{}_hue{:03d}.png'.format(width, height, hue)
            print(name)
            img.save(name)

if __name__ == '__main__':
    #make_lab_slices()
    #make_lab_cylinders()
    make_lab_spokes()
