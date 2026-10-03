# tooltip.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets

from __future__ import annotations

import os
import pathlib
from collections.abc import Iterable
from typing import Any, TYPE_CHECKING, Unpack

import pygame

from easypygamewidgets import misc
from easypygamewidgets.assets import epw_types, TypeHints
from easypygamewidgets.assets.theme import _style_dic as sd, _themed
from easypygamewidgets.masterWidgets import Deletable, Tooltipable, Widget

if TYPE_CHECKING:
	import easypygamewidgets

pygame.init()


class Tooltip(Widget, Deletable):
	@_themed
	def __init__(self,
	             widgets: list[Widget] | None = None,
	             auto_size: bool = True, width: int = 180,
	             height: int = 80,
	             text: str = "easypygamewidgets Tooltip",
	             state: str | None = None,
	             active_unpressed_text_color: tuple | None = sd["active_unpressed_text_color"],
	             disabled_unpressed_text_color: tuple | None = sd["disabled_unpressed_text_color"],
	             active_hover_text_color: tuple | None = sd["active_hover_text_color"],
	             disabled_hover_text_color: tuple | None = sd["disabled_hover_text_color"],
	             active_pressed_text_color: tuple | None = sd["active_pressed_text_color"],
	             active_unpressed_background_color: tuple | None = sd["active_unpressed_background_color"],
	             disabled_unpressed_background_color: tuple | None = sd["disabled_unpressed_background_color"],
	             active_hover_background_color: tuple | None = sd["active_hover_background_color"],
	             disabled_hover_background_color: tuple | None = sd["disabled_hover_background_color"],
	             active_pressed_background_color: tuple | None = sd["active_pressed_background_color"],
	             active_unpressed_border_color: tuple | None = sd["active_unpressed_border_color"],
	             disabled_unpressed_border_color: tuple | None = sd["disabled_unpressed_border_color"],
	             active_hover_border_color: tuple | None = sd["active_hover_border_color"],
	             disabled_hover_border_color: tuple | None = sd["disabled_hover_border_color"],
	             active_pressed_border_color: tuple | None = sd["active_pressed_border_color"],
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
	             layer: int = sd["layer"], style: str | None = None,
	             suppress_icon=False, icon: pygame.Surface | easypygamewidgets.Surface | None = None,
	             line_spacing: int = sd["line_spacing"], min_width: int | None = sd["min_width"],
	             max_width: int | None = sd["max_width"],
	             min_height: int | None = sd["min_height"], max_height: int | None = sd["max_height"],
	             alpha_based_collision_system: bool = sd["alpha_based_collision_system"],
	             anchor_x: str = sd["anchor_x"],
	             anchor_y: str = sd["anchor_y"], visible: bool = False, data: Any = None):
		super().__init__()
		self._bindings = {}
		self._style = style
		self._icon = None
		self._layer = layer
		self._font = font
		self._line_spacing = line_spacing
		self._state = state if state else "enabled"
		if not style:
			self._active_unpressed_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_unpressed_background_color = misc.normalize_color((50, 50, 50, 255))
			self._active_unpressed_border_color = misc.normalize_color((100, 100, 100, 255))
			self._disabled_unpressed_text_color = misc.normalize_color((200, 200, 200, 255))
			self._disabled_unpressed_background_color = misc.normalize_color((80, 80, 80, 255))
			self._disabled_unpressed_border_color = misc.normalize_color((60, 60, 60, 255))
			self._active_hover_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_hover_background_color = misc.normalize_color((65, 65, 65, 255))
			self._active_hover_border_color = misc.normalize_color((120, 120, 120, 255))
			self._disabled_hover_text_color = misc.normalize_color((200, 200, 200, 255))
			self._disabled_hover_background_color = misc.normalize_color((80, 80, 80, 255))
			self._disabled_hover_border_color = misc.normalize_color((60, 60, 60, 255))
			self._active_pressed_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_pressed_background_color = misc.normalize_color((40, 40, 40, 255))
			self._active_pressed_border_color = misc.normalize_color((140, 140, 140, 255))
		self._widgets = []
		if widgets:
			if not isinstance(widgets, Iterable):
				widgets = [widgets]
			for widget in widgets:
				widget.set_tooltip(self)
		self._auto_size = auto_size
		self._width = width
		self._height = height
		if auto_size:
			temp_surf = font.render(text, True, (0, 0, 0))
			text_w, text_h = temp_surf.get_size()
			self._height = text_h+20
			icon_offset = self._height if icon and not suppress_icon else 0
			self._width = text_w+(alignment_spacing*2)+icon_offset
			if min_width:
				self._width = max(self._width, min_width)
			if max_width:
				self._width = min(self._width, max_width)
			if min_height:
				self._height = max(self._height, min_height)
			if max_height:
				self._height = min(self._height, max_height)
		self._text = text
		self._border_thickness = border_thickness
		self._hide_text = hide_text
		self._hide_background = hide_background
		self._hide_border = hide_border
		if style=="info":
			if not icon:
				self._icon = pygame.image.load(
					os.path.join(
						pathlib.Path(__file__).resolve().parent,
						"assets", "tooltip", "info.png"
					)
				)
			self._active_unpressed_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_unpressed_background_color = misc.normalize_color((46, 55, 90, 255))
			self._active_unpressed_border_color = misc.normalize_color((39, 78, 194, 255))
			self._active_hover_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_hover_background_color = misc.normalize_color((56, 65, 100, 255))
			self._active_hover_border_color = misc.normalize_color((59, 98, 214, 255))
			self._active_pressed_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_pressed_background_color = misc.normalize_color((36, 45, 80, 255))
			self._active_pressed_border_color = misc.normalize_color((19, 58, 174, 255))
		elif style=="warning":
			if not icon:
				self._icon = pygame.image.load(
					os.path.join(
						pathlib.Path(__file__).resolve().parent,
						"assets", "tooltip", "warning.png"
					)
				)
			self._active_unpressed_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_unpressed_background_color = misc.normalize_color((178, 91, 53, 255))
			self._active_unpressed_border_color = misc.normalize_color((222, 108, 56, 255))
			self._active_hover_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_hover_background_color = misc.normalize_color((188, 101, 63, 255))
			self._active_hover_border_color = misc.normalize_color((242, 128, 76, 255))
			self._active_pressed_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_pressed_background_color = misc.normalize_color((168, 81, 43, 255))
			self._active_pressed_border_color = misc.normalize_color((202, 88, 36, 255))
		elif style=="blocked":
			if not icon:
				self._icon = pygame.image.load(
					os.path.join(
						pathlib.Path(__file__).resolve().parent,
						"assets", "tooltip", "blocked.png"
					)
				)
			self._active_unpressed_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_unpressed_background_color = misc.normalize_color((150, 63, 60, 255))
			self._active_unpressed_border_color = misc.normalize_color((188, 46, 41, 255))
			self._active_hover_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_hover_background_color = misc.normalize_color((160, 73, 70, 255))
			self._active_hover_border_color = misc.normalize_color((208, 66, 61, 255))
			self._active_pressed_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_pressed_background_color = misc.normalize_color((130, 53, 50, 255))
			self._active_pressed_border_color = misc.normalize_color((168, 26, 21, 255))
		if active_unpressed_text_color:
			self._active_unpressed_text_color = misc.normalize_color(active_unpressed_text_color)
			self._style = "custom"
		if disabled_unpressed_text_color:
			self._disabled_unpressed_text_color = misc.normalize_color(disabled_unpressed_text_color)
			self._style = "custom"
		if active_hover_text_color:
			self._active_hover_text_color = misc.normalize_color(active_hover_text_color)
			self._style = "custom"
		if disabled_hover_text_color:
			self._disabled_hover_text_color = misc.normalize_color(disabled_hover_text_color)
			self._style = "custom"
		if active_pressed_text_color:
			self._active_pressed_text_color = misc.normalize_color(active_pressed_text_color)
			self._style = "custom"
		if active_unpressed_background_color:
			self._active_unpressed_background_color = misc.normalize_color(active_unpressed_background_color)
			self._style = "custom"
		if disabled_unpressed_background_color:
			self._disabled_unpressed_background_color = misc.normalize_color(disabled_unpressed_background_color)
			self._style = "custom"
		if active_hover_background_color:
			self._active_hover_background_color = misc.normalize_color(active_hover_background_color)
			self._style = "custom"
		if disabled_hover_background_color:
			self._disabled_hover_background_color = misc.normalize_color(disabled_hover_background_color)
			self._style = "custom"
		if active_pressed_background_color:
			self._active_pressed_background_color = misc.normalize_color(active_pressed_background_color)
			self._style = "custom"
		if active_unpressed_border_color:
			self._active_unpressed_border_color = misc.normalize_color(active_unpressed_border_color)
			self._style = "custom"
		if disabled_unpressed_border_color:
			self._disabled_unpressed_border_color = misc.normalize_color(disabled_unpressed_border_color)
			self._style = "custom"
		if active_hover_border_color:
			self._active_hover_border_color = misc.normalize_color(active_hover_border_color)
			self._style = "custom"
		if disabled_hover_border_color:
			self._disabled_hover_border_color = misc.normalize_color(disabled_hover_border_color)
			self._style = "custom"
		if active_pressed_border_color:
			self._active_pressed_border_color = misc.normalize_color(active_pressed_border_color)
			self._style = "custom"
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
					print(
						f"No custom cursor is used for the tooltip {text} because it's not a pygame.Cursor object. ({cursor})"
					)
				self._cursors[name] = None
		self._alignment = alignment
		self._alignment_spacing = alignment_spacing
		self._top_left_corner_radius = top_left_corner_radius
		self._top_right_corner_radius = top_right_corner_radius
		self._bottom_left_corner_radius = bottom_left_corner_radius
		self._bottom_right_corner_radius = bottom_right_corner_radius
		self._suppress_icon = suppress_icon
		if icon:
			self._icon = icon
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
		self._is_hovered = False
		self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
		self._original_cursor = None
		self._needs_redraw = True
		self._needs_transform = True
		self._last_visual_state = None
		self._cached_surface = None
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

		self._font.set_linesize(self._line_spacing)

		misc._add_widget(self)

		self.place(self._x, self._y)  # apply the anchors

	@property
	def widgets(self):
		return self._widgets

	@widgets.setter
	def widgets(self, value):
		for widget in self._widgets:
			widget._tooltip = None

		if not isinstance(value, Iterable):
			value = [value]
		for widget in value:
			widget.set_tooltip(self)
		self._widgets = value

	@property
	def bindings(self):
		return self._bindings

	@bindings.setter
	def bindings(self, value):
		self._bindings = value

	@property
	def style(self):
		return self._style

	@style.setter
	def style(self, value):
		self._style = value
		if value=="info":
			self._icon = pygame.image.load(
				os.path.join(
					pathlib.Path(__file__).resolve().parent,
					"assets", "tooltip", "info.png"
				)
			)
			self._active_unpressed_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_unpressed_background_color = misc.normalize_color((46, 55, 90, 255))
			self._active_unpressed_border_color = misc.normalize_color((39, 78, 194, 255))
			self._active_hover_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_hover_background_color = misc.normalize_color((56, 65, 100, 255))
			self._active_hover_border_color = misc.normalize_color((59, 98, 214, 255))
			self._active_pressed_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_pressed_background_color = misc.normalize_color((36, 45, 80, 255))
			self._active_pressed_border_color = misc.normalize_color((19, 58, 174, 255))
		elif value=="warning":
			self._icon = pygame.image.load(
				os.path.join(
					pathlib.Path(__file__).resolve().parent,
					"assets", "tooltip", "warning.png"
				)
			)
			self._active_unpressed_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_unpressed_background_color = misc.normalize_color((178, 91, 53, 255))
			self._active_unpressed_border_color = misc.normalize_color((222, 108, 56, 255))
			self._active_hover_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_hover_background_color = misc.normalize_color((188, 101, 63, 255))
			self._active_hover_border_color = misc.normalize_color((242, 128, 76, 255))
			self._active_pressed_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_pressed_background_color = misc.normalize_color((168, 81, 43, 255))
			self._active_pressed_border_color = misc.normalize_color((202, 88, 36, 255))
		elif value=="blocked":
			self._icon = pygame.image.load(
				os.path.join(
					pathlib.Path(__file__).resolve().parent,
					"assets", "tooltip", "blocked.png"
				)
			)
			self._active_unpressed_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_unpressed_background_color = misc.normalize_color((150, 63, 60, 255))
			self._active_unpressed_border_color = misc.normalize_color((188, 46, 41, 255))
			self._active_hover_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_hover_background_color = misc.normalize_color((160, 73, 70, 255))
			self._active_hover_border_color = misc.normalize_color((208, 66, 61, 255))
			self._active_pressed_text_color = misc.normalize_color((255, 255, 255, 255))
			self._active_pressed_background_color = misc.normalize_color((130, 53, 50, 255))
			self._active_pressed_border_color = misc.normalize_color((168, 26, 21, 255))

	@property
	def state(self):
		return self._state

	@state.setter
	def state(self, value):
		self._state = value

	@property
	def icon(self):
		return self._icon

	@icon.setter
	def icon(self, value):
		self._icon = value

	@property
	def layer(self):
		return self._layer

	@layer.setter
	def layer(self, value):
		self._layer = value
		misc._resort_layers()

	@property
	def font(self):
		return self._font

	@font.setter
	def font(self, value):
		self._font = value
		self._font.set_linesize(self._line_spacing)

	@property
	def line_spacing(self):
		return self._line_spacing

	@line_spacing.setter
	def line_spacing(self, value):
		self._line_spacing = value
		self._font.set_linesize(value)

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
	def text(self):
		return self._text

	@text.setter
	def text(self, value):
		self._text = value

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
	def suppress_icon(self):
		return self._suppress_icon

	@suppress_icon.setter
	def suppress_icon(self, value):
		self._suppress_icon = value

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
	def pressed(self):
		return self._pressed

	@pressed.setter
	def pressed(self, value):
		self._pressed = value

	@property
	def alive(self):
		return self._alive

	@alive.setter
	def alive(self, value):
		self._alive = value

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
	def visible(self):
		return self._visible

	@visible.setter
	def visible(self, value):
		self._visible = value

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

	def configure(self, **kwargs: Unpack[TypeHints.TooltipConfig]) -> Tooltip:
		"""
		Updates one or more of the tooltip's attributes.

		Args:
			**kwargs: Tooltip attributes to update as defined in TypeHints.TooltipConfig

		Returns:
			Tooltip (Tooltip): This tooltip instance to allow method chaining.
		"""
		for key, value in kwargs.items():
			setattr(self, key, value)
		self._needs_redraw = True
		self._needs_transform = True
		if any(
				k in kwargs for k in
				(
						'auto_size', 'x', 'y', 'width', 'height', 'min_width', 'max_width', 'min_height', 'max_height',
						'text',
						'icon', 'suppress_icon', 'alignment_spacing', 'font', 'anchor_x', 'anchor_y'
				)
		):
			if self._auto_size:
				temp_surf = self._font.render(self._text, True, (0, 0, 0))
				text_w, text_h = temp_surf.get_size()
				self._height = text_h+20
				icon_offset = self._height if self._icon and not self._suppress_icon else 0
				self._width = text_w+(self._alignment_spacing*2)+icon_offset
				if self._min_width:
					self._width = max(self._width, self._min_width)
				if self._max_width:
					self._width = min(self._width, self._max_width)
				if self._min_height:
					self._height = max(self._height, self._min_height)
				if self._max_height:
					self._height = min(self._height, self._max_height)
			self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
		return self

	def config(self, **kwargs: Unpack[TypeHints.TooltipConfig]) -> Tooltip:
		"""
		Updates one or more of the tooltip's attributes.

		Args:
			**kwargs: Tooltip attributes to update as defined in TypeHints.TooltipConfig

		Returns:
			Tooltip (Tooltip): This tooltip instance to allow method chaining.
		"""
		return self.configure(**kwargs)

	def scale(self, value: int | float = 1, frames_to_finish: int = 1) -> Tooltip:
		"""
		Scale the tooltip by a factor. It's only a visual scale so upscaling could look pixelated.

		Args:
			 value (int|float): the scale factor
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Tooltip (Tooltip): This tooltip instance to allow method chaining.
		"""
		if frames_to_finish<=0:
			frames_to_finish = 1
		self._target_scale = value
		self._scale_step = (self._target_scale-self._current_scale)/frames_to_finish
		self._update_animation()
		return self

	def rotate(self, value: int | float = 0, frames_to_finish: int = 1) -> Tooltip:
		"""
		Rotate the tooltip by a degree.

		Args:
			 value (int|float): the rotation degree
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Tooltip (Tooltip): This tooltip instance to allow method chaining.
		"""
		if frames_to_finish<=0:
			frames_to_finish = 1
		self._target_rotation = value
		self._rotation_step = (self._target_rotation-self._current_rotation)/frames_to_finish
		self._update_animation()
		return self

	def rotozoom(self, scale: int | float = 1, rotation: int | float = 0, frames_to_finish: int = 1) -> Tooltip:
		"""
		Rotate the tooltip by a degree and scale it.

		Args:
			 scale (int|float): the scale factor
			 rotation (int|float): the rotation degree
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Tooltip (Tooltip): This tooltip instance to allow method chaining.
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

	def offset(self, value: Iterable[int] = (0, 0), frames_to_finish: int = 1) -> Tooltip:
		"""
		Offset the tooltip by an x and y value.

		Args:
			 value: an iterable thing with two values. The first being the x and the second the y offset.
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Tooltip (Tooltip): This tooltip instance to allow method chaining.
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

	def show(self) -> Tooltip:
		"""
		Show this tooltip.

		Returns:
			Tooltip (Tooltip): This tooltip instance to allow method chaining.
		"""
		self._visible = True
		self.trigger_event(epw_types.SHOW_TOOLTIP)
		return self

	def hide(self) -> Tooltip:
		"""
		Hides this tooltip.

		Returns:
			Tooltip (Tooltip): This tooltip instance to allow method chaining.
		"""
		self._visible = False
		self.trigger_event(epw_types.HIDE_TOOLTIP)
		if self._original_cursor:
			pygame.mouse.set_cursor(self._original_cursor)
			self._original_cursor = None
		return self

	def add_widget(self, widget: Tooltipable) -> Tooltip:
		"""
		Bind a widget to this tooltip. Hovering over the widget will lead to showing the tooltip.

		Args:
			 widget (Tooltipable): The widget to bind to this tooltip.

		Returns:
			Tooltip (Tooltip): This tooltip instance to allow method chaining.
		"""
		widget.set_tooltip(self)
		return self

	def remove_widget(self, widget: Tooltipable) -> Tooltip:
		"""
		Unbind a widget from this tooltip.

		Args:
			 widget (Tooltipable): The widget to unbind from this tooltip.

		Returns:
			Tooltip (Tooltip): This tooltip instance to allow method chaining.
		"""
		if widget not in self._widgets:
			return self
		widget.remove_tooltip()
		return self

	def add_widgets(self, widgets: Iterable[Tooltipable]) -> Tooltip:
		"""
		Bind multiple widgets to this tooltip. Hovering over the widgets will lead to showing the tooltip.

		Args:
			 widgets (Iterable[Tooltipable]): The widgets to bind to this tooltip.

		Returns:
			Tooltip (Tooltip): This tooltip instance to allow method chaining.
		"""
		for widget in widgets:
			widget.set_tooltip(self)
		return self

	def remove_widgets(self, widgets: Iterable[Tooltipable]) -> Tooltip:
		"""
		Unbind multiple widgets from this tooltip.

		Args:
			 widgets (Iterable[Tooltipable]): The widgets to unbind from this tooltip.

		Returns:
			Tooltip (Tooltip): This tooltip instance to allow method chaining.
		"""
		for widget in widgets:
			if widget not in self._widgets:
				continue
			widget.remove_tooltip()
		return self

	def _draw(self, surface: pygame.Surface) -> None:
		"""
		Internally used to draw the tooltip.

		Args:
			surface (pygame.Surface): The surface to draw the tooltip on.
		"""
		if not self._alive or not self._visible:
			return
		self._font.set_linesize(self._line_spacing)
		mouse_pos = pygame.mouse.get_pos()
		is_hovering = misc._is_point_over_widget(self, (0, 0))
		current_visual_state = (self._pressed, is_hovering)
		if self._needs_redraw or self._cached_surface is None or current_visual_state!=self._last_visual_state:
			_render_tooltip_surface(self, is_hovering)
		if self._needs_transform:
			if self._current_scale!=1 or self._current_rotation!=0:
				new_width = int(self._original_surface.get_width()*self._current_scale)
				new_height = int(self._original_surface.get_height()*self._current_scale)
				if new_width>0 and new_height>0:
					if self._use_rotozoom:
						self._cached_surface = pygame.transform.rotozoom(
							self._original_surface, self._current_rotation,
							self._current_scale
						)
					else:
						scaled_surface = pygame.transform.smoothscale(self._original_surface, (new_width, new_height))
						self._cached_surface = pygame.transform.rotate(scaled_surface, self._current_rotation)
				else:
					self._cached_surface = pygame.Surface((0, 0), pygame.SRCALPHA)
			else:
				self._cached_surface = self._original_surface.copy()
			base_rect = pygame.Rect(self._x, self._y, self._width, self._height)
			old_center = base_rect.center
			self._rect = self._cached_surface.get_rect()
			self._rect.center = old_center
			self._needs_transform = False
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
		elif is_hovering and self._is_hovered:
			self._is_hovered = True
			self.trigger_event(epw_types.HOVER)
		elif not is_hovering and self._is_hovered:
			self._is_hovered = False
			self.trigger_event(epw_types.MOUSE_OUT)

		total_offset_x = mouse_pos[0]+round(self._current_offset[0])
		total_offset_y = mouse_pos[1]+round(self._current_offset[1])
		draw_rect = self._rect.move(total_offset_x, total_offset_y)
		if self._visible:
			surface.blit(self._cached_surface, draw_rect)


def _render_tooltip_surface(tooltip: Tooltip, is_hovering: bool) -> None:
	"""
	Internally used to render the tooltip surface once and cache it.

	Args:
		 tooltip (Tooltip): the widget to render the surface for
		 is_hovering (bool): whether the mouse is hovering over the widget
	"""
	if tooltip.state=="enabled":
		if tooltip.pressed and is_hovering:
			text_color = tooltip.active_pressed_text_color
			bg_color = tooltip.active_pressed_background_color
			brd_color = tooltip.active_pressed_border_color
		elif is_hovering:
			text_color = tooltip.active_hover_text_color
			bg_color = tooltip.active_hover_background_color
			brd_color = tooltip.active_hover_border_color
		else:
			text_color = tooltip.active_unpressed_text_color
			bg_color = tooltip.active_unpressed_background_color
			brd_color = tooltip.active_unpressed_border_color
	else:
		if is_hovering:
			text_color = tooltip.disabled_hover_text_color
			bg_color = tooltip.disabled_hover_background_color
			brd_color = tooltip.disabled_hover_border_color
		else:
			text_color = tooltip.disabled_unpressed_text_color
			bg_color = tooltip.disabled_unpressed_background_color
			brd_color = tooltip.disabled_unpressed_border_color
	if tooltip.auto_size:
		temp_surf = tooltip.font.render(tooltip.text, True, (0, 0, 0))
		text_w, text_h = temp_surf.get_size()
		tooltip.height = text_h+20
		icon_offset = tooltip.height if tooltip.icon and not tooltip.suppress_icon else 0
		tooltip.width = text_w+(tooltip.alignment_spacing*2)+icon_offset
		if tooltip.min_width:
			tooltip.width = max(tooltip.width, tooltip.min_width)
		if tooltip.max_width:
			tooltip.width = min(tooltip.width, tooltip.max_width)
		if tooltip.min_height:
			tooltip.height = max(tooltip.height, tooltip.min_height)
		if tooltip.max_height:
			tooltip.height = min(tooltip.height, tooltip.max_height)
		tooltip.rect = pygame.Rect(tooltip.x, tooltip.y, tooltip.width, tooltip.height)
	cached = pygame.Surface((tooltip.width, tooltip.height), pygame.SRCALPHA)
	local_rect = pygame.Rect(0, 0, tooltip.width, tooltip.height)
	if not tooltip.hide_background:
		tmp = pygame.Surface(pygame.Rect(local_rect).size, pygame.SRCALPHA)
		pygame.draw.rect(
			tmp, bg_color, tmp.get_rect(),
			border_top_left_radius=tooltip.top_left_corner_radius,
			border_top_right_radius=tooltip.top_right_corner_radius,
			border_bottom_left_radius=tooltip.bottom_left_corner_radius,
			border_bottom_right_radius=tooltip.bottom_right_corner_radius
		)
		tmp.set_alpha(bg_color[3])
		cached.blit(tmp, local_rect)
	icon_offset = local_rect.height if tooltip.icon and not tooltip.suppress_icon else 0
	text_area_left = icon_offset
	text_area_width = local_rect.width-icon_offset
	if tooltip.icon and not tooltip.suppress_icon:
		scaled_icon = pygame.transform.smoothscale(
			tooltip.icon if isinstance(tooltip.icon, pygame.Surface)
			else tooltip.icon.surface, (local_rect.height, local_rect.height)
		)
		cached.blit(scaled_icon, (0, 0))
	if not tooltip.hide_border:
		tmp = pygame.Surface(pygame.Rect(local_rect).size, pygame.SRCALPHA)
		pygame.draw.rect(
			tmp, brd_color, tmp.get_rect(), width=tooltip.border_thickness,
			border_top_left_radius=tooltip.top_left_corner_radius,
			border_top_right_radius=tooltip.top_right_corner_radius,
			border_bottom_left_radius=tooltip.bottom_left_corner_radius,
			border_bottom_right_radius=tooltip.bottom_right_corner_radius
		)
		tmp.set_alpha(brd_color[3])
		cached.blit(tmp, local_rect)
	if not tooltip.hide_text:
		ascent = tooltip.font.get_ascent()
		descent = abs(tooltip.font.get_descent())
		optical_centre_offset = ascent-(ascent-descent)//2
		font_line_h = tooltip.font.get_height()
		effective_line_h = int(max(font_line_h, tooltip.line_spacing))
		if tooltip.alignment=="stretched" and len(tooltip.text)>1 and not tooltip.auto_size:
			total_char_width = sum(tooltip.font.render(char, True, text_color).get_width() for char in tooltip.text)
			available_width = text_area_width-(tooltip.alignment_spacing*2)
			if available_width>total_char_width:
				spacing = (available_width-total_char_width)/(len(tooltip.text)-1)
				current_x = text_area_left+tooltip.alignment_spacing
				char_y = local_rect.centery-optical_centre_offset+ascent
				for char in tooltip.text:
					char_surf = tooltip.font.render(char, True, text_color)
					char_surf.set_alpha(text_color[3])
					surf_top = char_y-tooltip.font.get_ascent()
					surf_top = max(local_rect.top, min(local_rect.bottom-char_surf.get_height(), surf_top))
					cached.blit(char_surf, (current_x, surf_top))
					current_x += char_surf.get_width()+spacing
			else:
				text_surf = tooltip.font.render(tooltip.text, True, text_color)
				text_surf.set_alpha(text_color[3])
				surf_top = local_rect.centery-optical_centre_offset
				surf_top = max(local_rect.top, min(local_rect.bottom-text_surf.get_height(), surf_top))
				cached.blit(
					text_surf,
					text_surf.get_rect(
						centerx=text_area_left+text_area_width//2, top=surf_top
					)
				)
		else:
			lines = tooltip.text.split("\n")
			total_text_height = (len(lines)-1)*effective_line_h+font_line_h
			block_top = local_rect.centery-total_text_height//2
			for i, line in enumerate(lines):
				text_surf = tooltip.font.render(line, True, text_color)
				text_surf.set_alpha(text_color[3])
				surf_top = block_top+i*effective_line_h
				surf_top = max(local_rect.top, min(local_rect.bottom-text_surf.get_height(), surf_top))
				if tooltip.alignment=="left":
					cached.blit(text_surf, (text_area_left+tooltip.alignment_spacing, surf_top))
				elif tooltip.alignment=="right":
					cached.blit(
						text_surf,
						(local_rect.right-tooltip.alignment_spacing-text_surf.get_width(), surf_top)
					)
				else:
					cached.blit(
						text_surf, text_surf.get_rect(centerx=text_area_left+(text_area_width//2), top=surf_top)
					)
	tooltip.original_surface = cached
	tooltip.cached_surface = cached
	tooltip._last_visual_state = (tooltip._pressed, is_hovering)
	tooltip.needs_redraw = False
	tooltip.needs_transform = True