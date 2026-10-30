# looped_animated_buttons.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)

button1 = epw.Button(text="everything is looped")
button1.anchor(anchor_x="center", anchor_y="center")
button1.place(x=50, y=40, mode="%")
(button1.animate(duration=1, rotation=10).then(duration=1, rotation=-10).then(duration=1, rotation=20).then(duration=1, rotation=-20)
 .then(duration=1, rotation=30).then(duration=1, rotation=-30).then(duration=1, rotation=40).then(duration=1, rotation=-40).loop())

button2 = epw.Button(text="a specific part is looped")
button2.anchor(anchor_x="center", anchor_y="center")
button2.place(x=50, y=60, mode="%")
button2.animate(rotation=90).then(duration=1, scale=1.1).then(duration=1, scale=1, rotation=0).loop[1:]


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