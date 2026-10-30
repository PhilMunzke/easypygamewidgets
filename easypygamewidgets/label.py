# label.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets
"""A label widget for pygame."""

from __future__ import annotations

import time
from typing import Any, cast, Self, TYPE_CHECKING, Unpack

import pygame

from easypygamewidgets import misc
from easypygamewidgets.assets import AttributeHints
from easypygamewidgets.assets.epw_types import color
from easypygamewidgets.assets.events import *
from easypygamewidgets.assets.theme import _style_dic as sd, _themed
from easypygamewidgets.masterWidgets import Animatable, Clonable, Deletable, Screenable, Tooltipable, Widget

if TYPE_CHECKING:
    import easypygamewidgets

pygame.init()

TO_UPDATE = [f"_{attr}" for attr in [
    "pressed", "state", "is_hovered", "text", "font", "alignment", "alignment_spacing", "line_spacing", "hide_text",
    "hide_background", "hide_border", "width", "height", "auto_size", "min_width", "max_width", "min_height",
    "max_height", "border_thickness", "top_left_corner_radius", "top_right_corner_radius", "bottom_left_corner_radius",
    "bottom_right_corner_radius", "underline", "strikethrough", "hide_shadow", "hide_underline", "hide_strikethrough",

    "active_hover_background_color", "active_hover_border_color", "active_hover_shadow_color",
    "active_hover_strikethrough_color", "active_hover_text_color", "active_hover_underline_color",
    "active_pressed_background_color", "active_pressed_border_color", "active_pressed_shadow_color",
    "active_pressed_strikethrough_color", "active_pressed_text_color", "active_pressed_underline_color",
    "active_unpressed_background_color", "active_unpressed_border_color", "active_unpressed_shadow_color",
    "active_unpressed_strikethrough_color", "active_unpressed_text_color", "active_unpressed_underline_color",
    "disabled_hover_background_color", "disabled_hover_border_color", "disabled_hover_shadow_color",
    "disabled_hover_strikethrough_color", "disabled_hover_text_color", "disabled_hover_underline_color",
    "disabled_unpressed_background_color", "disabled_unpressed_border_color", "disabled_unpressed_shadow_color",
    "disabled_unpressed_strikethrough_color", "disabled_unpressed_text_color", "disabled_unpressed_underline_color"
]]


class Label(Widget, Tooltipable, Screenable, Deletable, Clonable, Animatable):
    """Initializes a label widget for pygame."""

    @_themed
    def __init__(self, screen: easypygamewidgets.Screen | None = None, auto_size: bool = True, width: int = 180,
                 height: int = 80,
                 text: str = "easypygamewidgets Label", state: str | None = None,
                 active_hover_text_color: color = sd["active_hover_text_color"],
                 active_hover_shadow_color: color = sd["active_hover_shadow_color"],
                 active_hover_background_color: color = sd["active_hover_background_color"],
                 active_hover_underline_color: color = sd["active_hover_underline_color"],
                 active_hover_strikethrough_color: color = sd["active_hover_strikethrough_color"],
                 active_hover_border_color: color = sd["active_hover_border_color"],
                 active_pressed_text_color: color = sd["active_pressed_text_color"],
                 active_pressed_shadow_color: color = sd["active_pressed_shadow_color"],
                 active_pressed_background_color: color = sd["active_pressed_background_color"],
                 active_pressed_underline_color: color = sd["active_pressed_underline_color"],
                 active_pressed_strikethrough_color: color = sd["active_pressed_strikethrough_color"],
                 active_pressed_border_color: color = sd["active_pressed_border_color"],
                 active_unpressed_text_color: color = sd["active_unpressed_text_color"],
                 active_unpressed_shadow_color: color = sd["active_unpressed_shadow_color"],
                 active_unpressed_background_color: color = sd["active_unpressed_background_color"],
                 active_unpressed_underline_color: color = sd["active_unpressed_underline_color"],
                 active_unpressed_strikethrough_color: color = sd["active_unpressed_strikethrough_color"],
                 active_unpressed_border_color: color = sd["active_unpressed_border_color"],
                 disabled_hover_text_color: color = sd["disabled_hover_text_color"],
                 disabled_hover_shadow_color: color = sd["disabled_hover_shadow_color"],
                 disabled_hover_background_color: color = sd["disabled_hover_background_color"],
                 disabled_hover_underline_color: color = sd["disabled_hover_underline_color"],
                 disabled_hover_strikethrough_color: color = sd["disabled_hover_strikethrough_color"],
                 disabled_hover_border_color: color = sd["disabled_hover_border_color"],
                 disabled_unpressed_text_color: color = sd["disabled_unpressed_text_color"],
                 disabled_unpressed_shadow_color: color = sd["disabled_unpressed_shadow_color"],
                 disabled_unpressed_background_color: color = sd["disabled_unpressed_background_color"],
                 disabled_unpressed_underline_color: color = sd["disabled_unpressed_underline_color"],
                 disabled_unpressed_strikethrough_color: color = sd["disabled_unpressed_strikethrough_color"],
                 disabled_unpressed_border_color: color = sd["disabled_unpressed_border_color"],
                 border_thickness: int = sd["border_thickness"],
                 hide_text: bool = False,
                 hide_shadow: bool = False,
                 hide_underline: bool = False,
                 hide_strikethrough: bool = False,
                 hide_background: bool = False,
                 hide_border: bool = False,
                 active_hover_cursor: pygame.Cursor | int | None = sd["active_hover_cursor"],
                 disabled_hover_cursor: pygame.Cursor | int | None = sd["disabled_hover_cursor"],
                 active_pressed_cursor: pygame.Cursor | int | None = sd["active_pressed_cursor"],
                 font: pygame.font.Font | pygame.font.SysFont = sd["font"], alignment: str = "center",
                 alignment_spacing: int = sd["alignment_spacing"], dragable: bool = False,
                 top_left_corner_radius: int = sd["top_left_corner_radius"],
                 top_right_corner_radius: int = sd["top_right_corner_radius"],
                 bottom_left_corner_radius: int = sd["bottom_left_corner_radius"],
                 bottom_right_corner_radius: int = sd["bottom_right_corner_radius"], layer: int = sd["layer"],
                 line_spacing: int = sd["line_spacing"],
                 tooltip: easypygamewidgets.Tooltip | None = None, min_width: int | None = sd["min_width"],
                 max_width: int | None = sd["max_width"], min_height: int | None = sd["min_height"],
                 max_height: int | None = sd["max_height"],
                 alpha_based_collision_system: bool = sd["alpha_based_collision_system"],
                 anchor_x: str = sd["anchor_x"], anchor_y: str = sd["anchor_y"], visible: bool = sd["visible"],
                 data: Any = None) -> None:
        """
        Initializes a Label widget.

        Args:
            screen: The Screen this label is attached to. If None, the label is created without a parent screen.
            auto_size: If True, width and height are computed from the rendered text instead of using the given
                width/height.
            width: Fixed label width in pixels. Ignored if auto_size is True.
            height: Fixed label height in pixels. Ignored if auto_size is True.
            text: The label's text.
            state: Initial state, 'enabled' or 'disabled'. Defaults to 'enabled' if not given.
            active_hover_text_color: RGBA text color while enabled and hovered.
            active_hover_shadow_color: RGBA shadow color while enabled and hovered.
            active_hover_background_color: RGBA background color while enabled and hovered.
            active_hover_underline_color: RGBA underline color while enabled and hovered. Setting a value enables the
                underline.
            active_hover_strikethrough_color: RGBA strikethrough color while enabled and hovered. Setting a value
                enables the strikethrough.
            active_hover_border_color: RGBA border color while enabled and hovered.
            active_pressed_text_color: RGBA text color while enabled and pressed.
            active_pressed_shadow_color: RGBA shadow color while enabled and pressed.
            active_pressed_background_color: RGBA background color while enabled and pressed.
            active_pressed_underline_color: RGBA underline color while enabled and pressed. Setting a value enables the
                underline.
            active_pressed_strikethrough_color: RGBA strikethrough color while enabled and pressed. Setting a value
                enables the strikethrough.
            active_pressed_border_color: RGBA border color while enabled and pressed.
            active_unpressed_text_color: RGBA text color while enabled, not pressed, not hovered.
            active_unpressed_shadow_color: RGBA shadow color while enabled, not pressed, not hovered.
            active_unpressed_background_color: RGBA background color while enabled, not pressed, not hovered.
            active_unpressed_underline_color: RGBA underline color while enabled, not pressed, not hovered. Setting a
                value enables the underline.
            active_unpressed_strikethrough_color: RGBA strikethrough color while enabled, not pressed, not hovered.
                Setting a value enables the strikethrough.
            active_unpressed_border_color: RGBA border color while enabled, not pressed, not hovered.
            disabled_hover_text_color: RGBA text color while disabled and hovered.
            disabled_hover_shadow_color: RGBA shadow color while disabled and hovered.
            disabled_hover_background_color: RGBA background color while disabled and hovered.
            disabled_hover_underline_color: RGBA underline color while disabled and hovered. Setting a value enables
                the underline.
            disabled_hover_strikethrough_color: RGBA strikethrough color while disabled and hovered. Setting a value
                enables the strikethrough.
            disabled_hover_border_color: RGBA border color while disabled and hovered.
            disabled_unpressed_text_color: RGBA text color while disabled, not hovered.
            disabled_unpressed_shadow_color: RGBA shadow color while disabled, not hovered.
            disabled_unpressed_background_color: RGBA background color while disabled, not hovered.
            disabled_unpressed_underline_color: RGBA underline color while disabled, not hovered. Setting a value
                enables the underline.
            disabled_unpressed_strikethrough_color: RGBA strikethrough color while disabled, not hovered. Setting a
                value enables the strikethrough.
            disabled_unpressed_border_color: RGBA border color while disabled, not hovered.
            border_thickness: Border width in pixels.
            hide_text: If True, text is not rendered.
            hide_shadow: If True, the text shadow is not rendered.
            hide_underline: If True, the underline is not rendered.
            hide_strikethrough: If True, the strikethrough is not rendered.
            hide_background: If True, the background fill is not rendered.
            hide_border: If True, the border is not rendered.
            active_hover_cursor: Custom cursor shown on hover while enabled.
            disabled_hover_cursor: Custom cursor shown on hover while disabled.
            active_pressed_cursor: Custom cursor shown while pressed.
            font: The pygame font used to render the label text.
            alignment: Text alignment: 'left', 'right', 'center' or 'stretched'
            alignment_spacing: Horizontal padding reserved around the aligned text.
            dragable: If True, the label can be dragged with the mouse.
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
            ValueError: If a *_cursor argument is given but is not a pygame.Cursor or int.
        """
        super().__init__()
        _safe_set_linesize(font, line_spacing)
        lines = str(text).split("\n")
        if lines==[""]:
            lines = [" "]
        max_w = max((font.render(line, True, (255, 255, 255)).get_width() for line in lines), default=0)
        total_h = sum(font.render(line, True, (255, 255, 255)).get_height() for line in lines)
        self._screen = None
        if screen:
            screen.add_widget(self)
            if state: self._state = state
        else:
            self._visible = visible
            if state: self._state = state
            else: self._state = "enabled"
        self._strikethrough = False
        self._underline = False
        self._auto_size = auto_size
        if auto_size:
            self._width = max_w+alignment_spacing*2
            if min_width:
                self._width = max(max_w+alignment_spacing*2, min_width)
            if max_width:
                self._width = min(max_w+alignment_spacing*2, max_width)
            self._height = total_h+20
            if min_height:
                self._height = max(total_h+20, min_height)
            if max_height:
                self._height = min(total_h+20, max_height)
        else:
            self._width = width
            self._height = height
        self._text = text
        self._active_hover_text_color = misc.normalize_color(active_hover_text_color)
        self._active_hover_shadow_color = misc.normalize_color(active_hover_shadow_color)
        self._active_hover_background_color = misc.normalize_color(active_hover_background_color)
        if active_hover_underline_color:
            self._active_hover_underline_color = misc.normalize_color(active_hover_underline_color)
            self._underline = True
        else:
            self._active_hover_underline_color = self._active_hover_text_color
        if active_hover_strikethrough_color:
            self._active_hover_strikethrough_color = misc.normalize_color(active_hover_strikethrough_color)
            self._strikethrough = True
        else:
            self._active_hover_strikethrough_color = self._active_hover_text_color
        self._active_hover_border_color = misc.normalize_color(active_hover_border_color)
        self._active_pressed_text_color = misc.normalize_color(active_pressed_text_color)
        self._active_pressed_shadow_color = misc.normalize_color(active_pressed_shadow_color)
        self._active_pressed_background_color = misc.normalize_color(active_pressed_background_color)
        if active_pressed_underline_color:
            self._active_pressed_underline_color = misc.normalize_color(active_pressed_underline_color)
            self._underline = True
        else:
            self._active_pressed_underline_color = self._active_pressed_text_color
        if active_pressed_strikethrough_color:
            self._active_pressed_strikethrough_color = misc.normalize_color(active_pressed_strikethrough_color)
            self._strikethrough = True
        else:
            self._active_pressed_strikethrough_color = self._active_pressed_text_color
        self._active_pressed_border_color = misc.normalize_color(active_pressed_border_color)
        self._active_unpressed_text_color = misc.normalize_color(active_unpressed_text_color)
        self._active_unpressed_shadow_color = misc.normalize_color(active_unpressed_shadow_color)
        self._active_unpressed_background_color = misc.normalize_color(active_unpressed_background_color)
        if active_unpressed_underline_color:
            self._active_unpressed_underline_color = misc.normalize_color(active_unpressed_underline_color)
            self._underline = True
        else:
            self._active_unpressed_underline_color = self._active_unpressed_text_color
        if active_unpressed_strikethrough_color:
            self._active_unpressed_strikethrough_color = misc.normalize_color(active_unpressed_strikethrough_color)
            self._strikethrough = True
        else:
            self._active_unpressed_strikethrough_color = self._active_unpressed_text_color
        self._active_unpressed_border_color = misc.normalize_color(active_unpressed_border_color)
        self._disabled_hover_text_color = misc.normalize_color(disabled_hover_text_color)
        self._disabled_hover_shadow_color = misc.normalize_color(disabled_hover_shadow_color)
        self._disabled_hover_background_color = misc.normalize_color(disabled_hover_background_color)
        if disabled_hover_underline_color:
            self._disabled_hover_underline_color = misc.normalize_color(disabled_hover_underline_color)
            self._underline = True
        else:
            self._disabled_hover_underline_color = self._disabled_hover_text_color
        if disabled_hover_strikethrough_color:
            self._disabled_hover_strikethrough_color = misc.normalize_color(disabled_hover_strikethrough_color)
            self._strikethrough = True
        else:
            self._disabled_hover_strikethrough_color = self._disabled_hover_text_color
        self._disabled_hover_border_color = misc.normalize_color(disabled_hover_border_color)
        self._disabled_unpressed_text_color = misc.normalize_color(disabled_unpressed_text_color)
        self._disabled_unpressed_shadow_color = misc.normalize_color(disabled_unpressed_shadow_color)
        self._disabled_unpressed_background_color = misc.normalize_color(disabled_unpressed_background_color)
        if disabled_unpressed_underline_color:
            self._disabled_unpressed_underline_color = misc.normalize_color(disabled_unpressed_underline_color)
            self._underline = True
        else:
            self._disabled_unpressed_underline_color = self._disabled_unpressed_text_color
        if disabled_unpressed_strikethrough_color:
            self._disabled_unpressed_strikethrough_color = misc.normalize_color(disabled_unpressed_strikethrough_color)
            self._strikethrough = True
        else:
            self._disabled_unpressed_strikethrough_color = self._disabled_unpressed_text_color
        self._disabled_unpressed_border_color = misc.normalize_color(disabled_unpressed_border_color)
        self._border_thickness = border_thickness
        self._hide_text = hide_text
        self._hide_shadow = hide_shadow
        self._hide_underline = hide_underline
        self._hide_strikethrough = hide_strikethrough
        self._hide_background = hide_background
        self._hide_border = hide_border
        cursor_input = {
            "active_hover": active_hover_cursor,
            "disabled_hover": disabled_hover_cursor,
            "active_pressed": active_pressed_cursor
        }
        self._cursors = {}
        for name, cursor in cursor_input.items():
            if isinstance(cursor, (pygame.cursors.Cursor, int)): self._cursors[name] = cursor
            else:
                if cursor is not None:
                    raise ValueError(f"got {cursor} for {name}_cursor, expected pygame.cursors.Cursor or int")
                self._cursors[name] = None
        self._font = font
        self._alignment = alignment
        self._alignment_spacing = alignment_spacing
        self._dragable = dragable
        self._top_left_corner_radius = top_left_corner_radius
        self._top_right_corner_radius = top_right_corner_radius
        self._bottom_left_corner_radius = bottom_left_corner_radius
        self._bottom_right_corner_radius = bottom_right_corner_radius
        self._layer = layer
        self._tooltip = tooltip
        if tooltip:
            tooltip.configure(layer=self._layer+1)
            if not tooltip.style:
                bg_color = None
                bd_color = None
                if not self._active_unpressed_background_color: bg_color = (50, 50, 50, 255)
                if not self._active_unpressed_border_color: bd_color = (100, 100, 100, 255)
                tooltip.configure(
                    active_unpressed_text_color=self._active_unpressed_text_color,
                    active_unpressed_background_color=self._active_unpressed_background_color or bg_color,
                    active_unpressed_border_color=self._active_unpressed_border_color or bd_color
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
        self._drag_offset = None
        self._is_dragging = False
        self._last_checked_dragging = None
        self._bindings = {}
        self._needs_redraw = True
        self._needs_transform = True
        self._last_visual_state = None
        self._original_surface = pygame.Surface((1, 1))
        self._cached_surface = None
        self._is_hovered = False
        self._dialog = None

        misc._add_widget(self)

    @property
    def strikethrough(self):
        return self._strikethrough

    @strikethrough.setter
    def strikethrough(self, value):
        self._strikethrough = value

    @property
    def underline(self):
        return self._underline

    @underline.setter
    def underline(self, value):
        self._underline = value

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
    def active_hover_text_color(self):
        return self._active_hover_text_color

    @active_hover_text_color.setter
    def active_hover_text_color(self, value):
        self._active_hover_text_color = misc.normalize_color(value)

    @property
    def active_hover_shadow_color(self):
        return self._active_hover_shadow_color

    @active_hover_shadow_color.setter
    def active_hover_shadow_color(self, value):
        self._active_hover_shadow_color = misc.normalize_color(value)

    @property
    def active_hover_background_color(self):
        return self._active_hover_background_color

    @active_hover_background_color.setter
    def active_hover_background_color(self, value):
        self._active_hover_background_color = misc.normalize_color(value)

    @property
    def active_hover_underline_color(self):
        return self._active_hover_underline_color

    @active_hover_underline_color.setter
    def active_hover_underline_color(self, value):
        self._active_hover_underline_color = misc.normalize_color(value)
        self._underline = True

    @property
    def active_hover_strikethrough_color(self):
        return self._active_hover_strikethrough_color

    @active_hover_strikethrough_color.setter
    def active_hover_strikethrough_color(self, value):
        self._active_hover_strikethrough_color = misc.normalize_color(value)

    @property
    def active_hover_border_color(self):
        return self._active_hover_border_color

    @active_hover_border_color.setter
    def active_hover_border_color(self, value):
        self._active_hover_border_color = misc.normalize_color(value)

    @property
    def active_pressed_text_color(self):
        return self._active_pressed_text_color

    @active_pressed_text_color.setter
    def active_pressed_text_color(self, value):
        self._active_pressed_text_color = misc.normalize_color(value)

    @property
    def active_pressed_shadow_color(self):
        return self._active_pressed_shadow_color

    @active_pressed_shadow_color.setter
    def active_pressed_shadow_color(self, value):
        self._active_pressed_shadow_color = misc.normalize_color(value)

    @property
    def active_pressed_background_color(self):
        return self._active_pressed_background_color

    @active_pressed_background_color.setter
    def active_pressed_background_color(self, value):
        self._active_pressed_background_color = misc.normalize_color(value)

    @property
    def active_pressed_underline_color(self):
        return self._active_pressed_underline_color

    @active_pressed_underline_color.setter
    def active_pressed_underline_color(self, value):
        self._active_pressed_underline_color = misc.normalize_color(value)
        self._underline = True

    @property
    def active_pressed_strikethrough_color(self):
        return self._active_pressed_strikethrough_color

    @active_pressed_strikethrough_color.setter
    def active_pressed_strikethrough_color(self, value):
        self._active_pressed_strikethrough_color = misc.normalize_color(value)

    @property
    def active_pressed_border_color(self):
        return self._active_pressed_border_color

    @active_pressed_border_color.setter
    def active_pressed_border_color(self, value):
        self._active_pressed_border_color = misc.normalize_color(value)

    @property
    def active_unpressed_text_color(self):
        return self._active_unpressed_text_color

    @active_unpressed_text_color.setter
    def active_unpressed_text_color(self, value):
        self._active_unpressed_text_color = misc.normalize_color(value)

    @property
    def active_unpressed_shadow_color(self):
        return self._active_unpressed_shadow_color

    @active_unpressed_shadow_color.setter
    def active_unpressed_shadow_color(self, value):
        self._active_unpressed_shadow_color = misc.normalize_color(value)

    @property
    def active_unpressed_background_color(self):
        return self._active_unpressed_background_color

    @active_unpressed_background_color.setter
    def active_unpressed_background_color(self, value):
        self._active_unpressed_background_color = misc.normalize_color(value)

    @property
    def active_unpressed_underline_color(self):
        return self._active_unpressed_underline_color

    @active_unpressed_underline_color.setter
    def active_unpressed_underline_color(self, value):
        self._active_unpressed_underline_color = misc.normalize_color(value)
        self._underline = True

    @property
    def active_unpressed_strikethrough_color(self):
        return self._active_unpressed_strikethrough_color

    @active_unpressed_strikethrough_color.setter
    def active_unpressed_strikethrough_color(self, value):
        self._active_unpressed_strikethrough_color = misc.normalize_color(value)

    @property
    def active_unpressed_border_color(self):
        return self._active_unpressed_border_color

    @active_unpressed_border_color.setter
    def active_unpressed_border_color(self, value):
        self._active_unpressed_border_color = misc.normalize_color(value)

    @property
    def disabled_hover_text_color(self):
        return self._disabled_hover_text_color

    @disabled_hover_text_color.setter
    def disabled_hover_text_color(self, value):
        self._disabled_hover_text_color = misc.normalize_color(value)

    @property
    def disabled_hover_shadow_color(self):
        return self._disabled_hover_shadow_color

    @disabled_hover_shadow_color.setter
    def disabled_hover_shadow_color(self, value):
        self._disabled_hover_shadow_color = misc.normalize_color(value)

    @property
    def disabled_hover_background_color(self):
        return self._disabled_hover_background_color

    @disabled_hover_background_color.setter
    def disabled_hover_background_color(self, value):
        self._disabled_hover_background_color = misc.normalize_color(value)

    @property
    def disabled_hover_underline_color(self):
        return self._disabled_hover_underline_color

    @disabled_hover_underline_color.setter
    def disabled_hover_underline_color(self, value):
        self._disabled_hover_underline_color = misc.normalize_color(value)
        self._underline = True

    @property
    def disabled_hover_strikethrough_color(self):
        return self._disabled_hover_strikethrough_color

    @disabled_hover_strikethrough_color.setter
    def disabled_hover_strikethrough_color(self, value):
        self._disabled_hover_strikethrough_color = misc.normalize_color(value)

    @property
    def disabled_hover_border_color(self):
        return self._disabled_hover_border_color

    @disabled_hover_border_color.setter
    def disabled_hover_border_color(self, value):
        self._disabled_hover_border_color = misc.normalize_color(value)

    @property
    def disabled_unpressed_text_color(self):
        return self._disabled_unpressed_text_color

    @disabled_unpressed_text_color.setter
    def disabled_unpressed_text_color(self, value):
        self._disabled_unpressed_text_color = misc.normalize_color(value)

    @property
    def disabled_unpressed_shadow_color(self):
        return self._disabled_unpressed_shadow_color

    @disabled_unpressed_shadow_color.setter
    def disabled_unpressed_shadow_color(self, value):
        self._disabled_unpressed_shadow_color = misc.normalize_color(value)

    @property
    def disabled_unpressed_background_color(self):
        return self._disabled_unpressed_background_color

    @disabled_unpressed_background_color.setter
    def disabled_unpressed_background_color(self, value):
        self._disabled_unpressed_background_color = misc.normalize_color(value)

    @property
    def disabled_unpressed_underline_color(self):
        return self._disabled_unpressed_underline_color

    @disabled_unpressed_underline_color.setter
    def disabled_unpressed_underline_color(self, value):
        self._disabled_unpressed_underline_color = misc.normalize_color(value)
        self._underline = True

    @property
    def disabled_unpressed_strikethrough_color(self):
        return self._disabled_unpressed_strikethrough_color

    @disabled_unpressed_strikethrough_color.setter
    def disabled_unpressed_strikethrough_color(self, value):
        self._disabled_unpressed_strikethrough_color = misc.normalize_color(value)

    @property
    def disabled_unpressed_border_color(self):
        return self._disabled_unpressed_border_color

    @disabled_unpressed_border_color.setter
    def disabled_unpressed_border_color(self, value):
        self._disabled_unpressed_border_color = misc.normalize_color(value)

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
    def hide_shadow(self):
        return self._hide_shadow

    @hide_shadow.setter
    def hide_shadow(self, value):
        self._hide_shadow = value

    @property
    def hide_background(self):
        return self._hide_background

    @hide_background.setter
    def hide_background(self, value):
        self._hide_background = value

    @property
    def hide_underline(self):
        return self._hide_underline

    @hide_underline.setter
    def hide_underline(self, value):
        self._hide_underline = value

    @property
    def hide_strikethrough(self):
        return self._hide_strikethrough

    @hide_strikethrough.setter
    def hide_strikethrough(self, value):
        self._hide_strikethrough = value

    @property
    def hide_border(self):
        return self._hide_border

    @hide_border.setter
    def hide_border(self, value):
        self._hide_border = value

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
    def dragable(self):
        return self._dragable

    @dragable.setter
    def dragable(self, value):
        self._dragable = value

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
    def drag_offset(self):
        return self._drag_offset

    @drag_offset.setter
    def drag_offset(self, value):
        self._drag_offset = value

    @property
    def is_dragging(self):
        return self._is_dragging

    @is_dragging.setter
    def is_dragging(self, value):
        self._is_dragging = value

    @property
    def last_checked_dragging(self):
        return self._last_checked_dragging

    @last_checked_dragging.setter
    def last_checked_dragging(self, value):
        self._last_checked_dragging = value

    @property
    def needs_redraw(self):
        return self._needs_redraw

    @needs_redraw.setter
    def needs_redraw(self, value):
        self._needs_redraw = value

    @property
    def needs_transform(self):
        return self._needs_transform

    @needs_transform.setter
    def needs_transform(self, value):
        self._needs_transform = value

    @property
    def last_visual_state(self):
        return self._last_visual_state

    @last_visual_state.setter
    def last_visual_state(self, value):
        self._last_visual_state = value

    @property
    def original_surface(self):
        return self._original_surface

    @original_surface.setter
    def original_surface(self, value):
        self._original_surface = value

    @property
    def cached_surface(self):
        return self._cached_surface

    @cached_surface.setter
    def cached_surface(self, value):
        self._cached_surface = value

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self._needs_transform = True

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        self._needs_transform = True

    @property
    def offset_x(self):
        return self._offset_x

    @offset_x.setter
    def offset_x(self, value):
        self._offset_x = value

    @property
    def offset_y(self):
        return self._offset_y

    @offset_y.setter
    def offset_y(self, value):
        self._offset_y = value

    @property
    def is_hovered(self):
        return self._is_hovered

    @is_hovered.setter
    def is_hovered(self, value):
        self._is_hovered = value

    @property
    def dialog(self):
        return self._dialog

    @dialog.setter
    def dialog(self, value):
        self._dialog = value

    def configure(self, **kwargs: Unpack[AttributeHints.LabelConfig]) -> Self:
        """
        Updates one or more of the label's attributes.

        Args:
            **kwargs: Label attributes to update as defined in TypeHints.LabelConfig

        Returns:
            Self (Self): This label instance to allow method chaining.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._needs_redraw = True
        layout_keys = (
            'auto_size', 'x', 'y', 'width', 'height', 'text', 'line_spacing', 'font', 'alignment_spacing',
            'max_width', 'min_width', 'max_height', 'min_height', 'anchor_x', 'anchor_y'
        )
        if any(k in kwargs for k in layout_keys):
            _safe_set_linesize(self._font, self._line_spacing)
            lines = str(self._text).split("\n")
            max_w = max(
                (self._font.render(line, True, (255, 255, 255)).get_width() for line in lines),
                default=0
            )+self._alignment_spacing
            total_h = sum(self._font.render(line, True, (255, 255, 255)).get_height() for line in lines)
            if self._auto_size:
                self._width = max_w+self._alignment_spacing*2
                if self._min_width:
                    self._width = max(max_w+self._alignment_spacing*2, self._min_width)
                if self._max_width:
                    self._width = min(max_w+self._alignment_spacing*2, self._max_width)
                self._height = total_h+20
                if self._min_height:
                    self._height = max(total_h+20, self._min_height)
                if self._max_height:
                    self._height = min(total_h+20, self._max_height)
            self._rect = pygame.Rect(self._x, self._y, self._width, self._height)
        if 'screen' in kwargs:
            self.set_screen(kwargs["screen"])
        if 'layer' in kwargs:
            misc._resort_layers()
        if 'line_spacing' in kwargs:
            _safe_set_linesize(self._font, self._line_spacing)
        return self

    def config(self, **kwargs: Unpack[AttributeHints.LabelConfig]) -> Self:
        """
        Updates one or more of the label's attributes.

        Args:
            **kwargs: Label attributes to update as defined in TypeHints.LabelConfig

        Returns:
            Self (Self): This label instance to allow method chaining.
        """
        return self.configure(**kwargs)

    def set_strikethrough(self, value: bool) -> Label:
        """
        Enables or disables the strikethrough line.

        Args:
            value: True to show the strikethrough, False to hide it.

        Returns:
            Self (Self): This label instance to allow method chaining.
        """
        self._strikethrough = value
        self._needs_redraw = True
        return self

    def set_underline(self, value: bool) -> Self:
        """
        Enables or disables the underline.

        Args:
            value: True to show the underline, False to hide it.

        Returns:
            Self (Self): This label instance to allow method chaining.
        """
        self._underline = value
        self._needs_redraw = True
        return self

    def set_tooltip(self, tooltip: easypygamewidgets.Tooltip) -> Self:
        """
        Bind a tooltip to a widget.

        Args:
            tooltip (easypygamewidgets.Tooltip): The tooltip to bind to the widget.

        Returns:
            Self (Self): This widget instance to allow method chaining.
        """
        tooltip._widgets.append(self)
        self._tooltip = tooltip
        tooltip.configure(layer=self._layer+1)
        if not tooltip.style:
            tooltip.configure(
                active_unpressed_text_color=self._active_unpressed_text_color,
                active_unpressed_background_color=self._active_unpressed_background_color if
                self._active_unpressed_background_color else sd["active_unpressed_background_color"],
                active_unpressed_border_color=self._active_unpressed_border_color if
                self._active_unpressed_border_color else sd["active_unpressed_border_color"],
                disabled_unpressed_text_color=self._disabled_unpressed_text_color,
                disabled_unpressed_background_color=self._disabled_unpressed_background_color if
                self._disabled_unpressed_background_color else sd["disabled_unpressed_background_color"],
                disabled_unpressed_border_color=self._disabled_unpressed_border_color if
                self._disabled_unpressed_border_color else sd["disabled_unpressed_border_color"],
                active_hover_text_color=self._active_hover_text_color,
                active_hover_background_color=self._active_hover_background_color if
                self._active_hover_background_color else sd["active_hover_background_color"],
                active_hover_border_color=self._active_hover_border_color if
                self._active_hover_border_color else sd["active_hover_border_color"],
                disabled_hover_text_color=self._disabled_hover_text_color,
                disabled_hover_background_color=self._disabled_hover_background_color if
                self._disabled_hover_background_color else sd["disabled_hover_background_color"],
                disabled_hover_border_color=self._disabled_hover_border_color if
                self._disabled_hover_border_color else sd["disabled_hover_border_color"],
                active_pressed_text_color=self._active_pressed_text_color,
                active_pressed_background_color=self._active_pressed_background_color if
                self._active_pressed_background_color else sd["active_pressed_background_color"],
                active_pressed_border_color=self._active_pressed_border_color if
                self._active_pressed_border_color else sd["active_pressed_border_color"]
            )
        return self

    def _draw(self, surface: pygame.Surface) -> None:
        """
        Internally used to draw the label.

        Args:
            surface (pygame.Surface): The surface to draw the label on.
        """
        if not self._alive or not self._visible:
            return
        mouse_pos = pygame.mouse.get_pos()
        is_hovering = misc._is_point_over_widget(self, mouse_pos)
        current_visual_state = misc._get_vars(self, TO_UPDATE)
        if self._needs_redraw or self._last_visual_state!=current_visual_state:
            _render_label_surface(self, is_hovering)
        if self._needs_transform: self._apply_transform()
        draw_rect = self._rect.move(misc._get_offset(self))
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
            self.trigger_event(MOUSE_IN)
            if self._tooltip:
                self._tooltip.show()
        elif is_hovering and self._is_hovered:
            self._is_hovered = True
            self.trigger_event(HOVER)
        elif not is_hovering and self._is_hovered:
            self._is_hovered = False
            self.trigger_event(MOUSE_OUT)
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
        current_time = time.time()
        mouse_pos = pygame.mouse.get_pos()
        is_inside = misc._is_point_over_widget(self, mouse_pos)
        offset_x, offset_y = misc._get_offset(self)
        if event:
            if event.type==pygame.KEYDOWN:
                misc._trigger_key_bindings(self, event)
            if event.type==pygame.MOUSEMOTION:
                if self._pressed and self._dragable:
                    if is_inside or self._is_dragging:
                        self._is_dragging = True
                        self._last_checked_dragging = current_time
                        if self._drag_offset:
                            new_x = mouse_pos[0]-self._drag_offset[0]-offset_x
                            new_y = mouse_pos[1]-self._drag_offset[1]-offset_y
                            self.place(new_x, new_y, suppress_anchor=True)
            elif event.type==pygame.MOUSEBUTTONDOWN and is_inside:
                if event.button==1:
                    self._pressed = True
                    self._drag_offset = (
                        mouse_pos[0]-(self._x+offset_x),
                        mouse_pos[1]-(self._y+offset_y)
                    )
                    self.trigger_event(PRESS)
            elif event.type==pygame.MOUSEBUTTONUP:
                if event.button==1 and self._pressed:
                    self._pressed = False
                    self._is_dragging = False
                    self.trigger_event(RELEASE)
        if self._last_checked_dragging:
            if current_time-self._last_checked_dragging>0.2:
                self._is_dragging = False
        if self._pressed and not self._is_dragging:
            self.trigger_event(HOLD)
        if self._pressed and self._is_dragging:
            self.trigger_event(DRAG)


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


def _render_label_surface(label: Label, is_hovering: bool) -> None:
    """
    Internally used to draw the label surface once and cache it.

    Args:
        label (Label): the widget to render the surface for
        is_hovering (bool): whether the mouse is hovering over the widget
    """
    if label.state=="enabled":
        if label.pressed:
            text_color = label.active_pressed_text_color
            bg_color = label.active_pressed_background_color
            shadow_color = label.active_pressed_shadow_color
            underline_color = label.active_pressed_underline_color
            strikethrough_color = label.active_pressed_strikethrough_color
            brd_color = label.active_pressed_border_color
        elif is_hovering:
            text_color = label.active_hover_text_color
            bg_color = label.active_hover_background_color
            shadow_color = label.active_hover_shadow_color
            underline_color = label.active_hover_underline_color
            strikethrough_color = label.active_hover_strikethrough_color
            brd_color = label.active_hover_border_color
        else:
            text_color = label.active_unpressed_text_color
            bg_color = label.active_unpressed_background_color
            shadow_color = label.active_unpressed_shadow_color
            underline_color = label.active_unpressed_underline_color
            strikethrough_color = label.active_unpressed_strikethrough_color
            brd_color = label.active_unpressed_border_color
    else:
        if is_hovering:
            text_color = label.disabled_hover_text_color
            bg_color = label.disabled_hover_background_color
            shadow_color = label.disabled_hover_shadow_color
            underline_color = label.disabled_hover_underline_color
            strikethrough_color = label.disabled_hover_strikethrough_color
            brd_color = label.disabled_hover_border_color
        else:
            text_color = label.disabled_unpressed_text_color
            bg_color = label.disabled_unpressed_background_color
            shadow_color = label.disabled_unpressed_shadow_color
            underline_color = label.disabled_unpressed_underline_color
            strikethrough_color = label.disabled_unpressed_strikethrough_color
            brd_color = label.disabled_unpressed_border_color

    if label.auto_size:
        _safe_set_linesize(label.font, label.line_spacing)
        lines = str(label.text).split("\n")
        if lines==[""]:
            lines = [" "]
        max_w = max((label.font.render(line, True, text_color).get_width() for line in lines), default=0)
        total_h = sum(label.font.render(line, True, text_color).get_height() for line in lines)
        label._width = max_w+label.alignment_spacing*2
        if label.min_width:
            label._width = max(max_w+label.alignment_spacing*2, cast(int, label.min_width))
        if label.max_width:
            label._width = min(max_w+label.alignment_spacing*2, cast(int, label.max_width))
        label._height = total_h+20
        if label.min_height:
            label._height = max(total_h+20, cast(int, label.min_height))
        if label.max_height:
            label._height = min(total_h+20, cast(int, label.max_height))
        label.rect = pygame.Rect(label.x, label.y, label._width, label._height)
    label.original_surface = pygame.Surface((label._width, label._height), pygame.SRCALPHA)
    draw_req_rect = pygame.Rect(0, 0, label._width, label._height)
    if not label.hide_background:
        shape_surf = pygame.Surface((label._width, label._height), pygame.SRCALPHA)
        pygame.draw.rect(
            shape_surf, bg_color, draw_req_rect,
            border_top_left_radius=label.top_left_corner_radius,
            border_top_right_radius=label.top_right_corner_radius,
            border_bottom_left_radius=label.bottom_left_corner_radius,
            border_bottom_right_radius=label.bottom_right_corner_radius
        )
        shape_surf.set_alpha(bg_color[3])
        label.original_surface.blit(shape_surf, (0, 0))
    if not label.hide_border:
        shape_surf = pygame.Surface((label._width, label._height), pygame.SRCALPHA)
        pygame.draw.rect(
            shape_surf, brd_color, draw_req_rect, width=label.border_thickness,
            border_top_left_radius=label.top_left_corner_radius,
            border_top_right_radius=label.top_right_corner_radius,
            border_bottom_left_radius=label.bottom_left_corner_radius,
            border_bottom_right_radius=label.bottom_right_corner_radius
        )
        shape_surf.set_alpha(brd_color[3])
        label.original_surface.blit(shape_surf, (0, 0))

    def _render_text_line(txt: str, color: tuple[int, int, int, int], rect_ref: pygame.Rect,
                          offset: tuple[int, int] = (0, 0)) -> pygame.Rect | None:
        text_lines = str(txt).split("\n")
        if not text_lines: return None
        total_height = sum(label.font.render(line, True, color).get_height() for line in text_lines)
        ascent = label.font.get_ascent()
        descent = abs(label.font.get_descent())
        optical_centre_offset = ascent-(ascent-descent)//2
        first_line_h = label.font.render(text_lines[0], True, color).get_height()
        current_y = rect_ref.centery-total_height//2+offset[1]+(first_line_h//2-optical_centre_offset)
        union_rect = pygame.Rect(rect_ref.x, rect_ref.y, 0, 0)
        for line in text_lines:
            line_surf = label.font.render(line, True, color)
            line_h = line_surf.get_height()
            cx, cy = rect_ref.centerx+offset[0], current_y+line_h//2
            if label.alignment=="stretched" and len(line)>1:
                total_char_width = sum(label.font.render(char, True, color).get_width() for char in line)
                available_width = rect_ref.width-(label.alignment_spacing*2)
                if available_width>total_char_width:
                    spacing = (available_width-total_char_width)/(len(line)-1)
                    curr_x = rect_ref.left+label.alignment_spacing+offset[0]
                    line_rect = pygame.Rect(rect_ref.left+label.alignment_spacing+offset[0], cy, 0, 0)
                    for char in line:
                        char_s = label.font.render(char, True, color)
                        char_s.set_alpha(color[3])
                        char_r = char_s.get_rect(midleft=(curr_x, cy))
                        label.original_surface.blit(char_s, char_r)
                        curr_x += char_s.get_width()+spacing
                        line_rect.union_ip(char_r)
                    union_rect.union_ip(line_rect)
                    current_y += line_h
                    continue
            txt_rect = line_surf.get_rect()
            if label.alignment=="left":
                txt_rect.midleft = (rect_ref.left+label.alignment_spacing+offset[0], cy)
            elif label.alignment=="right":
                txt_rect.midright = (rect_ref.right-label.alignment_spacing+offset[0], cy)
            else:
                txt_rect.center = (cx, cy)
            line_surf.set_alpha(color[3])
            label.original_surface.blit(line_surf, txt_rect)
            union_rect.union_ip(txt_rect)
            current_y += line_h
        return union_rect

    surface_rect = label.original_surface.get_rect()
    if not label.hide_shadow:
        _render_text_line(label.text, shadow_color, surface_rect, offset=(2, 2))
    if not label.hide_text:
        final_text_rect = _render_text_line(label.text, text_color, surface_rect)
    else:
        final_text_rect = None
    if final_text_rect:
        if not label.hide_underline and label.underline:
            shape_surf = pygame.Surface(final_text_rect.size, pygame.SRCALPHA)
            shape_surf_rect = shape_surf.get_rect()
            start_pos = (shape_surf_rect.left, shape_surf_rect.bottom-2)
            end_pos = (shape_surf_rect.right, shape_surf_rect.bottom-2)
            shape_surf.set_alpha(underline_color[3])
            pygame.draw.line(shape_surf, underline_color, start_pos, end_pos, 2)
            label.original_surface.blit(shape_surf, final_text_rect)
        if not label.hide_strikethrough and label.strikethrough:
            shape_surf = pygame.Surface(final_text_rect.size, pygame.SRCALPHA)
            shape_surf_rect = shape_surf.get_rect()
            start_pos = (shape_surf_rect.left, shape_surf_rect.centery)
            end_pos = (shape_surf_rect.right, shape_surf_rect.centery)
            shape_surf.set_alpha(strikethrough_color[3])
            pygame.draw.line(shape_surf, strikethrough_color, start_pos, end_pos, 2)
            label.original_surface.blit(shape_surf, final_text_rect)
    label._last_visual_state = misc._get_vars(label, TO_UPDATE)
    label.needs_redraw = False
    label.needs_transform = True
    label.cached_surface = label.original_surface