# dialog.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets
"""A dialog widget for pygame."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, TYPE_CHECKING, Unpack

import pygame

from easypygamewidgets import misc
from easypygamewidgets.assets import epw_types, TypeHints
from easypygamewidgets.assets.epw_types import color_type
from easypygamewidgets.assets.theme import _style_dic as sd, _themed
from easypygamewidgets.masterWidgets import Deletable, Screenable, Widget

if TYPE_CHECKING:
	import easypygamewidgets

pygame.init()


# Sliders are bugged (Sliders 'width' and 'height' are miscalculated)
class Dialog(Widget, Screenable, Deletable):
	"""Initializes a dialog widget for pygame."""

	@_themed
	def __init__(self, screen: easypygamewidgets.Screen | None = None, auto_size: bool = True, width: int = 400,
	             height: int = 250, title: str = "Custom Dialog", description: str = "description unavailable",
	             require_value: bool = True,
	             widgets: list[easypygamewidgets.Button | easypygamewidgets.Checkbox | easypygamewidgets.Dialog |
	                           easypygamewidgets.Entry | easypygamewidgets.Label | easypygamewidgets.Slider |
	                           easypygamewidgets.Surface | easypygamewidgets.Timekeeper |
	                           easypygamewidgets.Tooltip] | None = None,
	             widgets_spacing: int = sd["widgets_spacing"], widget_alignment: str = "right",
	             state: str | None = None,
	             active_unpressed_title_color: color_type = sd["active_unpressed_title_color"],
	             disabled_unpressed_title_color: color_type = sd["disabled_unpressed_title_color"],
	             active_hover_title_color: color_type = sd["active_hover_title_color"],
	             disabled_hover_title_color: color_type = sd["disabled_hover_title_color"],
	             active_pressed_title_color: color_type = sd["active_pressed_title_color"],
	             active_unpressed_description_color: color_type = sd["active_unpressed_description_color"],
	             disabled_unpressed_description_color: color_type = sd["disabled_unpressed_description_color"],
	             active_hover_description_color: color_type = sd["active_hover_description_color"],
	             disabled_hover_description_color: color_type = sd["disabled_hover_description_color"],
	             active_pressed_description_color: color_type = sd["active_pressed_description_color"],
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
	             darken_background_with_alpha: int = sd["darken_background_with_alpha"],
	             hide_text: bool = False,
	             hide_background: bool = False,
	             hide_border: bool = False,
	             active_hover_cursor: pygame.Cursor | None = sd["active_hover_cursor"],
	             disabled_hover_cursor: pygame.Cursor | None = sd["disabled_hover_cursor"],
	             active_pressed_cursor: pygame.Cursor | None = sd["active_pressed_cursor"],
	             title_font: pygame.font.Font | pygame.font.SysFont = sd["font"],
	             title_alignment: str = "center", title_alignment_spacing: int = sd["title_alignment_spacing"],
	             description_font: pygame.font.Font | pygame.font.SysFont = sd["font"],
	             description_alignment: str = "center",
	             description_alignment_spacing: int = sd["description_alignment_spacing"],
	             top_left_corner_radius: int = sd["top_left_corner_radius"],
	             top_right_corner_radius: int = sd["top_right_corner_radius"],
	             bottom_left_corner_radius: int = sd["bottom_left_corner_radius"],
	             bottom_right_corner_radius: int = sd["bottom_right_corner_radius"],
	             layer: int = sd["layer"],
	             title_line_spacing: int = sd["title_line_spacing"],
	             description_line_spacing: int = sd["description_line_spacing"],
	             widget_area_padding: int = sd["widget_area_padding"],
	             min_width: int | None = sd["min_width"], max_width: int | None = sd["max_width"],
	             min_height: int | None = sd["min_height"], max_height: int | None = sd["max_height"],
	             alpha_based_collision_system: bool = sd["alpha_based_collision_system"],
	             anchor_x: str = sd["anchor_x"], anchor_y: str = sd["anchor_y"],
	             visible: bool = sd["visible"], data: Any = None) -> None:
		"""
		Initializes a Dialog widget.

		Args:
			screen: The Screen this dialog is attached to. If None, the dialog is created without a parent screen.
			auto_size: If True, width and height are computed from the title, description, and widgets instead of
				using the given width/height.
			width: Fixed dialog width in pixels. Ignored if auto_size is True.
			height: Fixed dialog height in pixels. Ignored if auto_size is True.
			title: The dialog's title text. Supports multi-line text via '\\n'.
			description: The dialog's description text. Supports multi-line text via '\\n'.
			require_value: Whether the dialog requires a value/response before it can be dismissed.
			widgets: A list of Button widgets shown in the dialog's action row, e.g. 'OK'/'Cancel' buttons.
			widgets_spacing: Horizontal spacing in pixels between widgets.
			widget_alignment: Alignment of the widget row: 'left', 'center', 'right', or 'stretched'.
			state: Initial state, 'enabled' or 'disabled'. Defaults to 'enabled' if not given.
			active_unpressed_title_color: RGBA title color while enabled, not pressed, not hovered.
			disabled_unpressed_title_color: RGBA title color while disabled, not hovered.
			active_hover_title_color: RGBA title color while enabled and hovered.
			disabled_hover_title_color: RGBA title color while disabled and hovered.
			active_pressed_title_color: RGBA title color while enabled and pressed.
			active_unpressed_description_color: RGBA description color while enabled, not pressed, not hovered.
			disabled_unpressed_description_color: RGBA description color while disabled, not hovered.
			active_hover_description_color: RGBA description color while enabled and hovered.
			disabled_hover_description_color: RGBA description color while disabled and hovered.
			active_pressed_description_color: RGBA description color while enabled and pressed.
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
			darken_background_with_alpha: Alpha value (0-255) for a full-window black overlay drawn behind this
			hide_text: If True, title and description are not rendered.
			hide_background: If True, the background fill is not rendered.
			hide_border: If True, the border is not rendered.
			active_hover_cursor: Custom cursor shown on hover while enabled.
			disabled_hover_cursor: Custom cursor shown on hover while disabled.
			active_pressed_cursor: Custom cursor shown while pressed.
			title_font: The pygame font used to render the title.
			title_alignment: Title alignment: 'left', 'right', or 'center'.
			title_alignment_spacing: Horizontal padding reserved around the aligned title text.
			description_font: The pygame font used to render the description.
			description_alignment: Description alignment: 'left', 'right', or 'center'.
			description_alignment_spacing: Horizontal padding reserved around the aligned description text.
			top_left_corner_radius: Corner radius in pixels for the top-left corner.
			top_right_corner_radius: Corner radius in pixels for the top-right corner.
			bottom_left_corner_radius: Corner radius in pixels for the bottom-left corner.
			bottom_right_corner_radius: Corner radius in pixels for the bottom-right corner.
			layer: Draw order layer; higher values draw on top. Widgets in the action row are drawn one layer
				above this.
			title_line_spacing: Line height in pixels for multi-line titles.
			description_line_spacing: Line height in pixels for multi-line descriptions.
			widget_area_padding: Padding in pixels around the widget row.
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
			self._visible = visible
			self._screen = None
			if state:
				self._state = state
			else:
				self._state = "enabled"
		self._title = title
		self._description = description
		self._require_value = require_value
		self._widgets = widgets if widgets else []
		if widgets:
			for widget in widgets:
				widget.parent = self
		self._widgets_spacing = widgets_spacing
		self._widget_alignment = widget_alignment
		self._widget_area_padding = widget_area_padding
		self._auto_size = auto_size
		self._title_font = title_font
		self._title_alignment = title_alignment
		self._title_alignment_spacing = title_alignment_spacing
		self._description_font = description_font
		self._description_alignment = description_alignment
		self._description_alignment_spacing = description_alignment_spacing
		self._title_line_spacing = title_line_spacing
		self._description_line_spacing = description_line_spacing
		self._min_width = min_width
		self._max_width = max_width
		self._min_height = min_height
		self._max_height = max_height
		for widget in self._widgets:
			widget.layer = layer+1
		if self._auto_size:
			self._width, self._height = self._compute_auto_size()
		else:
			self._width = width
			self._height = height
		self._active_unpressed_title_color = misc.normalize_color(active_unpressed_title_color)
		self._disabled_unpressed_title_color = misc.normalize_color(disabled_unpressed_title_color)
		self._active_hover_title_color = misc.normalize_color(active_hover_title_color)
		self._disabled_hover_title_color = misc.normalize_color(disabled_hover_title_color)
		self._active_pressed_title_color = misc.normalize_color(active_pressed_title_color)
		self._active_unpressed_description_color = misc.normalize_color(active_unpressed_description_color)
		self._disabled_unpressed_description_color = misc.normalize_color(disabled_unpressed_description_color)
		self._active_hover_description_color = misc.normalize_color(active_hover_description_color)
		self._disabled_hover_description_color = misc.normalize_color(disabled_hover_description_color)
		self._active_pressed_description_color = misc.normalize_color(active_pressed_description_color)
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
		self._darken_background_with_alpha = max(min(darken_background_with_alpha, 255), 0)
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
						f"No custom cursor is used for the dialog '{title}' because it's not a pygame.Cursor object. "
						f"{cursor} is a {type(cursor)}"
					)
				self._cursors[name] = None
		self._top_left_corner_radius = top_left_corner_radius
		self._top_right_corner_radius = top_right_corner_radius
		self._bottom_left_corner_radius = bottom_left_corner_radius
		self._bottom_right_corner_radius = bottom_right_corner_radius
		self._layer = layer
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
		self._cached_darken_surface = None
		_safe_set_linesize(self)
		misc._add_widget(self)

	def _compute_auto_size(self) -> tuple[int, int]:
		"""
		Computes the dialog's width and height needed to fit the title, description, and widgets.

		Returns:
			tuple[int, int]: The computed (width, height) in pixels.
		"""
		_safe_set_linesize(self)
		title_font = self._title_font
		description_font = self._description_font
		title_lines = self._title.split("\n")
		total_title_w = 0
		title_text_h = title_font.get_height()
		title_effective_line_h = max(title_text_h, self._title_line_spacing)
		for line in title_lines:
			lw = title_font.size(line)[0]
			if lw>total_title_w:
				total_title_w = lw
		total_title_h = (len(title_lines)-1)*title_effective_line_h+title_text_h
		desc_lines = self._description.split("\n")
		total_desc_w = 0
		desc_text_h = description_font.get_height()
		desc_effective_line_h = max(desc_text_h, self._description_line_spacing)
		for line in desc_lines:
			lw = description_font.size(line)[0]
			if lw>total_desc_w:
				total_desc_w = lw
		total_desc_h = (len(desc_lines)-1)*desc_effective_line_h+desc_text_h
		if self._widgets:
			widgets_total_w = (sum(w.width for w in self._widgets)
			                   +self._widgets_spacing*(len(self._widgets)-1))
			widgets_max_h = max(w.height for w in self._widgets)
		else:
			widgets_total_w = 0
			widgets_max_h = 0
		pad = self._widget_area_padding
		computed_w = max(
			total_title_w+self._title_alignment_spacing,
			total_desc_w+self._description_alignment_spacing, widgets_total_w+pad*2
		)
		if self._min_width is not None:
			computed_w = max(computed_w, self._min_width)
		if self._max_width is not None:
			computed_w = min(computed_w, self._max_width)
		gap = 12
		computed_h = total_title_h+gap+total_desc_h+gap+(widgets_max_h+pad if self._widgets else 0)+pad
		if self._min_height is not None:
			computed_h = max(computed_h, self._min_height)
		if self._max_height is not None:
			computed_h = min(computed_h, self._max_height)
		return computed_w, computed_h

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
	def title(self):
		return self._title

	@title.setter
	def title(self, value):
		self._title = value

	@property
	def description(self):
		return self._description

	@description.setter
	def description(self, value):
		self._description = value

	@property
	def require_value(self):
		return self._require_value

	@require_value.setter
	def require_value(self, value):
		self._require_value = value

	@property
	def widgets(self):
		return self._widgets

	@widgets.setter
	def widgets(self, value):
		self._widgets = value if value is not None else []

	@property
	def widgets_spacing(self):
		return self._widgets_spacing

	@widgets_spacing.setter
	def widgets_spacing(self, value):
		self._widgets_spacing = value

	@property
	def widget_alignment(self):
		return self._widget_alignment

	@widget_alignment.setter
	def widget_alignment(self, value):
		self._widget_alignment = value

	@property
	def widget_area_padding(self):
		return self._widget_area_padding

	@widget_area_padding.setter
	def widget_area_padding(self, value):
		self._widget_area_padding = value

	@property
	def active_unpressed_title_color(self):
		return self._active_unpressed_title_color

	@active_unpressed_title_color.setter
	def active_unpressed_title_color(self, value):
		self._active_unpressed_title_color = misc.normalize_color(value)

	@property
	def disabled_unpressed_title_color(self):
		return self._disabled_unpressed_title_color

	@disabled_unpressed_title_color.setter
	def disabled_unpressed_title_color(self, value):
		self._disabled_unpressed_title_color = misc.normalize_color(value)

	@property
	def active_hover_title_color(self):
		return self._active_hover_title_color

	@active_hover_title_color.setter
	def active_hover_title_color(self, value):
		self._active_hover_title_color = misc.normalize_color(value)

	@property
	def disabled_hover_title_color(self):
		return self._disabled_hover_title_color

	@disabled_hover_title_color.setter
	def disabled_hover_title_color(self, value):
		self._disabled_hover_title_color = misc.normalize_color(value)

	@property
	def active_pressed_title_color(self):
		return self._active_pressed_title_color

	@active_pressed_title_color.setter
	def active_pressed_title_color(self, value):
		self._active_pressed_title_color = misc.normalize_color(value)

	@property
	def active_unpressed_description_color(self):
		return self._active_unpressed_description_color

	@active_unpressed_description_color.setter
	def active_unpressed_description_color(self, value):
		self._active_unpressed_description_color = misc.normalize_color(value)

	@property
	def disabled_unpressed_description_color(self):
		return self._disabled_unpressed_description_color

	@disabled_unpressed_description_color.setter
	def disabled_unpressed_description_color(self, value):
		self._disabled_unpressed_description_color = misc.normalize_color(value)

	@property
	def active_hover_description_color(self):
		return self._active_hover_description_color

	@active_hover_description_color.setter
	def active_hover_description_color(self, value):
		self._active_hover_description_color = misc.normalize_color(value)

	@property
	def disabled_hover_description_color(self):
		return self._disabled_hover_description_color

	@disabled_hover_description_color.setter
	def disabled_hover_description_color(self, value):
		self._disabled_hover_description_color = misc.normalize_color(value)

	@property
	def active_pressed_description_color(self):
		return self._active_pressed_description_color

	@active_pressed_description_color.setter
	def active_pressed_description_color(self, value):
		self._active_pressed_description_color = misc.normalize_color(value)

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
	def darken_background_with_alpha(self):
		return self._darken_background_with_alpha

	@darken_background_with_alpha.setter
	def darken_background_with_alpha(self, value):
		self._darken_background_with_alpha = max(min(value, 255), 0)
		self._needs_redraw = True

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
	def title_font(self):
		return self._title_font

	@title_font.setter
	def title_font(self, value):
		self._title_font = value
		self._title_font.set_linesize(self._title_line_spacing)

	@property
	def title_alignment(self):
		return self._title_alignment

	@title_alignment.setter
	def title_alignment(self, value):
		self._title_alignment = value

	@property
	def title_alignment_spacing(self):
		return self._title_alignment_spacing

	@title_alignment_spacing.setter
	def title_alignment_spacing(self, value):
		self._title_alignment_spacing = value

	@property
	def description_font(self):
		return self._description_font

	@description_font.setter
	def description_font(self, value):
		self._description_font = value
		self._description_font.set_linesize(self._description_line_spacing)

	@property
	def description_alignment(self):
		return self._description_alignment

	@description_alignment.setter
	def description_alignment(self, value):
		self._description_alignment = value

	@property
	def description_alignment_spacing(self):
		return self._description_alignment_spacing

	@description_alignment_spacing.setter
	def description_alignment_spacing(self, value):
		self._description_alignment_spacing = value

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
		for w in self._widgets:
			w.layer = value+1
		misc._resort_layers()

	@property
	def title_line_spacing(self):
		return self._title_line_spacing

	@title_line_spacing.setter
	def title_line_spacing(self, value):
		self._title_line_spacing = value
		self._title_font.set_linesize(value)

	@property
	def description_line_spacing(self):
		return self._description_line_spacing

	@description_line_spacing.setter
	def description_line_spacing(self, value):
		self._description_line_spacing = value
		self._description_font.set_linesize(value)

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
	def cached_darken_surface(self):
		return self._cached_darken_surface

	@cached_darken_surface.setter
	def cached_darken_surface(self, value):
		self._cached_darken_surface = value

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

	def clone(self) -> Dialog:
		"""
		Creates a deep copy of this dialog.

		Returns:
			Dialog (Dialog): The cloned dialog instance. Its widget row is cleared, since cloned action widgets
				would otherwise still reference the original dialog.
		"""
		copied_widget = super().clone()
		copied_widget._widgets = []
		if copied_widget._auto_size:
			copied_widget._width, copied_widget._height = copied_widget.compute_auto_size()
			copied_widget._rect = pygame.Rect(
				copied_widget._x, copied_widget._y,
				copied_widget._width, copied_widget._height
			)
		return copied_widget

	def configure(self, **kwargs: Unpack[TypeHints.DialogConfig]) -> Dialog:
		"""
		Updates one or more of the dialog's attributes.

		Args:
			**kwargs: Dialog attributes to update as defined in TypeHints.DialogConfig

		Returns:
			Dialog (Dialog): This dialog instance to allow method chaining.
		"""
		for key, value in kwargs.items():
			setattr(self, key, value)
		self._needs_redraw = True
		self._needs_transform = True
		if any(
				k in kwargs for k in (
						'auto_size', 'x', 'y', 'width', 'height', 'title', 'description', 'title_font',
						'description_font', 'max_width', 'min_width', 'max_height', 'min_height',
						'title_line_spacing', 'description_line_spacing', 'title_alignment_spacing',
						'description_alignment_spacing', 'widgets', 'widgets_spacing',
						'widget_area_padding', 'anchor_x', 'anchor_y'
				)
		):
			if self._auto_size:
				self._width, self._height = self._compute_auto_size()
			self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
		if any(
				k in kwargs for k in (
						'title_line_spacing', 'title_font', 'description_font',
						'description_line_spacing'
				)
		):
			_safe_set_linesize(self)
		return self

	def config(self, **kwargs: Unpack[TypeHints.DialogConfig]) -> Dialog:
		"""
		Updates one or more of the dialog's attributes.

		Args:
			**kwargs: Dialog attributes to update as defined in TypeHints.DialogConfig

		Returns:
			Dialog (Dialog): This dialog instance to allow method chaining.
		"""
		return self.configure(**kwargs)

	def scale(self, value: int | float = 1, frames_to_finish: int = 1) -> Dialog:
		"""
		Scale the dialog by a factor. It's only a visual scale so upscaling could look pixelated.

		Args:
			 value (int|float): the scale factor
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Dialog (Dialog): This dialog instance to allow method chaining.
		"""
		if frames_to_finish<=0:
			frames_to_finish = 1
		self._target_scale = value
		self._scale_step = (self._target_scale-self._current_scale)/frames_to_finish
		self._update_animation()
		return self

	def rotate(self, value: int | float = 0, frames_to_finish: int = 1) -> Dialog:
		"""
		Rotate the dialog by a degree.

		Args:
			 value (int|float): the rotation degree
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Dialog (Dialog): This dialog instance to allow method chaining.
		"""
		if frames_to_finish<=0:
			frames_to_finish = 1
		self._target_rotation = value
		self._rotation_step = (self._target_rotation-self._current_rotation)/frames_to_finish
		self._update_animation()
		return self

	def rotozoom(self, scale: int | float = 1, rotation: int | float = 0, frames_to_finish: int = 1) -> Dialog:
		"""
		Rotate the dialog by a degree and scale it.

		Args:
			 scale (int|float): the scale factor
			 rotation (int|float): the rotation degree
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Dialog (Dialog): This dialog instance to allow method chaining.
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

	def offset(self, value: Iterable[int] = (0, 0), frames_to_finish: int = 1) -> Dialog:
		"""
		Offset the dialog by an x and y value.

		Args:
			 value: an iterable thing with two values. The first being the x and the second the y offset.
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Dialog (Dialog): This dialog instance to allow method chaining.
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
		for i in range(2):
			if self._current_offset[i]!=self._target_offset[i]:
				if abs(self._current_offset[i]-self._target_offset[i])<=abs(self._offset_step[i]):
					self._current_offset[i] = float(self._target_offset[i])
				else:
					self._current_offset[i] += self._offset_step[i]
		if scale_changed or rotation_changed:
			self._needs_transform = True

	def _draw(self, surface: pygame.Surface) -> None:
		"""
		Internally used to draw the dialog.

		Args:
			surface (pygame.Surface): The surface to draw the dialog on.
		"""
		if not self._alive or not self._visible:
			return
		mouse_pos = pygame.mouse.get_pos()
		is_hovering = misc._is_point_over_widget(self, mouse_pos)

		if (self._cached_darken_surface is None or self._cached_darken_surface.get_size()!=surface.get_size() or
				self._needs_redraw):
			self._cached_darken_surface = pygame.Surface(surface.get_size())
			self._cached_darken_surface.fill((0, 0, 0))
			self._cached_darken_surface.set_alpha(self.darken_background_with_alpha)

		if self._visible and self._darken_background_with_alpha>0:
			surface.blit(self._cached_darken_surface, (0, 0))

		current_visual_state = (self._pressed, is_hovering)
		if self._needs_redraw or self._last_visual_state!=current_visual_state:
			_render_dialog_surface(self, is_hovering)
		if self._needs_transform:
			if self._current_scale!=1 or self._current_rotation!=0:
				new_width = int(self._original_surface.get_width()*self._current_scale)
				new_height = int(self._original_surface.get_height()*self._current_scale)
				if new_width>0 and new_height>0:
					if self._use_rotozoom:
						self._cached_surface = pygame.transform.rotozoom(
							self._original_surface, self._current_rotation, self._current_scale
						)
					else:
						scaled_surface = pygame.transform.smoothscale(
							self._original_surface, (new_width, new_height)
						)
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
				cursor_key = "active_pressed" if self._pressed else "active_hover"
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


def _safe_set_linesize(dialog: Dialog) -> None:
	"""
	Internally used to sync the title and description fonts' linesize with the
	dialog's configured line spacing.

	Args:
		dialog (Dialog): The dialog whose fonts should be updated.
	"""
	dialog.title_font.set_linesize(dialog.title_line_spacing)
	dialog.description_font.set_linesize(dialog.description_line_spacing)


def _render_text_block(surface: pygame.Surface, text: str, font_obj: pygame.font.Font | pygame.font.SysFont,
                       color: tuple[int, int, int, int], alignment: str, alignment_spacing: int,
                       line_spacing: int, block_rect: pygame.Rect) -> None:
	"""
	Internally used to draw a block of (possibly multi-line) text centered vertically
	within a rect.

	Args:
		surface (pygame.Surface): The surface to draw the text on.
		text (str): The text to draw. Supports multi-line text via '\\n'.
		font_obj (pygame.font.Font | pygame.font.SysFont): The font used to render the text.
		color (tuple[int, int, int, int]): The RGBA text color.
		alignment (str): Text alignment: 'left', 'right', or 'center'.
		alignment_spacing (int): Horizontal padding reserved around the aligned text.
		line_spacing (int): Line height in pixels for multi-line text.
		block_rect (pygame.Rect): The rect the text block is centered within.
	"""
	lines = text.split("\n")
	font_line_h = font_obj.get_height()
	effective_line_h = max(font_line_h, line_spacing)
	total_text_h = (len(lines)-1)*effective_line_h+font_line_h
	block_top = block_rect.centery-total_text_h//2
	for i, line in enumerate(lines):
		text_surf = font_obj.render(line, True, color)
		text_surf.set_alpha(color[3])
		line_top = block_top+i*effective_line_h
		line_top = max(block_rect.top, min(block_rect.bottom-text_surf.get_height(), line_top))
		if alignment=="left":
			surface.blit(text_surf, (block_rect.left+alignment_spacing//2, line_top))
		elif alignment=="right":
			surface.blit(
				text_surf,
				(block_rect.right-alignment_spacing//2-text_surf.get_width(), line_top)
			)
		else:
			surface.blit(text_surf, text_surf.get_rect(centerx=block_rect.centerx, top=line_top))


def _render_dialog_surface(dialog: Dialog, is_hovering: bool) -> None:
	"""
	Internally used to draw the dialog surface once and cache it.

	Args:
		dialog (Dialog): the widget to render the surface for
		is_hovering (bool): whether the mouse is hovering over the widget
	"""
	if dialog.state=="enabled":
		if dialog.pressed and is_hovering:
			title_color = dialog.active_pressed_title_color
			desc_color = dialog.active_pressed_description_color
			bg_color = dialog.active_pressed_background_color
			brd_color = dialog.active_pressed_border_color
		elif is_hovering:
			title_color = dialog.active_hover_title_color
			desc_color = dialog.active_hover_description_color
			bg_color = dialog.active_hover_background_color
			brd_color = dialog.active_hover_border_color
		else:
			title_color = dialog.active_unpressed_title_color
			desc_color = dialog.active_unpressed_description_color
			bg_color = dialog.active_unpressed_background_color
			brd_color = dialog.active_unpressed_border_color
	else:
		if is_hovering:
			title_color = dialog.disabled_hover_title_color
			desc_color = dialog.disabled_hover_description_color
			bg_color = dialog.disabled_hover_background_color
			brd_color = dialog.disabled_hover_border_color
		else:
			title_color = dialog.disabled_unpressed_title_color
			desc_color = dialog.disabled_unpressed_description_color
			bg_color = dialog.disabled_unpressed_background_color
			brd_color = dialog.disabled_unpressed_border_color
	_safe_set_linesize(dialog)
	base_width = dialog.width
	base_height = dialog.height
	cached = pygame.Surface((base_width, base_height), pygame.SRCALPHA)
	local_rect = pygame.Rect(0, 0, base_width, base_height)
	if not dialog.hide_background:
		pygame.draw.rect(
			cached, bg_color, local_rect,
			border_top_left_radius=dialog.top_left_corner_radius,
			border_top_right_radius=dialog.top_right_corner_radius,
			border_bottom_left_radius=dialog.bottom_left_corner_radius,
			border_bottom_right_radius=dialog.bottom_right_corner_radius
		)
	if not dialog.hide_border:
		pygame.draw.rect(
			cached, brd_color, local_rect, width=dialog.border_thickness,
			border_top_left_radius=dialog.top_left_corner_radius,
			border_top_right_radius=dialog.top_right_corner_radius,
			border_bottom_left_radius=dialog.bottom_left_corner_radius,
			border_bottom_right_radius=dialog.bottom_right_corner_radius
		)
	gap = 12
	pad = dialog.widget_area_padding
	if dialog.widgets:
		widgets_max_h = max(w.height for w in dialog.widgets)
		widget_row_h = widgets_max_h+pad
	else:
		widget_row_h = 0
	title_font = dialog.title_font
	title_text_h = title_font.get_height()
	title_lines = dialog.title.split("\n")
	title_eff_lh = max(title_text_h, dialog.title_line_spacing)
	total_title_h = (len(title_lines)-1)*title_eff_lh+title_text_h
	desc_font = dialog.description_font
	desc_text_h = desc_font.get_height()
	desc_lines = dialog.description.split("\n")
	desc_eff_lh = max(desc_text_h, dialog.description_line_spacing)
	total_desc_h = (len(desc_lines)-1)*desc_eff_lh+desc_text_h
	content_h = total_title_h+gap+total_desc_h+gap+widget_row_h
	content_top = (base_height-content_h)//2
	title_rect = pygame.Rect(local_rect.left, content_top, local_rect.width, total_title_h)
	desc_top = content_top+total_title_h+gap
	desc_rect = pygame.Rect(local_rect.left, desc_top, local_rect.width, total_desc_h)
	if not dialog.hide_text:
		_render_text_block(
			cached, dialog.title, title_font, title_color, dialog.title_alignment,
			dialog.title_alignment_spacing, dialog.title_line_spacing, title_rect
		)
		_render_text_block(
			cached, dialog.description, desc_font, desc_color, dialog.description_alignment,
			dialog.description_alignment_spacing, dialog.description_line_spacing, desc_rect
		)
	if dialog.widgets:
		row_top = desc_top+total_desc_h+gap
		divider_y = row_top-gap//2
		if not dialog.hide_text:
			divider_color = (brd_color[0], brd_color[1], brd_color[2], brd_color[3]//2) if brd_color else None
			if divider_color:
				pygame.draw.line(
					cached, divider_color, (local_rect.left+pad, divider_y),
					(local_rect.right-pad, divider_y), 1
				)
		widget_top = row_top+(pad//2)
		widgets_total_w = (sum(w.width for w in dialog.widgets)
		                   +dialog.widgets_spacing*(len(dialog.widgets)-1))
		available_w = local_rect.width-pad*2
		dialog_screen_offset_x, dialog_screen_offset_y = 0, 0
		if dialog.screen:
			dialog_screen_offset_x, dialog_screen_offset_y = dialog.screen.x, dialog.screen.y
		dialog_screen_offset_x += round(dialog.current_offset[0])
		dialog_screen_offset_y += round(dialog.current_offset[1])
		alignment = dialog.widget_alignment
		if alignment=="stretched" and len(dialog.widgets)>1 and available_w>widgets_total_w:
			spacing = (available_w-sum(w.width for w in dialog.widgets))/(len(dialog.widgets)-1)
			cursor_x = local_rect.left+pad
			for w in dialog.widgets:
				w.anchor("left", "top")
				w.place(dialog_screen_offset_x+cursor_x, dialog_screen_offset_y+widget_top)
				cursor_x += w.width+spacing
		else:
			if alignment=="left":
				cursor_x = local_rect.left+pad
			elif alignment=="center":
				cursor_x = local_rect.left+(local_rect.width-widgets_total_w)//2
			elif alignment=="right":
				cursor_x = local_rect.right-pad-widgets_total_w
			elif alignment=="stretched":
				cursor_x = local_rect.right-pad-widgets_total_w
			else:
				raise ValueError(f"Invalid widget_alignment in {dialog.title} dialog: {alignment!r}")
			for w in dialog.widgets:
				w.anchor("left", "top")
				w.place(dialog_screen_offset_x+cursor_x, dialog_screen_offset_y+widget_top)
				cursor_x += w.width+dialog.widgets_spacing
	dialog.original_surface = cached
	dialog.cached_surface = cached
	dialog._last_visual_state = (dialog.pressed, is_hovering)
	dialog._needs_redraw = False
	dialog._needs_transform = True