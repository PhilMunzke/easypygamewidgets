# checkbox.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)


def check():
    print("checked")


def uncheck():
    print("unchecked")


button = epw.Checkbox(text="Accept terms and conditions", check_command=check, uncheck_command=uncheck)
button.anchor(anchor_x="center", anchor_y="center")
button.place(x=50, y=50, mode="%")


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