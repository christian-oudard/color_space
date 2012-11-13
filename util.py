import math

def interpolate(start, end, amount):
    return start + (end - start) * amount

def chroma_hue_to_ab(chroma, hue):
    a = math.sin(math.radians(hue)) * chroma
    b = math.cos(math.radians(hue)) * chroma
    return a, b
