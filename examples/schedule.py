# schedule.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)

time_left = 5


def task():
    global time_left
    time_left -= 1
    label.configure(text=f"Quitting in {time_left} seconds.")
    epw.schedule(function=task, time_to_execute=1, unit="seconds")
    if time_left<=0: exit(0)


label = epw.Label(text=f"Quitting in {time_left} seconds.", anchor_x="center", anchor_y="center").place(x=50, y=50, mode="%")
epw.schedule(function=task, time_to_execute=1, unit="seconds")


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