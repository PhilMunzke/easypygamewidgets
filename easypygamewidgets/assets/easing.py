# easing.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets
"""This file contains a collection of easing functions for easypygamewidgets."""

import math

# code from https://easings.net (TypeScript)
_C1: float = 1.70158
_C2: float = _C1*1.525
_C3: float = _C1+1
_C4: float = 2*math.pi/3
_C5: float = 2*math.pi/4.5
_N1: float = 7.5625
_D1: float = 2.75


def linear(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return t


def ease_in_sine(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 1-math.cos(t*math.pi/2)


def ease_out_sine(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return math.sin(t*math.pi/2)


def ease_in_out_sine(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return -(math.cos(t*math.pi)-1)/2


def ease_in_quad(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return t*t


def ease_out_quad(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 1-(1-t)*(1-t)


def ease_in_out_quad(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 2*t*t if t<0.5 else 1-math.pow(-2*t+2, 2)/2


def ease_in_cubic(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return t*t*t


def ease_out_cubic(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 1-math.pow(1-t, 3)


def ease_in_out_cubic(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 4*t*t*t if t<0.5 else 1-math.pow(-2*t+2, 3)/2


def ease_in_quart(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return t*t*t*t


def ease_out_quart(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 1-math.pow(1-t, 4)


def ease_in_out_quart(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 8*t*t*t*t if t<0.5 else 1-math.pow(-2*t+2, 4)/2


def ease_in_quint(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return t*t*t*t*t


def ease_out_quint(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 1-math.pow(1-t, 5)


def ease_in_out_quint(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 16*t*t*t*t*t if t<0.5 else 1-math.pow(-2*t+2, 5)/2


def ease_in_expo(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 0 if t==0 else math.pow(2, 10*t-10)


def ease_out_expo(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 1 if t==1 else 1-math.pow(2, -10*t)


def ease_in_out_expo(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 0 if t==0 else 1 if t==1 else math.pow(2, 20*t-10)/2 if t<0.5 else (2-math.pow(2, -20*t+10))/2


def ease_in_circ(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 1-math.sqrt(1-math.pow(t, 2))


def ease_out_circ(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return math.sqrt(1-math.pow(t-1, 2))


def ease_in_out_circ(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return (1-math.sqrt(1-math.pow(2*t, 2)))/2 if t<0.5 else (math.sqrt(1-math.pow(-2*t+2, 2))+1)/2


def ease_in_back(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return _C3*t*t*t-_C1*t*t


def ease_out_back(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 1+_C3*math.pow(t-1, 3)+_C1*math.pow(t-1, 2)


def ease_in_out_back(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return (math.pow(2*t, 2)*((_C2+1)*2*t-_C2))/2 if t<0.5 else (math.pow(2*t-2, 2)*((_C2+1)*(t*2-2)+_C2)+2)/2


def ease_in_elastic(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 0 if t==0 else 1 if t==1 else -math.pow(2, 10*t-10)*math.sin((t*10-10.75)*_C4)


def ease_out_elastic(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 0 if t==0 else 1 if t==1 else math.pow(2, -10*t)*math.sin((t*10-0.75)*_C4)+1


def ease_in_out_elastic(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    if t in (0, 1): return 0 if t==0 else 1
    return -(math.pow(2, 20*t-10)*math.sin((20*t-11.125)*_C5))/2 if t<0.5 else (math.pow(2, -20*t+10)*math.sin((20*t-11.125)*_C5))/2+1


def ease_in_bounce(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return 1-ease_out_bounce(1-t)


def ease_out_bounce(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    if t<1/_D1: return _N1*t*t
    elif t<2/_D1: return _N1*(t-1.5/_D1)**2+0.75
    elif t<2.5/_D1: return _N1*(t-2.25/_D1)**2+0.9375
    else: return _N1*(t-2.625/_D1)**2+0.984375


def ease_in_out_bounce(t: float | int) -> float | int:
    """easing function

    Args:
        t (float | int): the normalized time value (0 <= t <= 1)

    Returns:
        float | int: the eased value (0 <= t <= 1)
    """
    return (1-ease_out_bounce(1-2*t))/2 if t<0.5 else (1+ease_out_bounce(2*t-1))/2