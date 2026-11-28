# particle_sprayer.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)

SPEED = (120, 260)
HELD_SPEED = (SPEED[0]*1.4, SPEED[1]*1.4)

sprayer = epw.ParticleSprayer(
    spraying=True, repeated_spraying=True,
    particle_amount=4, particle_color=[(255, 255, 230), (255, 200, 70), (255, 90, 20), (80, 20, 10)], particle_texture=None,
    particle_blend_mode=pygame.BLEND_RGB_ADD, particle_speed=[SPEED], particle_duration=(48, 96),
    particle_size=[(20, 44), (6, 13.2)], particle_rotation=0, particle_gravity=[0, -48], particle_direction=[(-120, -60)],
    particle_alpha_keyframes=()
)

running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
        epw.handle_event(event)
    epw.handle_special_events()

    mx, my = pygame.mouse.get_pos()
    held = pygame.mouse.get_pressed()[0]
    sprayer.configure(x=mx, y=my)

    window.fill((12, 12, 20))
    epw.flip()
    clock.tick(60)
pygame.quit()