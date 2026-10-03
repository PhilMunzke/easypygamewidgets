# slider.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets
"""A slider widget for pygame."""

from __future__ import annotations

import math
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


# PERFECTION
# better 'width' and 'height' calculations ❌

class Slider(Widget, Tooltipable, Screenable, Deletable):
	"""Initializes a slider widget for pygame."""

	@_themed
	def __init__(self, screen: easypygamewidgets.Screen | None = None, auto_size: bool = True, width: int = 180,
	             height: int = 16,
	             text: str = "easypygamewidgets Slider", start: int | float = 0,
	             end: int | float = 100, initial_value: int | None = None, state: str | None = None,
	             top_left_corner_radius: int = sd["top_left_corner_radius"],
	             top_right_corner_radius: int = sd["top_right_corner_radius"],
	             bottom_left_corner_radius: int = sd["bottom_left_corner_radius"],
	             bottom_right_corner_radius: int = sd["bottom_right_corner_radius"],
	             dot_radius: int | None = sd["dot_radius"],
	             max_extra_dot_radius: int | None = sd["max_extra_dot_radius"],
	             move_text_with_dot_radius: bool = sd["move_text_with_dot_radius"],
	             active_unpressed_text_color: color_type = sd["active_unpressed_text_color"],
	             disabled_unpressed_text_color: color_type = sd["disabled_unpressed_text_color"],
	             active_hover_text_color: color_type = sd["active_hover_text_color"],
	             disabled_hover_text_color: color_type = sd["disabled_hover_text_color"],
	             active_pressed_text_color: color_type = sd["active_pressed_text_color"],
	             active_unpressed_used_background_color: color_type = sd["active_unpressed_used_background_color"],
	             disabled_unpressed_used_background_color: color_type = sd["disabled_unpressed_used_background_color"],
	             active_hover_used_background_color: color_type = sd["active_hover_used_background_color"],
	             disabled_hover_used_background_color: color_type = sd["disabled_hover_used_background_color"],
	             active_pressed_used_background_color: color_type = sd["active_pressed_used_background_color"],
	             active_unpressed_unused_background_color: color_type = sd["active_unpressed_unused_background_color"],
	             disabled_unpressed_unused_background_color: color_type =
	             sd["disabled_unpressed_unused_background_color"],
	             active_hover_unused_background_color: color_type = sd["active_hover_unused_background_color"],
	             disabled_hover_unused_background_color: color_type = sd["disabled_hover_unused_background_color"],
	             active_pressed_unused_background_color: color_type = sd["active_pressed_unused_background_color"],
	             active_unpressed_dot_color: color_type = sd["active_unpressed_dot_color"],
	             disabled_unpressed_dot_color: color_type = sd["disabled_unpressed_dot_color"],
	             active_hover_dot_color: color_type = sd["active_hover_dot_color"],
	             disabled_hover_dot_color: color_type = sd["disabled_hover_dot_color"],
	             active_pressed_dot_color: color_type = sd["active_pressed_dot_color"],
	             active_unpressed_border_color: color_type = sd["active_unpressed_border_color"],
	             disabled_unpressed_border_color: color_type = sd["disabled_unpressed_border_color"],
	             active_hover_border_color: color_type = sd["active_hover_border_color"],
	             disabled_hover_border_color: color_type = sd["disabled_hover_border_color"],
	             active_pressed_border_color: color_type = sd["active_pressed_border_color"],
	             active_pressed_display_color: color_type = sd["active_pressed_display_color"],
	             active_hover_display_color: color_type = sd["active_hover_display_color"],
	             active_unpressed_display_color: color_type = sd["active_unpressed_display_color"],
	             disabled_hover_display_color: color_type = sd["disabled_hover_display_color"],
	             disabled_unpressed_display_color: color_type = sd["disabled_unpressed_display_color"],
	             border_thickness: int = sd["border_thickness"],
	             hide_text: bool = False,
	             hide_used_background: bool = False,
	             hide_unused_background: bool = False,
	             hide_dot: bool = False,
	             hide_border: bool = False,
	             hide_display: bool = False,
	             active_hover_cursor: pygame.Cursor | None = sd["active_hover_cursor"],
	             disabled_hover_cursor: pygame.Cursor | None = sd["disabled_hover_cursor"],
	             active_pressed_cursor: pygame.Cursor | None = sd["active_pressed_cursor"],
	             font: pygame.font.Font | pygame.font.SysFont = sd["font"], alignment: str = "center",
	             alignment_spacing: int = sd["alignment_spacing"],
	             show_value_when_pressed: bool = sd["show_value_when_pressed"],
	             show_value_when_hovered: bool = sd["show_value_when_hovered"],
	             show_value_when_unpressed: bool = sd["show_value_when_unpressed"],
	             show_value_when_disabled: bool = sd["show_value_when_disabled"],
	             round_display_value: int = sd["round_display_value"],
	             show_full_rounding_of_whole_numbers: bool = sd["show_full_rounding_of_whole_numbers"],
	             trigger_hold_delay: int = sd["trigger_hold_delay"], layer: int = sd["layer"],
	             line_spacing: int = sd["line_spacing"], tooltip: easypygamewidgets.Tooltip | None = None,
	             min_width: int | None = sd["min_width"], max_width: int | None = sd["max_width"],
	             min_height: int | None = sd["min_height"],
	             max_height: int | None = sd["max_height"],
	             alpha_based_collision_system: bool = sd["alpha_based_collision_system"],
	             anchor_x: str = sd["anchor_x"], anchor_y: str = sd["anchor_y"],
	             visible: bool = sd["visible"], data: Any = None) -> None:
		"""
		Initializes a Slider widget.

		Args:
			screen: The Screen this slider is attached to. If None, the slider is created without a parent screen.
			auto_size: If True, width and height are computed from the required space instead of using the given
				width/height.
			width: Fixed slider width in pixels. Ignored if auto_size is True.
			height: Fixed slider height in pixels. Ignored if auto_size is True.
			text: The slider's label text. Supports multi-line text via '\n'.
			start: The minimum value of the slider's range.
			end: The maximum value of the slider's range.
			initial_value: The slider's starting value. Defaults to start if not given.
			state: Initial state, 'enabled' or 'disabled'. Defaults to 'enabled' if not given.
			top_left_corner_radius: Corner radius in pixels for the top-left corner.
			top_right_corner_radius: Corner radius in pixels for the top-right corner.
			bottom_left_corner_radius: Corner radius in pixels for the bottom-left corner.
			bottom_right_corner_radius: Corner radius in pixels for the bottom-right corner.
			dot_radius: Radius in pixels of the draggable dot. Defaults to half the slider height if not given.
			max_extra_dot_radius: Maximum extra radius in pixels the dot grows while hovered or pressed.
			move_text_with_dot_radius: If True, the label text shifts vertically to stay unoccupied by the dot when it
				grows.
			active_unpressed_text_color: RGBA text color while enabled, not pressed, not hovered.
			disabled_unpressed_text_color: RGBA text color while disabled, not hovered.
			active_hover_text_color: RGBA text color while enabled and hovered.
			disabled_hover_text_color: RGBA text color while disabled and hovered.
			active_pressed_text_color: RGBA text color while enabled and pressed.
			active_unpressed_used_background_color: RGBA color of the filled (used) track while enabled, not pressed,
				not hovered.
			disabled_unpressed_used_background_color: RGBA color of the filled (used) track while disabled, not hovered.
			active_hover_used_background_color: RGBA color of the filled (used) track while enabled and hovered.
			disabled_hover_used_background_color: RGBA color of the filled (used) track while disabled and hovered.
			active_pressed_used_background_color: RGBA color of the filled (used) track while enabled and pressed.
			active_unpressed_unused_background_color: RGBA color of the empty (unused) track while enabled, not
				pressed, not hovered.
			disabled_unpressed_unused_background_color: RGBA color of the empty (unused) track while disabled,
				not hovered.
			active_hover_unused_background_color: RGBA color of the empty (unused) track while enabled and hovered.
			disabled_hover_unused_background_color: RGBA color of the empty (unused) track while disabled and hovered.
			active_pressed_unused_background_color: RGBA color of the empty (unused) track while enabled and pressed.
			active_unpressed_dot_color: RGBA dot color while enabled, not pressed, not hovered.
			disabled_unpressed_dot_color: RGBA dot color while disabled, not hovered.
			active_hover_dot_color: RGBA dot color while enabled and hovered.
			disabled_hover_dot_color: RGBA dot color while disabled and hovered.
			active_pressed_dot_color: RGBA dot color while enabled and pressed.
			active_unpressed_border_color: RGBA border color while enabled, not pressed, not hovered.
			disabled_unpressed_border_color: RGBA border color while disabled, not hovered.
			active_hover_border_color: RGBA border color while enabled and hovered.
			disabled_hover_border_color: RGBA border color while disabled and hovered.
			active_pressed_border_color: RGBA border color while enabled and pressed.
			active_pressed_display_color: RGBA color of the value display while enabled and pressed.
			active_hover_display_color: RGBA color of the value display while enabled and hovered.
			active_unpressed_display_color: RGBA color of the value display while enabled, not pressed, not hovered.
			disabled_hover_display_color: RGBA color of the value display while disabled and hovered.
			disabled_unpressed_display_color: RGBA color of the value display while disabled, not hovered.
			border_thickness: Border width in pixels.
			hide_text: If True, the label text is not rendered.
			hide_used_background: If True, the filled (used) track is not rendered.
			hide_unused_background: If True, the empty (unused) track is not rendered.
			hide_dot: If True, the dot is not rendered.
			hide_border: If True, the border is not rendered.
			hide_display: If True, the value display is not rendered.
			active_hover_cursor: Custom cursor shown on hover while enabled.
			disabled_hover_cursor: Custom cursor shown on hover while disabled.
			active_pressed_cursor: Custom cursor shown while pressed.
			font: The pygame font used to render the label and value display text.
			alignment: Label text alignment: 'left', 'right', 'center' or 'stretched'.
			alignment_spacing: Horizontal padding reserved around aligned text.
			show_value_when_pressed: If True, the value display is shown while the slider is pressed.
			show_value_when_hovered: If True, the value display is shown while the slider is hovered.
			show_value_when_unpressed: If True, the value display is shown while the slider is not pressed.
			show_value_when_disabled: If True, the value display is shown while the slider is disabled.
			round_display_value: Number of decimal places to round the displayed value to.
			show_full_rounding_of_whole_numbers: If True, whole numbers keep their trailing zeros when rounded
				(e.g. '5.00' instead of '5').
			trigger_hold_delay: Time in milliseconds before a held drag starts triggering the HOLD event.
			layer: Draw order layer; higher values draw on top.
			line_spacing: Line height in pixels for multi-line text.
			tooltip: A Tooltip widget shown on hover, if given.
			min_width: Minimum width in pixels when auto_size is True.
			max_width: Maximum width in pixels when auto_size is True.
			min_height: Minimum height in pixels when auto_size is True.
			max_height: Maximum height in pixels when auto_size is True.
			alpha_based_collision_system: Use a pixel alpha test to check for collisions instead of math calculations.
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
			if min_width:
				self._width = max(width, min_width)
			if max_width:
				self._width = min(width, max_width)
			if min_height:
				self._height = max(height, min_height)
			if max_height:
				self._height = min(height, max_height)
		self._text = text
		self._start = start
		self._start = start
		self._end = end
		self._value = min(max(initial_value or start, start), end)
		self._top_left_corner_radius = top_left_corner_radius
		self._top_right_corner_radius = top_right_corner_radius
		self._bottom_left_corner_radius = bottom_left_corner_radius
		self._bottom_right_corner_radius = bottom_right_corner_radius
		if not dot_radius:
			self._dot_radius = height//2
		else:
			self._dot_radius = dot_radius
		if not max_extra_dot_radius:
			self._max_extra_dot_radius = self._dot_radius//5+1
		else:
			self._max_extra_dot_radius = max_extra_dot_radius
		self._move_text_with_dot_radius = move_text_with_dot_radius
		self._active_unpressed_text_color = misc.normalize_color(active_unpressed_text_color)
		self._disabled_unpressed_text_color = misc.normalize_color(disabled_unpressed_text_color)
		self._active_hover_text_color = misc.normalize_color(active_hover_text_color)
		self._disabled_hover_text_color = misc.normalize_color(disabled_hover_text_color)
		self._active_pressed_text_color = misc.normalize_color(active_pressed_text_color)
		self._active_unpressed_used_background_color = misc.normalize_color(active_unpressed_used_background_color)
		self._disabled_unpressed_used_background_color = misc.normalize_color(disabled_unpressed_used_background_color)
		self._active_hover_used_background_color = misc.normalize_color(active_hover_used_background_color)
		self._disabled_hover_used_background_color = misc.normalize_color(disabled_hover_used_background_color)
		self._active_pressed_used_background_color = misc.normalize_color(active_pressed_used_background_color)
		self._active_unpressed_unused_background_color = misc.normalize_color(active_unpressed_unused_background_color)
		self._disabled_unpressed_unused_background_color = misc.normalize_color(
			disabled_unpressed_unused_background_color
		)
		self._active_hover_unused_background_color = misc.normalize_color(active_hover_unused_background_color)
		self._disabled_hover_unused_background_color = misc.normalize_color(disabled_hover_unused_background_color)
		self._active_pressed_unused_background_color = misc.normalize_color(active_pressed_unused_background_color)
		self._active_unpressed_dot_color = misc.normalize_color(active_unpressed_dot_color)
		self._disabled_unpressed_dot_color = misc.normalize_color(disabled_unpressed_dot_color)
		self._active_hover_dot_color = misc.normalize_color(active_hover_dot_color)
		self._disabled_hover_dot_color = misc.normalize_color(disabled_hover_dot_color)
		self._active_pressed_dot_color = misc.normalize_color(active_pressed_dot_color)
		self._active_unpressed_border_color = misc.normalize_color(active_unpressed_border_color)
		self._disabled_unpressed_border_color = misc.normalize_color(disabled_unpressed_border_color)
		self._active_hover_border_color = misc.normalize_color(active_hover_border_color)
		self._disabled_hover_border_color = misc.normalize_color(disabled_hover_border_color)
		self._active_pressed_border_color = misc.normalize_color(active_pressed_border_color)
		self._active_pressed_display_color = misc.normalize_color(active_pressed_display_color)
		self._active_hover_display_color = misc.normalize_color(active_hover_display_color)
		self._active_unpressed_display_color = misc.normalize_color(active_unpressed_display_color)
		self._disabled_hover_display_color = misc.normalize_color(disabled_hover_display_color)
		self._disabled_unpressed_display_color = misc.normalize_color(disabled_unpressed_display_color)
		self._border_thickness = border_thickness
		self._hide_text = hide_text
		self._hide_used_background = hide_used_background
		self._hide_unused_background = hide_unused_background
		self._hide_dot = hide_dot
		self._hide_border = hide_border
		self._hide_display = hide_display
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
						f"No custom cursor is used for the slider '{text}' because it's not a pygame.Cursor "
						f"object. {cursor} is a {type(cursor)}"
					)
				self._cursors[name] = None
		self._font = font
		self._alignment = alignment
		self._alignment_spacing = alignment_spacing
		self._show_value_when_pressed = show_value_when_pressed
		self._show_value_when_hovered = show_value_when_hovered
		self._show_value_when_unpressed = show_value_when_unpressed
		self._show_value_when_disabled = show_value_when_disabled
		self._round_display_value = round_display_value
		self._show_full_rounding_of_whole_numbers = show_full_rounding_of_whole_numbers
		self._trigger_hold_delay = trigger_hold_delay
		self._layer = layer
		self._tooltip = tooltip
		if tooltip:
			tooltip.configure(layer=self._layer+1)
			if not tooltip.style:
				tooltip.configure(
					active_unpressed_text_color=self._active_unpressed_text_color,
					active_unpressed_background_color=self._active_unpressed_used_background_color,
					active_unpressed_border_color=self._active_unpressed_border_color
				)
		self._line_spacing = line_spacing
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
		self._extra_dot_radius = 0
		self._pressed_before = False
		self._last_value_update_time = 0
		self._bindings = {}
		self._dialog = None
		self._is_hovered = False
		self._last_visual_state = None
		self._needs_redraw = True
		self._cached_surface = None
		self._needs_transform = True
		self._original_surface = pygame.Surface((1, 1))
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

		_safe_set_linesize(font, line_spacing)

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
		return int(self._width*self._current_scale)

	@width.setter
	def width(self, value):
		self._width = value

	@property
	def height(self):
		return int(self._height*self._current_scale)

	@height.setter
	def height(self, value):
		self._height = value

	@property
	def text(self):
		return self._text

	@text.setter
	def text(self, value):
		self._text = value

	@property
	def start(self):
		return self._start

	@start.setter
	def start(self, value):
		self._start = value

	@property
	def end(self):
		return self._end

	@end.setter
	def end(self, value):
		self._end = value

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, v):
		self._value = v

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
	def dot_radius(self):
		return self._dot_radius

	@dot_radius.setter
	def dot_radius(self, value):
		self._dot_radius = value

	@property
	def max_extra_dot_radius(self):
		return self._max_extra_dot_radius

	@max_extra_dot_radius.setter
	def max_extra_dot_radius(self, value):
		self._max_extra_dot_radius = value

	@property
	def move_text_with_dot_radius(self):
		return self._move_text_with_dot_radius

	@move_text_with_dot_radius.setter
	def move_text_with_dot_radius(self, value):
		self._move_text_with_dot_radius = value

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
	def active_unpressed_used_background_color(self):
		return self._active_unpressed_used_background_color

	@active_unpressed_used_background_color.setter
	def active_unpressed_used_background_color(self, value):
		self._active_unpressed_used_background_color = misc.normalize_color(value)

	@property
	def disabled_unpressed_used_background_color(self):
		return self._disabled_unpressed_used_background_color

	@disabled_unpressed_used_background_color.setter
	def disabled_unpressed_used_background_color(self, value):
		self._disabled_unpressed_used_background_color = misc.normalize_color(value)

	@property
	def active_hover_used_background_color(self):
		return self._active_hover_used_background_color

	@active_hover_used_background_color.setter
	def active_hover_used_background_color(self, value):
		self._active_hover_used_background_color = misc.normalize_color(value)

	@property
	def disabled_hover_used_background_color(self):
		return self._disabled_hover_used_background_color

	@disabled_hover_used_background_color.setter
	def disabled_hover_used_background_color(self, value):
		self._disabled_hover_used_background_color = misc.normalize_color(value)

	@property
	def active_pressed_used_background_color(self):
		return self._active_pressed_used_background_color

	@active_pressed_used_background_color.setter
	def active_pressed_used_background_color(self, value):
		self._active_pressed_used_background_color = misc.normalize_color(value)

	@property
	def active_unpressed_unused_background_color(self):
		return self._active_unpressed_unused_background_color

	@active_unpressed_unused_background_color.setter
	def active_unpressed_unused_background_color(self, value):
		self._active_unpressed_unused_background_color = misc.normalize_color(value)

	@property
	def disabled_unpressed_unused_background_color(self):
		return self._disabled_unpressed_unused_background_color

	@disabled_unpressed_unused_background_color.setter
	def disabled_unpressed_unused_background_color(self, value):
		self._disabled_unpressed_unused_background_color = misc.normalize_color(value)

	@property
	def active_hover_unused_background_color(self):
		return self._active_hover_unused_background_color

	@active_hover_unused_background_color.setter
	def active_hover_unused_background_color(self, value):
		self._active_hover_unused_background_color = misc.normalize_color(value)

	@property
	def disabled_hover_unused_background_color(self):
		return self._disabled_hover_unused_background_color

	@disabled_hover_unused_background_color.setter
	def disabled_hover_unused_background_color(self, value):
		self._disabled_hover_unused_background_color = misc.normalize_color(value)

	@property
	def active_pressed_unused_background_color(self):
		return self._active_pressed_unused_background_color

	@active_pressed_unused_background_color.setter
	def active_pressed_unused_background_color(self, value):
		self._active_pressed_unused_background_color = misc.normalize_color(value)

	@property
	def active_unpressed_dot_color(self):
		return self._active_unpressed_dot_color

	@active_unpressed_dot_color.setter
	def active_unpressed_dot_color(self, value):
		self._active_unpressed_dot_color = misc.normalize_color(value)

	@property
	def disabled_unpressed_dot_color(self):
		return self._disabled_unpressed_dot_color

	@disabled_unpressed_dot_color.setter
	def disabled_unpressed_dot_color(self, value):
		self._disabled_unpressed_dot_color = misc.normalize_color(value)

	@property
	def active_hover_dot_color(self):
		return self._active_hover_dot_color

	@active_hover_dot_color.setter
	def active_hover_dot_color(self, value):
		self._active_hover_dot_color = misc.normalize_color(value)

	@property
	def disabled_hover_dot_color(self):
		return self._disabled_hover_dot_color

	@disabled_hover_dot_color.setter
	def disabled_hover_dot_color(self, value):
		self._disabled_hover_dot_color = misc.normalize_color(value)

	@property
	def active_pressed_dot_color(self):
		return self._active_pressed_dot_color

	@active_pressed_dot_color.setter
	def active_pressed_dot_color(self, value):
		self._active_pressed_dot_color = misc.normalize_color(value)

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
	def active_pressed_display_color(self):
		return self._active_pressed_display_color

	@active_pressed_display_color.setter
	def active_pressed_display_color(self, value):
		self._active_pressed_display_color = misc.normalize_color(value)

	@property
	def active_hover_display_color(self):
		return self._active_hover_display_color

	@active_hover_display_color.setter
	def active_hover_display_color(self, value):
		self._active_hover_display_color = misc.normalize_color(value)

	@property
	def active_unpressed_display_color(self):
		return self._active_unpressed_display_color

	@active_unpressed_display_color.setter
	def active_unpressed_display_color(self, value):
		self._active_unpressed_display_color = misc.normalize_color(value)

	@property
	def disabled_hover_display_color(self):
		return self._disabled_hover_display_color

	@disabled_hover_display_color.setter
	def disabled_hover_display_color(self, value):
		self._disabled_hover_display_color = misc.normalize_color(value)

	@property
	def disabled_unpressed_display_color(self):
		return self._disabled_unpressed_display_color

	@disabled_unpressed_display_color.setter
	def disabled_unpressed_display_color(self, value):
		self._disabled_unpressed_display_color = misc.normalize_color(value)

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
	def hide_used_background(self):
		return self._hide_used_background

	@hide_used_background.setter
	def hide_used_background(self, value):
		self._hide_used_background = value

	@property
	def hide_unused_background(self):
		return self._hide_unused_background

	@hide_unused_background.setter
	def hide_unused_background(self, value):
		self._hide_unused_background = value

	@property
	def hide_dot(self):
		return self._hide_dot

	@hide_dot.setter
	def hide_dot(self, value):
		self._hide_dot = value

	@property
	def hide_border(self):
		return self._hide_border

	@hide_border.setter
	def hide_border(self, value):
		self._hide_border = value

	@property
	def hide_display(self):
		return self._hide_display

	@hide_display.setter
	def hide_display(self, value):
		self._hide_display = value

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
		self._font.set_linesize(self._line_spacing)

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
	def show_value_when_pressed(self):
		return self._show_value_when_pressed

	@show_value_when_pressed.setter
	def show_value_when_pressed(self, value):
		self._show_value_when_pressed = value

	@property
	def show_value_when_hovered(self):
		return self._show_value_when_hovered

	@show_value_when_hovered.setter
	def show_value_when_hovered(self, value):
		self._show_value_when_hovered = value

	@property
	def show_value_when_unpressed(self):
		return self._show_value_when_unpressed

	@show_value_when_unpressed.setter
	def show_value_when_unpressed(self, value):
		self._show_value_when_unpressed = value

	@property
	def show_value_when_disabled(self):
		return self._show_value_when_disabled

	@show_value_when_disabled.setter
	def show_value_when_disabled(self, value):
		self._show_value_when_disabled = value

	@property
	def round_display_value(self):
		return self._round_display_value

	@round_display_value.setter
	def round_display_value(self, value):
		self._round_display_value = value

	@property
	def show_full_rounding_of_whole_numbers(self):
		return self._show_full_rounding_of_whole_numbers

	@show_full_rounding_of_whole_numbers.setter
	def show_full_rounding_of_whole_numbers(self, value):
		self._show_full_rounding_of_whole_numbers = value

	@property
	def trigger_hold_delay(self):
		return self._trigger_hold_delay

	@trigger_hold_delay.setter
	def trigger_hold_delay(self, value):
		self._trigger_hold_delay = value

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
		self._tooltip = value

	@property
	def line_spacing(self):
		return self._line_spacing

	@line_spacing.setter
	def line_spacing(self, value):
		self._line_spacing = value
		self._font.set_linesize(value)

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
	def extra_dot_radius(self):
		return self._extra_dot_radius

	@extra_dot_radius.setter
	def extra_dot_radius(self, value):
		self._extra_dot_radius = value

	@property
	def pressed_before(self):
		return self._pressed_before

	@pressed_before.setter
	def pressed_before(self, value):
		self._pressed_before = value

	@property
	def last_value_update_time(self):
		return self._last_value_update_time

	@last_value_update_time.setter
	def last_value_update_time(self, value):
		self._last_value_update_time = value

	@property
	def bindings(self):
		return self._bindings

	@bindings.setter
	def bindings(self, value):
		self._bindings = value

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

	def configure(self, **kwargs: Unpack[TypeHints.SliderConfig]) -> Slider:
		"""
		Updates one or more of the slider's attributes.

		Args:
			**kwargs: Slider attributes to update as defined in TypeHints.SliderConfig

		Returns:
			Slider (Slider): This slider instance to allow method chaining.
		"""
		for key, value in kwargs.items():
			setattr(self, key, value)
		self._needs_redraw = True
		self._needs_transform = True
		if any(
				k in kwargs for k in
				(
						'auto_size', 'x', 'y', 'width', 'height', 'min_width', 'max_width', 'min_height', 'max_height',
						'anchor_x', 'anchor_y'
				)
		):
			if self._auto_size:
				if self._min_width:
					self._width = max(self._width, self._min_width)
				if self._max_width:
					self._width = min(self._width, self._max_width)
				if self._min_height:
					self._height = max(self._height, self._min_height)
				if self._max_height:
					self._height = min(self._height, self._max_height)
			self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
		if 'screen' in kwargs:
			self.set_screen(kwargs["screen"])
		if 'layer' in kwargs:
			misc._resort_layers()
		if 'line_spacing' in kwargs or 'font' in kwargs:
			_safe_set_linesize(self._font, self._line_spacing)
		return self

	def config(self, **kwargs: Unpack[TypeHints.SliderConfig]) -> Slider:
		"""
		Updates one or more of the slider's attributes.

		Args:
			**kwargs: Slider attributes to update as defined in TypeHints.SliderConfig

		Returns:
			Slider (Slider): This slider instance to allow method chaining.
		"""
		return self.configure(**kwargs)

	def get(self) -> int | float:
		"""
		Returns the slider's current value.

		Returns:
			int | float: The slider's current value.
		"""
		return self._value

	def set(self, value: int | float) -> None:
		"""
		Sets the slider's current value inbounds of the slider's start/end range.

		Args:
			value: The value to set.
		"""
		self._value = min(max(value, self._start), self._end)
		self._needs_redraw = True

	def scale(self, value: int | float = 1, frames_to_finish: int = 1) -> Slider:
		"""
		Scale the slider by a factor. It's only a visual scale so upscaling could look pixelated.

		Args:
			 value (int|float): the scale factor
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Slider (Slider): This slider instance to allow method chaining.
		"""
		if frames_to_finish<=0:
			frames_to_finish = 1
		self._target_scale = value
		self._scale_step = (self._target_scale-self._current_scale)/frames_to_finish
		self._update_animation()
		return self

	def rotate(self, value: int | float = 0, frames_to_finish: int = 1) -> Slider:
		"""
		Rotate the slider by a degree.

		Args:
			 value (int|float): the rotation degree
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Slider (Slider): This slider instance to allow method chaining.
		"""
		if frames_to_finish<=0:
			frames_to_finish = 1
		self._target_rotation = value
		self._rotation_step = (self._target_rotation-self._current_rotation)/frames_to_finish
		self._update_animation()
		return self

	def rotozoom(self, scale: int | float = 1, rotation: int | float = 0, frames_to_finish: int = 1) -> Slider:
		"""
		Rotate the slider by a degree and scale it.

		Args:
			 scale (int|float): the scale factor
			 rotation (int|float): the rotation degree
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Slider (Slider): This slider instance to allow method chaining.
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

	def offset(self, value: Iterable[int] = (0, 0), frames_to_finish: int = 1) -> Slider:
		"""
		Offset the slider by an x and y value.

		Args:
			 value: an iterable thing with two values. The first being the x and the second the y offset.
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Slider (Slider): This slider instance to allow method chaining.
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
		Internally used to draw the slider.

		Args:
			surface (pygame.Surface): The surface to draw the slider on.
		"""
		if not self._alive or not self._visible:
			return
		mouse_pos = pygame.mouse.get_pos()
		is_hovering = misc._is_point_over_widget(self, mouse_pos)

		if self._auto_size:
			temp_surf = self._font.render(self._text, True, (0, 0, 0))
			self._width = temp_surf.get_width()+40+(self._alignment_spacing-20)
			if self._min_width:
				self._width = max(self._width, self._min_width)
			if self._max_width:
				self._width = min(self._width, self._max_width)
			if self._min_height:
				self._height = max(self._height, self._min_height)
			if self._max_height:
				self._height = min(self._height, self._max_height)
			self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
		current_visual_state = (self._pressed, is_hovering)
		if self._needs_redraw or self._last_visual_state!=current_visual_state:
			_render_slider_surface(self, is_hovering)

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
		if self._tooltip:
			if self._tooltip.visible:
				if not self._pressed and not is_hovering:
					self._tooltip.hide()

	def _react(self, event: pygame.Event | None = None) -> None:
		"""
		Internally used to react to events.

		Args:
			event (pygame.Event, optional): The event to react to.
		"""
		if self._state!="enabled" or not self._visible:
			return
		mouse_pos = pygame.mouse.get_pos()
		is_inside = misc._is_point_over_widget(self, mouse_pos)

		def update_value() -> None:
			offset_x, offset_y = misc._get_offset(self)
			total_offset_x = offset_x+round(self._current_offset[0])
			total_offset_y = offset_y+round(self._current_offset[1])
			draw_rect = self._rect.move(total_offset_x, total_offset_y)
			x, y = mouse_pos
			scale = self._current_scale
			rotation = self._current_rotation
			cx, cy = draw_rect.center
			if rotation!=0:
				v = pygame.math.Vector2(x-cx, y-cy)
				v = v.rotate(rotation)
				x, y = cx+v.x, cy+v.y
			if scale!=1 and scale!=0:
				x = cx+(x-cx)/scale
				y = cy+(y-cy)/scale
			orig_rect = self._original_surface.get_rect(center=(cx, cy))

			temp_surf = self._font.render(self._text, True, (0, 0, 0))
			text_height = temp_surf.get_height()
			track_y = orig_rect.top+text_height+10+self._height//2
			extra_dot = self._dot_radius+self._max_extra_dot_radius
			track_y = max(track_y, orig_rect.top+extra_dot)
			widest_magnitude = max(abs(self._start), abs(self._end))
			integer_digits = len(str(int(widest_magnitude)))
			decimal_digits = self._round_display_value if self._round_display_value>0 else 0
			widest_value_str = "9"*integer_digits+("."+"9"*decimal_digits if decimal_digits else "")
			if self._start<0 or self._end<0:
				widest_value_str = "-"+widest_value_str
			side_margin = self._max_extra_dot_radius+self._font.size(widest_value_str)[0]//2
			track_rect = pygame.Rect(
				orig_rect.x+side_margin, track_y-(self._height//2),
				orig_rect.width-side_margin*2, self._height
			)
			relative_x = x-track_rect.x
			pct = relative_x/track_rect.width
			pct = max(0, min(1, pct))
			new_slider_value = self._start+(pct*(self._end-self._start))
			moved = self._value!=new_slider_value
			self._value = new_slider_value
			current_time = pygame.time.get_ticks()
			if not self._pressed_before:
				self.trigger_event(epw_types.PRESS)
				self._pressed_before = True
			else:
				if moved:
					self._last_value_update_time = current_time
					self.trigger_event(epw_types.DRAG)
				else:
					if current_time-self._last_value_update_time>self._trigger_hold_delay:
						self.trigger_event(epw_types.HOLD)

		if not event:
			if self._pressed:
				if pygame.mouse.get_pressed()[0]:
					update_value()
				else:
					self._pressed = False
					self._pressed_before = False
					self.trigger_event(epw_types.RELEASE)
		else:
			if event.type==pygame.KEYDOWN:
				misc._trigger_key_bindings(self, event)
			elif event.type==pygame.MOUSEBUTTONDOWN:
				if event.button==1 and is_inside:
					self._pressed = True
					update_value()
			elif event.type==pygame.MOUSEBUTTONUP:
				if event.button==1 and self._pressed:
					self._pressed = False
					self._pressed_before = False
					self.trigger_event(epw_types.RELEASE)
			elif event.type==pygame.MOUSEMOTION:
				if self._pressed:
					update_value()
		t = pygame.time.get_ticks()*0.01
		pulse = (1-math.cos(t*math.pi))*0.5
		if self._pressed:
			self._extra_dot_radius = min(self._max_extra_dot_radius, self._extra_dot_radius+pulse)
		else:
			self._extra_dot_radius = max(0, self._extra_dot_radius-pulse)


def _render_slider_surface(slider: Slider, is_hovering: bool) -> None:
	"""
	Internally used to draw the slider surface once and cache it.

	Args:
		slider (Slider): the widget to render the surface for
		is_hovering (bool): whether the mouse is hovering over the widget
	"""
	if slider.state=="enabled":
		if slider.pressed:
			text_color = slider.active_pressed_text_color
			bg_color_used = slider.active_pressed_used_background_color
			bg_color_unused = slider.active_pressed_unused_background_color
			brd_color = slider.active_pressed_border_color
			dot_color = slider.active_pressed_dot_color
			display_color = slider.active_pressed_display_color
		elif is_hovering:
			text_color = slider.active_hover_text_color
			bg_color_used = slider.active_hover_used_background_color
			bg_color_unused = slider.active_hover_unused_background_color
			brd_color = slider.active_hover_border_color
			dot_color = slider.active_hover_dot_color
			display_color = slider.active_hover_display_color
		else:
			text_color = slider.active_unpressed_text_color
			bg_color_used = slider.active_unpressed_used_background_color
			bg_color_unused = slider.active_unpressed_unused_background_color
			brd_color = slider.active_unpressed_border_color
			dot_color = slider.active_unpressed_dot_color
			display_color = slider.active_unpressed_display_color
	else:
		if is_hovering:
			text_color = slider.disabled_hover_text_color
			bg_color_used = slider.disabled_hover_used_background_color
			bg_color_unused = slider.disabled_hover_unused_background_color
			brd_color = slider.disabled_hover_border_color
			dot_color = slider.disabled_hover_dot_color
			display_color = slider.disabled_hover_display_color
		else:
			text_color = slider.disabled_unpressed_text_color
			bg_color_used = slider.disabled_unpressed_used_background_color
			bg_color_unused = slider.disabled_unpressed_unused_background_color
			brd_color = slider.disabled_unpressed_border_color
			dot_color = slider.disabled_unpressed_dot_color
			display_color = slider.disabled_unpressed_display_color
	base_width = slider._width
	base_height = slider._height
	text_surf = slider.font.render(slider.text, True, text_color)
	text_height = text_surf.get_height()
	track_y = text_height+10+base_height//2
	extra_dot = slider.dot_radius+slider.max_extra_dot_radius
	track_y = max(track_y, extra_dot)
	display_dot_offset = slider.dot_radius+slider.max_extra_dot_radius if slider.move_text_with_dot_radius else slider.dot_radius
	extra_bottom = 25+display_dot_offset+text_height//2 if not slider.hide_display else 0
	canvas_height = track_y+base_height//2+extra_bottom
	canvas_height = max(canvas_height, track_y+extra_dot+extra_bottom)
	widest_magnitude = max(abs(slider.start), abs(slider.end))
	integer_digits = len(str(int(widest_magnitude)))
	decimal_digits = slider.round_display_value if slider.round_display_value>0 else 0
	widest_value_str = "9"*integer_digits+("."+"9"*decimal_digits if decimal_digits else "")
	if slider.start<0 or slider.end<0:
		widest_value_str = "-"+widest_value_str
	widest_value_width = slider.font.size(widest_value_str)[0]
	side_margin = slider.max_extra_dot_radius+widest_value_width//2
	canvas_width = base_width+side_margin*2
	cached = pygame.Surface((canvas_width, canvas_height), pygame.SRCALPHA)
	local_rect = pygame.Rect(0, 0, canvas_width, canvas_height)
	track_rect = pygame.Rect(side_margin, track_y-(base_height//2), base_width, base_height)
	max_radius = min(track_rect.width, track_rect.height)//2
	tl = min(slider.top_left_corner_radius, max_radius)
	tr = min(slider.top_right_corner_radius, max_radius)
	bl = min(slider.bottom_left_corner_radius, max_radius)
	br = min(slider.bottom_right_corner_radius, max_radius)
	if not slider.hide_unused_background:
		pygame.draw.rect(
			cached, bg_color_unused, track_rect, border_top_left_radius=tl,
			border_top_right_radius=tr, border_bottom_left_radius=bl,
			border_bottom_right_radius=br
		)
	if slider.end-slider.start!=0:
		pct = (slider.value-slider.start)/(slider.end-slider.start)
	else:
		pct = 0
	pct = max(0, min(1, pct))
	used_width = int(track_rect.width*pct)
	if used_width>0 and not slider.hide_used_background:
		clip_surf = pygame.Surface(track_rect.size, pygame.SRCALPHA)
		mask_rect = pygame.Rect(0, 0, track_rect.width, track_rect.height)
		pygame.draw.rect(
			clip_surf, (255, 255, 255), mask_rect, border_top_left_radius=tl,
			border_bottom_left_radius=bl, border_top_right_radius=tr,
			border_bottom_right_radius=br
		)
		used_fill_rect = pygame.Rect(0, 0, used_width, track_rect.height)
		fill_surf = pygame.Surface(track_rect.size, pygame.SRCALPHA)
		pygame.draw.rect(fill_surf, bg_color_used, used_fill_rect)
		clip_surf.blit(fill_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
		cached.blit(clip_surf, track_rect.topleft)
	if not slider.hide_border:
		pygame.draw.rect(
			cached, brd_color, track_rect, width=slider.border_thickness, border_top_left_radius=tl,
			border_top_right_radius=tr, border_bottom_left_radius=bl,
			border_bottom_right_radius=br
		)
	dot_x = track_rect.x+used_width
	dot_x = max(track_rect.left+slider.dot_radius, min(dot_x, track_rect.right-slider.dot_radius))
	if not slider.hide_dot:
		pygame.draw.aacircle(
			cached, dot_color, (int(dot_x), int(track_rect.centery)),
			slider.dot_radius+slider.extra_dot_radius
		)
	if not slider.hide_display:
		if (slider.state=="enabled" or slider.show_value_when_disabled) and (
				slider.show_value_when_pressed and slider.pressed or
				slider.show_value_when_hovered and is_hovering and not slider.pressed or
				slider.show_value_when_unpressed):
			if slider.show_full_rounding_of_whole_numbers:
				display_surf = slider.font.render(
					str(round(slider.value, slider.round_display_value)), True,
					display_color
				)
			elif round(slider.value, slider.round_display_value)%1==0:
				display_surf = slider.font.render(
					str(round(slider.value, slider.round_display_value)).replace(".0", ""), True, display_color
				)
			else:
				display_surf = slider.font.render(
					str(round(slider.value, slider.round_display_value)), True,
					display_color
				)
			display_surf.set_alpha(display_color[3])
			display_rect = display_surf.get_rect()
			if slider.move_text_with_dot_radius:
				display_rect.center = (dot_x, track_rect.centery+25+slider.dot_radius+slider.extra_dot_radius)
			else:
				display_rect.center = (dot_x, track_rect.centery+25+slider.dot_radius)
			cached.blit(display_surf, display_rect)
	if not slider.hide_text:
		text_surf.set_alpha(text_color[3])
		text_rect = text_surf.get_rect()
		if slider.move_text_with_dot_radius:
			text_y_center = track_rect.centery-25-slider.dot_radius-slider.extra_dot_radius
		else:
			text_y_center = track_rect.centery-25-slider.dot_radius
		if slider.alignment=="stretched" and len(slider.text)>1 and not slider.auto_size:
			total_char_width = sum(slider.font.render(char, True, text_color).get_width() for char in slider.text)
			available_width = local_rect.width-(slider.alignment_spacing*2)
			if available_width>total_char_width:
				spacing = (available_width-total_char_width)/(len(slider.text)-1)
				current_x = local_rect.left+slider.alignment_spacing
				for char in slider.text:
					char_surf = slider.font.render(char, True, text_color)
					char_surf.set_alpha(text_color[3])
					cached.blit(char_surf, char_surf.get_rect(midleft=(current_x, text_y_center)))
					current_x += char_surf.get_width()+spacing
			else:
				cached.blit(text_surf, text_surf.get_rect(center=(local_rect.centerx, text_y_center)))
		else:
			if slider.alignment=="left":
				text_rect.midleft = (local_rect.left+slider.alignment_spacing, text_y_center)
			elif slider.alignment=="right":
				text_rect.midright = (local_rect.right-slider.alignment_spacing, text_y_center)
			else:
				text_rect.center = (local_rect.centerx, text_y_center)
			cached.blit(text_surf, text_rect)
	slider.original_surface = cached
	slider.cached_surface = cached
	slider._last_visual_state = (slider.pressed, is_hovering)
	slider._needs_redraw = False
	slider._needs_transform = True


def _safe_set_linesize(font: pygame.font.Font | pygame.font.SysFont, line_spacing: int) -> None:
	"""
	Internally used to set a font's linesize while compensating for the font's descent, so multi-line text
	spacing stays visually consistent across different fonts.

	Args:
		font (pygame.font.Font | pygame.font.SysFont): The font to update.
		line_spacing (int): The desired line spacing in pixels.
	"""
	descent = abs(font.get_descent())
	font.set_linesize(line_spacing+descent)