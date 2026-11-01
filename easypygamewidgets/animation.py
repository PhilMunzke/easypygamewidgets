# animation.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets
"""the animation system for easypygamewidgets"""
import json
import os
from typing import Any, Callable, TYPE_CHECKING, Unpack

from .assets.AttributeHints import AnimatableAttributes
from .assets.easing import _get_easing_call, ease_out_quint

_ANIMATION_DEFAULTS: dict[str, float | int | str | None | bool] = {
    "duration": 0.3,
    "easing": "ease-out-quint",
    "on_finish": None,
    "delay": 0,
    "repeat": 0,
    "repeat_delay": 0,
    "loop": False
}
_ANIMATION_OPTIONS: tuple[str] = ("duration", "easing", "on_finish", "delay", "repeat", "repeat_delay")

if TYPE_CHECKING:
    from .masterWidgets import AnimatableCore


def _resolve_value(value: Any) -> Any:
    """
    Internally used to get the current value of a function. Static values will just be returned like they were before.

    Args:
        value (Any): the value that should be checked for an update

    Returns:
        Any: the updated value
    """
    return value() if callable(value) else value


class _Tween:
    """a helper class for easing calculations"""

    def __init__(self, target: "AnimatableCore", attr: str, to: float | int | Callable, easing: Callable) -> None:
        self._target = target
        self._attr = attr
        self._to = to
        self._easing = easing
        self._t = 0
        self._from = None
        self._resolved_to = None
        self._needs_resolve = True

    def _update(self, dt: float | int) -> bool:
        """
        Internally used to update the animation.

        Args:
            dt (float | int): the time elapsed since the last update

        Returns:
            bool: True if the animation is finished otherwise False
        """
        if self._needs_resolve:
            self._resolved_to = _resolve_value(self._to)
            self._needs_resolve = False
        self._t = min(self._t+dt/max(self._duration, 0.001), 1)
        value = self._from+(self._resolved_to-self._from)*self._easing(self._t)
        setattr(self._target, self._attr, value)
        return self._t>=1

    def _start(self) -> None:
        """Internally used to get the current value of the attribute."""
        self._from = getattr(self._target, self._attr)
        self._t = 0
        self._needs_resolve = True

    def _reset(self) -> None:
        """Internally used to play the animation again."""
        self._t = 0
        self._needs_resolve = True


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
    """
    An object that can be used to animate a widget's attributes. An attribute value can be a static value or a function which will be called
    everytime before it's used. The function should return the value and not take any arguments. Only the function for the 'easing' attribute
    receives the time parameter. When using functions it's important to pass the 'functions' argument to the '.animate(…)' call as a dictionary.

    If working with animation files, the file structure should look like this:
    {
      "animations": [
        {
          "scale": 1.2,
          "duration": "get_duration", <- This is the name of a function that is defined in the .py file.
          "easing": "ease-in-out"
        },
        {
          "scale": 1,
          "duration": "get_duration",
          "easing": "ease-in-out"
        }
      ],
      "loop": true
    }

    'loop' can be a boolean to loop everything or a string to loop a specific part of the animation like list indexes work
    e.g. "2:5" or "2:10:2"
    """

    def __init__(self, target: "AnimatableCore", attr: dict[str, Any], duration: float | int = 0.3, easing: Callable = ease_out_quint,
                 on_finish: Callable | None = None, delay: float | int = 0, repeat: int = 0, repeat_delay: float | int = 0,
                 loop: bool = False, chain: _Chain | None = None) -> None:
        self._target = target
        self._attr = attr.keys()
        self._duration = duration
        self._tweens = [_Tween(target, attribute, to, easing) for attribute, to in attr.items()]
        self._on_finish = on_finish
        self._delay = delay
        self._repeat = repeat
        self._repeat_delay = repeat_delay
        self._loop = loop
        self._wait = 0
        self._repeats_left = 0
        self._started = False
        self._needs_resolve = True
        self._chain = chain or _Chain()
        self._chain.steps.append(self)
        if len(self._chain.steps)==1: self._rewind()  # calling '._rewind(…)' would call possible functions too early

    def _rewind(self) -> None:
        """Internally used to reset the animation."""
        self._wait = _resolve_value(self._delay)
        self._repeats_left = _resolve_value(self._repeat)
        self._started = False
        self._needs_resolve = True

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
        if self._needs_resolve:
            duration = _resolve_value(self._duration)
            for tween in self._tweens: tween._duration = duration
            self._needs_resolve = False
        if not self._started:
            for tween in self._tweens: tween._start()
            self._started = True
        finished = all([tween._update(dt) for tween in self._tweens])
        if not finished: return False
        if self._loop or self._repeats_left>0:
            if not self._loop: self._repeats_left -= 1
            self._wait = _resolve_value(self._repeat_delay)
            self._needs_resolve = True
            for tween in self._tweens: tween._reset()
            return False
        return True

    def then(self, *, duration: float | int = 0.3, easing: Callable = ease_out_quint, on_finish: Callable | None = None, delay: float | int = 0,
             repeat: int = 0, repeat_delay: float | int = 0, loop: bool = False, **attributes: Unpack[AnimatableAttributes]) -> "Animation":
        """
        This function adds an animation to the queue which will play after the previous animation has finished.

        Args:
            duration (float | int): the duration of the animation in seconds. defaults to 0.3
            easing (Callable): the easing function to use. defaults to ease_out_quint
            on_finish (Callable | None): the function to call when the animation is finished. defaults to None
            delay (float | int): the delay before the animation starts. defaults to 0
            repeat (int): the amount of times the animation repeats. defaults to 0
            repeat_delay (float | int): the delay before the animation repeats. defaults to 0
            loop (bool): if the animation should loop. defaults to False
            **attributes (Unpack[AnimatableAttributes]): the attributes to animate

        Returns:
            Animation: the animation object

        Raises:
            ValueError: if no animatable attributes are provided or 'loop' was used before which would make the sequel animation never start
        """
        if self._chain.steps[-1]._loop:
            raise ValueError("'loop' and '.then(…)' can't be combined because the sequel animation would never start.")
        if not attributes:
            raise ValueError(f"{self.__class__.__name__} requires at least one attribute on their 'animate(…)' call that can be animated.")
        animation = Animation(
            self._target, attr=attributes, duration=duration, easing=easing, on_finish=on_finish, delay=delay, repeat=repeat,
            repeat_delay=repeat_delay, loop=loop, chain=self._chain
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
            Type parentheses to loop everything.

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


def _convert_loop_key(loop: bool | str) -> tuple | None:
    """
    Internally used to convert the 'loop' key from an animation file into a usable form for the '_Chain' class.

    Args:
        loop (bool | str): the value that is stored in the 'loop' key

    Returns:
        tuple | None: the converted value
    """
    if isinstance(loop, bool): return (slice(None),) if loop else None
    keys = []
    for part in loop.split(","):
        part = part.strip()
        if ":" in part:
            bits = part.split(":")
            try: keys.append(slice(*[int(bit) if bit.strip() else None for bit in bits]))
            except ValueError: raise ValueError(f"Invalid loop selector: {part}")
        else:
            try: keys.append(int(part))
            except ValueError: raise ValueError(f"Invalid loop selector: {part}")
    return tuple(keys)


def _get_function(value: Any, functions: dict[str, Callable] | None) -> Any:
    """
    This function looks the function name up and returns the corresponding function.

    Args:
        value (Any): the function name
        functions (dict[str, Callable] | None): a dictionary of the function names and their corresponding functions

    Returns:
        value (Any): the passed value if it's not a function name or if the 'functions' attribute is empty on the '.animate(…)' call
        Callable: the function that is linked to the function name
    """
    if functions is None: return value
    if value in functions: return functions[value]
    return value


def _load_animation(path: str | os.PathLike, target: "AnimatableCore", functions: dict[str, Callable] | None = None) -> Animation:
    """
    Load an animation file that contains the animations for a widget.

    Example file:
    {
      "animations": [
        {
          "scale": 1.2,
          "duration": "get_duration", <- This is the name of a function that is defined in the .py file.
          "easing": "ease-in-out"
        },
        {
          "scale": 1,
          "duration": "get_duration",
          "easing": "ease-in-out"
        }
      ],
      "loop": true
    }

    'loop' can be a boolean to loop everything or a string to loop a specific part of the animation like list indexes work
    e.g. "2:5" or "2:10:2"

    Every value can be a static value or a function which will be called every time before it's used. The function should return the value
    and not take any arguments. Only the function for the 'easing' attribute receives the time parameter. When using functions it's important to pass
    the 'functions' argument to the '.animate(…)' call as a dictionary.


    Args:
        path (str | os.PathLike): the path to the JSON file
        target (AnimatableCore): the object to animate
        functions (dict[str, Callable] | None): a dictionary of function references

    Returns:
        Animation: the animation object

    Raises:
        ValueError: If the specified path does not exist or is not a valid JSON file.
    """
    path = os.fspath(path)
    if not path.endswith(".json"): raise ValueError("The specified path is not a JSON file.")
    if not os.path.exists(path): raise ValueError("The specified path does not exist.")
    with open(path) as f: data = json.load(f)
    if not isinstance(data, dict): raise ValueError("The specified path does not use the correct JSON format.")
    if not isinstance(data.get("animations"), list): raise ValueError("The specified path does not use the correct JSON format.")
    if not isinstance(data.get("loop", False), (bool, str)): raise ValueError("The specified path does not use the correct JSON format.")
    animations = data["animations"]
    defaults = {**_ANIMATION_DEFAULTS, **{keyword: data[keyword] for keyword in _ANIMATION_OPTIONS if keyword in data}}
    first = None
    for animation in animations:
        if not isinstance(animation, dict): raise ValueError("The specified path does not use the correct JSON format.")
        animation = dict(animation)
        options = {**defaults, **{keyword: animation.pop(keyword) for keyword in list(animation) if keyword in _ANIMATION_OPTIONS}}
        if not animation: raise ValueError(f"Every animation requires at least one attribute on their 'animate(…)' call that can be animated.")
        options = {keyword: _get_function(value, functions) for keyword, value in options.items()}
        animation = {keyword: _get_function(value, functions) for keyword, value in animation.items()}
        if not callable(options["easing"]): options["easing"] = _get_easing_call([options["easing"]])
        if first is None: first = Animation(target, attr=animation, **options)
        else: first.then(**options, **animation)
    first._chain.loop_keys = _convert_loop_key(data.get("loop", False))
    try:
        if first._chain.loop_keys is not None: first._chain._selected()
    except IndexError: raise IndexError("A loop index is out of range.")
    return first