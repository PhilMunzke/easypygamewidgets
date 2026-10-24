# epw_types.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets
"""This file contains a collection of types for easypygamewidgets."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

color = tuple[int, int, int, int] | tuple[int, int, int] | list[int] | str | None


@dataclass
class ScheduledTask:
    """A scheduled task that is executed after a certain amount of time."""
    function: Callable[..., Any]
    time_to_execute: int