# button.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)
epw.set_appearance_mode(2)
epw.load_global_theme("styleguide.json")

button = epw.Button(
	text="This is a button styled with the\n theme function. "
	     "You can also override\nthe theme settings.\n(eg. active_pressed_text_color)",
	active_pressed_text_color=(255, 255, 255, 255)
)
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