# self_in_bindings.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)
epw.set_appearance_mode(2)


def change_text(self):
	self.config(text="You pressed the button!")
	self.place(50, 50, mode="%")


button = epw.Button(
	text="This is a button!", top_left_corner_radius=15, top_right_corner_radius=15, bottom_left_corner_radius=15,
	bottom_right_corner_radius=15
)
button.anchor(anchor_x="center", anchor_y="center")
button.place(x=50, y=50, mode="%")
button.bind(epw.RELEASE, lambda self: change_text(self))


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