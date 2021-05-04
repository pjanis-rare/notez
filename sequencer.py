import cfg
import harmony
from synth import Synth


class Sequencer:

    def __init__(self, scale_selector):
        self.scale_selector = scale_selector
        self.synth = Synth(44000)
        self.note_queue = []
        self.base_note = cfg.TENOR_RANGE[12]
        self.second_time = False
        self.beat = 0
        self.beats = 4

    def stop(self):
        self.synth.stop(self.base_note, harmony.get_stack(self.base_note, self.scale_selector.state))

    def step(self):
        if self.beat == self.beats - 1:
            self.synth.stop(self.base_note, harmony.get_stack(self.base_note, self.scale_selector.state))
        elif self.beat == 0:
            #if not note_queue:
            #    note_queue = TENOR_RANGE.copy()[::-1]
            #    #np.random.shuffle(note_queue)
            #base_note = note_queue.pop()
            if self.scale_selector.state == 'dorian':
                self.scale_selector.set_state('mixolydian')
                self.base_note -= 7
            elif self.scale_selector.state == 'mixolydian':
                self.scale_selector.set_state('major')
                self.base_note += 5
                self.second_time = False
            elif self.scale_selector.state == 'major':
                if not self.second_time:
                    self.second_time = not self.second_time
                else:
                    self.scale_selector.set_state('dorian')
                    if self.base_note == cfg.TENOR_RANGE[0]:
                        self.base_note += 11
                    elif self.base_note < cfg.TENOR_RANGE[0]:
                        self.base_note += 13
                    #self.base_note +=2
            self.synth.play(self.base_note, harmony.get_stack(self.base_note, self.scale_selector.state))
        self.beat = (self.beat + 1) % self.beats
