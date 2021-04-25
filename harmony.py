import numpy as np


SCALES = {
    'major': [2, 2, 1, 2, 2, 2, 1],
    'mixolydian': [2, 2, 1, 2, 2, 1, 2],
    'dorian': [2, 1, 2, 2, 2, 1, 2],
}


STACKS = {}
for key in SCALES:
    scale = SCALES[key] * 2
    triads = [e + o for e, o in zip(scale[0::2], scale[1::2])]
    STACKS[key] = np.cumsum(triads)


def get_stack(note: int, scale: str):
    return [note + s for s in STACKS[scale]]