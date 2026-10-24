# masterWidgets.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets
"""Internally used to reduce duplicate code across different widgets."""

from __future__ import annotations

import copy
from collections.abc import Callable
from typing import Any, Self, TYPE_CHECKING, Unpack

import pygame

from easypygamewidgets import misc
from .animation import Animation
from .assets.AttributeHints import AnimatableAttributes
from .assets.easing import ease_out_quint
from .assets.events import _binding as binding

if TYPE_CHECKING:
    import easypygamewidgets


class Widget:
    """Initializes a default widget."""

    def bind(self, event: binding, command: Callable | None = None, require_hover: bool = True,
             widget_boolean_value: Callable | None = None,
             required_value_for_widget_boolean_value: Any = True) -> Self:
        """
        Bind an event to a widget.

        Args:
            event (str): the event to bind
            command (Callable|None): the command to execute when the event is triggered
            require_hover (bool, optional): whether the event should be triggered only when the mouse is over the widget
            widget_boolean_value (Callable|None): an attribute/function that returns a boolean value to check for the
                required value
            required_value_for_widget_boolean_value (Any, optional): the value to check for in the widget_boolean_value

        Returns:
            Self (Self): This widget instance to allow method chaining.
        """
        if command is None:
            self.unbind(event)
            return self
        if widget_boolean_value and not callable(widget_boolean_value):
            print(
                'Please use this bind function as follows: '
                'entry.bind("<TAB>", lambda: print(1), widget_boolean_value=lambda: entry.focused)'
            )
        self._bindings[event] = {
            "command": command, "require_hover": require_hover,
            "widget_boolean_value": widget_boolean_value,
            "required_value_for_widget_boolean_value": required_value_for_widget_boolean_value
        }
        return self

    def trigger_event(self, event: binding, *args: Any, **kwargs: Any) -> None:
        """
        Internally used to trigger events.

        Args:
            event (str): the event to check for
            *args (Any, optional): additional keyword arguments to pass to the command
            **kwargs (Any, optional): additional arguments to pass to the command
        """
        if event in self._bindings:
            binding_data = self._bindings[event]
            command = binding_data["command"]
            require_hover = binding_data["require_hover"]
            widget_boolean_value = binding_data["widget_boolean_value"]
            required_value_for_widget_boolean_value = binding_data["required_value_for_widget_boolean_value"]
            if not require_hover or misc._is_point_over_widget(self, pygame.mouse.get_pos()):
                value = widget_boolean_value() if callable(widget_boolean_value) else widget_boolean_value
                if value is None or value==required_value_for_widget_boolean_value:
                    try:
                        command(self, *args, **kwargs)
                    except TypeError:
                        command(*args, **kwargs)

    def unbind(self, event: binding) -> Self:
        """
        Unbind an event from a widget.

        Args:
            event (str): the event to unbind

        Returns:
            Self (Self): This widget instance to allow method chaining.
        """
        if event in self._bindings:
            del self._bindings[event]
        return self

    def unbind_all(self) -> Self:
        """
        Unbinds all bindings from a widget.

        Returns:
            Self (Self): This widget instance to allow method chaining.
        """
        self._bindings.clear()
        return self

    def place(self, x: int, y: int, mode: str = "px", suppress_anchor: bool = False) -> Self:
        """
        Place a widget on the screen at specific coordinate. This function will consider the anchor that was set with
        anchor_x and anchor_y by default. If suppress_anchor is True, the anchor will be ignored.

        Args:
            x (int): the x coordinate
            y (int): the y coordinate
            mode (str, optional): the mode to use for the coordinates (default: px)
                (options: px, %, percent, percentage)
            suppress_anchor (bool, optional): whether to ignore the anchors (default: False)

        Returns:
            Self (Self): This widget instance to allow method chaining.
        """
        if mode=="px":
            self._x = x
            self._y = y
        elif mode in ("%", "percent", "percentage"):
            screen_width = misc._pg.get_width()
            screen_height = misc._pg.get_height()
            self._x = int(x*screen_width/100)
            self._y = int(y*screen_height/100)
        else:
            self._x = x
            self._y = y
            print(f"Invalid Mode: {mode}\nFallback: px")
        if not suppress_anchor:
            anchor_offset = [0, 0]
            if self._anchor_x=="left":
                anchor_offset[0] = 0
            elif self._anchor_x=="center":
                anchor_offset[0] = self.width//2
            elif self._anchor_x=="right":
                anchor_offset[0] = self.width
            if self._anchor_y=="top":
                anchor_offset[1] = 0
            elif self._anchor_y=="center":
                anchor_offset[1] = self.height//2
            elif self._anchor_y=="bottom":
                anchor_offset[1] = self.height
            self.x -= anchor_offset[0]
            self.y -= anchor_offset[1]
        self._rect = pygame.Rect(self._x, self._y, self.width, self.height)
        self._needs_transform = True
        return self

    def anchor(self, anchor_x: str, anchor_y: str) -> Self:
        """
        Set an anchor to the widget that should be used when using .place on it.

        Args:
            anchor_x (str): the x anchor (options: left, center, right)
            anchor_y (str): the y anchor (options: top, center, bottom)

        Returns:
            Self (Self): This widget instance to allow method chaining.
        """
        self._anchor_x = anchor_x
        self._anchor_y = anchor_y
        self.place(self._x, self._y)
        return self

    def grid(self, screen: easypygamewidgets.Screen, row: int, column: int, rowspan: int = 1,
             columnspan: int = 1) -> Self:
        """
        Place a widget on the screen using a grid system. This function will ignore the anchor that was set with
        .anchor.

        Args:
            screen (easypygamewidget.Screen): the screen that should be used as a grid
            row (int): the row in which is should be placed
            column (int): the column in which is should be placed
            rowspan (int, optional): the number of rows the widget should span (default: 1)
            columnspan (int, optional): the number of columns the widget should span (default: 1)

        Returns:
            Self (Self): This widget instance to allow method chaining.
        """
        if rowspan<1:
            rowspan = 1
        if columnspan<1:
            columnspan = 1
        if hasattr(self, "set_screen"):
            self.set_screen(screen)
        self._grid_row = row
        self._grid_column = column
        self._grid_rowspan = rowspan
        self._grid_columnspan = columnspan
        screen.recalculate_grid()
        return self

    def remove_grid(self) -> Self:
        """
        Remove the grid bounding from a widget. This will not move the widget to a different position. The widget
        will just not be part of the grid system anymore. -> It won't replace when resizing the grid.

        Returns:
            Self (Self): This widget instance to allow method chaining.
        """
        if hasattr(self, "_grid_row"):
            del self._grid_row
            del self._grid_column
            del self._grid_rowspan
            del self._grid_columnspan
        screen = getattr(self, "screen", None)
        if screen is not None:
            screen.recalculate_grid()
        return self

    def _draw(self, surface: pygame.Surface) -> None:
        """
        Internally used to draw the widget.

        Args:
            surface (pygame.Surface): The surface to draw the widget on.
        """
        ...

    def _react(self, event=None) -> None:
        """
        Internally used to react to events.

        Args:
            event (pygame.Event, optional): The event to react to.
        """
        ...


class Tooltipable:
    """A template to add tooltip functionality to a widget."""

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
                active_unpressed_background_color=self._active_unpressed_background_color,
                active_unpressed_border_color=self._active_unpressed_border_color,
                disabled_unpressed_text_color=self._disabled_unpressed_text_color,
                disabled_unpressed_background_color=self._disabled_unpressed_background_color,
                disabled_unpressed_border_color=self._disabled_unpressed_border_color,
                active_hover_text_color=self._active_hover_text_color,
                active_hover_background_color=self._active_hover_background_color,
                active_hover_border_color=self._active_hover_border_color,
                disabled_hover_text_color=self._disabled_hover_text_color,
                disabled_hover_background_color=self._disabled_hover_background_color,
                disabled_hover_border_color=self._disabled_hover_border_color,
                active_pressed_text_color=self._active_pressed_text_color,
                active_pressed_background_color=self._active_pressed_background_color,
                active_pressed_border_color=self._active_pressed_border_color
            )
        return self

    def remove_tooltip(self) -> Self:
        """
        Unbind a tooltip from a widget.

        Returns:
            Self (Self): This widget instance to allow method chaining.
        """
        if self._tooltip:
            self._tooltip._widgets.remove(self)
            self._tooltip.visible = False
            self._tooltip = None
        return self


class Screenable:
    """A template to add screen functionality to a widget."""

    def set_screen(self, screen: easypygamewidgets.Screen) -> Self:
        """
        Bind a screen to a widget.

        Args:
            screen (easypygamewidgets.Screen): The screen to bind to the widget.

        Returns:
            Self (Self): This widget instance to allow method chaining.
        """
        screen.add_widget(self)
        return self

    def remove_screen(self) -> Self:
        """
        Unbind the screen from a widget.

        Returns:
            Self (Self): This widget instance to allow method chaining.
        """
        self._screen.remove_widget(self)
        return self

    def hide(self) -> Self:
        """
        Hide the widget this method is used one.

        Return:
            Self (Self): This widget instance to allow method chaining.
        """
        self.visible = False
        return self

    def show(self) -> Self:
        """
        Hide the widget this method is used one.

        Return:
            Self (Self): This widget instance to allow method chaining.
        """
        self.visible = True
        return self


class Deletable:
    """A template to add deletion functionality to a widget."""

    def delete(self) -> None:
        """Delete a widget from the screen and internal list."""
        self._alive = False
        if self in misc._all_widgets: misc._all_widgets.remove(self)
        if getattr(self, "_tooltip", None): self._tooltip.visible = False
        misc._animations[:] = [a for a in misc._animations if a._target is not self]
        if getattr(self, "_screen", None) is not None: self.remove_screen()


class Clonable:
    """A template to add cloning functionality to a widget."""

    def clone(self) -> Self:
        """
        Clones the widget.

        Returns:
            Self: the cloned widget
        """
        copied_widget = copy.deepcopy(self)
        misc._all_widgets.append(copied_widget)
        misc._resort_layers()
        return copied_widget


class Animatable:
    """A template to add animation functionality to a widget."""

    def animate(self, *, duration: float | int = 0.3, easing: Callable = ease_out_quint, on_finish: Callable | None = None,
                **kwargs: Unpack[AnimatableAttributes]) -> Animation:
        """
        Create an animation.

        Args:
            duration (float | int): the duration of the animation in seconds. defaults to 0.3
            easing (Callable): the easing function to use. defaults to ease_out_quint
            on_finish (Callable | None): the function to call when the animation is finished. defaults to None
            **kwargs (Unpack[AnimatableAttributes]): the attributes to animate

        Returns:
            Animation: the animation object for the last attribute in kwargs
                       This is the object that'll trigger the on_finish function.

        Raises:
            ValueError: if no attributes that can be animated are provided
        """
        if not kwargs: raise ValueError(f"{self.__class__.__name__} requires at least one attribute on their animate() call that can be animated.")
        misc._animations[:] = [a for a in misc._animations if not (a._target is self and a._attr in kwargs)]
        frames = [Animation(self, attr=attr, to=to, duration=duration, easing=easing) for attr, to in kwargs.items()]
        misc._animations.extend(frames)
        frames[-1]._on_finish = on_finish
        return frames[-1]