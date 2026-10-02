# button.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets
"""A button widget for pygame."""

from __future__ import annotations

from collections.abc import Callable, Iterable
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


class Button(Widget, Tooltipable, Screenable, Deletable):
	"""Initializes a button widget for pygame."""

	@_themed
	def __init__(self, screen: easypygamewidgets.Screen | None = None, auto_size: bool = True, width: int = 180,
	             height: int = 80,
	             text: str = "easypygamewidgets Button",
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
	             hide_text: bool = False, hide_background: bool = False, hide_border: bool = False,
	             active_hover_cursor: pygame.Cursor | None = sd["active_hover_cursor"],
	             disabled_hover_cursor: pygame.Cursor | None = sd["disabled_hover_cursor"],
	             active_pressed_cursor: pygame.Cursor | None = sd["active_pressed_cursor"],
	             font: pygame.font.Font | pygame.font.SysFont = sd["font"], alignment: str = "center",
	             command: Callable | None = None, alignment_spacing: int = sd["alignment_spacing"],
	             top_left_corner_radius: int = sd["top_left_corner_radius"],
	             top_right_corner_radius: int = sd["top_right_corner_radius"],
	             bottom_left_corner_radius: int = sd["bottom_left_corner_radius"],
	             bottom_right_corner_radius: int = sd["bottom_right_corner_radius"],
	             layer: int = sd["layer"], line_spacing: int = sd["line_spacing"],
	             tooltip: easypygamewidgets.Tooltip | None = None, min_width: int | None = sd["min_width"],
	             max_width: int | None = sd["max_width"], min_height: int | None = sd["min_height"],
	             max_height: int | None = sd["max_height"],
	             alpha_based_collision_system: bool = sd["alpha_based_collision_system"],
	             anchor_x: str = sd["anchor_x"], anchor_y: str = sd["anchor_y"],
	             visible: bool = sd["visible"], data: Any = None) -> None:
		"""
		Initializes a Button widget.

		Args:
			screen: The Screen this button is attached to. If None, the button is created without a parent screen.
			auto_size: If True, width and height are computed from the rendered text instead of using the given
				width/height.
			width: Fixed button width in pixels. Ignored if auto_size is True.
			height: Fixed button height in pixels. Ignored if auto_size is True.
			text: The text displayed on the button. Supports multi-line text via '\n'.
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
			hide_text: If True, text is not rendered.
			hide_background: If True, the background fill is not rendered.
			hide_border: If True, the border is not rendered.
			active_hover_cursor: Custom cursor shown on hover while enabled.
			disabled_hover_cursor: Custom cursor shown on hover while disabled.
			active_pressed_cursor: Custom cursor shown while pressed.
			font: The pygame font used to render the button text.
			alignment: Text alignment: 'left', 'right', 'center', or 'stretched'.
			command: Callback bound to the '<RELEASE>' event.
			alignment_spacing: Horizontal padding reserved around aligned text.
			top_left_corner_radius: Corner radius in pixels for the top-left corner.
			top_right_corner_radius: Corner radius in pixels for the top-right corner.
			bottom_left_corner_radius: Corner radius in pixels for the bottom-left corner.
			bottom_right_corner_radius: Corner radius in pixels for the bottom-right corner.
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
		self._bindings = {}
		if screen:
			screen.add_widget(self)
			self._screen = screen
			if state:
				self._state = state
		else:
			self._screen = None
			if state:
				self._state = state
			else:
				self._state = "enabled"
		self._auto_size = auto_size
		if self._auto_size:
			font.set_linesize(line_spacing)
			lines = text.split("\n")
			total_w = 0
			text_h = font.get_height()
			effective_line_h = max(text_h, line_spacing)
			for line in lines:
				text_w = font.size(line)[0]
				if text_w>total_w:
					total_w = text_w
			total_h = (len(lines)-1)*effective_line_h+text_h
			vertical_padding = max(20, min(40, text_h//2))
			self._width = total_w+alignment_spacing
			if min_width:
				self._width = max(self._width, min_width)
			if max_width:
				self._width = min(self._width, max_width)
			self._height = total_h+vertical_padding
			if min_height:
				self._height = max(self._height, min_height)
			if max_height:
				self._height = min(self._height, max_height)
		else:
			self._width = width
			self._height = height
		self._text = text
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
			if isinstance(cursor, pygame.Cursor):
				self._cursors[name] = cursor
			else:
				if cursor is not None:
					raise ValueError(
						f"No custom cursor is used for the button '{text}' because it's not a pygame.Cursor object. "
						f"{cursor} is a {type(cursor)}"
					)
				self._cursors[name] = None
		self._font = font
		self._alignment = alignment
		self._alignment_spacing = alignment_spacing
		if command:
			self.bind(epw_types.RELEASE, command)
		self._top_left_corner_radius = top_left_corner_radius
		self._top_right_corner_radius = top_right_corner_radius
		self._bottom_left_corner_radius = bottom_left_corner_radius
		self._bottom_right_corner_radius = bottom_right_corner_radius
		self._layer = layer
		self._tooltip = tooltip
		if tooltip:
			tooltip.configure(_layer=layer+1)
			if not tooltip.style:
				tooltip.configure(
					active_unpressed_text_color=self._active_unpressed_text_color,
					active_unpressed_background_color=self._active_unpressed_background_color,
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
		self._visible = visible
		self._data = data
		self._x = 0
		self._y = 0
		self._alive = True
		self._pressed = False
		self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
		self._original_cursor = None
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
		self._current_offset = [0.0, 0.0]
		self._offset_step = [0, 0]
		self._use_rotozoom = False
		self._dialog = None

		font.set_linesize(line_spacing)

		misc._add_widget(self)

	@property
	def bindings(self):
		return self._bindings

	@bindings.setter
	def bindings(self, value):
		self._bindings = value

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
	def text(self):
		return self._text

	@text.setter
	def text(self, value):
		self._text = value

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
		self._font.set_linesize(self._line_spacing)

	@property
	def alignment(self):
		return self._alignment

	@alignment.setter
	def alignment(self, value):
		self._alignment = value

	@property
	def command(self):
		return self._bindings[epw_types.RELEASE]

	@command.setter
	def command(self, value):
		self.bind(epw_types.RELEASE, value)

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

	@property
	def dialog(self):
		return self._dialog

	@dialog.setter
	def dialog(self, value):
		self._dialog = value

	def configure(self, **kwargs: Unpack[TypeHints.ButtonConfig]) -> Button:
		"""
		Updates one or more of the button's attributes.

		Args:
			**kwargs: Button attributes to update as defined in TypeHints.ButtonConfig

		Returns:
			Button (Button): This button instance to allow method chaining.
		"""
		for key, value in kwargs.items():
			setattr(self, key, value)
		self._needs_redraw = True
		self._needs_transform = True
		if any(
				k in kwargs for k in (
						'auto_size', 'x', 'y', 'width', 'height', 'text', 'font', 'max_width', 'min_width',
						'max_height',
						'min_height', 'line_spacing', 'alignment_spacing', 'anchor_x', 'anchor_y'
				)
		):
			if self._auto_size:
				self._font.set_linesize(self._line_spacing)
				lines = self._text.split("\n")
				total_w = 0
				text_h = self._font.get_height()
				effective_line_h = max(text_h, self._line_spacing)
				for line in lines:
					text_w = self._font.size(line)[0]
					if text_w>total_w:
						total_w = text_w
				total_h = (len(lines)-1)*effective_line_h+text_h
				vertical_padding = max(20, min(40, text_h//2))
				self._width = total_w+self._alignment_spacing
				if self._min_width:
					self._width = max(self._width, self._min_width)
				if self._max_width:
					self._width = min(self._width, self._max_width)
				self._height = total_h+vertical_padding
				if self._min_height:
					self._height = max(total_h+vertical_padding, self._min_height)
				if self._max_height:
					self._height = min(total_h+vertical_padding, self._max_height)
			self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
		if 'line_spacing' in kwargs:
			self._font.set_linesize(self._line_spacing)
		return self

	def config(self, **kwargs: Unpack[TypeHints.ButtonConfig]) -> Button:
		"""
		Updates one or more of the button's attributes.

		Args:
			**kwargs: Button attributes to update as defined in TypeHints.ButtonConfig

		Returns:
			Button (Button): This button instance to allow method chaining.
		"""
		return self.configure(**kwargs)

	def scale(self, value: int | float = 1, frames_to_finish: int = 1) -> Button:
		"""
		Scale the button by a factor. It's only a visual scale so upscaling could look pixelated.

		Args:
			 value (int|float): the scale factor
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Button (Button): This button instance to allow method chaining.
		"""
		if frames_to_finish<=0:
			frames_to_finish = 1
		self._target_scale = value
		self._scale_step = (self._target_scale-self._current_scale)/frames_to_finish
		self._update_animation()
		return self

	def rotate(self, value: int | float = 0, frames_to_finish: int = 1) -> Button:
		"""
		Rotate the button by a degree.

		Args:
			 value (int|float): the rotation degree
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Button (Button): This button instance to allow method chaining.
		"""
		if frames_to_finish<=0:
			frames_to_finish = 1
		self._target_rotation = value
		self._rotation_step = (self._target_rotation-self._current_rotation)/frames_to_finish
		self._update_animation()
		return self

	def rotozoom(self, scale: int | float = 1, rotation: int | float = 0, frames_to_finish: int = 1) -> Button:
		"""
		Rotate the button by a degree and scale it.

		Args:
			 scale (int|float): the scale factor
			 rotation (int|float): the rotation degree
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Button (Button): This button instance to allow method chaining.
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

	def offset(self, value: Iterable[int] = (0, 0), frames_to_finish: int = 1) -> Button:
		"""
		Offset the button by an x and y value.

		Args:
			 value: an iterable thing with two values. The first being the x and the second the y offset.
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Button (Button): This button instance to allow method chaining.
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
		Internally used to draw the button.

		Args:
			surface (pygame.Surface): The surface to draw the button on.
		"""
		if not self._alive or not self._visible: return
		mouse_pos = pygame.mouse.get_pos()
		is_hovering = misc._is_point_over_widget(self, mouse_pos)
		current_visual_state = (self._pressed, is_hovering)
		if self._needs_redraw or self._last_visual_state!=current_visual_state:
			_render_button_surface(self, is_hovering)

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
		mouse_pos = pygame.mouse.get_pos()
		is_inside = misc._is_point_over_widget(self, mouse_pos)
		if not event:
			if pygame.mouse.get_pressed()[0]:
				self.trigger_event(epw_types.HOLD)
				if is_inside:
					self._pressed = True
			elif not pygame.mouse.get_pressed()[0]:
				if self._pressed:
					self.trigger_event(epw_types.RELEASE)
					self._pressed = False
		else:
			if event.type==pygame.KEYDOWN:
				misc._trigger_key_bindings(self, event)
			elif event.type==pygame.MOUSEBUTTONDOWN:
				if event.button==1:
					self.trigger_event(epw_types.PRESS)
					if is_inside:
						self._pressed = True
			elif event.type==pygame.MOUSEBUTTONUP:
				if event.button==1:
					self.trigger_event(epw_types.RELEASE)
					self._pressed = False


def _render_button_surface(button: Button, is_hovering: bool) -> None:
	"""
	Internally used to render the button surface once and cache it.

	Args:
		 button (Button): the widget to render the surface for
		 is_hovering (bool): whether the mouse is hovering over the widget
	"""
	if button.state=="enabled":
		if button.pressed and is_hovering:
			text_color = button.active_pressed_text_color
			bg_color = button.active_pressed_background_color
			brd_color = button.active_pressed_border_color
		elif is_hovering:
			text_color = button.active_hover_text_color
			bg_color = button.active_hover_background_color
			brd_color = button.active_hover_border_color
		else:
			text_color = button.active_unpressed_text_color
			bg_color = button.active_unpressed_background_color
			brd_color = button.active_unpressed_border_color
	else:
		if is_hovering:
			text_color = button.disabled_hover_text_color
			bg_color = button.disabled_hover_background_color
			brd_color = button.disabled_hover_border_color
		else:
			text_color = button.disabled_unpressed_text_color
			bg_color = button.disabled_unpressed_background_color
			brd_color = button.disabled_unpressed_border_color

	base_width = button._width
	base_height = button._height
	cached = pygame.Surface((base_width, base_height), pygame.SRCALPHA)
	local_rect = pygame.Rect(0, 0, base_width, base_height)
	if not button.hide_background:
		pygame.draw.rect(
			cached, bg_color, local_rect,
			border_top_left_radius=button.top_left_corner_radius,
			border_top_right_radius=button.top_right_corner_radius,
			border_bottom_left_radius=button.bottom_left_corner_radius,
			border_bottom_right_radius=button.bottom_right_corner_radius
		)
	if not button.hide_border:
		pygame.draw.rect(
			cached, brd_color, local_rect, width=button.border_thickness,
			border_top_left_radius=button.top_left_corner_radius,
			border_top_right_radius=button.top_right_corner_radius,
			border_bottom_left_radius=button.bottom_left_corner_radius,
			border_bottom_right_radius=button.bottom_right_corner_radius
		)

	if not button.hide_text:
		ascent = button.font.get_ascent()
		descent = abs(button.font.get_descent())
		optical_centre_offset = ascent-(ascent-descent)//2
		font_line_h = button.font.get_height()
		effective_line_h = int(max(font_line_h, button.line_spacing))
		if button.alignment=="stretched" and len(button.text)>1 and not button.auto_size:
			total_char_width = sum(button.font.render(char, True, text_color).get_width() for char in button.text)
			available_width = local_rect.width-button.alignment_spacing
			if available_width>total_char_width:
				spacing = (available_width-total_char_width)/(len(button.text)-1)
				current_x = local_rect.left+button.alignment_spacing//2
				char_y = local_rect.centery-optical_centre_offset+ascent
				for char in button.text:
					char_surf = button.font.render(char, True, text_color)
					char_surf.set_alpha(text_color[3])
					surf_top = char_y-button.font.get_ascent()
					surf_top = max(local_rect.top, min(local_rect.bottom-char_surf.get_height(), surf_top))
					cached.blit(char_surf, (current_x, surf_top))
					current_x += char_surf.get_width()+spacing
			else:
				text_surf = button.font.render(button.text, True, text_color)
				text_surf.set_alpha(text_color[3])
				surf_top = local_rect.centery-optical_centre_offset
				surf_top = max(local_rect.top, min(local_rect.bottom-text_surf.get_height(), surf_top))
				cached.blit(text_surf, text_surf.get_rect(centerx=local_rect.centerx, top=surf_top))
		else:
			lines = button.text.split("\n")
			total_text_height = (len(lines)-1)*effective_line_h+font_line_h
			block_top = local_rect.centery-total_text_height//2
			for i, line in enumerate(lines):
				text_surf = button.font.render(line, True, text_color)
				text_surf.set_alpha(text_color[3])
				surf_top = block_top+i*effective_line_h
				surf_top = max(local_rect.top, min(local_rect.bottom-text_surf.get_height(), surf_top))
				if button.alignment=="left":
					cached.blit(text_surf, (local_rect.left+button.alignment_spacing//2, surf_top))
				elif button.alignment=="right":
					cached.blit(
						text_surf,
						(local_rect.right-button.alignment_spacing//2-text_surf.get_width(), surf_top)
					)
				else:
					cached.blit(text_surf, text_surf.get_rect(centerx=local_rect.centerx, top=surf_top))
	button.original_surface = cached
	button.cached_surface = cached
	button._last_visual_state = (button.pressed, is_hovering)
	button.needs_redraw = False
	button._needs_transform = True