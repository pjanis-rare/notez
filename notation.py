import cmocean.cm
import numpy as np


NAME = {
    'notez': ["ki", "ko", "ku", "li", "lo", "lu", "vi", "vo", "vu", "mi", "mo", "mu",],
    'notez_alt': ["ki", "vo", "lu", "mi", "ko", "vu", "li", "mo", "ku", "vi", "lo", "mu",],
    'trad': ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G",],
}


DIV = 24
HSTEP = 3.5 * 3 ** 0.5 / DIV
WSTEP = 1.5 / DIV


def get_color(note: int):
    x = note % 12 / 12
    r, g, b, _ = cmocean.cm.phase(x)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    return r, g, b


def get_name(note: int, system: str):
    n = note % 12
    octave = note // 12
    name = NAME[system][n]

    return name, octave


def get_positions(note: int):
    y = 1.0 - (note + 11) * HSTEP / 3.5
    x = -0.1
    p = []
    idx = []
    for i in range(30):
        if -0.1 <= x <= 1.6 and -0.1 <= y <= 1.1:
            p.append(np.array([x, y]))
            idx.append(i)
        y += HSTEP * 0.9
        x += WSTEP
        
    return p, idx

    return p