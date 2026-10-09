# screen.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)
epw.set_appearance_mode(2)

bg = (30, 30, 30)
screen = epw.Screen(visible=True, x=76, y=100)


def change_color():
	global bg
	bg = (120, 20, 20)


button = epw.Button(screen=screen, text="Click Me!", command=change_color, auto_size=False, width=300)
slider = epw.Slider(text="Slide Me!", auto_size=False, width=300)
entry = epw.Entry(placeholder_text="Enter something!", auto_size=False, width=300)
entry.set_screen(screen)
screen.add_widget(slider)

hide_button = epw.Button(text="Hide", command=screen.hide)
show_button = epw.Button(text="Show", command=screen.show)
disable_button = epw.Button(text="Disable", command=screen.disable)
enable_button = epw.Button(text="Enable", command=screen.enable)

button.place(50, 50)
slider.place(126, 300)
entry.place(400, 50)
hide_button.place(50, 440)
show_button.place(50, 520)
disable_button.place(200, 440)
enable_button.place(200, 520)


def draw():
	window.fill(bg)


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