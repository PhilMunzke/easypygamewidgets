# grid.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()
epw.link_pygame_window(window)

screen = epw.Screen(visible=True, auto_size=False, width=1000, height=100, row_spacing=80).place(x=0, y=20)

label = epw.Label(text="Login", font=epw.Font(font_size=35, bold=True))
username = epw.Entry(placeholder_text="Username", auto_size=False, width=220, height=60)
password = epw.Entry(placeholder_text="Password", show="*", auto_size=False, width=220, height=60)
login = epw.Button(text="Login", auto_size=False, width=220, height=60)

label.grid(screen=screen, row=0, column=0, columnspan=4)
username.grid(screen=screen, row=1, column=0)
password.grid(screen=screen, row=1, column=1)
login.grid(screen=screen, row=1, column=3)


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