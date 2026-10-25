# animated_screens.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((1000, 900))
clock = pygame.time.Clock()
epw.link_pygame_window(window)

screen = epw.Screen(visible=True).place(1050, 0)
speed = 15


def trigger_show():
    screen.animate(offset_x=-700, duration=1, easing=epw.easing.ease_in_out_quint)


def trigger_hide():
    screen.animate(offset_x=0, duration=1, easing=epw.easing.ease_in_out_quint)


button1 = epw.Button(text="Show GUI", auto_size=False, command=trigger_show).place(x=50, y=100)
button2 = epw.Button(screen=screen, text="Hide GUI", auto_size=False, command=trigger_hide).place(x=0, y=100)
label = epw.Label(screen=screen, text="Multiple widgets slide\nbecause of one animation", alignment="stretched").place(x=-40, y=200)


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