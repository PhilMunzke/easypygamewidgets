# combobox.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)

combobox = epw.Combobox(
    placeholder_text="Fruits", anchor_x="center",
    values=["Apple", "Banana", "Lemon", "Strawberry", "Cherry", "Orange", "Grape", "Kiwi", "Mango", "Watermelon"]
).place(50, 20, mode="%")


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