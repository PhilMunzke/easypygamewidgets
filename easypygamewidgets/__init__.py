# __init__.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets
"""
easypygamewidgets is a widget library for pygame and based on pygame. It uses pygame-ce instead of pygame for a
better performance, more features and support for the newest python versions.
"""

from __future__ import annotations

from collections.abc import Callable

import pygame

from . import misc
from .assets.epw_types import *
from .assets.theme import load_global_theme
from .button import Button
from .checkbox import Checkbox
from .dialog import Dialog
from .entry import Entry
from .font import default_font, emoji_font, Font, SysFont, tooltip_font
from .label import Label
from .masterWidgets import Widget
from .misc import (create_frames, create_pygame_layer, disable_update_check, link_pygame_window, schedule,
                   set_appearance_mode)
from .screen import Screen
from .slider import Slider
from .surface import Surface
from .timekeeper import Timekeeper
from .tooltip import Tooltip


def flip() -> None:
	"""
	Update the display.
	You don't need to call pygame.display.flip() or pygame.display.update() after this.
	"""
	if not misc._pg:
		misc._check_linked()
	misc._update_clock()
	for widget in misc._all_widgets:
		if isinstance(widget, tuple):
			if isinstance(widget[0], Callable):
				try:
					widget[0]()
				except TypeError:
					pass
		else:
			if hasattr(widget, "_update_animation"):
				widget._update_animation()
			widget._draw(misc._pg)
	pygame.display.flip()


def handle_event(event: pygame.Event) -> None:
	"""
	This will make widgets interactable.
	(Used for interactions with pygame.Event. Don't forget to use epw.handle_special_events().)

	Args:
		event: pygame.Event

	Raises:
		ValueError: if event is not a pygame.Event
	"""
	if isinstance(event, pygame.Event):
		for widget in misc._all_widgets:
			if hasattr(widget, "_react"):
				widget._react(event)
	else:
		raise ValueError("Event must be a pygame.Event")


def handle_special_events() -> None:
	"""
	This will make widgets interactable.
	(Used for interactions with the mouse. Don't forget to use epw.handle_event(event).)
	"""
	for func in misc._scheduled_functions[:]:
		func[1] -= misc._dt
		if func[1]<=0:
			func[0]()
			misc._scheduled_functions.remove(func)
	for widget in misc._all_widgets:
		if hasattr(widget, "_react"):
			widget._react()