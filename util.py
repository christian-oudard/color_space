import math
from grapefruit import Color

def interpolate(start, end, amount):
    return start + (end - start) * amount

def chroma_hue_to_ab(chroma, hue):
    a = math.sin(math.radians(hue)) * chroma
    b = math.cos(math.radians(hue)) * chroma
    return a, b

def lab_chroma(l, a, b):
    color = Color.NewFromLab(l, a, b)
    if not color.isLegal:
        return 0
    return math.sqrt(a**2 + b**2)
