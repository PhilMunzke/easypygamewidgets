# button.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)
epw.set_appearance_mode(2)

button = epw.Button(
	text="EXIT", auto_size=False, width=325, active_hover_cursor=pygame.cursors.tri_left,
	command=exit,
	alignment="stretched", alignment_spacing=45,
	font=epw.font.Font(epw.font.default_font_path, 40),
	active_hover_text_color=(255, 59, 59),
	active_unpressed_text_color=(214, 40, 40),
	active_pressed_text_color=(155, 28, 28),
	active_hover_border_color=(255, 59, 59),
	active_unpressed_border_color=(214, 40, 40),
	active_pressed_border_color=(155, 28, 28)
)
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