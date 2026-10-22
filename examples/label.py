# label.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)

label1 = epw.Label(text="Hello World").place(0, 10)
label2 = epw.Label(
    text="You can\ndrag me!", dragable=True, font=epw.SysFont(font="Calibri", font_size=70),
    anchor_x="center", anchor_y="center"
).place(50, 50, mode="%")


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