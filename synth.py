import numpy as np
import pygame

import notation


FREQ = [
    207.65,
    220,
    233.08,
    246.94,
    261.63,
    277.18,
    293.66,
    311.13,
    329.63,
    349.23,
    369.99,
    392,
]


def frequency(note: int):
    n = note % 12
    octave = note // 12 - 2
    freq = FREQ[n]
    freq = freq * 2 ** octave

    return(freq)

class Synth:
    def __init__(self, fs: int):
        self.fs = fs

        self.sounds = []
        t = np.array(range(fs))
        t = np.tile([t, t], 2).T

        for n in range(64):
            f = frequency(n)
            waveform = np.sin(t * f / fs * 2 * np.pi)
            waveform = np.sign(waveform) * np.abs(waveform) ** 0.6
            waveform *= 100 * 500 / f
            waveform = waveform.astype(np.int16)
            waveform = np.ascontiguousarray(waveform)
            self.sounds.append(pygame.sndarray.make_sound(waveform))

    def play(self, note: int, stack: list):
        if note < len(self.sounds):
            self.sounds[note].play(loops = -1)
            self.sounds[note-12].play(loops = -1)
        if stack[0] < len(self.sounds):
            self.sounds[stack[0]].play(loops = -1)
        if stack[2] < len(self.sounds):
            self.sounds[stack[2]].play(loops = -1)

    def stop(self, note: int, stack: list):
        if note < len(self.sounds):
            self.sounds[note].stop()
            self.sounds[note-12].stop()
        if stack[0] < len(self.sounds):
            self.sounds[stack[0]].stop()
        if stack[2] < len(self.sounds):
            self.sounds[stack[2]].stop()
