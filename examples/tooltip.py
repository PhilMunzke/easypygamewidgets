# tooltip.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

import pygame

import easypygamewidgets as epw

pygame.init()
window = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
epw.link_pygame_window(window)
epw.set_appearance_mode(2)

button1 = epw.Button(
	text="This tooltip will be color-matched to the button.",
	active_unpressed_text_color=(255, 255, 255), active_hover_text_color=(255, 255, 255),
	active_pressed_text_color=(220, 220, 230),
	active_unpressed_background_color=(140, 70, 180),
	active_hover_background_color=(160, 90, 200),
	active_pressed_background_color=(110, 40, 150),
	active_unpressed_border_color=(120, 50, 160),
	active_hover_border_color=(180, 110, 220),
	active_pressed_border_color=(90, 30, 130)
).place(30, 30)
button1.set_tooltip(epw.Tooltip(text="This is a tooltip"))

tooltip2 = epw.Tooltip(text="They are automatically above their last bound widget", style="info")
epw.Button(text="This is a button with an info tooltip.", tooltip=tooltip2).place(30, 110)

tooltip3 = epw.Tooltip(text="Their last bound widget?", style="warning")
button3 = epw.Button(text="and this a warning").place(30, 190)
tooltip3.add_widget(button3)

button4 = epw.Button(text="And if a widget is blocked it can look like this :)").place(30, 270)
epw.Tooltip(text="Yeah, tooltips can be bound to multiple widgets", style="blocked", widgets=button4)

tooltip5 = epw.Tooltip(
	text="but a widget only to one tooltip.", active_unpressed_text_color=(150, 200, 150),
	active_unpressed_background_color=(48, 83, 57),
	active_unpressed_border_color=(47, 122, 66)
)
button5 = epw.Button(text="You can also create your own style.").place(30, 350)
button5.set_tooltip(tooltip5)


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