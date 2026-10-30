# animation.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets
"""the animation system for easypygamewidgets"""

from typing import Any, Callable, Unpack

from .assets.AttributeHints import AnimatableAttributes
from .assets.easing import ease_out_quint


class _Tween:
    """a helper class for easing calculations"""

    def __init__(self, target: "Animatable", attr: str, to: float | int, duration: float | int, easing: Callable) -> None:
        self._target = target
        self._attr = attr
        self._to = to
        self._duration = duration
        self._easing = easing
        self._t = 0
        self._from = None

    def _update(self, dt: float | int) -> bool:
        """
        Internally used to update the animation.

        Args:
            dt (float | int): the time elapsed since the last update

        Returns:
            bool: True if the animation is finished otherwise False
        """
        self._t = min(self._t+dt/max(self._duration, 0.001), 1)
        value = self._from+(self._to-self._from)*self._easing(self._t)
        setattr(self._target, self._attr, value)
        return self._t>=1

    def _start(self) -> None:
        """Internally used to get the current value of the attribute."""
        self._from = getattr(self._target, self._attr)
        self._t = 0

    def _reset(self) -> None:
        """Internally used to play the animation again."""
        self._t = 0


class _Chain:
    """a helper class for animation chaining"""

    def __init__(self) -> None:
        self.steps = []
        self.queue = None
        self.loop_keys = None

    def _next_step(self) -> "Animation | None":
        """
        Internally used to get the next frame of the animation that needs to be played.

        Returns:
             Animation: the next step
             None: whether the chain is finished
        """
        if self.queue is None: self.queue = self.steps[1:]
        if not self.queue and self.loop_keys is not None: self.queue = self._selected()
        if not self.queue: return None
        step = self.queue.pop(0)
        step._rewind()
        return step

    def _selected(self) -> list["Animation"]:
        """
        Internally used to convert the selected keys into steps that need to be repeated.

        Returns:
            list[Animation]: the selected steps in order

        Raises:
             IndexError: if an index is out of range
        """
        idx = range(len(self.steps))
        chosen = set()
        for key in self.loop_keys or (): chosen.update(idx[key] if isinstance(key, slice) else [idx[key]])
        return [self.steps[i] for i in sorted(chosen)]


class Animation:
    """An object that can be used to animate a widget's attributes."""

    def __init__(self, target: "Animatable", attr: dict[str, Any], duration: float | int = 0.3, easing: Callable = ease_out_quint,
                 on_finish: Callable | None = None, delay: float | int = 0, repeat: int = 0, repeat_delay: float | int = 0,
                 looping: bool = False, chain: _Chain | None = None) -> None:
        self._target = target
        self._attr = attr.keys()
        self._tweens = [_Tween(target, attribute, to, duration, easing) for attribute, to in attr.items()]
        self._on_finish = on_finish
        self._delay = delay
        self._repeat = repeat
        self._repeat_delay = repeat_delay
        self._looping = looping
        self._chain = chain or _Chain()
        self._chain.steps.append(self)
        self._rewind()

    def _rewind(self) -> None:
        """Internally used to reset the animation."""
        self._wait = self._delay
        self._repeats_left = self._repeat
        self._started = False

    def _update(self, dt: float | int) -> bool:
        """
        Internally used to update the animation.

        Args:
            dt (float | int): the time elapsed since the last update

        Returns:
            bool: True if the animation is finished otherwise False
        """
        if self._wait>0:
            self._wait -= dt
            if self._wait>0: return False
            dt, self._wait = -self._wait, 0
        if not self._started:
            for tween in self._tweens: tween._start()
            self._started = True

        finished = all([tween._update(dt) for tween in self._tweens])
        if not finished: return False

        if self._looping or self._repeats_left>0:
            if not self._looping: self._repeats_left -= 1
            self._wait = self._repeat_delay
            for tween in self._tweens: tween._reset()
            return False
        return True

    def then(self, *, duration: float | int = 0.3, easing: Callable = ease_out_quint, on_finish: Callable | None = None, delay: float | int = 0,
             repeat: int = 0, repeat_delay: float | int = 0, looping: bool = False, **attributes: Unpack[AnimatableAttributes]) -> "Animation":
        """
        This function adds an animation to the queue which will play after the previous animation has finished.

        Args:
            duration (float | int): the duration of the animation in seconds. defaults to 0.3
            easing (Callable): the easing function to use. defaults to ease_out_quint
            on_finish (Callable | None): the function to call when the animation is finished. defaults to None
            delay (float | int): the delay before the animation starts. defaults to 0
            repeat (int): the amount of times the animation repeats. defaults to 0
            repeat_delay (float | int): the delay before the animation repeats. defaults to 0
            looping (bool): if the animation should loop. defaults to False
            **attributes (Unpack[AnimatableAttributes]): the attributes to animate

        Returns:
            Animation: the animation object

        Raises:
            ValueError: if no animatable attributes are provided or 'looping' was used before which would make the sequel animation never start
        """
        if self._chain.steps[-1]._looping:
            raise ValueError("'looping' and '.then(…)' can't be combined because the sequel animation would never start.")
        if not attributes:
            raise ValueError(f"{self.__class__.__name__} requires at least one attribute on their animate() call that can be animated.")
        if self._chain.steps[-1]._looping: raise ValueError(...)
        animation = Animation(
            self._target, attr=attributes, duration=duration, easing=easing, on_finish=on_finish, delay=delay, repeat=repeat,
            repeat_delay=repeat_delay, looping=looping, chain=self._chain
        )
        return animation

    @property
    def loop(self) -> "_LoopSelector":
        """
        This selects what animations should be looped after the last one finished playing. There are two types of looping.
        First: selecting animations to loop like list indexes
            e.g. my_button.animate(rotation=5).then(duration=1, scale=1.1).then(duration=1, scale=1).loop[1:]
            available selectors:
                [1, 5, 7]
                [2:]
                [:4]
                [1:5]
                or a combination of them: [:3, 5, 7:10, 13:]

                Type square brackets to use index looping.
        Second: a plain call that loops everything
            e.g. my_button.loop()

            Type parentheses to looping everything.

        Returns:
            _LoopSelector: the loop selector object that is used to use the __getitem__ or __call__ functions
        """
        return _LoopSelector(self)


class _LoopSelector:
    """allows .loop() and .loop[…]"""

    def __init__(self, animation) -> None:
        self._animation = animation

    def __call__(self) -> Animation:
        """
        Calling this will loop all animations.

        Returns:
            Animation: the animation this was called on
        """
        return self[:]

    def __getitem__(self, position: int | slice) -> Animation:
        """
        Calling this will repeat the selected parts.

        Args:
            position (int | slice): the index or indexes of the parts to repeat

        Returns:
            Animation: the animation this was called on
        """
        self._animation._chain.loop_keys = position if isinstance(position, tuple) else (position,)
        return self._animation