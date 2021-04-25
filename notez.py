import sys
        
import numpy as np 
import pygame
import pygame.locals

import harmony
import notation
from synth import Synth


BEATEVENT = pygame.USEREVENT + 1
BEATS = 4
#TENOR_RANGE = list(range(12, 44))
TENOR_RANGE = list(range(24, 56))
POSITIONS = []
for note in range(256):
    p = notation.get_positions(note)
    POSITIONS.append(p)


def __main__(): 
    pygame.mixer.pre_init()    
    pygame.init()
 
    width, height = 1400, 900
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    synth = Synth(44000)
    note_queue = []
    base_note = TENOR_RANGE[12]
    scale = 'major'
    second_time = False
    pygame.time.set_timer(BEATEVENT, 200)
    
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 24)

    running = False
    beat = 0
    # Main loop.
    while True:
        screen.fill((0, 0, 0))
    
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
            
            if event.type == BEATEVENT and not running:
                synth.stop(base_note, harmony.get_stack(base_note, scale))
            
            if event.type == BEATEVENT and running:
                if beat == BEATS - 1:
                    synth.stop(base_note, harmony.get_stack(base_note, scale))
                elif beat == 0:
                    #if not note_queue:
                    #    note_queue = TENOR_RANGE.copy()[::-1]
                    #    #np.random.shuffle(note_queue)
                    #base_note = note_queue.pop()
                    if scale == 'dorian':
                        scale = 'mixolydian'
                        base_note -= 7
                    elif scale == 'mixolydian':
                        scale = 'major'
                        base_note += 5
                        second_time = False
                    elif scale == 'major':
                        if not second_time:
                            second_time = not second_time
                        else:
                            scale = 'dorian'
                            if base_note == TENOR_RANGE[0]:
                                base_note += 11
                            elif base_note < TENOR_RANGE[0]:
                                base_note += 13
                            #base_note +=2
                    synth.play(base_note, harmony.get_stack(base_note, scale))
                beat = (beat + 1) % BEATS
            
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
    
        # Update.

        # Draw harmony.
        note = base_note % 12
        for octave in range(4):
            stack_begin_note = base_note % 12 + 12 * octave
            positions, replica_indices = POSITIONS[stack_begin_note]
            stack_notes = harmony.get_stack(stack_begin_note, scale)
            for stack_begin_pos, replica_idx in zip(positions, replica_indices):
                line_start = stack_begin_pos
                next_replica = replica_idx + 1
                for stack_note in stack_notes:
                    stack_note_positions, stack_note_replica_indices = POSITIONS[stack_note]
                    try:
                        line_end = stack_note_positions[stack_note_replica_indices.index(next_replica)]
                    except ValueError:
                        continue
                    if stack_note in TENOR_RANGE:
                        pygame.draw.line(screen, (128, 128, 128), line_start * height, line_end * height, width=4)
                    next_replica +=1
                    line_start = line_end

        # Draw notes.
        for note in range(12, 68):
            textsurface = myfont.render(notation.get_name(note)[0], True, (0, 0, 0))
            positions, replica_indices = POSITIONS[note]
            for p in positions:
                pygame.draw.circle(screen, notation.get_color(note), p * height,
                    radius=30 if note % 12 == base_note % 12 else 20 if note in TENOR_RANGE else 10
                )
                screen.blit(textsurface, p * height - 17)
            pass
        textsurface = myfont.render(notation.get_name(base_note)[0], False, (255, 0, 0))
        screen.blit(textsurface,(1200,0))

        pygame.display.flip()
        clock.tick(10)


if __name__=="__main__":
    __main__()