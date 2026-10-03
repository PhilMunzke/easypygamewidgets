# timekeeper.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets
"""A timekeeper (timer/stopwatch) widget for pygame."""

from __future__ import annotations

import math
import time
from collections.abc import Iterable
from typing import Any, TYPE_CHECKING, Unpack

import pygame

from easypygamewidgets import misc
from easypygamewidgets.assets import epw_types, TypeHints
from easypygamewidgets.assets.epw_types import color_type
from easypygamewidgets.assets.theme import _style_dic as sd, _themed
from easypygamewidgets.masterWidgets import Deletable, Screenable, Tooltipable, Widget

if TYPE_CHECKING:
	import easypygamewidgets

pygame.init()


class Timekeeper(Widget, Tooltipable, Screenable, Deletable):
	"""Initializes a timekeeper (timer/stopwatch) widget for pygame."""

	@_themed
	def __init__(self, screen: easypygamewidgets.Screen | None = None, auto_size: bool = True, width: int = 160,
	             height: int = 50, start_at: float | int = 60, end_at: float | int | None = None,
	             show_milliseconds: bool = sd["show_milliseconds"], show_seconds: bool = sd["show_seconds"],
	             show_minutes: bool = sd["show_minutes"], smart_minutes: bool = sd["smart_minutes"],
	             show_hours: bool = sd["show_hours"], smart_hours: bool = sd["smart_hours"],
	             state: str | None = None,
	             active_unpressed_text_color: color_type = sd["active_unpressed_text_color"],
	             disabled_unpressed_text_color: color_type = sd["disabled_unpressed_text_color"],
	             active_hover_text_color: color_type = sd["active_hover_text_color"],
	             disabled_hover_text_color: color_type = sd["disabled_hover_text_color"],
	             active_pressed_text_color: color_type = sd["active_pressed_text_color"],
	             active_unpressed_background_color: color_type = sd["active_unpressed_background_color"],
	             disabled_unpressed_background_color: color_type = sd["disabled_unpressed_background_color"],
	             active_hover_background_color: color_type = sd["active_hover_background_color"],
	             disabled_hover_background_color: color_type = sd["disabled_hover_background_color"],
	             active_pressed_background_color: color_type = sd["active_pressed_background_color"],
	             active_unpressed_border_color: color_type = sd["active_unpressed_border_color"],
	             disabled_unpressed_border_color: color_type = sd["disabled_unpressed_border_color"],
	             active_hover_border_color: color_type = sd["active_hover_border_color"],
	             disabled_hover_border_color: color_type = sd["disabled_hover_border_color"],
	             active_pressed_border_color: color_type = sd["active_pressed_border_color"],
	             border_thickness: int = sd["border_thickness"],
	             hide_text: bool = False,
	             hide_background: bool = False,
	             hide_border: bool = False,
	             active_hover_cursor: pygame.Cursor | None = sd["active_hover_cursor"],
	             disabled_hover_cursor: pygame.Cursor | None = sd["disabled_hover_cursor"],
	             active_pressed_cursor: pygame.Cursor | None = sd["active_pressed_cursor"],
	             font: pygame.font.Font | pygame.font.SysFont = sd["font"], alignment: str = "center",
	             alignment_spacing: int = sd["alignment_spacing"],
	             top_left_corner_radius: int = sd["top_left_corner_radius"],
	             top_right_corner_radius: int = sd["top_right_corner_radius"],
	             bottom_left_corner_radius: int = sd["bottom_left_corner_radius"],
	             bottom_right_corner_radius: int = sd["bottom_right_corner_radius"],
	             ticking: bool = False,
	             type_order: list[str] | tuple[str, ...] = sd["type_order"],
	             reversed: bool = False,
	             layer: int = sd["layer"],
	             tooltip: easypygamewidgets.Tooltip | None = None, min_width: int | None = sd["min_width"],
	             max_width: int | None = sd["max_width"], min_height: int | None = sd["min_height"],
	             max_height: int | None = sd["max_height"],
	             alpha_based_collision_system: bool = sd["alpha_based_collision_system"],
	             anchor_x: str = sd["anchor_x"], anchor_y: str = sd["anchor_y"],
	             visible: bool = sd["visible"], data: Any = None) -> None:
		"""
		Initializes a Timekeeper widget.

		Args:
			screen: The Screen this timekeeper is attached to. If None, the timekeeper is created without a
				parent screen.
			auto_size: If True, width and height are computed from the rendered time instead of using
				the given width/height.
			width: Fixed timekeeper width in pixels. Ignored if auto_size is True.
			height: Fixed timekeeper height in pixels. Ignored if auto_size is True.
			start_at: The starting time in seconds.
			end_at: The time in seconds at which ticking should stop. None means endless.
			show_milliseconds: If milliseconds are included in the time.
			show_seconds: If seconds are included in the time.
			show_minutes: If minutes are included in the time.
			smart_minutes: If minutes are shown whenever they're not zero even if show_minutes is False.
			show_hours: If hours are included in the time.
			smart_hours: If hours are shown whenever they're non-zero, even if show_hours is False.
			state: Initial state, 'enabled' or 'disabled'. Defaults to 'enabled' if not given.
			active_unpressed_text_color: RGBA text color while enabled, not pressed, not hovered.
			disabled_unpressed_text_color: RGBA text color while disabled, not hovered.
			active_hover_text_color: RGBA text color while enabled and hovered.
			disabled_hover_text_color: RGBA text color while disabled and hovered.
			active_pressed_text_color: RGBA text color while enabled and pressed.
			active_unpressed_background_color: RGBA background color while enabled, not pressed, not hovered.
			disabled_unpressed_background_color: RGBA background color while disabled, not hovered.
			active_hover_background_color: RGBA background color while enabled and hovered.
			disabled_hover_background_color: RGBA background color while disabled and hovered.
			active_pressed_background_color: RGBA background color while enabled and pressed.
			active_unpressed_border_color: RGBA border color while enabled, not pressed, not hovered.
			disabled_unpressed_border_color: RGBA border color while disabled, not hovered.
			active_hover_border_color: RGBA border color while enabled and hovered.
			disabled_hover_border_color: RGBA border color while disabled and hovered.
			active_pressed_border_color: RGBA border color while enabled and pressed.
			border_thickness: Border width in pixels.
			hide_text: If True, the time is not rendered.
			hide_background: If True, the background fill is not rendered.
			hide_border: If True, the border is not rendered.
			active_hover_cursor: Custom cursor shown on hover while enabled.
			disabled_hover_cursor: Custom cursor shown on hover while disabled.
			active_pressed_cursor: Custom cursor shown while pressed.
			font: The pygame font used to render the time.
			alignment: Text alignment: 'left', 'right', 'center', or 'stretched'.
			alignment_spacing: Horizontal padding reserved around the aligned time.
			top_left_corner_radius: Corner radius in pixels for the top-left corner.
			top_right_corner_radius: Corner radius in pixels for the top-right corner.
			bottom_left_corner_radius: Corner radius in pixels for the bottom-left corner.
			bottom_right_corner_radius: Corner radius in pixels for the bottom-right corner.
			ticking: If True, the timekeeper starts counting immediately.
			type_order: The order and separators used to display the time. Default: ('h', ':', 'm', ':', 's', '.', 'ms')
			reversed: If True, time counts down instead of up.
			layer: Draw order layer; higher values draw on top.
			tooltip: A Tooltip widget shown on hover, if given.
			min_width: Minimum width in pixels when auto_size is True.
			max_width: Maximum width in pixels when auto_size is True.
			min_height: Minimum height in pixels when auto_size is True.
			max_height: Maximum height in pixels when auto_size is True.
			alpha_based_collision_system: Use a pixel alpha test to check for collisions instead of math
				calculations.
			anchor_x: Horizontal anchor point: 'left', 'center', or 'right'.
			anchor_y: Vertical anchor point: 'top', 'center', or 'bottom'.
			visible: Initial visibility. Defaults to True.
			data: Arbitrary user data attached to the widget.

		Raises:
			ValueError: If a *_cursor argument is given but is not a pygame.Cursor instance.
		"""
		super().__init__()
		if screen:
			screen.add_widget(self)
			self._screen = screen
			if state:
				self._state = state
		else:
			self._visible = visible
			self._screen = None
			if state:
				self._state = state
			else:
				self._state = "enabled"
		self._auto_size = auto_size
		self._width = width
		self._height = height
		if auto_size:
			if min_width: self._width = max(width, min_width)
			if max_width: self._width = min(width, max_width)
			if min_height: self._height = max(height, min_height)
			if max_height: self._height = min(height, max_height)
		self._start_at = start_at
		self._end_at = end_at
		self._show_milliseconds = show_milliseconds
		self._show_seconds = show_seconds
		self._show_minutes = show_minutes
		self._smart_minutes = smart_minutes
		self._show_hours = show_hours
		self._smart_hours = smart_hours
		self._active_unpressed_text_color = misc.normalize_color(active_unpressed_text_color)
		self._disabled_unpressed_text_color = misc.normalize_color(disabled_unpressed_text_color)
		self._active_hover_text_color = misc.normalize_color(active_hover_text_color)
		self._disabled_hover_text_color = misc.normalize_color(disabled_hover_text_color)
		self._active_pressed_text_color = misc.normalize_color(active_pressed_text_color)
		self._active_unpressed_background_color = misc.normalize_color(active_unpressed_background_color)
		self._disabled_unpressed_background_color = misc.normalize_color(disabled_unpressed_background_color)
		self._active_hover_background_color = misc.normalize_color(active_hover_background_color)
		self._disabled_hover_background_color = misc.normalize_color(disabled_hover_background_color)
		self._active_pressed_background_color = misc.normalize_color(active_pressed_background_color)
		self._active_unpressed_border_color = misc.normalize_color(active_unpressed_border_color)
		self._disabled_unpressed_border_color = misc.normalize_color(disabled_unpressed_border_color)
		self._active_hover_border_color = misc.normalize_color(active_hover_border_color)
		self._disabled_hover_border_color = misc.normalize_color(disabled_hover_border_color)
		self._active_pressed_border_color = misc.normalize_color(active_pressed_border_color)
		self._border_thickness = border_thickness
		self._hide_text = hide_text
		self._hide_background = hide_background
		self._hide_border = hide_border
		cursor_input = {
			"active_hover": active_hover_cursor,
			"disabled_hover": disabled_hover_cursor,
			"active_pressed": active_pressed_cursor
		}
		self._cursors = {}
		for name, cursor in cursor_input.items():
			if isinstance(cursor, pygame.cursors.Cursor):
				self._cursors[name] = cursor
			else:
				if cursor is not None:
					raise ValueError(
						f"No custom cursor is used for the timekeeper {start_at=}, {end_at=} because it's not a "
						f"pygame.Cursor object. {cursor} is a {type(cursor)}"
					)
				self._cursors[name] = None
		self._font = font
		self._alignment = alignment
		self._alignment_spacing = alignment_spacing
		self._top_left_corner_radius = top_left_corner_radius
		self._top_right_corner_radius = top_right_corner_radius
		self._bottom_left_corner_radius = bottom_left_corner_radius
		self._bottom_right_corner_radius = bottom_right_corner_radius
		self._ticking = ticking
		self._type_order = type_order
		self._reversed = reversed
		self._layer = layer
		self._tooltip = tooltip
		if tooltip:
			tooltip.configure(layer=self._layer+1)
			if not tooltip.style:
				tooltip.configure(
					active_unpressed_text_color=self._active_unpressed_text_color,
					active_unpressed_background_color=self._active_unpressed_background_color,
					active_unpressed_border_color=self._active_unpressed_border_color
				)
		self._min_width = min_width
		self._max_width = max_width
		self._min_height = min_height
		self._max_height = max_height
		self._alpha_based_collision_system = alpha_based_collision_system
		self._anchor_x = anchor_x
		self._anchor_y = anchor_y
		self._data = data
		self._x = 0
		self._y = 0
		self._alive = True
		self._pressed = False
		self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
		self._original_cursor = None
		self._last_updated = None
		self._is_negative = False
		self._bindings = {}
		self._dialog = None
		self._is_hovered = False
		self._last_visual_state = None
		self._needs_redraw = True
		self._needs_transform = True
		self._original_surface = pygame.Surface((1, 1))
		self._cached_surface = None
		self._target_scale = 1
		self._current_scale = 1
		self._scale_step = 0
		self._target_rotation = 0
		self._current_rotation = 0
		self._rotation_step = 0
		self._target_offset = (0, 0)
		self._current_offset = [0, 0]
		self._offset_step = [0, 0]
		self._use_rotozoom = False

		self._milliseconds = None
		self._seconds = None
		self._minutes = None
		self._hours = None
		_split_to_values(self, start_at)

		misc._add_widget(self)

	@property
	def screen(self):
		return self._screen

	@screen.setter
	def screen(self, value):
		self.set_screen(value)

	@property
	def state(self):
		return self._state

	@state.setter
	def state(self, value):
		self._state = value

	@property
	def visible(self):
		return self._visible

	@visible.setter
	def visible(self, value):
		self._visible = value

	@property
	def auto_size(self):
		return self._auto_size

	@auto_size.setter
	def auto_size(self, value):
		self._auto_size = value

	@property
	def width(self):
		return self._width

	@width.setter
	def width(self, value):
		self._width = value

	@property
	def height(self):
		return self._height

	@height.setter
	def height(self, value):
		self._height = value

	@property
	def start_at(self):
		return self._start_at

	@start_at.setter
	def start_at(self, value):
		self._start_at = value

	@property
	def end_at(self):
		return self._end_at

	@end_at.setter
	def end_at(self, value):
		self._end_at = value

	@property
	def show_milliseconds(self):
		return self._show_milliseconds

	@show_milliseconds.setter
	def show_milliseconds(self, value):
		self._show_milliseconds = value

	@property
	def show_seconds(self):
		return self._show_seconds

	@show_seconds.setter
	def show_seconds(self, value):
		self._show_seconds = value

	@property
	def show_minutes(self):
		return self._show_minutes

	@show_minutes.setter
	def show_minutes(self, value):
		self._show_minutes = value

	@property
	def smart_minutes(self):
		return self._smart_minutes

	@smart_minutes.setter
	def smart_minutes(self, value):
		self._smart_minutes = value

	@property
	def show_hours(self):
		return self._show_hours

	@show_hours.setter
	def show_hours(self, value):
		self._show_hours = value

	@property
	def smart_hours(self):
		return self._smart_hours

	@smart_hours.setter
	def smart_hours(self, value):
		self._smart_hours = value

	@property
	def active_unpressed_text_color(self):
		return self._active_unpressed_text_color

	@active_unpressed_text_color.setter
	def active_unpressed_text_color(self, value):
		self._active_unpressed_text_color = misc.normalize_color(value)

	@property
	def disabled_unpressed_text_color(self):
		return self._disabled_unpressed_text_color

	@disabled_unpressed_text_color.setter
	def disabled_unpressed_text_color(self, value):
		self._disabled_unpressed_text_color = misc.normalize_color(value)

	@property
	def active_hover_text_color(self):
		return self._active_hover_text_color

	@active_hover_text_color.setter
	def active_hover_text_color(self, value):
		self._active_hover_text_color = misc.normalize_color(value)

	@property
	def disabled_hover_text_color(self):
		return self._disabled_hover_text_color

	@disabled_hover_text_color.setter
	def disabled_hover_text_color(self, value):
		self._disabled_hover_text_color = misc.normalize_color(value)

	@property
	def active_pressed_text_color(self):
		return self._active_pressed_text_color

	@active_pressed_text_color.setter
	def active_pressed_text_color(self, value):
		self._active_pressed_text_color = misc.normalize_color(value)

	@property
	def active_unpressed_background_color(self):
		return self._active_unpressed_background_color

	@active_unpressed_background_color.setter
	def active_unpressed_background_color(self, value):
		self._active_unpressed_background_color = misc.normalize_color(value)

	@property
	def disabled_unpressed_background_color(self):
		return self._disabled_unpressed_background_color

	@disabled_unpressed_background_color.setter
	def disabled_unpressed_background_color(self, value):
		self._disabled_unpressed_background_color = misc.normalize_color(value)

	@property
	def active_hover_background_color(self):
		return self._active_hover_background_color

	@active_hover_background_color.setter
	def active_hover_background_color(self, value):
		self._active_hover_background_color = misc.normalize_color(value)

	@property
	def disabled_hover_background_color(self):
		return self._disabled_hover_background_color

	@disabled_hover_background_color.setter
	def disabled_hover_background_color(self, value):
		self._disabled_hover_background_color = misc.normalize_color(value)

	@property
	def active_pressed_background_color(self):
		return self._active_pressed_background_color

	@active_pressed_background_color.setter
	def active_pressed_background_color(self, value):
		self._active_pressed_background_color = misc.normalize_color(value)

	@property
	def active_unpressed_border_color(self):
		return self._active_unpressed_border_color

	@active_unpressed_border_color.setter
	def active_unpressed_border_color(self, value):
		self._active_unpressed_border_color = misc.normalize_color(value)

	@property
	def disabled_unpressed_border_color(self):
		return self._disabled_unpressed_border_color

	@disabled_unpressed_border_color.setter
	def disabled_unpressed_border_color(self, value):
		self._disabled_unpressed_border_color = misc.normalize_color(value)

	@property
	def active_hover_border_color(self):
		return self._active_hover_border_color

	@active_hover_border_color.setter
	def active_hover_border_color(self, value):
		self._active_hover_border_color = misc.normalize_color(value)

	@property
	def disabled_hover_border_color(self):
		return self._disabled_hover_border_color

	@disabled_hover_border_color.setter
	def disabled_hover_border_color(self, value):
		self._disabled_hover_border_color = misc.normalize_color(value)

	@property
	def active_pressed_border_color(self):
		return self._active_pressed_border_color

	@active_pressed_border_color.setter
	def active_pressed_border_color(self, value):
		self._active_pressed_border_color = misc.normalize_color(value)

	@property
	def border_thickness(self):
		return self._border_thickness

	@border_thickness.setter
	def border_thickness(self, value):
		self._border_thickness = value

	@property
	def hide_text(self):
		return self._hide_text

	@hide_text.setter
	def hide_text(self, value):
		self._hide_text = value

	@property
	def hide_background(self):
		return self._hide_background

	@hide_background.setter
	def hide_background(self, value):
		self._hide_background = value

	@property
	def hide_border(self):
		return self._hide_border

	@hide_border.setter
	def hide_border(self, value):
		self._hide_border = value

	@property
	def active_hover_cursor(self):
		return self._cursors["active_hover"]

	@active_hover_cursor.setter
	def active_hover_cursor(self, value):
		self._cursors["active_hover"] = value

	@property
	def disabled_hover_cursor(self):
		return self._cursors["disabled_hover"]

	@disabled_hover_cursor.setter
	def disabled_hover_cursor(self, value):
		self._cursors["disabled_hover"] = value

	@property
	def active_pressed_cursor(self):
		return self._cursors["active_pressed"]

	@active_pressed_cursor.setter
	def active_pressed_cursor(self, value):
		self._cursors["active_pressed"] = value

	@property
	def cursors(self):
		return self._cursors

	@cursors.setter
	def cursors(self, value):
		self._cursors = value

	@property
	def font(self):
		return self._font

	@font.setter
	def font(self, value):
		self._font = value

	@property
	def alignment(self):
		return self._alignment

	@alignment.setter
	def alignment(self, value):
		self._alignment = value

	@property
	def alignment_spacing(self):
		return self._alignment_spacing

	@alignment_spacing.setter
	def alignment_spacing(self, value):
		self._alignment_spacing = value

	@property
	def top_left_corner_radius(self):
		return self._top_left_corner_radius

	@top_left_corner_radius.setter
	def top_left_corner_radius(self, value):
		self._top_left_corner_radius = value

	@property
	def top_right_corner_radius(self):
		return self._top_right_corner_radius

	@top_right_corner_radius.setter
	def top_right_corner_radius(self, value):
		self._top_right_corner_radius = value

	@property
	def bottom_left_corner_radius(self):
		return self._bottom_left_corner_radius

	@bottom_left_corner_radius.setter
	def bottom_left_corner_radius(self, value):
		self._bottom_left_corner_radius = value

	@property
	def bottom_right_corner_radius(self):
		return self._bottom_right_corner_radius

	@bottom_right_corner_radius.setter
	def bottom_right_corner_radius(self, value):
		self._bottom_right_corner_radius = value

	@property
	def ticking(self):
		return self._ticking

	@ticking.setter
	def ticking(self, value):
		self._ticking = value

	@property
	def type_order(self):
		return self._type_order

	@type_order.setter
	def type_order(self, value):
		self._type_order = value

	@property
	def reversed(self):
		return self._reversed

	@reversed.setter
	def reversed(self, value):
		self._reversed = value

	@property
	def layer(self):
		return self._layer

	@layer.setter
	def layer(self, value):
		self._layer = value
		if self._tooltip:
			self._tooltip.configure(layer=self._layer+1)
		misc._resort_layers()

	@property
	def tooltip(self):
		return self._tooltip

	@tooltip.setter
	def tooltip(self, value):
		self.set_tooltip(value)

	@property
	def min_width(self):
		return self._min_width

	@min_width.setter
	def min_width(self, value):
		self._min_width = value

	@property
	def max_width(self):
		return self._max_width

	@max_width.setter
	def max_width(self, value):
		self._max_width = value

	@property
	def min_height(self):
		return self._min_height

	@min_height.setter
	def min_height(self, value):
		self._min_height = value

	@property
	def max_height(self):
		return self._max_height

	@max_height.setter
	def max_height(self, value):
		self._max_height = value

	@property
	def alpha_based_collision_system(self):
		return self._alpha_based_collision_system

	@alpha_based_collision_system.setter
	def alpha_based_collision_system(self, value):
		self._alpha_based_collision_system = value

	@property
	def anchor_x(self):
		return self._anchor_x

	@anchor_x.setter
	def anchor_x(self, value):
		self._anchor_x = value

	@property
	def anchor_y(self):
		return self._anchor_y

	@anchor_y.setter
	def anchor_y(self, value):
		self._anchor_y = value

	@property
	def data(self):
		return self._data

	@data.setter
	def data(self, value):
		self._data = value

	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, value):
		self._x = value

	@property
	def y(self):
		return self._y

	@y.setter
	def y(self, value):
		self._y = value

	@property
	def alive(self):
		return self._alive

	@alive.setter
	def alive(self, value):
		self._alive = value

	@property
	def pressed(self):
		return self._pressed

	@pressed.setter
	def pressed(self, value):
		self._pressed = value

	@property
	def rect(self):
		return self._rect

	@rect.setter
	def rect(self, value):
		self._rect = value

	@property
	def original_cursor(self):
		return self._original_cursor

	@original_cursor.setter
	def original_cursor(self, value):
		self._original_cursor = value

	@property
	def last_updated(self):
		return self._last_updated

	@last_updated.setter
	def last_updated(self, value):
		self._last_updated = value

	@property
	def is_negative(self):
		return self._is_negative

	@is_negative.setter
	def is_negative(self, value):
		self._is_negative = value

	@property
	def bindings(self):
		return self._bindings

	@bindings.setter
	def bindings(self, value):
		self._bindings = value

	@property
	def milliseconds(self):
		return self._milliseconds

	@milliseconds.setter
	def milliseconds(self, value):
		self._milliseconds = value

	@property
	def seconds(self):
		return self._seconds

	@seconds.setter
	def seconds(self, value):
		self._seconds = value

	@property
	def minutes(self):
		return self._minutes

	@minutes.setter
	def minutes(self, value):
		self._minutes = value

	@property
	def hours(self):
		return self._hours

	@hours.setter
	def hours(self, value):
		self._hours = value

	@property
	def dialog(self):
		return self._dialog

	@dialog.setter
	def dialog(self, value):
		self._dialog = value

	@property
	def is_hovered(self):
		return self._is_hovered

	@is_hovered.setter
	def is_hovered(self, value):
		self._is_hovered = value

	@property
	def last_visual_state(self):
		return self._last_visual_state

	@last_visual_state.setter
	def last_visual_state(self, value):
		self._last_visual_state = value

	@property
	def needs_redraw(self):
		return self._needs_redraw

	@needs_redraw.setter
	def needs_redraw(self, value):
		self._needs_redraw = value

	@property
	def cached_surface(self):
		return self._cached_surface

	@cached_surface.setter
	def cached_surface(self, value):
		self._cached_surface = value

	@property
	def needs_transform(self):
		return self._needs_transform

	@needs_transform.setter
	def needs_transform(self, value):
		self._needs_transform = value

	@property
	def original_surface(self):
		return self._original_surface

	@original_surface.setter
	def original_surface(self, value):
		self._original_surface = value

	@property
	def target_scale(self):
		return self._target_scale

	@target_scale.setter
	def target_scale(self, value):
		self._target_scale = value

	@property
	def current_scale(self):
		return self._current_scale

	@current_scale.setter
	def current_scale(self, value):
		self._current_scale = value

	@property
	def scale_step(self):
		return self._scale_step

	@scale_step.setter
	def scale_step(self, value):
		self._scale_step = value

	@property
	def target_rotation(self):
		return self._target_rotation

	@target_rotation.setter
	def target_rotation(self, value):
		self._target_rotation = value

	@property
	def current_rotation(self):
		return self._current_rotation

	@current_rotation.setter
	def current_rotation(self, value):
		self._current_rotation = value

	@property
	def rotation_step(self):
		return self._rotation_step

	@rotation_step.setter
	def rotation_step(self, value):
		self._rotation_step = value

	@property
	def target_offset(self):
		return self._target_offset

	@target_offset.setter
	def target_offset(self, value):
		self._target_offset = value

	@property
	def current_offset(self):
		return self._current_offset

	@current_offset.setter
	def current_offset(self, value):
		self._current_offset = value

	@property
	def offset_step(self):
		return self._offset_step

	@offset_step.setter
	def offset_step(self, value):
		self._offset_step = value

	@property
	def use_rotozoom(self):
		return self._use_rotozoom

	@use_rotozoom.setter
	def use_rotozoom(self, value):
		self._use_rotozoom = value

	def configure(self, **kwargs: Unpack[TypeHints.TimekeeperConfig]) -> Timekeeper:
		"""
		Updates one or more of the timekeeper's attributes.

		Args:
			**kwargs: Timekeeper attributes to update as defined in TypeHints.TimekeeperConfig

		Returns:
			Timekeeper (Timekeeper): This timekeeper instance to allow method chaining.
		"""
		for key, value in kwargs.items():
			setattr(self, key, value)
		self._needs_redraw = True
		self._needs_transform = True
		_update_size(self)
		if any(
				k in kwargs for k in
				(
						'auto_size', 'x', 'y', 'width', 'height', 'min_width', 'max_width', 'min_height', 'max_height',
						'anchor_x', 'anchor_y', 'milliseconds', 'seconds', 'minutes', 'hours', 'smart_minutes',
						'smart_hours', 'show_milliseconds', 'show_seconds', 'show_minutes', 'show_hours'
				)
		):
			if self._auto_size:
				if self._min_width: self._width = max(self._width, self._min_width)
				if self._max_width: self._width = min(self._width, self._max_width)
				if self._min_height: self._height = max(self._height, self._min_height)
				if self._max_height: self._height = min(self._height, self._max_height)
			self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
		if 'screen' in kwargs:
			self.set_screen(kwargs["screen"])
		if 'layer' in kwargs:
			misc._resort_layers()
		return self

	def config(self, **kwargs: Unpack[TypeHints.TimekeeperConfig]) -> Timekeeper:
		"""
		Updates one or more of the timekeeper's attributes.

		Args:
			**kwargs: Timekeeper attributes to update as defined in TypeHints.TimekeeperConfig

		Returns:
			Timekeeper (Timekeeper): This timekeeper instance to allow method chaining.
		"""
		return self.configure(**kwargs)

	def get_display_text(self) -> str:
		"""
		Returns the currently formatted time according to type_order, show_* and smart_* settings.

		Returns:
			str: The formatted display text.
		"""
		values = {
			"ms": self._milliseconds if self._show_milliseconds else None,
			"s": self._seconds if self._show_seconds else None,
			"m": self._minutes if (self._show_minutes or (self._smart_minutes and self._minutes!=0) or (
					self._smart_minutes and self._hours!=0)) else None,
			"h": self._hours if (self._show_hours or (self._smart_hours and self._hours!=0)) else None,
		}
		parts = []
		pending_sep = None
		for token in self._type_order:
			if token in values:
				value = values[token]
				if value is not None:
					if pending_sep and parts:
						parts.append(pending_sep)
					if token=="ms":
						ms_int = int(round(value, 4)*100)%100
						parts.append(f"{ms_int:02}")
					else:
						parts.append(f"{value:02}")
					pending_sep = None
			else:
				pending_sep = token
		display_str = "".join(parts)
		if self._is_negative:
			display_str = "-"+display_str
		return display_str

	def set(self, milliseconds: int = 0, seconds: int = 0, minutes: int = 0, hours: int = 0) -> Timekeeper:
		"""
		Sets the timekeeper's current time.

		Args:
			milliseconds (int): Amount of milliseconds of the new time.
			seconds (int): Amount of seconds of the new time.
			minutes (int): Amount of minutes of the new time.
			hours (int): Amount of hours of the new time.

		Returns:
			Timekeeper (Timekeeper): This timekeeper instance to allow method chaining.
		"""
		_split_to_values(self, hours*3600+minutes*60+seconds+milliseconds/1000)
		return self

	def stop(self) -> Timekeeper:
		"""
		Stops the timekeeper from ticking.

		Returns:
			Timekeeper (Timekeeper): This timekeeper instance to allow method chaining.
		"""
		self._ticking = False
		self._last_updated = None
		return self

	def resume(self) -> Timekeeper:
		"""
		Resumes ticking from the current time.

		Returns:
			Timekeeper (Timekeeper): This timekeeper instance to allow method chaining.
		"""
		self._ticking = True
		self._last_updated = None
		return self

	def start(self) -> Timekeeper:
		"""
		Starts the timekeeper ticking from the current time.

		Returns:
			Timekeeper (Timekeeper): This timekeeper instance to allow method chaining.
		"""
		self._ticking = True
		self._last_updated = None
		return self

	def reset(self) -> Timekeeper:
		"""
		Resets the timekeeper's time back to start_at. This function will not change the ticking state.

		Returns:
			Timekeeper (Timekeeper): This timekeeper instance to allow method chaining.
		"""
		_split_to_values(self, self._start_at)
		self._last_updated = None
		return self

	def add(self, amount: int) -> Timekeeper:
		"""
		Adds an amount of seconds to the timekeeper's current time.

		Args:
			amount: The number of seconds to add.

		Returns:
			Timekeeper (Timekeeper): This timekeeper instance to allow method chaining.
		"""
		sign = -1 if self._is_negative else 1
		curr = ((self._hours*3600)+(self._minutes*60)+self._seconds+self._milliseconds)*sign
		curr += amount
		_split_to_values(self, curr)
		return self

	def subtract(self, amount: int) -> Timekeeper:
		"""
		Subtracts an amount of seconds from the timekeeper's current time.

		Args:
			amount: The number of seconds to subtract.

		Returns:
			Timekeeper (Timekeeper): This timekeeper instance to allow method chaining.
		"""
		sign = -1 if self._is_negative else 1
		curr = ((self._hours*3600)+(self._minutes*60)+self._seconds+self._milliseconds)*sign
		curr -= amount
		_split_to_values(self, curr)
		return self

	def scale(self, value: int | float = 1, frames_to_finish: int = 1) -> Timekeeper:
		"""
		Scale the timekeeper by a factor. It's only a visual scale so upscaling could look pixelated.

		Args:
			 value (int|float): the scale factor
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Timekeeper (Timekeeper): This timekeeper instance to allow method chaining.
		"""
		if frames_to_finish<=0:
			frames_to_finish = 1
		self._target_scale = value
		self._scale_step = (self._target_scale-self._current_scale)/frames_to_finish
		self._update_animation()
		return self

	def rotate(self, value: int | float = 0, frames_to_finish: int = 1) -> Timekeeper:
		"""
		Rotate the timekeeper by a degree.

		Args:
			 value (int|float): the rotation degree
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Timekeeper (Timekeeper): This timekeeper instance to allow method chaining.
		"""
		if frames_to_finish<=0:
			frames_to_finish = 1
		self._target_rotation = value
		self._rotation_step = (self._target_rotation-self._current_rotation)/frames_to_finish
		self._update_animation()
		return self

	def rotozoom(self, scale: int | float = 1, rotation: int | float = 0, frames_to_finish: int = 1) -> Timekeeper:
		"""
		Rotate the timekeeper by a degree and scale it.

		Args:
			 scale (int|float): the scale factor
			 rotation (int|float): the rotation degree
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Timekeeper (Timekeeper): This timekeeper instance to allow method chaining.
		"""
		if frames_to_finish<=0:
			frames_to_finish = 1
		self._target_scale = scale
		self._scale_step = (self._target_scale-self._current_scale)/frames_to_finish
		self._target_rotation = rotation
		self._rotation_step = (self._target_rotation-self._current_rotation)/frames_to_finish
		self._use_rotozoom = True
		self._update_animation()
		return self

	def offset(self, value: Iterable[int] = (0, 0), frames_to_finish: int = 1) -> Timekeeper:
		"""
		Offset the timekeeper by an x and y value.

		Args:
			 value: an iterable thing with two values. The first being the x and the second the y offset.
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Timekeeper (Timekeeper): This timekeeper instance to allow method chaining.
		"""
		if frames_to_finish<=0:
			frames_to_finish = 1
		self._target_offset = value
		self._offset_step[0] = (self._target_offset[0]-self._current_offset[0])/frames_to_finish
		self._offset_step[1] = (self._target_offset[1]-self._current_offset[1])/frames_to_finish
		self._update_animation()
		return self

	def _update_animation(self) -> None:
		"""Internally used to update the animation until it's finished."""
		scale_changed = False
		rotation_changed = False
		if self._current_scale!=self._target_scale:
			if abs(self._current_scale-self._target_scale)<=abs(self._scale_step):
				self._current_scale = self._target_scale
			else:
				self._current_scale += self._scale_step
			scale_changed = True
		if self._current_rotation!=self._target_rotation:
			if abs(self._current_rotation-self._target_rotation)<=abs(self._rotation_step):
				self._current_rotation = self._target_rotation
			else:
				self._current_rotation += self._rotation_step
			rotation_changed = True
		for x in range(2):
			if self._current_offset[x]!=self._target_offset[x]:
				if abs(self._current_offset[x]-self._target_offset[x])<=abs(self._offset_step[x]):
					self._current_offset[x] = float(self._target_offset[x])
				else:
					self._current_offset[x] += self._offset_step[x]
		if scale_changed or rotation_changed:
			self._needs_transform = True

	def _draw(self, surface: pygame.Surface) -> None:
		"""
		Internally used to draw the timekeeper.

		Args:
			surface (pygame.Surface): The surface to draw the timekeeper on.
		"""
		if not self._alive or not self._visible: return
		mouse_pos = pygame.mouse.get_pos()
		is_hovering = misc._is_point_over_widget(self, mouse_pos)

		current_visual_state = (self._pressed, is_hovering)
		if self._needs_redraw or self._last_visual_state!=current_visual_state:
			_render_timekeeper_surface(self, is_hovering)

		if self._needs_transform:
			if self._current_scale!=1 or self._current_rotation!=0:
				new_width = int(self._original_surface.get_width()*self._current_scale)
				new_height = int(self._original_surface.get_height()*self._current_scale)
				if new_width>0 and new_height>0:
					if self._use_rotozoom:
						self._cached_surface = pygame.transform.rotozoom(
							self._original_surface,
							self._current_rotation,
							self._current_scale
						)
					else:
						scaled_surface = pygame.transform.smoothscale(self._original_surface, (new_width, new_height))
						self._cached_surface = pygame.transform.rotate(scaled_surface, self._current_rotation)
				else:
					self._cached_surface = pygame.Surface((0, 0), pygame.SRCALPHA)
			else:
				self._cached_surface = self._original_surface.copy()
			old_center = self._rect.center
			self._rect = self._cached_surface.get_rect()
			self._rect.center = old_center
			self._needs_transform = False
		offset_x, offset_y = misc._get_offset(self)
		total_offset_x = offset_x+round(self._current_offset[0])
		total_offset_y = offset_y+round(self._current_offset[1])
		draw_rect = self._rect.move(total_offset_x, total_offset_y)
		surface.blit(self._cached_surface, draw_rect)

		if is_hovering:
			if self._state=="enabled":
				if self._pressed:
					cursor_key = "active_pressed"
				else:
					cursor_key = "active_hover"
			else:
				cursor_key = "disabled_hover"
			target_cursor = self._cursors.get(cursor_key)
			if target_cursor:
				current_cursor = pygame.mouse.get_cursor()
				if current_cursor!=target_cursor:
					if self._original_cursor is None:
						self._original_cursor = current_cursor
					pygame.mouse.set_cursor(target_cursor)
		else:
			if self._original_cursor:
				pygame.mouse.set_cursor(self._original_cursor)
				self._original_cursor = None

		if is_hovering and not self._is_hovered:
			self._is_hovered = True
			self.trigger_event(epw_types.MOUSE_IN)
			if self._tooltip:
				self._tooltip.show()
		elif is_hovering and self._is_hovered:
			self._is_hovered = True
			self.trigger_event(epw_types.HOVER)
		elif not is_hovering and self._is_hovered:
			self._is_hovered = False
			self.trigger_event(epw_types.MOUSE_OUT)
			if self._tooltip:
				self._tooltip.hide()

	def _react(self, event: pygame.Event | None = None) -> None:
		"""
		Internally used to react to events.

		Args:
			event (pygame.Event, optional): The event to react to.
		"""
		if self._state!="enabled" or not self._visible:
			self._pressed = False
			return
		is_inside = misc._is_point_over_widget(self, pygame.mouse.get_pos())
		if event:
			if event.type==pygame.MOUSEBUTTONDOWN and event.button==1 and is_inside:
				self._pressed = True
				self.trigger_event(epw_types.PRESS)
			elif event.type==pygame.MOUSEBUTTONUP and event.button==1 and self._pressed:
				self._pressed = False
				self.trigger_event(epw_types.RELEASE)
			elif event.type==pygame.KEYDOWN:
				misc._trigger_key_bindings(self, event)
		else:
			if self._ticking:
				now = time.time()
				if not self._last_updated:
					self._last_updated = now
				dt = now-self._last_updated
				self._last_updated = now
				sign = -1 if self._is_negative else 1
				curr = ((self._hours*3600)+(
						self._minutes*60)+self._seconds+self._milliseconds)*sign
				change = -dt if self._reversed else dt
				next_value = curr+change
				if self._end_at is not None:
					reached_limit = False
					if not self._reversed and next_value>=self._end_at:
						reached_limit = True
					elif self._reversed and next_value<=self._end_at:
						reached_limit = True
					if reached_limit:
						_split_to_values(self, self._end_at)
						self.stop()
						self.trigger_event(epw_types.FINISHED)
						return
				_split_to_values(self, next_value)


def _render_timekeeper_surface(timekeeper: Timekeeper, is_hovering: bool) -> None:
	"""
	Internally used to draw the timekeeper surface once and cache it.

	Args:
		timekeeper (Timekeeper): the widget to render the surface for
		is_hovering (bool): whether the mouse is hovering over the widget
	"""
	if timekeeper.state=="enabled":
		if timekeeper.pressed and is_hovering:
			text_color = timekeeper.active_pressed_text_color
			bg_color = timekeeper.active_pressed_background_color
			brd_color = timekeeper.active_pressed_border_color
		elif is_hovering:
			text_color = timekeeper.active_hover_text_color
			bg_color = timekeeper.active_hover_background_color
			brd_color = timekeeper.active_hover_border_color
		else:
			text_color = timekeeper.active_unpressed_text_color
			bg_color = timekeeper.active_unpressed_background_color
			brd_color = timekeeper.active_unpressed_border_color
	else:
		if is_hovering:
			text_color = timekeeper.disabled_hover_text_color
			bg_color = timekeeper.disabled_hover_background_color
			brd_color = timekeeper.disabled_hover_border_color
		else:
			text_color = timekeeper.disabled_unpressed_text_color
			bg_color = timekeeper.disabled_unpressed_background_color
			brd_color = timekeeper.disabled_unpressed_border_color

	display_text = timekeeper.get_display_text()
	cached = pygame.Surface((timekeeper.width, timekeeper.height), pygame.SRCALPHA)
	draw_rect = pygame.Rect(0, 0, timekeeper.width, timekeeper.height)
	if not timekeeper.hide_background:
		pygame.draw.rect(
			cached, bg_color, draw_rect,
			border_top_left_radius=timekeeper.top_left_corner_radius,
			border_top_right_radius=timekeeper.top_right_corner_radius,
			border_bottom_left_radius=timekeeper.bottom_left_corner_radius,
			border_bottom_right_radius=timekeeper.bottom_right_corner_radius
		)
	if not timekeeper.hide_border:
		pygame.draw.rect(
			cached, brd_color, draw_rect, width=timekeeper.border_thickness,
			border_top_left_radius=timekeeper.top_left_corner_radius,
			border_top_right_radius=timekeeper.top_right_corner_radius,
			border_bottom_left_radius=timekeeper.bottom_left_corner_radius,
			border_bottom_right_radius=timekeeper.bottom_right_corner_radius
		)
	old_clip = cached.get_clip()
	clip_rect = draw_rect.inflate(-4, -4)
	cached.set_clip(clip_rect)
	y_pos = draw_rect.centery
	drawn_stretched = False
	if not timekeeper.hide_text:
		ascent = timekeeper.font.get_ascent()
		descent = abs(timekeeper.font.get_descent())
		optical_centre_offset = ascent-(ascent-descent)//2
		if timekeeper.alignment=="stretched" and len(display_text)>1 and not timekeeper.auto_size:
			total_char_width = sum(
				timekeeper.font.render(char, True, text_color).get_width() for char in display_text
			)
			available_width = draw_rect.width-(timekeeper.alignment_spacing*2)
			if available_width>total_char_width:
				drawn_stretched = True
				spacing = (available_width-total_char_width)/(len(display_text)-1)
				current_x = draw_rect.left+timekeeper.alignment_spacing
				for char in display_text:
					char_surf = timekeeper.font.render(char, True, text_color)
					surf_top = y_pos-optical_centre_offset
					surf_top = max(draw_rect.top, min(draw_rect.bottom-char_surf.get_height(), surf_top))
					cached.blit(char_surf, (current_x, surf_top))
					current_x += char_surf.get_width()+spacing
		if not drawn_stretched:
			text_surf = timekeeper.font.render(display_text, True, text_color)
			text_rect = text_surf.get_rect()
			surf_top = y_pos-optical_centre_offset
			surf_top = max(draw_rect.top, min(draw_rect.bottom-text_surf.get_height(), surf_top))
			if timekeeper.alignment=="left":
				text_rect.topleft = (draw_rect.left+timekeeper.alignment_spacing, surf_top)
			elif timekeeper.alignment=="right":
				text_rect.topright = (draw_rect.right-timekeeper.alignment_spacing, surf_top)
			else:
				text_rect.midtop = (draw_rect.centerx, surf_top)
			cached.blit(text_surf, text_rect)
	cached.set_clip(old_clip)
	timekeeper.original_surface = cached
	timekeeper._last_visual_state = (timekeeper.pressed, is_hovering)
	timekeeper._needs_redraw = False
	timekeeper._needs_transform = True


def _update_size(timekeeper: Timekeeper) -> None:
	"""
	Internally used to recompute the timekeeper's width and height from its time when auto_size is enabled.

	Args:
		timekeeper (Timekeeper): The timekeeper to resize.
	"""
	if timekeeper.auto_size:
		display_text = timekeeper.get_display_text()
		text_w = timekeeper.font.size(display_text)[0]
		extra_w = text_w+(timekeeper.alignment_spacing*2)
		timekeeper.width = (extra_w+39)//40*40
		timekeeper.height = (timekeeper.font.size(display_text)[1]+39)//40*40
		if timekeeper.min_width: timekeeper.width = max(timekeeper.width, timekeeper.min_width)
		if timekeeper.max_width: timekeeper.width = min(timekeeper.width, timekeeper.max_width)
		if timekeeper.min_height: timekeeper.height = max(timekeeper.height, timekeeper.min_height)
		if timekeeper.max_height: timekeeper.height = min(timekeeper.height, timekeeper.max_height)
		timekeeper.rect = pygame.Rect(timekeeper.x, timekeeper.y, timekeeper.width, timekeeper.height)


def _split_to_values(widget: Timekeeper, total_seconds: float) -> None:
	"""
	Internally used to split a total number of seconds into hours/minutes/seconds/milliseconds and store them
	on the timekeeper, updating its size and triggering the '<TICKING>' event if the display text changed.

	Args:
		widget (Timekeeper): The timekeeper to update.
		total_seconds (float): The total time in seconds, positive or negative.
	"""
	old_display_text = widget.get_display_text()
	base_seconds = math.floor(total_seconds)
	widget.is_negative = base_seconds<0
	abs_secs = abs(base_seconds)
	widget.hours = int(abs_secs//3600)
	widget.minutes = int((abs_secs%3600)//60)
	widget.seconds = int(abs_secs%60)
	widget.milliseconds = abs(total_seconds)-int(abs(abs_secs))
	_update_size(widget)
	if widget.get_display_text()!=old_display_text:
		widget.needs_redraw = True
		widget.trigger_event(epw_types.TICKING)