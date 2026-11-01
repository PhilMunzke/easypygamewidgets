# animated_button.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)

small = True


def anim():
    global small
    if small:
        button.animate(scale=2, easing=epw.easing.ease_in_out_bounce, duration=2)
        small = not small
    else:
        button.animate(scale=1, easing=epw.easing.ease_in_out_bounce, duration=2)
        small = not small


button = epw.Button(text="PRESS ME!", command=anim)
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