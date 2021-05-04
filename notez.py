import sys
        
import numpy as np 
import pygame
import pygame.locals

from buttons import *
import harmony
import notation
from sequencer import Sequencer

import cfg


POSITIONS = []
for note in range(256):
    p = notation.get_positions(note)
    POSITIONS.append(p)


def __main__(): 
    pygame.mixer.pre_init()    
    pygame.init()
 
    screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    clock = pygame.time.Clock()

    scale_selector = SelectorButton(list(harmony.SCALES.keys()), 1300, 640, 90, 30)

    sequencer = Sequencer(scale_selector)
    pygame.time.set_timer(cfg.BEATEVENT, 200)
    
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 24)

    run_button = ToggleButton(1300, 500, 90, 30, text="run")
    run_button.state = False
    system_selector = SelectorButton(list(notation.NAME.keys()), 1300, 540, 90, 30)

    # Main loop.
    while True:
        screen.fill((0, 0, 0))
    
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run_button.state = not run_button.state

            if event.type == pygame.MOUSEBUTTONDOWN:
                run_button.actuate(event.pos)
                system_selector.actuate(event.pos)
                scale_selector.actuate(event.pos)

            if event.type == cfg.BEATEVENT and not run_button.state:
                sequencer.stop()
            
            if event.type == cfg.BEATEVENT and run_button.state:
                sequencer.step()
            
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
    
        # Draw buttons.
        run_button.draw(screen)
        system_selector.draw(screen)
        scale_selector.draw(screen)

        # Draw harmony.
        note = sequencer.base_note % 12
        for octave in range(4):
            stack_begin_note = sequencer.base_note % 12 + 12 * octave
            positions, replica_indices = POSITIONS[stack_begin_note]
            stack_notes = harmony.get_stack(stack_begin_note, scale_selector.state)
            for stack_begin_pos, replica_idx in zip(positions, replica_indices):
                line_start = stack_begin_pos
                next_replica = replica_idx + 1
                for stack_note in stack_notes:
                    stack_note_positions, stack_note_replica_indices = POSITIONS[stack_note]
                    try:
                        line_end = stack_note_positions[stack_note_replica_indices.index(next_replica)]
                    except ValueError:
                        continue
                    if stack_note in cfg.TENOR_RANGE:
                        pygame.draw.line(screen, (128, 128, 128), line_start * cfg.HEIGHT, line_end * cfg.HEIGHT, width=4)
                    next_replica +=1
                    line_start = line_end

        # Draw notes.
        for note in range(12, 68):
            textsurface = myfont.render(notation.get_name(note, system_selector.state)[0], True, (0, 0, 0))
            positions, replica_indices = POSITIONS[note]
            for p in positions:
                pygame.draw.circle(screen, notation.get_color(note), p * cfg.HEIGHT,
                    radius=30 if note % 12 == sequencer.base_note % 12 else 20 if note in cfg.TENOR_RANGE else 10
                )
                screen.blit(textsurface, p * cfg.HEIGHT - 17)
            pass
        textsurface = myfont.render(notation.get_name(sequencer.base_note, system_selector.state)[0], False, (255, 0, 0))
        screen.blit(textsurface,(1200,0))

        pygame.display.flip()
        clock.tick(cfg.TICK)


if __name__=="__main__":
    __main__()