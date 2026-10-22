# dialog.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)

yes_button = epw.Button(text='Yes')
no_button = epw.Button(text='No')
entry = epw.Entry()
dialog = epw.Dialog(
    title="Info", description="This is the description", widgets=[yes_button, no_button, entry],
    widget_alignment="center", title_alignment="stretched", anchor_x="center", anchor_y="center",
    darken_background_with_alpha=0
)
dialog.place(50, 50, mode="%")


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