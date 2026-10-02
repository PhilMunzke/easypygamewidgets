# screen.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets
"""A screen container widget for pygame used to group and grid-layout other widgets."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, TYPE_CHECKING, Unpack

import pygame

from easypygamewidgets import misc
from easypygamewidgets.assets import epw_types, TypeHints
from easypygamewidgets.assets.theme import _style_dic as sd
from easypygamewidgets.masterWidgets import Deletable, Widget

if TYPE_CHECKING:
	import easypygamewidgets

pygame.init()


# PERFECTION
# missing three animations ❔

class Screen(Widget, Deletable):
	"""Initializes a screen container widget for pygame used to group and grid-layout other widgets."""

	def __init__(self, auto_size: bool = True, width: int | None = None, height: int | None = None,
	             min_width: int | None = sd["min_width"], max_width: int | None = sd["max_width"],
	             min_height: int | None = sd["min_height"],
	             max_height: int | None = sd["max_height"], fill_width: bool = False, fill_height: bool = False,
	             active_hover_cursor: pygame.Cursor | None = sd["active_hover_cursor"],
	             disabled_hover_cursor: pygame.Cursor | None = sd["disabled_hover_cursor"],
	             active_pressed_cursor: pygame.Cursor | None = sd["active_pressed_cursor"],
	             widgets: list[easypygamewidgets.Button | easypygamewidgets.Checkbox | easypygamewidgets.Dialog |
	                           easypygamewidgets.Entry | easypygamewidgets.Label | easypygamewidgets.Slider |
	                           easypygamewidgets.Surface | easypygamewidgets.Timekeeper |
	                           easypygamewidgets.Tooltip] | None = None,
	             darken_background_with_alpha: int = 0,
	             alpha_based_collision_system: bool = sd["alpha_based_collision_system"],
	             anchor_x: str = sd["anchor_x"], anchor_y: str = sd["anchor_y"],
	             visible: bool = False, state: str = "enabled", x: int = 0,
	             y: int = 0, layer: int = sd["layer"], ignore_empty_cells: bool = False,
	             row_spacing: int = sd["row_spacing"],
	             column_spacing: int = sd["column_spacing"], data: Any = None) -> None:
		"""
		Initializes a Screen widget.

		Args:
			auto_size: If True, width and height are computed from the gridded widgets instead of using the
				given width/height. Ignored if fill_width or fill_height is True.
			width: Fixed screen width in pixels. Ignored if auto_size is True.
			height: Fixed screen height in pixels. Ignored if auto_size is True.
			min_width: Minimum width in pixels when auto_size is True.
			max_width: Maximum width in pixels when auto_size is True.
			min_height: Minimum height in pixels when auto_size is True.
			max_height: Maximum height in pixels when auto_size is True.
			fill_width: If True, the screen always fills the full window width.
			fill_height: If True, the screen always fills the full window height.
			active_hover_cursor: Custom cursor shown on hover while enabled.
			disabled_hover_cursor: Custom cursor shown on hover while disabled.
			active_pressed_cursor: Custom cursor shown while pressed.
			widgets: A list of widgets already attached to this screen.
			darken_background_with_alpha: Alpha value (0-255) for a full-window black overlay drawn behind this
				screen while visible. 0 disables the overlay.
			alpha_based_collision_system: Use a pixel alpha test to check for collisions instead of math calculations.
			anchor_x: Horizontal anchor point: 'left', 'center', or 'right'.
			anchor_y: Vertical anchor point: 'top', 'center', or 'bottom'.
			visible: Initial visibility. Defaults to False.
			state: Initial state, 'enabled' or 'disabled'.
			x: Initial x position in pixels.
			y: Initial y position in pixels.
			layer: Draw order layer; higher values draw on top.
			ignore_empty_cells: If True, empty rows/columns in the grid are collapsed instead of taking up space.
			row_spacing: Vertical spacing in pixels between grid rows.
			column_spacing: Horizontal spacing in pixels between grid columns.
			data: Arbitrary user data attached to the widget.

		Raises:
			ValueError: If a *_cursor argument is given but is not a pygame.Cursor instance.
		"""
		super().__init__()
		self._bindings = {}
		self._row_spacing = row_spacing
		self._column_spacing = column_spacing
		self._auto_size = auto_size
		if auto_size and not fill_width and not fill_height:
			self._width = 0
			self._height = 0
		else:
			self._auto_size = False
			self._width = width if width is not None else (misc._pg.get_width())
			self._height = height if height is not None else (misc._pg.get_height())
		self._fill_width = fill_width
		self._fill_height = fill_height
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
						f"No custom cursor is used for this screen because it's not a pygame.Cursor object. "
						f"{cursor} is a {type(cursor)}"
					)
				self._cursors[name] = None
		self._widgets = widgets if widgets is not None else []
		self._darken_background_with_alpha = max(min(darken_background_with_alpha, 255), 0)
		self._min_width = min_width
		self._max_width = max_width
		self._min_height = min_height
		self._max_height = max_height
		self._alpha_based_collision_system = alpha_based_collision_system
		self._anchor_x = anchor_x
		self._anchor_y = anchor_y
		self._visible = visible
		self._state = state
		self._x = x
		self._y = y
		self._layer = layer
		self._ignore_empty_cells = ignore_empty_cells
		self._data = data
		self._last_pg_size = None
		self._alive = True
		self._pressed = False
		self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
		self._original_cursor = None
		self._is_hovered = False
		self._target_offset = (0, 0)
		self._current_offset = [0, 0]
		self._offset_step = [0, 0]

		misc._add_widget(self)

		self.update_widget_state(True, True)

	@property
	def bindings(self):
		return self._bindings

	@bindings.setter
	def bindings(self, value):
		self._bindings = value

	@property
	def auto_size(self):
		return self._auto_size

	@auto_size.setter
	def auto_size(self, value):
		self._auto_size = value
		self.recalculate_grid()

	@property
	def width(self):
		return self._width

	@width.setter
	def width(self, value):
		self._fill_width = value is None
		self._width = value if value is not None else (misc._pg.get_width())
		if not self._auto_size:
			self.recalculate_grid()

	@property
	def height(self):
		return self._height

	@height.setter
	def height(self, value):
		self._fill_height = value is None
		self._height = value if value is not None else (misc._pg.get_height())
		if not self._auto_size:
			self.recalculate_grid()

	@property
	def row_spacing(self):
		return self._row_spacing

	@row_spacing.setter
	def row_spacing(self, value):
		self._row_spacing = value
		if not self._auto_size:
			self.recalculate_grid()

	@property
	def column_spacing(self):
		return self._column_spacing

	@column_spacing.setter
	def column_spacing(self, value):
		self._column_spacing = value
		if not self._auto_size:
			self.recalculate_grid()

	@property
	def min_width(self):
		return self._min_width

	@min_width.setter
	def min_width(self, value):
		self._min_width = value
		if not self._auto_size:
			self.recalculate_grid()

	@property
	def max_width(self):
		return self._max_width

	@max_width.setter
	def max_width(self, value):
		self._max_width = value
		if not self._auto_size:
			self.recalculate_grid()

	@property
	def min_height(self):
		return self._min_height

	@min_height.setter
	def min_height(self, value):
		self._min_height = value
		if not self._auto_size:
			self.recalculate_grid()

	@property
	def max_height(self):
		return self._max_height

	@max_height.setter
	def max_height(self, value):
		self._max_height = value
		if not self._auto_size:
			self.recalculate_grid()

	@property
	def fill_width(self):
		return self._fill_width

	@fill_width.setter
	def fill_width(self, value):
		self._fill_width = value
		self._auto_size = False
		self.recalculate_grid()

	@property
	def fill_height(self):
		return self._fill_height

	@fill_height.setter
	def fill_height(self, value):
		self._fill_height = value
		self._auto_size = False
		self.recalculate_grid()

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
	def widgets(self):
		return self._widgets

	@widgets.setter
	def widgets(self, value):
		self._widgets = value

	@property
	def darken_background_with_alpha(self):
		return self._darken_background_with_alpha

	@darken_background_with_alpha.setter
	def darken_background_with_alpha(self, value):
		self._darken_background_with_alpha = value

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
	def visible(self):
		return self._visible

	@visible.setter
	def visible(self, value):
		self._visible = value

	@property
	def state(self):
		return self._state

	@state.setter
	def state(self, value):
		self._state = value

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
	def layer(self):
		return self._layer

	@layer.setter
	def layer(self, value):
		self._layer = value

	@property
	def ignore_empty_cells(self):
		return self._ignore_empty_cells

	@ignore_empty_cells.setter
	def ignore_empty_cells(self, value):
		self._ignore_empty_cells = value
		self.recalculate_grid()

	@property
	def data(self):
		return self._data

	@data.setter
	def data(self, value):
		self._data = value

	@property
	def last_pg_size(self):
		return self._last_pg_size

	@last_pg_size.setter
	def last_pg_size(self, value):
		self._last_pg_size = value

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
		self._auto_size = False
		self.recalculate_grid()

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

	def configure(self, **kwargs: Unpack[TypeHints.ScreenConfig]) -> "Screen":
		"""
		Updates one or more of the screen's attributes.

		Args:
			**kwargs: Screen attributes to update as defined in TypeHints.ScreenConfig

		Returns:
			Screen (Screen): This screen instance to allow method chaining.
		"""
		for key, value in kwargs.items():
			setattr(self, key, value)
		return self

	def config(self, **kwargs: Unpack[TypeHints.ScreenConfig]) -> "Screen":
		"""
		Updates one or more of the screen's attributes.

		Args:
			**kwargs: Screen attributes to update as defined in TypeHints.ScreenConfig

		Returns:
			Screen (Screen): This screen instance to allow method chaining.
		"""
		return self.configure(**kwargs)

	def offset(self, value: Iterable[int] = (0, 0), frames_to_finish: int = 1) -> "Screen":
		"""
		Offset the screen by an x and y value.

		Args:
			 value: an iterable thing with two values. The first being the x and the second the y offset.
			 frames_to_finish (int): the number of frames to finish the animation

		Returns:
			Screen (Screen): This screen instance to allow method chaining.
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
		for x in range(2):
			if self._current_offset[x]!=self._target_offset[x]:
				if abs(self._current_offset[x]-self._target_offset[x])<=abs(self._offset_step[x]):
					self._current_offset[x] = float(self._target_offset[x])
				else:
					self._current_offset[x] += self._offset_step[x]

	def add_widget(self, widget: easypygamewidgets.Button | easypygamewidgets.Checkbox | easypygamewidgets.Dialog |
	                             easypygamewidgets.Entry | easypygamewidgets.Label | easypygamewidgets.Slider |
	                             easypygamewidgets.Surface | easypygamewidgets.Timekeeper | easypygamewidgets.Tooltip
	               ) -> "Screen":
		"""
		Attaches a widget to this screen. If the widget is already attached to a different screen, it's moved
		over.

		Args:
			widget: The widget to add.

		Returns:
			Screen (Screen): This screen instance to allow method chaining.
		"""
		if widget in self.widgets:
			widget.screen.remove_widget(widget)
		self.widgets.append(widget)
		widget.screen = self
		widget.visible = self._visible
		widget.state = self._state
		return self

	def remove_widget(self, widget: easypygamewidgets.Button | easypygamewidgets.Checkbox | easypygamewidgets.Dialog |
	                                easypygamewidgets.Entry | easypygamewidgets.Label | easypygamewidgets.Slider |
	                                easypygamewidgets.Surface | easypygamewidgets.Timekeeper | easypygamewidgets.Tooltip
	                  ) -> "Screen":
		"""
		Detaches a widget from this screen and, if it was placed in the grid, recalculates the grid.

		Args:
			widget: The widget to remove.

		Returns:
			Screen (Screen): This screen instance to allow method chaining.
		"""
		if widget in self.widgets:
			self.widgets.remove(widget)
		if hasattr(widget, "_grid_row"):
			self.recalculate_grid()
		return self

	def show(self) -> "Screen":
		"""
		Shows this screen and its widgets.

		Returns:
			Screen (Screen): This screen instance to allow method chaining.
		"""
		self.visible = True
		self.update_widget_state(True, False)
		return self

	def hide(self) -> "Screen":
		"""
		Hides this screen and its widgets.

		Returns:
			Screen (Screen): This screen instance to allow method chaining.
		"""
		self.visible = False
		self.update_widget_state(True, False)
		return self

	def enable(self) -> "Screen":
		"""
		Enables this screen and its widgets.

		Returns:
			Screen (Screen): This screen instance to allow method chaining.
		"""
		self._state = "enabled"
		self.update_widget_state(False, True)
		return self

	def disable(self) -> "Screen":
		"""
		Disables this screen and its widgets.

		Returns:
			Screen (Screen): This screen instance to allow method chaining.
		"""
		self._state = "disabled"
		self.update_widget_state(False, True)
		return self

	def update_widget_state(self, update_visibility: bool = True, update_state: bool = True) -> None:
		"""
		Updates the visibility and/or state of the screens widgets to match what the screen has set.

		Args:
			update_visibility: If True, sets every widget's visible attribute to match this screen's.
			update_state: If True, sets every widget's state attribute to match this screen's.
		"""
		for widget in self._widgets:
			if update_visibility:
				if self._visible:
					widget.configure(visible=True)
				else:
					widget.configure(visible=False)
			if update_state:
				if self._state=="enabled":
					widget.configure(state="enabled")
				else:
					widget.configure(state="disabled")

	def delete(self) -> None:
		"""Delete this screen AND all the widgets attached to it."""
		if self in misc._all_widgets:
			misc._all_widgets.remove(self)
		for widget in self._widgets:
			widget.set_screen(None)
			widget.delete()
		self.widgets.clear()

	def recalculate_grid(self) -> None:
		"""Internally used to recompute the position and size of every gridded widget on this screen."""
		grid_widgets = [w for w in self._widgets if hasattr(w, "_grid_row")]
		if not grid_widgets: return
		occupied_rows = []
		occupied_cols = []
		for w in grid_widgets:
			occupied_rows.extend(range(w._grid_row, w._grid_row+w._grid_rowspan))
			occupied_cols.extend(range(w._grid_column, w._grid_column+w._grid_columnspan))
		sorted_rows = sorted(occupied_rows)
		sorted_cols = sorted(occupied_cols)
		max_row = sorted_rows[-1]+1
		max_col = sorted_cols[-1]+1
		if self._ignore_empty_cells:
			row_map = {orig: i for i, orig in enumerate(sorted_rows)}
			col_map = {orig: i for i, orig in enumerate(sorted_cols)}
			num_rows = len(sorted_rows)
			num_cols = len(sorted_cols)
		else:
			row_map = {i: i for i in range(max_row)}
			col_map = {i: i for i in range(max_col)}
			num_rows = max_row
			num_cols = max_col
		if num_rows==0 or num_cols==0: return
		if self._auto_size:
			col_widths = [0]*num_cols
			row_heights = [0]*num_rows
			for w in grid_widgets:
				if w._grid_columnspan==1:
					c = col_map.get(w._grid_column)
					if c is not None:
						col_widths[c] = max(col_widths[c], w.width)
				if w._grid_rowspan==1:
					r = row_map.get(w._grid_row)
					if r is not None:
						row_heights[r] = max(row_heights[r], w.height)
			for w in grid_widgets:
				if w._grid_columnspan>1:
					cols = [col_map[c] for c in range(w._grid_column, w._grid_column+w._grid_columnspan) if
					        c in col_map]
					if cols:
						current = sum(col_widths[c] for c in cols)+self._column_spacing*(len(cols)-1)
						if w.width>current:
							share = (w.width-current)/len(cols)
							for c in cols:
								col_widths[c] += share
				if w._grid_rowspan>1:
					rows = [row_map[r] for r in range(w._grid_row, w._grid_row+w._grid_rowspan) if r in row_map]
					if rows:
						current = sum(row_heights[r] for r in rows)+self._row_spacing*(len(rows)-1)
						if w.height>current:
							share = (w.height-current)/len(rows)
							for r in rows:
								row_heights[r] += share
			self._width = int(sum(col_widths)+self._column_spacing*(num_cols-1))
			self._height = int(sum(row_heights)+self._row_spacing*(num_rows-1))
			if self._min_width:
				self._width = max(self._width, self._min_width)
			if self._max_width:
				self._width = min(self._width, self._max_width)
			if self._min_height:
				self._height = max(self._height, self._min_height)
			if self._max_height:
				self._height = min(self._height, self._max_height)
		else:
			available_width = misc._pg.get_width() if self._fill_width else self._width
			available_height = misc._pg.get_height() if self._fill_height else self._height
			self._width = available_width
			self._height = available_height
			col_width = (available_width-self._column_spacing*(num_cols-1))/num_cols
			row_height = (available_height-self._row_spacing*(num_rows-1))/num_rows
			col_widths = [col_width]*num_cols
			row_heights = [row_height]*num_rows
		self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
		col_x = [0.0]*num_cols
		for i in range(1, num_cols):
			col_x[i] = col_x[i-1]+col_widths[i-1]+self._column_spacing
		row_y = [0.0]*num_rows
		for i in range(1, num_rows):
			row_y[i] = row_y[i-1]+row_heights[i-1]+self._row_spacing
		for w in grid_widgets:
			mapped_c = col_map.get(w._grid_column)
			mapped_r = row_map.get(w._grid_row)
			if mapped_c is None or mapped_r is None:
				continue
			end_c = min(mapped_c+w._grid_columnspan-1, num_cols-1)
			end_r = min(mapped_r+w._grid_rowspan-1, num_rows-1)
			cell_x = col_x[mapped_c]
			cell_y = row_y[mapped_r]
			cell_w = col_x[end_c]+col_widths[end_c]-cell_x
			cell_h = row_y[end_r]+row_heights[end_r]-cell_y
			offset_x = (cell_w-w.width)/2
			offset_y = (cell_h-w.height)/2
			target_x = int(self._x+cell_x+offset_x)
			target_y = int(self._y+cell_y+offset_y)
			w.place(target_x, target_y, suppress_anchor=True)

	def _draw(self, surface: pygame.Surface) -> None:
		"""
		Internally used to draw the button. Widgets attached to this screen are drawn separately.

		Args:
			surface (pygame.Surface): The surface to draw on.
		"""
		if not self._alive or not self._visible: return
		mouse_pos = pygame.mouse.get_pos()
		is_hovering = misc._is_point_over_widget(self, mouse_pos)

		current_pg_size = misc._pg.get_size()
		if current_pg_size!=self._last_pg_size:
			self._last_pg_size = current_pg_size
			self.recalculate_grid()
		if self.darken_background_with_alpha and self.visible:
			background_surf = pygame.Surface(surface.get_size())
			background_surf.fill((0, 0, 0))
			background_surf.set_alpha(self.darken_background_with_alpha)
			surface.blit(background_surf, (0, 0))

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
			if pygame.mouse.get_pressed()[0] and is_inside and self._pressed:
				self.trigger_event(epw_types.HOLD)
		else:
			if event.type==pygame.KEYDOWN:
				misc._trigger_key_bindings(self, event)
			elif event.type==pygame.MOUSEBUTTONDOWN:
				if event.button==1:
					self.trigger_event(epw_types.PRESS)
					if is_inside:
						self._pressed = True
			elif event.type==pygame.MOUSEBUTTONUP:
				if event.button==1 and self._pressed:
					self.trigger_event(epw_types.RELEASE)
					self._pressed = False