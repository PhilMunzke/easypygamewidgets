# slider.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)
epw.set_appearance_mode(2)

speed = 1
x_pos = 380


def change_speed():
	global speed
	speed = slider.get()


slider = epw.Slider(text="Speed", start=0, end=2, initial_value=speed, round_display_value=2)
slider.bind(epw.PRESS, change_speed)
slider.bind(epw.DRAG, change_speed, False)
# slider.set(speed)
slider.place(50, 50)


def draw():
	global x_pos, speed
	change_speed()
	window.fill((30, 30, 30))
	if x_pos>380:
		pygame.draw.aacircle(window, (255, 255, 255), (x_pos-400, 250), 20)
	pygame.draw.aacircle(window, (255, 255, 255), (x_pos, 250), 20)
	x_pos += speed
	if x_pos>420:
		x_pos = 20


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