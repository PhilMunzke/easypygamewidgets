# animated_screens.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((1000, 900))
clock = pygame.time.Clock()
epw.link_pygame_window(window)

screen = epw.Screen(visible=True).place(1000, 0)
target_x = 1000
speed = 15


def trigger_show():
    global target_x
    target_x = 350


def trigger_hide():
    global target_x
    target_x = 1000


button1 = epw.Button(text="Show GUI", auto_size=False, command=trigger_show).place(x=50, y=100)
button2 = epw.Button(screen=screen, text="Hide GUI", auto_size=False, command=trigger_hide).place(x=0, y=100)


def draw():
    window.fill((30, 30, 30))


epw.create_pygame_layer(draw, 500)

running = True
while running:
    if screen.x!=target_x:
        direction = 1 if target_x>screen.x else -1
        new_x = screen.x+(speed*direction)
        if (direction==1 and new_x>target_x) or (direction==-1 and new_x<target_x):
            new_x = target_x
        screen.place(new_x, 0)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
        epw.handle_event(event)
    epw.handle_special_events()
    epw.flip()
    clock.tick(60)

pygame.quit()