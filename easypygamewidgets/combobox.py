# combobox.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets
"""A combobox widget for pygame."""

from __future__ import annotations

import sys
from collections.abc import Iterable
from typing import Any, TYPE_CHECKING, Unpack

import pygame

from easypygamewidgets import misc
from easypygamewidgets.assets import epw_types, TypeHints
from easypygamewidgets.assets.epw_types import color_type
from easypygamewidgets.assets.theme import _style_dic as sd, _themed
from easypygamewidgets.masterWidgets import Deletable, Screenable, Tooltipable, Widget
from easypygamewidgets.misc import normalize_color as nc

if TYPE_CHECKING:
	import easypygamewidgets

pygame.init()

TO_UPDATE = [f"_{attr}" for attr in [
	"pressed", "state", "is_hovered", "text", "font", "alignment", "alignment_spacing", "line_spacing", "hide_text",
	"hide_background", "hide_border", "width", "height", "auto_size", "min_width", "max_width", "min_height",
	"max_height", "border_thickness", "top_left_corner_radius", "top_right_corner_radius", "bottom_left_corner_radius",
	"bottom_right_corner_radius", "focused", "cursor_visible", "cursor_position", "blinking_cursor", "scroll_offset",
	"selected_text", "hide_selection", "show", "placeholder_text", "values", "filtering", "max_dropdown_items",
	"floating_dropdown", "dropdown_open", "dropdown_scroll", "dropdown_above", "highlight",
	"casesensitive", "dropdown_spacing", "dropdown_alignment", "dropdown_alignment_spacing", "dropdown_hovered",
	"hide_dropdown_text", "hide_dropdown_background", "hide_dropdown_border",

	"active_hover_background_color", "active_hover_border_color", "active_hover_text_color",
	"active_pressed_background_color", "active_pressed_border_color", "active_pressed_text_color",
	"active_unpressed_background_color", "active_unpressed_border_color", "active_unpressed_text_color",
	"disabled_hover_background_color", "disabled_hover_border_color", "disabled_hover_text_color",
	"disabled_selection_color", "disabled_unpressed_background_color", "disabled_unpressed_border_color",
	"disabled_unpressed_text_color", "selection_color", "active_unpressed_text_dropdown_color",
	"disabled_unpressed_text_dropdown_color", "active_hover_text_dropdown_color", "disabled_hover_text_dropdown_color",
	"active_pressed_text_dropdown_color", "active_unpressed_background_dropdown_color",
	"disabled_unpressed_background_dropdown_color", "active_hover_background_dropdown_color",
	"disabled_hover_background_dropdown_color", "active_pressed_background_dropdown_color",
	"active_unpressed_border_dropdown_color", "disabled_unpressed_border_dropdown_color",
	"active_hover_border_dropdown_color", "disabled_hover_border_dropdown_color",
	"active_pressed_border_dropdown_color"
]]


class Combobox(Widget, Tooltipable, Screenable, Deletable):
	"""Initializes a combobox widget for pygame."""

	@_themed
	def __init__(self, screen: easypygamewidgets.Screen | None = None, auto_size: bool = True, width: int = 180,
	             height: int = 80, placeholder_text: str = "",
	             text: str = "", character_limit: int | None = sd["character_limit"],
	             show: str | None = None, state: str | None = None,
	             values: Any | None = None, max_dropdown_items: int = 7,
	             floating_dropdown: bool = False, dropdown_offset: Iterable[int] = (0, 4),
	             casesensitive: bool = False, dropdown_spacing: int = 8, dropdown_alignment: str = "left",
	             dropdown_alignment_spacing: int = 20,
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
	             selection_color: color_type = sd["selection_color"],
	             disabled_selection_color: color_type = sd["disabled_selection_color"],
	             active_unpressed_text_dropdown_color: color_type = sd["active_unpressed_text_dropdown_color"],
	             disabled_unpressed_text_dropdown_color: color_type = sd["disabled_unpressed_text_dropdown_color"],
	             active_hover_text_dropdown_color: color_type = sd["active_hover_text_dropdown_color"],
	             disabled_hover_text_dropdown_color: color_type = sd["disabled_hover_text_dropdown_color"],
	             active_pressed_text_dropdown_color: color_type = sd["active_pressed_text_dropdown_color"],
	             active_unpressed_background_dropdown_color: color_type =
	             sd["active_unpressed_background_dropdown_color"],
	             disabled_unpressed_background_dropdown_color: color_type =
	             sd["disabled_unpressed_background_dropdown_color"],
	             active_hover_background_dropdown_color: color_type = sd["active_hover_background_dropdown_color"],
	             disabled_hover_background_dropdown_color: color_type = sd["disabled_hover_background_dropdown_color"],
	             active_pressed_background_dropdown_color: color_type = sd["active_pressed_background_dropdown_color"],
	             active_unpressed_border_dropdown_color: color_type = sd["active_unpressed_border_dropdown_color"],
	             disabled_unpressed_border_dropdown_color: color_type = sd["disabled_unpressed_border_dropdown_color"],
	             active_hover_border_dropdown_color: color_type = sd["active_hover_border_dropdown_color"],
	             disabled_hover_border_dropdown_color: color_type = sd["disabled_hover_border_dropdown_color"],
	             active_pressed_border_dropdown_color: color_type = sd["active_pressed_border_dropdown_color"],
	             border_thickness: int = sd["border_thickness"],
	             hide_text: bool = False,
	             hide_background: bool = False,
	             hide_border: bool = False,
	             hide_selection: bool = False,
	             hide_dropdown_text: bool = False,
	             hide_dropdown_background: bool = False,
	             hide_dropdown_border: bool = False,
	             active_hover_cursor: pygame.Cursor | None = sd["active_hover_cursor"],
	             disabled_hover_cursor: pygame.Cursor | None = sd["disabled_hover_cursor"],
	             active_pressed_cursor: pygame.Cursor | None = sd["active_pressed_cursor"],
	             blinking_cursor: str = sd["blinking_cursor"], blinking_speed: int = sd["blinking_speed"],
	             font: pygame.font.Font | pygame.font.SysFont = sd["font"], alignment: str = "left",
	             alignment_spacing: int = sd["alignment_spacing"],
	             top_left_corner_radius: int = sd["top_left_corner_radius"],
	             top_right_corner_radius: int = sd["top_right_corner_radius"],
	             bottom_left_corner_radius: int = sd["bottom_left_corner_radius"],
	             bottom_right_corner_radius: int = sd["bottom_right_corner_radius"],
	             repeat_delay: int = sd["repeat_delay"], repeat_interval: int = sd["repeat_interval"],
	             layer: int = sd["layer"], line_spacing: int = sd["line_spacing"],
	             tooltip: easypygamewidgets.Tooltip | None = None, min_width: int | None = sd["min_width"],
	             max_width: int | None = sd["max_width"], min_height: int | None = sd["min_height"],
	             max_height: int | None = sd["max_height"],
	             alpha_based_collision_system: bool = sd["alpha_based_collision_system"],
	             anchor_x: str = sd["anchor_x"], anchor_y: str = sd["anchor_y"], visible: bool = sd["visible"],
	             data: Any = None) -> None:
		"""
		Initializes a Combobox widget.

		Args:
			screen: The Screen this combobox is attached to. If None, the combobox is created without a parent screen.
			auto_size: If True, width and height are computed from the text or placeholder text instead of using the
				given width/height.
			width: Fixed combobox width in pixels. Ignored if auto_size is True.
			height: Fixed combobox height in pixels. Ignored if auto_size is True.
			placeholder_text: Text shown when the combobox is empty and not focused.
			text: Initial text content.
			character_limit: Maximum number of characters allowed. None means no limit.
			show: If given, each character is masked and displayed as this character (e.g. for password fields).
			values: The options shown in the dropdown.
			max_dropdown_items: Maximum number of dropdown rows that are shown at once.
			floating_dropdown: If True, the dropdown floats a little below the combobox instead of being attached to it.
			dropdown_offset: [x, y] offset of the dropdown in pixels. If the dropdown opens above the combobox the y
				coordinate is mirrored.
			casesensitive: If True, the dropdown will consider the case for the suggestions.
			dropdown_spacing: Vertical padding in pixels for every dropdown item.
			dropdown_alignment: Dropdown text alignment: 'left', 'right', 'center', or 'stretched'
			dropdown_alignment_spacing: Horizontal padding reserved around the aligned dropdown options.
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
			selection_color: RGBA background color for selected text while enabled.
			disabled_selection_color: RGBA background color for selected text while disabled.
			active_unpressed_text_dropdown_color: RGBA text color for dropdown while enabled, not pressed, not hovered.
			disabled_unpressed_text_dropdown_color: RGBA text color for dropdown while disabled, not hovered.
			active_hover_text_dropdown_color: RGBA text color for dropdown while enabled and hovered.
			disabled_hover_text_dropdown_color: RGBA text color for dropdown while disabled and hovered.
			active_pressed_text_dropdown_color: RGBA text color for dropdown while enabled and pressed.
			active_unpressed_background_dropdown_color: RGBA background color for dropdown while enabled, not pressed,
				not hovered.
			disabled_unpressed_background_dropdown_color: RGBA background color for dropdown while disabled,
				not hovered.
			active_hover_background_dropdown_color: RGBA background color for dropdown while enabled and hovered.
			disabled_hover_background_dropdown_color: RGBA background color for dropdown while disabled and hovered.
			active_pressed_background_dropdown_color: RGBA background color for dropdown while enabled and pressed.
			active_unpressed_border_dropdown_color: RGBA border color for dropdown while enabled, not pressed,
				not hovered.
			disabled_unpressed_border_dropdown_color: RGBA border color for dropdown while disabled, not hovered.
			active_hover_border_dropdown_color: RGBA border color for dropdown while enabled and hovered.
			disabled_hover_border_dropdown_color: RGBA border color for dropdown while disabled and hovered.
			active_pressed_border_dropdown_color: RGBA border color for dropdown while enabled and pressed.
			border_thickness: Border width in pixels.
			hide_text: If True, text is not rendered.
			hide_background: If True, the background fill is not rendered.
			hide_border: If True, the border is not rendered.
			hide_selection: If True, the text selection highlight is not rendered.
			hide_dropdown_text: If True, the dropdown option text is not rendered.
			hide_dropdown_background: If True, the dropdown background fill is not rendered.
			hide_dropdown_border: If True, the dropdown border is not rendered.
			active_hover_cursor: Custom cursor shown on hover while enabled.
			disabled_hover_cursor: Custom cursor shown on hover while disabled.
			active_pressed_cursor: Custom cursor shown while pressed.
			blinking_cursor: The character used to render the blinking text cursor.
			blinking_speed: Time in milliseconds between blink toggles.
			font: The pygame font used to render the combobox text.
			alignment: Text alignment: 'left', 'right' or 'center'
			alignment_spacing: Horizontal padding reserved around the aligned text.
			top_left_corner_radius: Corner radius in pixels for the top-left corner.
			top_right_corner_radius: Corner radius in pixels for the top-right corner.
			bottom_left_corner_radius: Corner radius in pixels for the bottom-left corner.
			bottom_right_corner_radius: Corner radius in pixels for the bottom-right corner.
			repeat_delay: Time in milliseconds before a held key starts repeating.
			repeat_interval: Time in milliseconds between repeats of a held key.
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
			display_text = ""
			if text:
				if show:
					display_text = show*len(text)
				else:
					display_text = text
			elif placeholder_text:
				display_text = placeholder_text
			lines = display_text.split("\n")
			total_w = 0
			text_h = font.size(display_text)[1]
			for line in lines:
				text_w, text_h = font.size(line)
				if text_w>total_w:
					total_w = text_w
			total_h = len(lines)*text_h

			self._width = total_w+alignment_spacing*2
			if min_width:
				self._width = max(self._width, min_width)
			if max_width:
				self._width = min(self._width, max_width)
			self._height = total_h+20
			if min_height:
				self._height = max(self._height, min_height)
			if max_height:
				self._height = min(self._height, max_height)
		self._placeholder_text = placeholder_text
		self._text = text
		self._character_limit = character_limit
		self._show = show
		self._values = [str(v) for v in values] if values else []
		self._max_dropdown_items = max_dropdown_items
		self._floating_dropdown = floating_dropdown
		self._dropdown_offset = dropdown_offset
		self._casesensitive = casesensitive
		self._dropdown_spacing = dropdown_spacing
		self._dropdown_alignment = dropdown_alignment
		self._dropdown_alignment_spacing = dropdown_alignment_spacing
		self._active_unpressed_text_color = nc(active_unpressed_text_color)
		self._disabled_unpressed_text_color = nc(disabled_unpressed_text_color)
		self._active_hover_text_color = nc(active_hover_text_color)
		self._disabled_hover_text_color = nc(disabled_hover_text_color)
		self._active_pressed_text_color = nc(active_pressed_text_color)
		self._active_unpressed_background_color = nc(active_unpressed_background_color)
		self._disabled_unpressed_background_color = nc(disabled_unpressed_background_color)
		self._active_hover_background_color = nc(active_hover_background_color)
		self._disabled_hover_background_color = nc(disabled_hover_background_color)
		self._active_pressed_background_color = nc(active_pressed_background_color)
		self._active_unpressed_border_color = nc(active_unpressed_border_color)
		self._disabled_unpressed_border_color = nc(disabled_unpressed_border_color)
		self._active_hover_border_color = nc(active_hover_border_color)
		self._disabled_hover_border_color = nc(disabled_hover_border_color)
		self._active_pressed_border_color = nc(active_pressed_border_color)
		self._selection_color = nc(selection_color)
		self._disabled_selection_color = nc(disabled_selection_color)
		self._active_unpressed_text_dropdown_color = nc(active_unpressed_text_dropdown_color)
		self._disabled_unpressed_text_dropdown_color = nc(disabled_unpressed_text_dropdown_color)
		self._active_hover_text_dropdown_color = nc(active_hover_text_dropdown_color)
		self._disabled_hover_text_dropdown_color = nc(disabled_hover_text_dropdown_color)
		self._active_pressed_text_dropdown_color = nc(active_pressed_text_dropdown_color)
		self._active_unpressed_background_dropdown_color = nc(active_unpressed_background_dropdown_color)
		self._disabled_unpressed_background_dropdown_color = nc(disabled_unpressed_background_dropdown_color)
		self._active_hover_background_dropdown_color = nc(active_hover_background_dropdown_color)
		self._disabled_hover_background_dropdown_color = nc(disabled_hover_background_dropdown_color)
		self._active_pressed_background_dropdown_color = nc(active_pressed_background_dropdown_color)
		self._active_unpressed_border_dropdown_color = nc(active_unpressed_border_dropdown_color)
		self._disabled_unpressed_border_dropdown_color = nc(disabled_unpressed_border_dropdown_color)
		self._active_hover_border_dropdown_color = nc(active_hover_border_dropdown_color)
		self._disabled_hover_border_dropdown_color = nc(disabled_hover_border_dropdown_color)
		self._active_pressed_border_dropdown_color = nc(active_pressed_border_dropdown_color)
		self._border_thickness = border_thickness
		self._hide_text = hide_text
		self._hide_background = hide_background
		self._hide_border = hide_border
		self._hide_selection = hide_selection
		self._hide_dropdown_text = hide_dropdown_text
		self._hide_dropdown_background = hide_dropdown_background
		self._hide_dropdown_border = hide_dropdown_border
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
						f"No custom cursor is used for the combobox '{placeholder_text}' because it's not a "
						f"pygame.Cursor object. {cursor} is a {type(cursor)}"
					)
				self._cursors[name] = None
		self._blinking_cursor = blinking_cursor
		self._blinking_speed = blinking_speed
		self._font = font
		self._alignment = alignment
		self._alignment_spacing = alignment_spacing
		self._top_left_corner_radius = top_left_corner_radius
		self._top_right_corner_radius = top_right_corner_radius
		self._bottom_left_corner_radius = bottom_left_corner_radius
		self._bottom_right_corner_radius = bottom_right_corner_radius
		self._repeat_delay = repeat_delay
		self._repeat_interval = repeat_interval
		self._layer = layer
		self._line_spacing = line_spacing
		self._tooltip = tooltip
		if tooltip:
			tooltip.configure(layer=layer+1)
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
		self._selected_text = None
		self._focused = False
		if text:
			self._cursor_position = len(text)
		else:
			self._cursor_position = 0
		self._scroll_offset = 0
		self._selection_anchor = None
		self._last_text_x = self._rect.left
		self._held_key_info = None
		self._next_repeat_time = 0
		self._cursor_visible = visible
		self._last_blink_time = pygame.time.get_ticks()
		self._bindings = {}
		self._last_visual_state = None
		self._needs_redraw = True
		self._cached_surface = None
		self._local_text_x = 0
		self._dropdown_open = False
		self._dropdown_hovered = False
		self._filtering = False
		self._highlight = -1
		self._dropdown_scroll = 0
		self._last_text = text
		self._draw_rect = self._rect.copy()
		self._dropdown_above = False
		self._list_local = None
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
		self._dialog = None

		self._font.set_linesize(line_spacing)

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
	def placeholder_text(self):
		return self._placeholder_text

	@placeholder_text.setter
	def placeholder_text(self, value):
		self._placeholder_text = value

	@property
	def text(self):
		return self._text

	@text.setter
	def text(self, value):
		self._text = value

	@property
	def character_limit(self):
		return self._character_limit

	@character_limit.setter
	def character_limit(self, value):
		self._character_limit = value

	@property
	def show(self):
		return self._show

	@show.setter
	def show(self, value):
		self._show = value

	@property
	def values(self):
		return self._values

	@values.setter
	def values(self, value):
		self._values = [str(v) for v in value] if value is not None else None

	@property
	def max_dropdown_items(self):
		return self._max_dropdown_items

	@max_dropdown_items.setter
	def max_dropdown_items(self, value):
		self._max_dropdown_items = value

	@property
	def floating_dropdown(self):
		return self._floating_dropdown

	@floating_dropdown.setter
	def floating_dropdown(self, value):
		self._floating_dropdown = value

	@property
	def dropdown_offset(self):
		return self._dropdown_offset

	@dropdown_offset.setter
	def dropdown_offset(self, value):
		self._dropdown_offset = tuple(value)

	@property
	def casesensitive(self):
		return self._casesensitive

	@casesensitive.setter
	def casesensitive(self, value):
		self._casesensitive = value

	@property
	def dropdown_spacing(self):
		return self._dropdown_spacing

	@dropdown_spacing.setter
	def dropdown_spacing(self, value):
		self._dropdown_spacing = value

	@property
	def dropdown_alignment(self):
		return self._dropdown_alignment

	@dropdown_alignment.setter
	def dropdown_alignment(self, value):
		self._dropdown_alignment = value

	@property
	def dropdown_alignment_spacing(self):
		return self._dropdown_alignment_spacing

	@dropdown_alignment_spacing.setter
	def dropdown_alignment_spacing(self, value):
		self._dropdown_alignment_spacing = value

	@property
	def active_unpressed_text_color(self):
		return self._active_unpressed_text_color

	@active_unpressed_text_color.setter
	def active_unpressed_text_color(self, value):
		self._active_unpressed_text_color = nc(value)

	@property
	def disabled_unpressed_text_color(self):
		return self._disabled_unpressed_text_color

	@disabled_unpressed_text_color.setter
	def disabled_unpressed_text_color(self, value):
		self._disabled_unpressed_text_color = nc(value)

	@property
	def active_hover_text_color(self):
		return self._active_hover_text_color

	@active_hover_text_color.setter
	def active_hover_text_color(self, value):
		self._active_hover_text_color = nc(value)

	@property
	def disabled_hover_text_color(self):
		return self._disabled_hover_text_color

	@disabled_hover_text_color.setter
	def disabled_hover_text_color(self, value):
		self._disabled_hover_text_color = nc(value)

	@property
	def active_pressed_text_color(self):
		return self._active_pressed_text_color

	@active_pressed_text_color.setter
	def active_pressed_text_color(self, value):
		self._active_pressed_text_color = nc(value)

	@property
	def active_unpressed_background_color(self):
		return self._active_unpressed_background_color

	@active_unpressed_background_color.setter
	def active_unpressed_background_color(self, value):
		self._active_unpressed_background_color = nc(value)

	@property
	def disabled_unpressed_background_color(self):
		return self._disabled_unpressed_background_color

	@disabled_unpressed_background_color.setter
	def disabled_unpressed_background_color(self, value):
		self._disabled_unpressed_background_color = nc(value)

	@property
	def active_hover_background_color(self):
		return self._active_hover_background_color

	@active_hover_background_color.setter
	def active_hover_background_color(self, value):
		self._active_hover_background_color = nc(value)

	@property
	def disabled_hover_background_color(self):
		return self._disabled_hover_background_color

	@disabled_hover_background_color.setter
	def disabled_hover_background_color(self, value):
		self._disabled_hover_background_color = nc(value)

	@property
	def active_pressed_background_color(self):
		return self._active_pressed_background_color

	@active_pressed_background_color.setter
	def active_pressed_background_color(self, value):
		self._active_pressed_background_color = nc(value)

	@property
	def active_unpressed_border_color(self):
		return self._active_unpressed_border_color

	@active_unpressed_border_color.setter
	def active_unpressed_border_color(self, value):
		self._active_unpressed_border_color = nc(value)

	@property
	def disabled_unpressed_border_color(self):
		return self._disabled_unpressed_border_color

	@disabled_unpressed_border_color.setter
	def disabled_unpressed_border_color(self, value):
		self._disabled_unpressed_border_color = nc(value)

	@property
	def active_hover_border_color(self):
		return self._active_hover_border_color

	@active_hover_border_color.setter
	def active_hover_border_color(self, value):
		self._active_hover_border_color = nc(value)

	@property
	def disabled_hover_border_color(self):
		return self._disabled_hover_border_color

	@disabled_hover_border_color.setter
	def disabled_hover_border_color(self, value):
		self._disabled_hover_border_color = nc(value)

	@property
	def active_pressed_border_color(self):
		return self._active_pressed_border_color

	@active_pressed_border_color.setter
	def active_pressed_border_color(self, value):
		self._active_pressed_border_color = nc(value)

	@property
	def selection_color(self):
		return self._selection_color

	@selection_color.setter
	def selection_color(self, value):
		self._selection_color = nc(value)

	@property
	def disabled_selection_color(self):
		return self._disabled_selection_color

	@disabled_selection_color.setter
	def disabled_selection_color(self, value):
		self._disabled_selection_color = nc(value)

	@property
	def active_unpressed_text_dropdown_color(self):
		return self._active_unpressed_text_dropdown_color

	@active_unpressed_text_dropdown_color.setter
	def active_unpressed_text_dropdown_color(self, value):
		self._active_unpressed_text_dropdown_color = nc(value)

	@property
	def disabled_unpressed_text_dropdown_color(self):
		return self._disabled_unpressed_text_dropdown_color

	@disabled_unpressed_text_dropdown_color.setter
	def disabled_unpressed_text_dropdown_color(self, value):
		self._disabled_unpressed_text_dropdown_color = nc(value)

	@property
	def active_hover_text_dropdown_color(self):
		return self._active_hover_text_dropdown_color

	@active_hover_text_dropdown_color.setter
	def active_hover_text_dropdown_color(self, value):
		self._active_hover_text_dropdown_color = nc(value)

	@property
	def disabled_hover_text_dropdown_color(self):
		return self._disabled_hover_text_dropdown_color

	@disabled_hover_text_dropdown_color.setter
	def disabled_hover_text_dropdown_color(self, value):
		self._disabled_hover_text_dropdown_color = nc(value)

	@property
	def active_pressed_text_dropdown_color(self):
		return self._active_pressed_text_dropdown_color

	@active_pressed_text_dropdown_color.setter
	def active_pressed_text_dropdown_color(self, value):
		self._active_pressed_text_dropdown_color = nc(value)

	@property
	def active_unpressed_background_dropdown_color(self):
		return self._active_unpressed_background_dropdown_color

	@active_unpressed_background_dropdown_color.setter
	def active_unpressed_background_dropdown_color(self, value):
		self._active_unpressed_background_dropdown_color = nc(value)

	@property
	def disabled_unpressed_background_dropdown_color(self):
		return self._disabled_unpressed_background_dropdown_color

	@disabled_unpressed_background_dropdown_color.setter
	def disabled_unpressed_background_dropdown_color(self, value):
		self._disabled_unpressed_background_dropdown_color = nc(value)

	@property
	def active_hover_background_dropdown_color(self):
		return self._active_hover_background_dropdown_color

	@active_hover_background_dropdown_color.setter
	def active_hover_background_dropdown_color(self, value):
		self._active_hover_background_dropdown_color = nc(value)

	@property
	def disabled_hover_background_dropdown_color(self):
		return self._disabled_hover_background_dropdown_color

	@disabled_hover_background_dropdown_color.setter
	def disabled_hover_background_dropdown_color(self, value):
		self._disabled_hover_background_dropdown_color = nc(value)

	@property
	def active_pressed_background_dropdown_color(self):
		return self._active_pressed_background_dropdown_color

	@active_pressed_background_dropdown_color.setter
	def active_pressed_background_dropdown_color(self, value):
		self._active_pressed_background_dropdown_color = nc(value)

	@property
	def active_unpressed_border_dropdown_color(self):
		return self._active_unpressed_border_dropdown_color

	@active_unpressed_border_dropdown_color.setter
	def active_unpressed_border_dropdown_color(self, value):
		self._active_unpressed_border_dropdown_color = nc(value)

	@property
	def disabled_unpressed_border_dropdown_color(self):
		return self._disabled_unpressed_border_dropdown_color

	@disabled_unpressed_border_dropdown_color.setter
	def disabled_unpressed_border_dropdown_color(self, value):
		self._disabled_unpressed_border_dropdown_color = nc(value)

	@property
	def active_hover_border_dropdown_color(self):
		return self._active_hover_border_dropdown_color

	@active_hover_border_dropdown_color.setter
	def active_hover_border_dropdown_color(self, value):
		self._active_hover_border_dropdown_color = nc(value)

	@property
	def disabled_hover_border_dropdown_color(self):
		return self._disabled_hover_border_dropdown_color

	@disabled_hover_border_dropdown_color.setter
	def disabled_hover_border_dropdown_color(self, value):
		self._disabled_hover_border_dropdown_color = nc(value)

	@property
	def active_pressed_border_dropdown_color(self):
		return self._active_pressed_border_dropdown_color

	@active_pressed_border_dropdown_color.setter
	def active_pressed_border_dropdown_color(self, value):
		self._active_pressed_border_dropdown_color = nc(value)

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
	def hide_selection(self):
		return self._hide_selection

	@hide_selection.setter
	def hide_selection(self, value):
		self._hide_selection = value

	@property
	def hide_dropdown_text(self):
		return self._hide_dropdown_text

	@hide_dropdown_text.setter
	def hide_dropdown_text(self, value):
		self._hide_dropdown_text = value

	@property
	def hide_dropdown_background(self):
		return self._hide_dropdown_background

	@hide_dropdown_background.setter
	def hide_dropdown_background(self, value):
		self._hide_dropdown_background = value

	@property
	def hide_dropdown_border(self):
		return self._hide_dropdown_border

	@hide_dropdown_border.setter
	def hide_dropdown_border(self, value):
		self._hide_dropdown_border = value

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
	def blinking_cursor(self):
		return self._blinking_cursor

	@blinking_cursor.setter
	def blinking_cursor(self, value):
		self._blinking_cursor = value

	@property
	def blinking_speed(self):
		return self._blinking_speed

	@blinking_speed.setter
	def blinking_speed(self, value):
		self._blinking_speed = value

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
	def repeat_delay(self):
		return self._repeat_delay

	@repeat_delay.setter
	def repeat_delay(self, value):
		self._repeat_delay = value

	@property
	def repeat_interval(self):
		return self._repeat_interval

	@repeat_interval.setter
	def repeat_interval(self, value):
		self._repeat_interval = value

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
	def line_spacing(self):
		return self._line_spacing

	@line_spacing.setter
	def line_spacing(self, value):
		self._line_spacing = value
		self._font.set_linesize(value)

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
	def is_hovered(self):
		return self._is_hovered

	@is_hovered.setter
	def is_hovered(self, value):
		self._is_hovered = value

	@property
	def selected_text(self):
		return self._selected_text

	@selected_text.setter
	def selected_text(self, value):
		self._selected_text = value

	@property
	def focused(self):
		return self._focused

	@focused.setter
	def focused(self, value):
		self._focused = value

	@property
	def cursor_position(self):
		return self._cursor_position

	@cursor_position.setter
	def cursor_position(self, value):
		self._cursor_position = value

	@property
	def scroll_offset(self):
		return self._scroll_offset

	@scroll_offset.setter
	def scroll_offset(self, value):
		self._scroll_offset = value

	@property
	def selection_anchor(self):
		return self._selection_anchor

	@selection_anchor.setter
	def selection_anchor(self, value):
		self._selection_anchor = value

	@property
	def last_text_x(self):
		return self._last_text_x

	@last_text_x.setter
	def last_text_x(self, value):
		self._last_text_x = value

	@property
	def held_key_info(self):
		return self._held_key_info

	@held_key_info.setter
	def held_key_info(self, value):
		self._held_key_info = value

	@property
	def next_repeat_time(self):
		return self._next_repeat_time

	@next_repeat_time.setter
	def next_repeat_time(self, value):
		self._next_repeat_time = value

	@property
	def cursor_visible(self):
		return self._cursor_visible

	@cursor_visible.setter
	def cursor_visible(self, value):
		self._cursor_visible = value

	@property
	def last_blink_time(self):
		return self._last_blink_time

	@last_blink_time.setter
	def last_blink_time(self, value):
		self._last_blink_time = value

	@property
	def bindings(self):
		return self._bindings

	@bindings.setter
	def bindings(self, value):
		self._bindings = value

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
	def local_text_x(self):
		return self._local_text_x

	@local_text_x.setter
	def local_text_x(self, value):
		self._local_text_x = value

	@property
	def dropdown_open(self):
		return self._dropdown_open

	@dropdown_open.setter
	def dropdown_open(self, value):
		self._dropdown_open = value

	@property
	def dropdown_hovered(self):
		return self._dropdown_hovered

	@dropdown_hovered.setter
	def dropdown_hovered(self, value):
		self._dropdown_hovered = value

	@property
	def filtering(self):
		return self._filtering

	@filtering.setter
	def filtering(self, value):
		self._filtering = value

	@property
	def highlight(self):
		return self._highlight

	@highlight.setter
	def highlight(self, value):
		self._highlight = value

	@property
	def dropdown_scroll(self):
		return self._dropdown_scroll

	@dropdown_scroll.setter
	def dropdown_scroll(self, value):
		self._dropdown_scroll = value

	@property
	def last_text(self):
		return self._last_text

	@last_text.setter
	def last_text(self, value):
		self._last_text = value

	@property
	def draw_rect(self):
		return self._draw_rect

	@draw_rect.setter
	def draw_rect(self, value):
		self._draw_rect = value

	@property
	def dropdown_above(self):
		return self._dropdown_above

	@dropdown_above.setter
	def dropdown_above(self, value):
		self._dropdown_above = value

	@property
	def list_local(self):
		return self._list_local

	@list_local.setter
	def list_local(self, value):
		self._list_local = value

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

	@property
	def dialog(self):
		return self._dialog

	@dialog.setter
	def dialog(self, value):
		self._dialog = value

	def configure(self, **kwargs: Unpack[TypeHints.ComboboxConfig]) -> Combobox:
		"""
		Updates one or more of the combobox's attributes.

		Args:
			**kwargs: Combobox attributes to update as defined in TypeHints.ComboboxConfig

		Returns:
			Combobox (Combobox): This combobox instance to allow method chaining.
		"""
		for key, value in kwargs.items():
			setattr(self, key, value)
		self._needs_redraw = True
		if any(
				k in kwargs for k in
				(
						'auto_size', 'x', 'y', 'width', 'height', 'max_width', 'min_width', 'max_height', 'min_height',
						'anchor_x', 'anchor_y'
				)
		):
			self._width = self._width
			self._height = self._height
			if self._auto_size:
				display_text = ""
				if self._text:
					if self._show:
						display_text = self._show*len(self._text)
					else:
						display_text = self._text
				elif self._placeholder_text and not self._focused:
					display_text = self._placeholder_text
				lines = display_text.split("\n")
				total_w = 0
				text_h = self._font.size(display_text)[1]
				for line in lines:
					text_w, text_h = self._font.size(line)
					if text_w>total_w:
						total_w = text_w
				total_h = len(lines)*text_h
				self._width = total_w+self._alignment_spacing*2
				if self._min_width:
					self._width = max(self._width, self._min_width)
				if self._max_width:
					self._width = min(self._width, self._max_width)
				self._height = total_h+20
				if self._min_height:
					self._height = max(self._height, self._min_height)
				if self._max_height:
					self._height = min(self._height, self._max_height)
			self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
		if 'screen' in kwargs:
			self.set_screen(kwargs["screen"])
		return self

	def config(self, **kwargs: Unpack[TypeHints.ComboboxConfig]) -> Combobox:
		"""
		Updates one or more of the combobox's attributes.

		Args:
			**kwargs: Combobox attributes to update as defined in TypeHints.ComboboxConfig

		Returns:
			Combobox (Combobox): This combobox instance to allow method chaining.
		"""
		return self.configure(**kwargs)

	def get(self) -> str:
		"""
		Returns the combobox's current text content.

		Returns:
			str: The combobox's current text.
		"""
		return self._text

	def text_delete(self, position_start: int = 0, position_end: int | None = None) -> None:
		"""
		Deletes text between two character positions.

		Args:
			position_start: The start index of the range to delete inclusively.
			position_end: The end index of the range to delete exclusively. if None: deletes to the end of the text.
		"""
		if position_end is None:
			position_end = len(self._text)
		position_start = max(0, min(position_start, len(self._text)))
		position_end = max(0, min(position_end, len(self._text)))
		if position_start<position_end:
			self._text = self._text[:position_start]+self._text[position_end:]
			if self._cursor_position>position_end:
				self._cursor_position -= (position_end-position_start)
			elif self._cursor_position>position_start:
				self._cursor_position = position_start
		self.reset_cursor_blink()

	def text_insert(self, text: str, position: int | None = None) -> None:
		"""
		Inserts text at a given character position.

		Args:
			text: The text to insert.
			position: The character index to insert at. if None: inserts at the end of the text.

		Note:
			If character_limit is set and the resulting text would exceed it, the insertion is skipped entirely.
		"""
		if position is None:
			position = len(self._text)
		if self._character_limit is not None and len(self._text)+len(text)>self._character_limit:
			return
		self._text = self._text[:position]+text+self._text[position:]
		self._cursor_position += len(text)
		self.reset_cursor_blink()

	def text_select(self, position_start: int = 0, position_end: int | None = None) -> None:
		"""
		Selects text between two character positions.

		Args:
			position_start: The start index of the selection.
			position_end: The end index of the selection. if None: selects to the end of the text.
		"""
		if position_end is None:
			position_end = len(self._text)
		self._selected_text = [min(position_start, position_end), max(position_start, position_end)]
		self.reset_cursor_blink()

	def text_copy(self) -> None:
		"""Copies the currently selected text to the system clipboard if any text is selected."""
		if self._selected_text and self._selected_text[0]!=self._selected_text[1]:
			start, end = self._selected_text
			clipboard_text = self._text[start:end]
			pygame.scrap.put(pygame.SCRAP_TEXT, clipboard_text.encode('utf-8'))

	def text_cut(self) -> None:
		"""Copies the currently selected text to the system clipboard and removes it from the combobox."""
		if self._selected_text and self._selected_text[0]!=self._selected_text[1]:
			self.text_copy()
			self.text_delete(self._selected_text[0], self._selected_text[1])
			self._selected_text = None

	def text_paste(self) -> None:
		"""Pastes text from the system clipboard at the cursor position replacing any current selection."""
		if not pygame.scrap.get_init():
			pygame.scrap.init()
		if self._selected_text:
			self.text_delete(self._selected_text[0], self._selected_text[1])
			self._selected_text = None
		clipboard = pygame.scrap.get(pygame.SCRAP_TEXT)
		if clipboard:
			try:
				paste_text = clipboard.decode('utf-8').split('\x00')[0]
				self.text_insert(paste_text, self._cursor_position)
			except Exception as e:
				print(f"Paste error: {e}")

	def open_dropdown(self, filtering: bool = True) -> Combobox:
		"""
		Open the dropdown.

		Args:
			filtering (bool): True to filter the options by the current text, False to show all.

		Returns:
			Combobox (Combobox): This combobox instance to allow method chaining.
		"""
		self._dropdown_open = True
		self._filtering = filtering
		self._highlight = 0 if filtering else -1
		self._dropdown_scroll = 0
		self._dropdown_hovered = False
		self.trigger_event(epw_types.COMBOBOX_OPENED)
		return self

	def close_dropdown(self) -> Combobox:
		"""
		Closes the dropdown.

		Returns:
			Combobox (Combobox): This combobox instance to allow method chaining.
		"""
		self._dropdown_open = False
		self._dropdown_hovered = False
		self.trigger_event(epw_types.COMBOBOX_CLOSED)
		return self

	def reset_cursor_blink(self) -> None:
		"""Makes the blinking text cursor visible and restarts its blink timer."""
		self._cursor_visible = True
		self._last_blink_time = pygame.time.get_ticks()

	def get_display_text(self) -> str:
		"""
		Returns the text that should currently be displayed, considering for masking (show attribute) and the
		placeholder text.

		Returns:
			str: the masked text
		"""
		if self._text:
			if self._show:
				return self._show*len(self._text)
			return self._text
		elif self._placeholder_text and not self._focused:
			return self._placeholder_text
		return ""

	def scale(self, value: int | float = 1, frames_to_finish: int = 1) -> Combobox:
		"""
		Scale the combobox by a factor. It's only a visual scale so upscaling could look pixelated.

		Args:
			 value (int|float): the scale factor
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Combobox (Combobox): This combobox instance to allow method chaining.
		"""
		if frames_to_finish<=0:
			frames_to_finish = 1
		self._target_scale = value
		self._scale_step = (self._target_scale-self._current_scale)/frames_to_finish
		self._update_animation()
		return self

	def rotate(self, value: int | float = 0, frames_to_finish: int = 1) -> Combobox:
		"""
		Rotate the combobox by a degree.

		Args:
			 value (int|float): the rotation degree
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Combobox (Combobox): This combobox instance to allow method chaining.
		"""
		if frames_to_finish<=0:
			frames_to_finish = 1
		self._target_rotation = value
		self._rotation_step = (self._target_rotation-self._current_rotation)/frames_to_finish
		self._update_animation()
		return self

	def rotozoom(self, scale: int | float = 1, rotation: int | float = 0, frames_to_finish: int = 1) -> Combobox:
		"""
		Rotate the combobox by a degree and scale it.

		Args:
			 scale (int|float): the scale factor
			 rotation (int|float): the rotation degree
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Combobox (Combobox): This combobox instance to allow method chaining.
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

	def offset(self, value: Iterable[int] = (0, 0), frames_to_finish: int = 1) -> Combobox:
		"""
		Offset the combobox by an x and y value.

		Args:
			 value: an iterable thing with two values. The first being the x and the second the y offset.
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Combobox (Combobox): This combobox instance to allow method chaining.
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

	def _get_options(self) -> list[str]:
		"""
		Internally used to get the dropdown options filtered by the current text.

		Returns:
			list[str]: The filtered values.
		"""
		if not self._filtering: return self._values
		if self._casesensitive: return [v for v in self._values if self._text in v]
		query = self._text.lower()
		return [v for v in self._values if query in v.lower()]

	def _get_render_state(self) -> tuple:
		"""
		Internally used to get everything (besides hovering) that changes how the combobox and its dropdown look.

		Returns:
			tuple: a snapshot that can be compared to the snapshot of the last render
		"""
		selected = tuple(self._selected_text) if self._selected_text else None
		dropdown = (
			self._filtering, self._highlight, self._dropdown_scroll, self._dropdown_above
		) if self._dropdown_open else None
		return (
			self._pressed, self._cursor_visible, self._text, self._cursor_position, selected, self._focused,
			self._state, dropdown
		)

	def _select_option(self, value: str) -> None:
		"""
		Internally used to put a dropdown option into the combobox and close the dropdown.

		Args:
			value (bool): the selected option
		"""
		self._text = self._last_text = value
		self._cursor_position = len(value)
		self._selected_text = None
		self.close_dropdown()
		self.reset_cursor_blink()

	def _item_height(self) -> int:
		"""
		Internally used to get the height of one dropdown row.

		Returns:
			int: the height in pixel
		"""
		return self._font.get_height()+self._dropdown_spacing

	def _dropdown_flips(self) -> bool:
		"""
		Internally used to check if the dropdown has to open above the combobox because there is no space below it.

		Returns:
			bool: True if the dropdown should open above the combobox
		"""
		visible = min(len(self._get_options()), self._max_dropdown_items)
		gap = self._dropdown_offset[1]
		needed = (gap+visible*self._item_height())*self._current_scale
		box = self._draw_rect
		return box.bottom+needed>misc._pg.get_height() and box.top>=needed

	def _dropdown_layout(self) -> tuple[pygame.Rect, pygame.Rect, list[str]]:
		"""
		Internally used to get the dropdown's rects and options relative to the combobox.

		Returns:
			tuple[pygame.Rect, pygame.Rect, list[str]]: the rect of the whole dropdown, the rect of only the option rows
			and a list of the available options
		"""
		options = self._get_options()
		visible = min(len(options), self._max_dropdown_items)
		self._dropdown_scroll = max(0, min(self._dropdown_scroll, len(options)-visible))
		off_x, off_y = self._dropdown_offset
		list_h = visible*self._item_height()
		list_top = -off_y-list_h if self._dropdown_above else self._height+off_y
		list_rect = pygame.Rect(off_x, list_top, self._width, list_h)
		if self._floating_dropdown: rect = list_rect.copy()
		elif self._dropdown_above: rect = pygame.Rect(off_x, list_top, self._width, self._height-list_top)
		else: rect = pygame.Rect(off_x, 0, self._width, list_top+list_h)
		return rect, list_rect, options

	def _item_at(self, pos: tuple[int, int]) -> int | None:
		"""
		Internally used to get the index of the option at a position.

		Args:
			pos (tuple[int, int]): the position with x and y coordinates

		Returns:
			int: the index of the option at the given position
			None: if the position is not over one option
		"""
		if not self._dropdown_open or self._list_local is None: return None
		# convert the screen position back into the unscaled, unrotated surface the options were rendered on
		vec = pygame.math.Vector2(pos[0]-self._draw_rect.centerx, pos[1]-self._draw_rect.centery)
		if self._current_rotation!=0: vec = vec.rotate(self._current_rotation)
		if self._current_scale!=0: vec /= self._current_scale
		surf_w, surf_h = self._original_surface.get_size()
		x, y = int(vec.x+surf_w/2), int(vec.y+surf_h/2)
		if not self._list_local.collidepoint(x, y): return None
		return self._dropdown_scroll+(y-self._list_local.top)//self._item_height()

	def _navigate_dropdown(self, key: int) -> None:
		"""
		Internally used to handle the up/down/enter/escape keys for the dropdown.

		Args:
			key (int): the key pressed
		"""
		if key==pygame.K_ESCAPE: self.close_dropdown()
		elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
			options = self._get_options()
			if self._dropdown_open and 0<=self._highlight<len(options): self._select_option(options[self._highlight])
		else:
			if not self._dropdown_open: self.open_dropdown(False)
			options = self._get_options()
			if not options: return
			step = 1 if key==pygame.K_DOWN else -1
			self._highlight = max(0, min(len(options)-1, self._highlight+step))
			if self._highlight<self._dropdown_scroll: self._dropdown_scroll = self._highlight
			elif self._highlight>=self._dropdown_scroll+self._max_dropdown_items:
				self._dropdown_scroll = self._highlight-self._max_dropdown_items+1

	def _draw(self, surface: pygame.Surface) -> None:
		"""
		Internally used to draw the combobox.

		Args:
			surface (pygame.Surface): The surface to draw the combobox on.
		"""
		if not self._alive or not self._visible:
			return
		if self._focused and self._held_key_info:
			current_time = pygame.time.get_ticks()
			if current_time>=self._next_repeat_time:
				key, unicode_char = self._held_key_info
				_process_key_action(self, key, unicode_char)
				self._next_repeat_time = current_time+self._repeat_interval

		if self._text!=self._last_text:
			self._last_text = self._text
			if self._focused: self.open_dropdown()

		if not pygame.scrap.get_init():
			pygame.scrap.init()

		mouse_pos = pygame.mouse.get_pos()
		is_hovering = misc._is_point_over_widget(self, mouse_pos)
		now = pygame.time.get_ticks()
		display_text = self.get_display_text()

		has_selection = self._selected_text and self._selected_text[0]!=self._selected_text[1]
		if self._focused and self._state=="enabled" and not has_selection:
			if now-self._last_blink_time>self._blinking_speed:
				self._cursor_visible = not self._cursor_visible
				self._last_blink_time = now

		self._font.set_linesize(self._line_spacing)
		if self._auto_size:
			lines = display_text.split("\n")
			total_w = 0
			text_h = self._font.size(display_text)[1]
			for line in lines:
				text_w, text_h = self._font.size(line)
				if text_w>total_w:
					total_w = text_w
			total_h = len(lines)*text_h

			required_width = total_w+self._alignment_spacing*2
			if self._min_width:
				required_width = max(required_width, self._min_width)
			if self._max_width:
				required_width = min(required_width, self._max_width)
			required_height = total_h+20
			if self._min_height:
				required_height = max(required_height, self._min_height)
			if self._max_height:
				required_height = min(required_height, self._max_height)

			if self._width!=required_width:
				self._width = required_width
				self._needs_redraw = True
			if self._height!=required_height:
				self._height = required_height
				self._needs_redraw = True

		if self._dropdown_open and not (self._focused and self._state=="enabled"): self.close_dropdown()
		if self._dropdown_open: self._dropdown_above = self._dropdown_flips()
		current_visual_state = misc._get_vars(self, TO_UPDATE)
		if self._needs_redraw or self._last_visual_state!=current_visual_state:
			temp_topleft = self._rect.topleft
			self._rect.size = (self._width, self._height)
			self._rect.topleft = temp_topleft
			_render_combobox_surface(self, is_hovering)

		if self._needs_transform:
			def transform(surf: pygame.Surface) -> pygame.Surface:
				"""
				Internally used to apply the current scale and rotation to the surface.

				Args:
					surf (pygame.Surface): the surface to transform

				Returns:
					pygame.Surface: the transformed surface
				"""
				if self._current_scale==1 and self._current_rotation==0: return surf.copy()
				new_width = int(surf.get_width()*self._current_scale)
				new_height = int(surf.get_height()*self._current_scale)
				if new_width<=0 or new_height<=0: return pygame.Surface((0, 0), pygame.SRCALPHA)
				if self._use_rotozoom:
					return pygame.transform.rotozoom(surf, self._current_rotation, self._current_scale)
				scaled_surface = pygame.transform.smoothscale(surf, (new_width, new_height))
				return pygame.transform.rotate(scaled_surface, self._current_rotation)

			self._cached_surface = transform(self._original_surface)
			if self._original_surface.get_size()==(self._width, self._height):
				rect_size = self._cached_surface.get_size()
			else: rect_size = transform(pygame.Surface((self._width, self._height), pygame.SRCALPHA)).get_size()
			self._rect = pygame.Rect(self._rect.topleft, rect_size)
			self._needs_transform = False
		offset_x, offset_y = misc._get_offset(self)
		total_offset_x = offset_x+round(self._current_offset[0])
		total_offset_y = offset_y+round(self._current_offset[1])
		draw_rect = self._rect.move(total_offset_x, total_offset_y)
		self._draw_rect = draw_rect
		surface.blit(self._cached_surface, self._cached_surface.get_rect(center=draw_rect.center))

		self._last_text_x = self._local_text_x+draw_rect.x

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

		if is_hovering and not getattr(self, "is_hovered", False):
			self._is_hovered = True
			self.trigger_event(epw_types.MOUSE_IN)
			if self._tooltip:
				self._tooltip.show()
		elif is_hovering and getattr(self, "is_hovered", False):
			self._is_hovered = True
			self.trigger_event(epw_types.HOVER)
		elif not is_hovering and getattr(self, "is_hovered", False):
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
			self._focused = False
			return
		display_text = self.get_display_text()
		is_inside = misc._is_point_over_widget(self, pygame.mouse.get_pos())

		def get_idx_at_mouse(mouse_x: int) -> int:
			"""
			Internally used to get the index position where the mouse currently is.

			Args:
				 mouse_x (int): The x-coordinate of the mouse.

			Returns:
				 int: The index position where the mouse currently is.
			"""
			curr_x = self._last_text_x
			for i, char in enumerate(display_text):
				char_w = self._font.size(char)[0]
				if mouse_x<curr_x+char_w/2: return i
				curr_x += char_w
			return min(len(display_text), len(self._text))

		if event:
			if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
				if self._dropdown_open:
					idx = self._item_at(event.pos)
					if idx is not None:
						self._select_option(self._get_options()[idx])
						return
				if is_inside:
					self.trigger_event(epw_types.PRESS)
				if not self._focused:
					self.trigger_event(epw_types.FOCUS_IN)
				if is_inside:
					self._pressed = True
					idx = get_idx_at_mouse(event.pos[0])
					# This somehow has to be redone because """return min(len(display_text), len(self._text))""" doesn't work
					self._cursor_position = min(len(self._text), idx)
					self._selection_anchor = idx
					self._selected_text = None
					if not self._focused:
						self._focused = True
					self.reset_cursor_blink()
					if not self._dropdown_open:
						self.open_dropdown(False)
				else:
					if self._focused:
						self.trigger_event(epw_types.FOCUS_OUT)
					self._focused = False
					self.close_dropdown()
			elif event.type==pygame.MOUSEBUTTONUP and event.button==1:
				if self._pressed:
					self.trigger_event(epw_types.RELEASE)
				self._pressed = False
				self._selection_anchor = None
			elif event.type==pygame.MOUSEMOTION and self._pressed:
				if self._selection_anchor is not None:
					self._cursor_position = get_idx_at_mouse(event.pos[0])
					self.text_select(self._selection_anchor, self._cursor_position)
					self.reset_cursor_blink()
			elif event.type==pygame.MOUSEMOTION and self._dropdown_open:
				idx = self._item_at(event.pos)
				self._dropdown_hovered = idx is not None
				if idx is not None: self._highlight = idx
			elif event.type==pygame.MOUSEWHEEL and self._dropdown_open:
				if self._item_at(pygame.mouse.get_pos()) is not None: self._dropdown_scroll -= event.y
			elif event.type==pygame.KEYDOWN:
				if self._focused:
					_process_key_action(self, event.key, event.unicode)
					self._held_key_info = (event.key, event.unicode)
					self._next_repeat_time = pygame.time.get_ticks()+self._repeat_delay
				misc._trigger_key_bindings(self, event)
			elif event.type==pygame.KEYUP:
				if self._held_key_info and event.key==self._held_key_info[0]:
					self._held_key_info = None


def _process_key_action(combobox: Combobox, key: int, unicode_char: str) -> None:
	"""
	Internally used to handle a single keydown/repeat action for a combobox, covering
	cursor movement, selection, clipboard shortcuts, deletion, and character insertion.

	Args:
		combobox (Combobox): The combobox receiving the key action.
		key (int): The pygame key constant that was pressed.
		unicode_char (str): The Unicode character produced by the key press, if any.
	"""
	is_linux = sys.platform.startswith("linux")
	mods = pygame.key.get_mods()
	ctrl = (mods & pygame.KMOD_CTRL) or (mods & pygame.KMOD_META)
	shift = mods & pygame.KMOD_SHIFT
	combobox.reset_cursor_blink()
	if key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_HOME, pygame.K_END):
		if shift and combobox.selected_text is None:
			combobox.selection_anchor = combobox.cursor_position
		if key==pygame.K_LEFT:
			combobox.cursor_position = max(0, combobox.cursor_position-1)
		elif key==pygame.K_RIGHT:
			combobox.cursor_position = min(len(combobox.text), combobox.cursor_position+1)
		elif key==pygame.K_HOME:
			combobox.cursor_position = 0
		elif key==pygame.K_END:
			combobox.cursor_position = len(combobox.text)
		if shift:
			combobox.text_select(combobox.selection_anchor, combobox.cursor_position)
		else:
			combobox.selected_text = None
			combobox.selection_anchor = None
		return
	if key in (pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_ESCAPE):
		combobox._navigate_dropdown(key)
		return
	if ctrl:
		if not is_linux or shift:
			if key==pygame.K_c:
				combobox.text_copy()
				combobox.trigger_event(epw_types.COPY)
			elif key==pygame.K_v:
				combobox.text_paste()
				combobox.trigger_event(epw_types.PASTE)
			elif key==pygame.K_x:
				combobox.text_cut()
				combobox.trigger_event(epw_types.CUT)
		if key==pygame.K_a:
			combobox.selection_anchor = 0
			combobox.cursor_position = len(combobox.text)
			combobox.text_select(0, len(combobox.text))
			combobox.trigger_event(epw_types.SELECT_ALL)
		return
	if key==pygame.K_BACKSPACE:
		if combobox.selected_text:
			combobox.text_delete(*combobox.selected_text)
			combobox.selected_text = None
		elif combobox.cursor_position>0:
			combobox.text_delete(combobox.cursor_position-1, combobox.cursor_position)
		combobox.trigger_event(epw_types.BACKSPACE)
		return
	elif key==pygame.K_DELETE:
		if combobox.selected_text:
			combobox.text_delete(*combobox.selected_text)
			combobox.selected_text = None
		elif combobox.cursor_position<len(combobox.text):
			combobox.text_delete(combobox.cursor_position, combobox.cursor_position+1)
		combobox.trigger_event(epw_types.DELETE)
		return
	elif unicode_char.isprintable() and unicode_char!="":
		if combobox.selected_text:
			combobox.text_delete(*combobox.selected_text)
			combobox.selected_text = None
		combobox.text_insert(unicode_char, combobox.cursor_position)
		combobox.trigger_event(epw_types.TYPING)


def _render_combobox_surface(combobox: Combobox, is_hovering: bool) -> None:
	"""
	Internally used to draw the combobox surface once and cache it.

	Args:
		combobox (Combobox): the widget to render the surface for
		is_hovering (bool): whether the mouse is hovering over the widget
	"""
	if combobox.state=="enabled":
		if combobox.pressed and is_hovering:
			text_color = combobox.active_pressed_text_color
			bg_color = combobox.active_pressed_background_color
			brd_color = combobox.active_pressed_border_color
		elif is_hovering:
			text_color = combobox.active_hover_text_color
			bg_color = combobox.active_hover_background_color
			brd_color = combobox.active_hover_border_color
		else:
			text_color = combobox.active_unpressed_text_color
			bg_color = combobox.active_unpressed_background_color
			brd_color = combobox.active_unpressed_border_color
		selection_color = combobox.selection_color
	else:
		if is_hovering:
			text_color = combobox.disabled_hover_text_color
			bg_color = combobox.disabled_hover_background_color
			brd_color = combobox.disabled_hover_border_color
		else:
			text_color = combobox.disabled_unpressed_text_color
			bg_color = combobox.disabled_unpressed_background_color
			brd_color = combobox.disabled_unpressed_border_color
		selection_color = combobox.disabled_selection_color
	base_width = combobox.width
	base_height = combobox.height
	cached = pygame.Surface((base_width, base_height), pygame.SRCALPHA)
	local_rect = pygame.Rect(0, 0, base_width, base_height)
	if not combobox.hide_background:
		pygame.draw.rect(
			cached, bg_color, local_rect, border_top_left_radius=combobox.top_left_corner_radius,
			border_top_right_radius=combobox.top_right_corner_radius,
			border_bottom_left_radius=combobox.bottom_left_corner_radius,
			border_bottom_right_radius=combobox.bottom_right_corner_radius
		)
	if not combobox.hide_border:
		pygame.draw.rect(
			cached, brd_color, local_rect, width=combobox.border_thickness,
			border_top_left_radius=combobox.top_left_corner_radius,
			border_top_right_radius=combobox.top_right_corner_radius,
			border_bottom_left_radius=combobox.bottom_left_corner_radius,
			border_bottom_right_radius=combobox.bottom_right_corner_radius
		)
	clip_rect = local_rect.inflate(-4, -4)
	cached.set_clip(clip_rect)
	ascent = combobox.font.get_ascent()
	descent = abs(combobox.font.get_descent())
	optical_centre_offset = ascent-(ascent-descent)//2
	surf_top = local_rect.centery-optical_centre_offset
	surf_top = max(local_rect.top, min(local_rect.bottom-combobox.font.get_height(), surf_top))
	display_text = combobox.get_display_text()
	drawn_stretched = False
	if not combobox.hide_text and combobox.alignment=="stretched" and len(display_text)>1 and not combobox.auto_size:
		total_char_width = sum(combobox.font.render(char, True, text_color).get_width() for char in display_text)
		available_width = local_rect.width-(combobox.alignment_spacing*2)
		if available_width>total_char_width:
			drawn_stretched = True
			spacing = (available_width-total_char_width)/(len(display_text)-1)
			current_x = local_rect.left+combobox.alignment_spacing
			for char in display_text:
				char_surf = combobox.font.render(char, True, text_color)
				char_surf.set_alpha(text_color[3])
				cached.blit(char_surf, (current_x, surf_top))
				current_x += char_surf.get_width()+spacing
	if not drawn_stretched:
		text_surf = combobox.font.render(display_text, True, text_color)
		text_surf.set_alpha(text_color[3])
		text_rect = text_surf.get_rect()
		visible_left = local_rect.left+combobox.alignment_spacing
		visible_right = local_rect.right-combobox.alignment_spacing
		visible_width = visible_right-visible_left
		cursor_x_rel = combobox.font.size(display_text[:combobox.cursor_position])[0]
		if combobox.auto_size: combobox.scroll_offset = 0
		if text_rect.width>visible_width and not combobox.auto_size:
			text_rect.topleft = (visible_left+combobox.scroll_offset, surf_top)
			cursor_screen_x = text_rect.x+cursor_x_rel
			if cursor_screen_x>visible_right: combobox.scroll_offset -= (cursor_screen_x-visible_right)
			elif cursor_screen_x<visible_left: combobox.scroll_offset += (visible_left-cursor_screen_x)
			min_scroll = visible_width-text_rect.width
			max_scroll = 0
			combobox.scroll_offset = max(min_scroll, min(max_scroll, combobox.scroll_offset))
			text_rect.x = visible_left+combobox.scroll_offset
		else:
			combobox.scroll_offset = 0
			if combobox.alignment=="left":
				text_rect.topleft = (visible_left, surf_top)
			elif combobox.alignment=="right":
				text_rect.topright = (visible_right, surf_top)
			else:
				text_rect.topleft = (local_rect.centerx-text_rect.width//2, surf_top)
		if combobox.selected_text and combobox.selected_text[0]!=combobox.selected_text[1]:
			start_idx = min(combobox.selected_text)
			end_idx = max(combobox.selected_text)
			sel_start_x = combobox.font.size(display_text[:start_idx])[0]
			sel_end_x = combobox.font.size(display_text[:end_idx])[0]
			highlight_rect = pygame.Rect(
				text_rect.x+sel_start_x, text_rect.top, sel_end_x-sel_start_x,
				text_rect.height
			)
			if not combobox.hide_selection:
				sel_surf = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
				sel_surf.fill(selection_color)
				cached.blit(sel_surf, highlight_rect)
				pygame.draw.rect(cached, selection_color, highlight_rect)
		if not combobox.hide_text:
			cached.blit(text_surf, text_rect)
		has_selection = combobox.selected_text and combobox.selected_text[0]!=combobox.selected_text[1]
		if combobox.focused and combobox.state=="enabled" and not has_selection:
			if combobox.cursor_visible:
				line_x = text_rect.x+cursor_x_rel
				if visible_left-2<=line_x<=visible_right+2:
					cursor_surf = combobox.font.render(combobox.blinking_cursor, True, text_color)
					cursor_surf.set_alpha(text_color[3])
					cursor_rect = cursor_surf.get_rect(center=(line_x, text_rect.centery))
					cached.blit(cursor_surf, cursor_rect)
		combobox.local_text_x = text_rect.x
	cached.set_clip(None)
	combobox._list_local = None
	if combobox._dropdown_open:
		dd_rect, list_rect, options = combobox._dropdown_layout()
		if list_rect.height:
			bounds = local_rect.union(dd_rect)
			pad_x = max(-bounds.left, bounds.right-base_width)
			pad_y = max(-bounds.top, bounds.bottom-base_height)
			dd_rect.move_ip(pad_x, pad_y)
			list_rect.move_ip(pad_x, pad_y)
			dropdown = pygame.Surface(dd_rect.size, pygame.SRCALPHA)
			if not combobox.hide_dropdown_background:
				if combobox.state=="enabled": dropdown.fill(combobox.active_unpressed_background_dropdown_color)
				else: dropdown.fill(combobox.disabled_unpressed_background_dropdown_color)
			item_h = combobox._item_height()
			for row in range(list_rect.height//item_h):
				idx = combobox._dropdown_scroll+row
				item = pygame.Rect(0, list_rect.top-dd_rect.top+row*item_h, dd_rect.width, item_h)
				item_hovering = idx==combobox._highlight
				if combobox.state=="enabled":
					if combobox.pressed and combobox.dropdown_hovered and item_hovering:
						item_text_color = combobox.active_pressed_text_dropdown_color
						item_bg_color = combobox.active_pressed_background_dropdown_color
					elif item_hovering:
						item_text_color = combobox.active_hover_text_dropdown_color
						item_bg_color = combobox.active_hover_background_dropdown_color
					else:
						item_text_color = combobox.active_unpressed_text_dropdown_color
						item_bg_color = combobox.active_unpressed_background_dropdown_color
				else:
					if item_hovering:
						item_text_color = combobox.disabled_hover_text_dropdown_color
						item_bg_color = combobox.disabled_hover_background_dropdown_color
					else:
						item_text_color = combobox.disabled_unpressed_text_dropdown_color
						item_bg_color = combobox.disabled_unpressed_background_dropdown_color
				if item_hovering and not combobox.hide_dropdown_background:
					item_bg_surf = pygame.Surface(item.size, pygame.SRCALPHA)
					item_bg_surf.fill(item_bg_color)
					dropdown.blit(item_bg_surf, item)
				if combobox.hide_dropdown_text: continue
				item_text = options[idx]
				item_drawn_stretched = False
				if combobox.dropdown_alignment=="stretched" and len(item_text)>1:
					total_char_width = sum(combobox.font.size(char)[0] for char in item_text)
					available_width = item.width-(combobox.dropdown_alignment_spacing*2)
					if available_width>total_char_width:
						item_drawn_stretched = True
						char_spacing = (available_width-total_char_width)/(len(item_text)-1)
						current_x = item.left+combobox.dropdown_alignment_spacing
						for char in item_text:
							char_surf = combobox.font.render(char, True, item_text_color)
							char_surf.set_alpha(item_text_color[3])
							dropdown.blit(char_surf, (current_x, item.centery-char_surf.get_height()//2))
							current_x += char_surf.get_width()+char_spacing
				if not item_drawn_stretched:
					item_surf = combobox.font.render(item_text, True, item_text_color)
					item_surf.set_alpha(item_text_color[3])
					if combobox.dropdown_alignment=="right":
						item_x = item.right-combobox.dropdown_alignment_spacing-item_surf.get_width()
					elif combobox.dropdown_alignment=="center": item_x = item.centerx-item_surf.get_width()//2
					else: item_x = item.left+combobox.dropdown_alignment_spacing
					dropdown.blit(item_surf, (item_x, item.centery-item_surf.get_height()//2))
			dd_local = dropdown.get_rect()
			mask = pygame.Surface(dd_rect.size, pygame.SRCALPHA)
			pygame.draw.rect(
				mask, (255, 255, 255, 255), dd_local,
				border_top_left_radius=combobox.top_left_corner_radius,
				border_top_right_radius=combobox.top_right_corner_radius,
				border_bottom_left_radius=combobox.bottom_left_corner_radius,
				border_bottom_right_radius=combobox.bottom_right_corner_radius
			)
			dropdown.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
			if not combobox.hide_dropdown_border:
				if combobox.state=="enabled":
					if combobox.pressed and combobox.dropdown_hovered:
						dropdown_brd_color = combobox.active_pressed_border_dropdown_color
					elif combobox.dropdown_hovered:
						dropdown_brd_color = combobox.active_hover_border_dropdown_color
					else:
						dropdown_brd_color = combobox.active_unpressed_border_dropdown_color
				else:
					if combobox.dropdown_hovered:
						dropdown_brd_color = combobox.disabled_hover_border_dropdown_color
					else:
						dropdown_brd_color = combobox.disabled_unpressed_border_dropdown_color
				pygame.draw.rect(
					dropdown, dropdown_brd_color, dd_local, width=combobox.border_thickness,
					border_top_left_radius=combobox.top_left_corner_radius,
					border_top_right_radius=combobox.top_right_corner_radius,
					border_bottom_left_radius=combobox.bottom_left_corner_radius,
					border_bottom_right_radius=combobox.bottom_right_corner_radius
				)
			combined = pygame.Surface((base_width+pad_x*2, base_height+pad_y*2), pygame.SRCALPHA)
			combined.blit(dropdown, dd_rect)
			combined.blit(cached, (pad_x, pad_y))
			cached = combined
			combobox._list_local = list_rect
	combobox.original_surface = cached
	combobox._last_visual_state = misc._get_vars(combobox, TO_UPDATE)
	combobox._needs_redraw = True
	combobox._needs_transform = True
	print(1)