# timekeeper.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)

stopwatch = epw.Timekeeper(ticking=True, start_at=0)
stopwatch.place(50, 50)

timer = epw.Timekeeper(ticking=True, start_at=90, end_at=0, reversed_ticking=True)
timer.place(50, 200)

timer_with_milliseconds = epw.Timekeeper(ticking=True, start_at=90, end_at=-60, reversed_ticking=True, show_milliseconds=True)
timer_with_milliseconds.place(50, 350)


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