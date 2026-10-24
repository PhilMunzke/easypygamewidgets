# animation.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets
"""the animation system for easypygamewidgets"""

from typing import Callable

from .assets.easing import ease_out_quint


class Animation:
    """An animation object that can be used to animate a widget's attributes."""

    def __init__(self, target: "Animatable", attr: str, to, duration: float | int = 0.3, easing: Callable = ease_out_quint,
                 on_finish: Callable | None = None) -> None:
        self._target = target
        self._attr = attr
        self._to = to
        self._duration = duration
        self._easing = easing
        self._on_finish = on_finish
        self._t = 0
        self._start = getattr(target, attr)

    def update(self, dt: float | int) -> bool:
        """
        updates the animation

        Args:
            dt (float | int): the time elapsed since the last update

        Returns:
            bool: True if the animation is finished otherwise False
        """
        self._t = min(self._t+dt/max(self._duration, 0.001), 1)
        value = self._start+(self._to-self._start)*self._easing(self._t)
        setattr(self._target, self._attr, value)
        return self._t>=1