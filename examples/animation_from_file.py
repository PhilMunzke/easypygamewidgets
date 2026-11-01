# animation_from_file.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets
import random

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)


def get_duration():
    return random.random()*2.9+0.1  # values from .1 to 3


def custom_linear_function(t):
    return t


button = epw.Button(text="TEXT", anchor_x="center", anchor_y="center").place(x=50, y=50, mode="%")
button.animate(path="animation_from_file.json", functions={"get_duration": get_duration, "custom_linear_function": custom_linear_function})


def draw():
    window.fill((30, 30, 30))


epw.create_pygame_layer(draw, 500)

running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
        epw.handle_event(event)
    epw.handle_special_events()
    epw.flip()
    clock.tick(60)
pygame.quit()