import pygame


class ToggleButton:

    def __init__(self, left, top, width, height, text=None):
        self.rect = pygame.Rect(left, top, width, height)
        if text is not None:
            font = pygame.font.SysFont('Comic Sans MS', 18)
            self.text = font.render(text, True, (0, 0, 0))
        else:
            self.text = None
        self.state = False

    def actuate(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.state = not self.state

    def draw(self, screen):
        color = (127, 255, 127) if self.state else (100, 150, 100)
        pygame.draw.rect(screen, color, self.rect)
        if self.text is not None:
            screen.blit(self.text, (self.rect.left, self.rect.top))


class SelectorButton:

    def __init__(self, choices, left, top, width, height):
        self.buttons = {}
        for idx, choice in enumerate(choices):
            button = ToggleButton(left, top + height * idx, width, height, text=choice)
            button.state = idx == 0
            self.buttons[choice] = button

        self.state = choices[0]

    def actuate(self, mouse_pos):
        for choice in self.buttons:
            button = self.buttons[choice]
            if button.state:
                continue
            button.actuate(mouse_pos)
            if button.state:
                self.state = choice
                for other_button in self.buttons:
                    if other_button != choice:
                        self.buttons[other_button].state = False

    def draw(self, screen):
        for button in self.buttons.values():
            button.draw(screen)