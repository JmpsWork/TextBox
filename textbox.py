"""Textbox class which can receive keyboard inputs and display them in a 'text box' on the screen."""

import pygame
import math


closed = False
pygame.init()

clock = pygame.time.Clock()
size = (1680, 1050)
display = pygame.display.set_mode(size)
CENTER = size[0] / 2, size[1] / 2
FPS = 60
pygame.display.set_mode(size)
pygame.display.set_caption('Jam #2')
bg_color = (30, 30, 30)
def_font = pygame.font.SysFont('System Bold', 46)

rendered = []


print(pygame.K_ESCAPE)


dict_keymap = {
    pygame.K_a: 'a',  # Integer key connects to correct string representing character
    pygame.K_b: 'b',
    pygame.K_c: 'c',
    pygame.K_d: 'd',
    pygame.K_e: 'e',
    pygame.K_f: 'f',
    pygame.K_g: 'g',
    pygame.K_h: 'h',
    pygame.K_i: 'i',
    pygame.K_j: 'j',
    pygame.K_k: 'k',
    pygame.K_l: 'l',
    pygame.K_m: 'm',
    pygame.K_n: 'n',
    pygame.K_o: 'o',
    pygame.K_p: 'p',
    pygame.K_q: 'q',
    pygame.K_r: 'r',
    pygame.K_s: 's',
    pygame.K_t: 't',
    pygame.K_u: 'u',
    pygame.K_v: 'v',
    pygame.K_w: 'w',
    pygame.K_x: 'x',
    pygame.K_y: 'y',
    pygame.K_z: 'z',
    pygame.K_SPACE: ' ',
    # Numbers
    pygame.K_0: '0',
    pygame.K_1: '1',
    pygame.K_2: '2',
    pygame.K_3: '3',
    pygame.K_4: '4',
    pygame.K_5: '5',
    pygame.K_6: '6',
    pygame.K_7: '7',
    pygame.K_8: '8',
    pygame.K_9: '9',
    # Boolean keys (backspace, enter, etc.)
    pygame.K_BACKSPACE: 'BACKSPACE',
    pygame.K_RSHIFT: 'RSHIFT',
    pygame.K_LSHIFT: 'LSHIFT',
    pygame.K_CAPSLOCK: 'CAPSLOCK',
    pygame.K_KP_ENTER: 'ENTER'
}


class Text:
    def __init__(self, coords: tuple, color: tuple, text: str, *, centered: bool=True, font=None):
        self.x, self.y = coords
        self.color = color
        self.text = text
        self.centered = centered
        if font is None:
            self.font = def_font
        else:
            self.font = font

    def __repr__(self):
        return f'{self.text}'

    def draw(self):
        text = self.font.render(self.text, True, self.color)
        # thinking = resource_font.render(f'{self.thinking} +({round(self.total_thinking * self.thinking_mod)})', True, (0, 100, 200))
        if self.centered:
            center = text.get_rect(center=(self.x, self.y))
            display.blit(text, center)
        else:
            display.blit(text, (self.x, self.y))

    def set_text(self, text: str):
        self.text = text


class TextBox:
    """Displays keyboard inputs and manages key inputs for proper output."""
    def __init__(self, coords: tuple, color: tuple):
        self.text = Text(coords, color, '')
        self.current_pressed = {}  # Keyindex: [key, time pressed (frames)]
        self.upper = False
        self.invalid = ('CAPSLOCK', 'LSHIFT', 'RSHIFT', 'BACKSPACE')

    def draw(self):
        self.text.draw()

        for key, value in self.current_pressed.items():
            value[1] += 1  # Count how long keys have been pressed

    def feed(self, keys: list):
        """Determines what keys to 'feed' in to the string to be displayed."""
        input_string = self.text.text

        is_caps = keymap[pygame.K_CAPSLOCK] == 1 or keymap[pygame.K_RSHIFT] == 1 or keymap[pygame.K_LSHIFT] == 1
        if is_caps is True:
            self.upper = True

        for key in keys:  # key being the key index for the dict_keymap
            letter = dict_keymap[key]
            if self.upper is True:
                letter = letter.upper()
            pressed = self.current_pressed.get(key)
            # Exceptions for certain keys (such as capslock)
            if pressed is None:
                self.current_pressed[key] = [letter, 0]

            time = self.current_pressed[key][1]
            if time == 0:  # Determine when the pressed key can be sent to the string
                if letter == 'BACKSPACE':
                    input_string = input_string[:-1]
                elif letter not in self.invalid:  # Ignore keys which don't have letters
                    input_string += letter
            elif time % 5 == 0 and time > FPS / 2:
                if letter == 'BACKSPACE':
                    input_string = input_string[:-1]
                elif letter not in self.invalid:
                    input_string += letter

        for key in list(self.current_pressed):
            if key not in keys:
                self.current_pressed.pop(key)  # Delete unused keys to reset time

        self.text.set_text(input_string)
        self.upper = False


textbox = TextBox((size[0] / 2, size[1] / 2), (200, 200, 200))
rendered.append(textbox)


while not closed:

    pygame.display.update()
    display.fill(bg_color)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                closed = True
                pygame.quit()
                quit()

    for thing in rendered:
        thing.draw()

    keymap = pygame.key.get_pressed()
    to_feed = []
    for key, value in dict_keymap.items():
        is_pressed = keymap[key]
        if is_pressed == 1:
            # print(is_pressed, f'Key pressed: {value}')
            to_feed.append(key)

    textbox.feed(to_feed)
    clock.tick(FPS)
