from __future__ import division

from grapefruit import Color
from util import chroma_hue_to_ab

def transition_point(func, lo, hi, epsilon=10e-5, depth=0):
    """
    Find the place where a boolean function changes from True to False.

    Arguments are a function "func", and bounds "lo" and "hi", where func(lo)
    is True and func(hi) is False.

    >>> import math
    >>> def func(x):
    ...     return x < math.pi
    >>> result = transition_point(func, 3, 4)
    >>> print('{:.4f}'.format(math.pi))
    3.1416
    >>> print('{:.4f}'.format(result))
    3.1416
    """
    if depth == 0:
        assert lo < hi
        assert func(lo) is True
        assert func(hi) is False

    if (hi - lo) < epsilon:
        return lo

    midpoint = (lo + hi) / 2

    value = func(midpoint)
    if value is True:
        return transition_point(func, midpoint, hi, epsilon, depth + 1)
    elif value is False:
        return transition_point(func, lo, midpoint, epsilon, depth + 1)

def most_colorful_lightness():
    """
    What is the lightness value that can express the highest chroma in all hues?
    Equivalently, at what lightness level can you draw the biggest circle around
    neutral gray without going out of gamut?

    Answer: L74, with chroma 0.4
    """
    best_lightness = 0
    best_chroma = 0
    for lightness in range(0, 100):
        chroma = min_global_chroma(lightness)
        if chroma > best_chroma:
            best_chroma = chroma
            best_lightness = lightness
    return best_lightness, best_chroma

def peak_chroma_color():
    """
    What is the color with the highest chroma value?
    """
    best_chroma = 0
    best_color = None
    for lightness in range(0, 100):
        for hue in range(0, 360):
            chroma = max_chroma(hue, lightness)
            if chroma > best_chroma:
                best_chroma = chroma
                a, b = chroma_hue_to_ab(chroma, hue)
                best_color = Color.NewFromLab(lightness, a, b)
    return best_color, best_chroma
    #1.3187713623046875
    ##0a0cff
    #(32.9999966526222, 0.7751544267050672, -1.0669084698150417)

def peak_chroma_color_scipy():
    """
    Most intensely chromatic color:
    #0000ff
    L 32.310726263632034
    a 0.79175287142984774
    b -1.0784594584851654
    chroma: 1.3378890973099862
    """

    import scipy.optimize
    import math

    guess = (33, 0.7, -0.9)

    def chroma(l, a, b):
        color = Color.NewFromLab(l, a, b)
        if not color.isLegal:
            return -1
        return math.sqrt(a**2 + b**2)

    def f(x):
        l, a, b = x
        return -chroma(l, a, b)

    l, a, b = scipy.optimize.fmin(f, guess, xtol=1e-5)
    return Color.NewFromLab(l, a, b), chroma(l, a, b)

def max_chroma(hue, lightness):
    def valid_for_chroma(chroma):
        a, b = chroma_hue_to_ab(chroma, hue)
        color = Color.NewFromLab(lightness, a, b)
        return color.isLegal
    return transition_point(valid_for_chroma, 0.0, 1.5)

def min_global_chroma(lightness):
    """
    For the given lightness, what is the lowest chroma that crosses the edge of
    the gamut?
    """
    return min(
        max_chroma(hue, lightness)
        for hue in range(0, 360)
    )
#print(most_colorful_lightness())
#color, chroma = peak_chroma_color()
color, chroma = peak_chroma_color_scipy()
print(chroma)
print(color.html)
print(color.lab)

