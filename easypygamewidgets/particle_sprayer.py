# particle_sprayer.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets
"""A particle sprayer for pygame."""

from __future__ import annotations

import random
from collections.abc import Sequence
from typing import Any, Self, TYPE_CHECKING, Unpack

import pygame

from easypygamewidgets import misc
from easypygamewidgets.assets import AttributeHints
from easypygamewidgets.assets.events import *
from easypygamewidgets.assets.theme import _style_dic as sd, _themed
from easypygamewidgets.masterWidgets import Animatable, Clonable, Deletable, Screenable, Widget
from easypygamewidgets.particle import Particle

if TYPE_CHECKING: import easypygamewidgets

pygame.init()


class ParticleSprayer(Widget, Screenable, Deletable, Clonable, Animatable):
    """Initializes a particle sprayer for pygame."""

    @_themed
    def __init__(self,
                 screen: easypygamewidgets.Screen | None = None,
                 state: str | None = None, width: int | float = 1, height: int | float = 1,
                 active_hover_cursor: pygame.Cursor | int | None = sd["active_hover_cursor"],
                 disabled_hover_cursor: pygame.Cursor | int | None = sd["disabled_hover_cursor"],
                 active_pressed_cursor: pygame.Cursor | int | None = sd["active_pressed_cursor"],
                 layer: int = sd["layer"],
                 alpha_based_collision_system: bool = sd["alpha_based_collision_system"],
                 anchor_x: str = sd["anchor_x"], anchor_y: str = sd["anchor_y"], visible: bool = sd["visible"],
                 spraying: bool = sd["spraying"], repeated_spraying: int | bool = sd["repeated_spraying"],
                 particle_interpolate: bool = sd["particle_interpolate"],
                 particle_color: Any | Sequence[Any | Sequence[Any]] = sd["particle_color"],
                 particle_texture: Any | Sequence[Any | Sequence[Any]] = sd["particle_texture"],
                 particle_amount: Any | Sequence[Any | Sequence[Any]] = sd["particle_amount"],
                 particle_speed: Any | Sequence[Any | Sequence[Any]] = sd["particle_speed"],
                 particle_duration: Any | Sequence[Any | Sequence[Any]] = sd["particle_duration"],
                 particle_size: Any | Sequence[Any | Sequence[Any]] = sd["particle_size"],
                 particle_rotation: Any | Sequence[Any | Sequence[Any]] = sd["particle_rotation"],
                 particle_gravity: Any | Sequence[Any | Sequence[Any]] = sd["particle_gravity"],
                 particle_direction: Any | Sequence[Any | Sequence[Any]] = sd["particle_direction"],
                 particle_alpha_keyframes: Sequence[tuple] = sd["particle_alpha_keyframes"],
                 particle_avoid_mouse: bool = sd["particle_avoid_mouse"],
                 particle_physics: bool = sd["particle_physics"],
                 particle_blend_mode: int = sd["particle_blend_mode"],
                 particle_split_effect: bool = sd["particle_split_effect"],
                 particle_split_effect_recursion_amount: int = sd["particle_split_effect_recursion_amount"],
                 particle_split_color: Any | Sequence[Any | Sequence[Any]] = sd["particle_split_effect_color"],
                 particle_split_texture: Any | Sequence[Any | Sequence[Any]] = sd["particle_split_effect_texture"],
                 particle_split_effect_amount: Any | Sequence[Any | Sequence[Any]] = sd["particle_split_effect_amount"],
                 particle_split_speed: Any | Sequence[Any | Sequence[Any]] = sd["particle_split_effect_speed"],
                 particle_split_duration: Any | Sequence[Any | Sequence[Any]] = sd["particle_split_duration"],
                 particle_split_size: Any | Sequence[Any | Sequence[Any]] = sd["particle_split_effect_size"],
                 particle_split_rotation: Any | Sequence[Any | Sequence[Any]] = sd["particle_split_rotation"],
                 particle_split_gravity: Any | Sequence[Any | Sequence[Any]] = sd["particle_split_effect_gravity"],
                 particle_split_direction: Any | Sequence[Any | Sequence[Any]] = sd["particle_split_effect_direction"],
                 particle_split_alpha_keyframes: Sequence[tuple] = sd["particle_split_effect_alpha_keyframes"],
                 data: Any = None) -> None:
        """
        Initializes a ParticleSprayer widget.

        Every 'particle_*' and 'particle_split_*' attribute accept either a plain value or a Sequence describing how that attribute changes over
        the time. The first element of the Sequence is the value that is used on the particle's first frame. 'particle_duration' decides
        how many frames are displayed before the value continues to the next element. If an element is another Sequence, one value is
        randomly picked from it once when the particle is spawned and never changes during the particle's lifetime.

        Args:
            screen: The Screen this sprayer is attached to. If None, the sprayer is created without a parent screen.
            state: Initial state, 'enabled' or 'disabled'. Defaults to 'enabled' if not given.
            width: The width of the area particles can spawn in.
            height: The height of the area particles can spawn in.
            active_hover_cursor: Custom cursor shown on hover while enabled.
            disabled_hover_cursor: Custom cursor shown on hover while disabled.
            active_pressed_cursor: Custom cursor shown while pressed.
            layer: Draw order layer; higher values draw on top.
            alpha_based_collision_system: Use a pixel alpha test to check for collisions instead of math calculations.
            anchor_x: Horizontal anchor point: 'left', 'center', or 'right'.
            anchor_y: Vertical anchor point: 'top', 'center', or 'bottom'.
            visible: Initial visibility. Defaults to True.
            spraying: If True, the sprayer starts spraying particles immediately.
            repeated_spraying: If True (or an int amount of times), the sprayer keeps spawning new particles instead of spraying only once.
            particle_interpolate: If True, the numeric and color schedules blend smoothly from one element to the next instead of jumping to it.
            particle_color: The particle's color over its lifetime (see the schedule rules above).
            particle_texture: The particle's texture over its lifetime. If None for a frame, the particle is drawn as a filled circle using
                particle_color instead.
            particle_amount: The amount of particles spawned per spray.
            particle_speed: The particle's travel speed over its lifetime.
            particle_duration: The amount of frames a particle lives for.
            particle_size: The particle's size (diameter in pixels) over its lifetime.
            particle_rotation: The particle's rotation (in degrees) over its lifetime.
            particle_gravity: The particle's downward acceleration over its lifetime.
            particle_direction: The particle's travel direction (in degrees) over its lifetime.
            particle_alpha_keyframes: Controls the particle's opacity over its lifetime. A Sequence of
                (life, alpha, fade duration) triples:
                    - life: how 'old' the particle is (0 = just spawned, 1 = end of life). This can also be a Sequence with two values in which case a
                        random value is picked within this range
                    - alpha: the opacity (0-255) the particle should have at the end which also accepts a range like life does
                    - fade duration: how many frames the fade should take and this also accepts a range like life does
            particle_avoid_mouse: If True, particles steer away from the mouse cursor.
            particle_physics: If True, particles can split according to the 'particle_split_*' settings.
            particle_blend_mode: The pygame special_flags value used to draw the particles (e.g. pygame.BLEND_RGB_ADD for a glowing look). Defaults to
                0 which is normal blending.
            particle_split_effect: If True, particles split into new particles using the 'particle_split_*' settings instead of simply disappearing.
            particle_split_effect_recursion_amount: The amount of times the split effect should be given to the split particles
            particle_split_color: The split particle's color over its lifetime (see the schedule rules above).
            particle_split_texture: The split particle's texture over its lifetime.
            particle_split_effect_amount: The amount of particles spawned per split.
            particle_split_speed: The split particle's travel speed over its lifetime.
            particle_split_duration: The amount of frames a split particle lives for.
            particle_split_size: The split particle's size (diameter in pixels) over its lifetime.
            particle_split_rotation: The split particle's rotation (in degrees) over its lifetime.
            particle_split_gravity: The split particle's downward acceleration over its lifetime.
            particle_split_direction: The split particle's travel direction (in degrees) over its lifetime.
            particle_split_alpha_keyframes: Controls a split particle's opacity over its lifetime (see particle_alpha_keyframes above for the format).
            data: Arbitrary user data attached to the widget.

        Raises:
            ValueError: If a *_cursor argument is given but is not a pygame.Cursor or int.
        """
        super().__init__()
        self._screen = None
        if screen:
            screen.add_widget(self)
            if state: self._state = state
        else:
            self._visible = visible
            if state: self._state = state
            else: self._state = "enabled"
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
        self._layer = layer
        self._alpha_based_collision_system = alpha_based_collision_system
        self._anchor_x = anchor_x
        self._anchor_y = anchor_y
        self._data = data
        self._width = width
        self._height = height
        self._x = 0
        self._y = 0
        self._alive = True
        self._pressed = False
        self._rect = pygame.rect.Rect(self._x, self._y, self._width, self._height)
        self._original_cursor = None
        self._drag_offset = None
        self._is_dragging = False
        self._last_checked_dragging = None
        self._bindings = {}
        self._needs_transform = True
        self._dialog = None
        self._spraying = spraying
        self._repeated_spraying = repeated_spraying
        self._particle_color = particle_color
        self._particle_texture = particle_texture
        self._particle_amount = particle_amount
        self._particle_speed = particle_speed
        self._particle_duration = particle_duration
        self._particle_size = particle_size
        self._particle_rotation = particle_rotation
        self._particle_gravity = particle_gravity
        self._particle_direction = particle_direction
        self._particle_alpha_keyframes = particle_alpha_keyframes
        self._particle_avoid_mouse = particle_avoid_mouse
        self._particle_physics = particle_physics
        self._particle_interpolate = particle_interpolate
        self._particle_blend_mode = particle_blend_mode
        self._particle_split_effect = particle_split_effect
        self._particle_split_effect_recursion_amount = particle_split_effect_recursion_amount
        self._particle_split_color = particle_split_color
        self._particle_split_texture = particle_split_texture
        self._particle_split_effect_amount = particle_split_effect_amount
        self._particle_split_speed = particle_split_speed
        self._particle_split_duration = particle_split_duration
        self._particle_split_size = particle_split_size
        self._particle_split_rotation = particle_split_rotation
        self._particle_split_gravity = particle_split_gravity
        self._particle_split_direction = particle_split_direction
        self._particle_split_alpha_keyframes = particle_split_alpha_keyframes
        self._particles: list[Particle] = []
        self._times_sprayed = 0

        misc._add_widget(self)

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = value
        misc._resort_layers()

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
    def dialog(self):
        return self._dialog

    @dialog.setter
    def dialog(self, value):
        self._dialog = value

    @property
    def spraying(self):
        return self._spraying

    @spraying.setter
    def spraying(self, value):
        self._spraying = value

    @property
    def repeated_spraying(self):
        return self._repeated_spraying

    @repeated_spraying.setter
    def repeated_spraying(self, value):
        self._repeated_spraying = value

    @property
    def particle_color(self):
        return self._particle_color

    @particle_color.setter
    def particle_color(self, value):
        self._particle_color = value

    @property
    def particle_texture(self):
        return self._particle_texture

    @particle_texture.setter
    def particle_texture(self, value):
        self._particle_texture = value

    @property
    def particle_amount(self):
        return self._particle_amount

    @particle_amount.setter
    def particle_amount(self, value):
        self._particle_amount = value

    @property
    def particle_speed(self):
        return self._particle_speed

    @particle_speed.setter
    def particle_speed(self, value):
        self._particle_speed = value

    @property
    def particle_duration(self):
        return self._particle_duration

    @particle_duration.setter
    def particle_duration(self, value):
        self._particle_duration = value

    @property
    def particle_size(self):
        return self._particle_size

    @particle_size.setter
    def particle_size(self, value):
        self._particle_size = value

    @property
    def particle_rotation(self):
        return self._particle_rotation

    @particle_rotation.setter
    def particle_rotation(self, value):
        self._particle_rotation = value

    @property
    def particle_gravity(self):
        return self._particle_gravity

    @particle_gravity.setter
    def particle_gravity(self, value):
        self._particle_gravity = value

    @property
    def particle_direction(self):
        return self._particle_direction

    @particle_direction.setter
    def particle_direction(self, value):
        self._particle_direction = value

    @property
    def particle_alpha_keyframes(self):
        return self._particle_alpha_keyframes

    @particle_alpha_keyframes.setter
    def particle_alpha_keyframes(self, value):
        self._particle_alpha_keyframes = value

    @property
    def particle_avoid_mouse(self):
        return self._particle_avoid_mouse

    @particle_avoid_mouse.setter
    def particle_avoid_mouse(self, value):
        self._particle_avoid_mouse = value

    @property
    def particle_physics(self):
        return self._particle_physics

    @particle_physics.setter
    def particle_physics(self, value):
        self._particle_physics = value

    @property
    def particle_interpolate(self):
        return self._particle_interpolate

    @particle_interpolate.setter
    def particle_interpolate(self, value):
        self._particle_interpolate = value

    @property
    def particle_blend_mode(self):
        return self._particle_blend_mode

    @particle_blend_mode.setter
    def particle_blend_mode(self, value):
        self._particle_blend_mode = value

    @property
    def particle_split_effect(self):
        return self._particle_split_effect

    @particle_split_effect.setter
    def particle_split_effect(self, value):
        self._particle_split_effect = value

    @property
    def particle_split_color(self):
        return self._particle_split_color

    @property
    def particle_split_effect_recursion_amount(self):
        return self._particle_split_effect_recursion_amount

    @particle_split_effect_recursion_amount.setter
    def particle_split_effect_recursion_amount(self, value):
        self._particle_split_effect_recursion_amount = value

    @particle_split_color.setter
    def particle_split_color(self, value):
        self._particle_split_color = value

    @property
    def particle_split_texture(self):
        return self._particle_split_texture

    @particle_split_texture.setter
    def particle_split_texture(self, value):
        self._particle_split_texture = value

    @property
    def particle_split_effect_amount(self):
        return self._particle_split_effect_amount

    @particle_split_effect_amount.setter
    def particle_split_effect_amount(self, value):
        self._particle_split_effect_amount = value

    @property
    def particle_split_speed(self):
        return self._particle_split_speed

    @particle_split_speed.setter
    def particle_split_speed(self, value):
        self._particle_split_speed = value

    @property
    def particle_split_duration(self):
        return self._particle_split_duration

    @particle_split_duration.setter
    def particle_split_duration(self, value):
        self._particle_split_duration = value

    @property
    def particle_split_size(self):
        return self._particle_split_size

    @particle_split_size.setter
    def particle_split_size(self, value):
        self._particle_split_size = value

    @property
    def particle_split_rotation(self):
        return self._particle_split_rotation

    @particle_split_rotation.setter
    def particle_split_rotation(self, value):
        self._particle_split_rotation = value

    @property
    def particle_split_gravity(self):
        return self._particle_split_gravity

    @particle_split_gravity.setter
    def particle_split_gravity(self, value):
        self._particle_split_gravity = value

    @property
    def particle_split_direction(self):
        return self._particle_split_direction

    @particle_split_direction.setter
    def particle_split_direction(self, value):
        self._particle_split_direction = value

    @property
    def particle_split_alpha_keyframes(self):
        return self._particle_split_alpha_keyframes

    @particle_split_alpha_keyframes.setter
    def particle_split_alpha_keyframes(self, value):
        self._particle_split_alpha_keyframes = value

    @property
    def particles(self):
        return self._particles

    def configure(self, **kwargs: Unpack[AttributeHints.ParticleSprayerConfig]) -> Self:
        """
        Updates one or more of the sprayer's attributes.

        Args:
            **kwargs: ParticleSprayer attributes to update as defined in AttributeHints.ParticleSprayerConfig

        Returns:
            Self (Self): This sprayer instance to allow method chaining.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        if any(k in kwargs for k in ('x', 'y', 'width', 'height', 'anchor_x', 'anchor_y',)):
            self._rect = pygame.Rect(self._x, self._y, self.width, self.height)
            self._needs_transform = True
        if 'screen' in kwargs:
            self.set_screen(kwargs["screen"])
        if 'layer' in kwargs:
            misc._resort_layers()
        return self

    def config(self, **kwargs: Unpack[AttributeHints.ParticleSprayerConfig]) -> Self:
        """
        Updates one or more of the sprayer's attributes.

        Args:
            **kwargs: ParticleSprayer attributes to update as defined in AttributeHints.ParticleSprayerConfig

        Returns:
            Self (Self): This sprayer instance to allow method chaining.
        """
        return self.configure(**kwargs)

    def start(self) -> Self:
        """
        Starts or resumes spraying particles.

        Returns:
            Self (Self): This sprayer instance to allow method chaining.
        """
        self._spraying = True
        return self

    def stop(self) -> Self:
        """
        Stops spraying new particles. Particles already spawned don't disappear immediately.

        Returns:
            Self (Self): This sprayer instance to allow method chaining.
        """
        self._spraying = False
        return self

    def _resolve_particle_schedules(self, split: bool = False, frame_count: int | None = None) -> dict[str, list]:
        """
        Internally used to resolves a particle attribute value into a fixed per-frame schedule.

        Args:
            split (bool, optional): if True, resolve the 'particle_split_*' attributes instead of the regular 'particle_*' ones.
            frame_count (int | None, optional): the amount of frames the schedule should take. If None it is taken from the duration attribute.

        Returns:
            dict[str, list]: the resolved schedule
        """
        prefix = "particle_split_" if split else "particle_"
        if frame_count is None:
            duration = getattr(self, f"{prefix}duration")
            if _is_numeric_range(duration): duration = random.uniform(duration[0], duration[1])
            frame_count = max(int(duration), 1)
        return {
            "color": _resolve_value_schedule(getattr(self, f"{prefix}color"), frame_count, self._particle_interpolate),
            "texture": _resolve_value_schedule(getattr(self, f"{prefix}texture"), frame_count),
            "speed": _resolve_value_schedule(getattr(self, f"{prefix}speed"), frame_count, self._particle_interpolate),
            "size": _resolve_value_schedule(getattr(self, f"{prefix}size"), frame_count, self._particle_interpolate),
            "rotation": _resolve_value_schedule(getattr(self, f"{prefix}rotation"), frame_count, self._particle_interpolate),
            "gravity": _resolve_value_schedule(getattr(self, f"{prefix}gravity"), frame_count, self._particle_interpolate),
            "direction": _resolve_value_schedule(getattr(self, f"{prefix}direction"), frame_count, self._particle_interpolate),
        }

    def _spawn_particles(self, x: int | float, y: int | float, split: bool = False,
                         generation: int = 1) -> list[Particle]:
        """
        Internally used to spawn particles from the sprayer.

        Args:
            x (int | float): the x position of the particles
            y (int | float): the y position of the particles
            split (bool, optional): if True, the 'particle_split_*' attributes are used instead of the regular 'particle_*' ones. Defaults to False.
            generation (int, optional): which generation this particle belongs to (1=spawned by the sprayer, 2=first split, 3=second split, …)

        Returns:
            list[Particle]: the spawned particles
        """
        amount_attr = "particle_split_effect_amount" if split else "particle_amount"
        amount = getattr(self, amount_attr)
        duration_attr = "particle_split_duration" if split else "particle_duration"
        alpha_attr = "particle_split_alpha_keyframes" if split else "particle_alpha_keyframes"
        avoid_mouse = self._particle_avoid_mouse
        physics = self._particle_physics

        new_particles = []
        for _ in range(int(amount)):
            duration = getattr(self, duration_attr)
            if _is_numeric_range(duration): duration = random.uniform(duration[0], duration[1])
            frame_count = max(int(duration), 1)
            schedules = self._resolve_particle_schedules(split=split, frame_count=frame_count)
            alpha_schedule = _resolve_alpha_schedule(getattr(self, alpha_attr), frame_count)
            if split: spawn_x, spawn_y = x, y
            else:
                spawn_x = self._x+random.uniform(0, self.width)
                spawn_y = self._y+random.uniform(0, self.height)
            particle = Particle(
                sprayer=self, x=spawn_x, y=spawn_y,
                color_schedule=schedules["color"], texture_schedule=schedules["texture"],
                speed_schedule=schedules["speed"], size_schedule=schedules["size"],
                rotation_schedule=schedules["rotation"], gravity_schedule=schedules["gravity"],
                direction_schedule=schedules["direction"], alpha_schedule=alpha_schedule,
                avoid_mouse=avoid_mouse, physics=physics, generation=generation,
                blend_mode=self._particle_blend_mode
            )
            new_particles.append(particle)
        self._particles.extend(new_particles)
        return new_particles

    def spray(self) -> Self:
        """
        Spawns one batch of particles even if 'spraying' is set to False.

        Returns:
            Self (Self): This sprayer instance to allow method chaining.
        """
        center_x = self._x+self.width//2
        center_y = self._y+self.height//2
        self._spawn_particles(center_x, center_y)
        self._times_sprayed += 1
        return self

    def _draw(self, surface: pygame.Surface) -> None:
        """
        Internally used to draw the particles.

        Args:
            surface (pygame.Surface): The surface to draw the particles on.
        """
        if not self._alive or not self._visible:
            return

        if self._spraying:
            can_spray_again = self._repeated_spraying is True or (
                    isinstance(self._repeated_spraying, int) and self._times_sprayed<self._repeated_spraying)
            if not self._particles or can_spray_again: self.spray()

        still_alive = []
        for particle in self._particles:
            updated = particle._update(misc._dt)
            if updated:
                particle._draw(surface)
                still_alive.append(particle)
            else:
                self.trigger_event(PARTICLE_DIED)
                if particle._physics and self._particle_split_effect: still_alive.extend(particle.split())
        self._particles = still_alive

    def _react(self, event: pygame.Event | None = None) -> None:
        """
        Internally used to react to events.

        Args:
            event (pygame.Event, optional): The event to react to.
        """
        if self._state!="enabled" or not self._visible:
            self._pressed = False
            return


def _is_numeric_range(item: Any) -> bool:
    """
    Internally used to check if a given value consists out of two numbers.

    Args:
        item (Any): the item which should be checked

    Returns:
        bool: whether it is fitting the criteria or not
    """
    if not isinstance(item, Sequence): item = [item]
    return (len(item)==2 and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in item))


def _lerp_value(first_color: Any, second_color: Any, lerp_by: float) -> Any:
    """
    Internally used to blend two colors or two equally long tuples out of colors.

    Args:
        first_color (Any): the first color
        second_color (Any): the second color
        lerp_by (float): the lerp value

    Returns:
        float: the blended number if both values are plain numbers
        tuple[float, ...]: the blended tuple if both values are number sequences of the same length
        None: if the values can't be blended
    """

    def _test_for_number(value: Any) -> bool:
        """
        Internally used to check if a given value is a real number.

        Args:
            value (Any): the value which should be checked

        Returns:
            bool: whether it is an integer or a float and not a boolean
        """
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    if _test_for_number(first_color) and _test_for_number(second_color): return first_color+(second_color-first_color)*lerp_by
    if (isinstance(first_color, Sequence) and isinstance(second_color, Sequence) and not isinstance(first_color, (str, bytes)) and not isinstance(
            second_color, (str, bytes)
    )
            and len(first_color)==len(second_color) and all(_test_for_number(v) for v in first_color) and all(
                _test_for_number(v) for v in second_color
            )):
        return tuple(round(x+(y-x)*lerp_by) for x, y in zip(first_color, second_color))
    return None


def _resolve_value_schedule(value: Any, duration: int | float, interpolate: bool = False) -> list[Any]:
    """
    Internally used to resolves a particle attribute value into a fixed per-frame schedule.

    'value' can be:
        - a plain value
        - a Sequence of plain values: each value is used for 'duration/len(value)' frames before continuing
        - a Sequence of Sequences: a random value is picked once from the inner Sequence
        - a (min, max) pair inside the Sequence: a random value in that range. All pairs of one attribute share the same random roll per particle so a particle keeps the same relative position inside every range

    Args:
        value (Any): this value that can be given like explained above
        duration (int | float): the amount of frames the schedule should take
        interpolate (bool): whether the value should be interpolated

    Returns:
        list[Any]: a resolved value for every frame
    """
    frame_count = max(int(duration), 1)
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)): return [value]*frame_count

    def _is_sequence(item: Any) -> bool:
        """
        Internally used to check if a given item is a Sequence.

        Args:
            item (Any): the item which should be checked

        Returns:
            bool: whether it is a Sequence or not
        """
        return isinstance(item, Sequence) and not isinstance(item, (str, bytes))

    def _is_choice_set(item: Sequence) -> bool:
        """
        Internally used to check if a given value can be used to get a random choice.

        Args:
            item (Sequence): the item which should be checked

        Returns:
            bool: whether it can be used or not
        """
        return len(item)>0 and all(_is_sequence(item) for item in item)

    shared_roll = random.random()
    resolved_steps = []
    for step in value:
        if _is_sequence(step) and _is_numeric_range(step): resolved_steps.append(step[0]+(step[1]-step[0])*shared_roll)
        elif _is_sequence(step) and _is_choice_set(step): resolved_steps.append(random.choice(step))
        else: resolved_steps.append(step)
    if not resolved_steps: return [None]*frame_count
    step_count = len(resolved_steps)
    schedule = []
    for frame in range(frame_count):
        if interpolate and step_count>1:
            position = frame*(step_count-1)/max(frame_count-1, 1)
            index = min(int(position), step_count-2)
            blended = _lerp_value(resolved_steps[index], resolved_steps[index+1], position-index)
            if blended is not None:
                schedule.append(blended)
                continue
        step_index = min(frame*step_count//frame_count, step_count-1)
        schedule.append(resolved_steps[step_index])
    return schedule


def _resolve_alpha_schedule(keyframes: Any, duration: int | float) -> list[int]:
    """
    Internally used to resolves a particle alpha value into a fixed per-frame schedule.

    'keyframes' is a Sequence of (life, alpha, fade duration):
        - life: how 'old' the particle is (0 = just spawned, 1 = end of life). This can also be a Sequence with two values in which case a random
            value is picked within this range
        - alpha: the opacity (0-255) the particle should have at the end which also accepts a range like life does
        - fade duration: how many frames the fade should take and this also accepts a range like life does
    Keyframes are applied in the given order but if the life points don't match they're sorted by them.

    Args:
        keyframes (Any): this value that can be given like explained above
        duration (int | float): the amount of frames the schedule should take

    Returns:
        list[int]: a resolved opacity for every frame
    """
    frame_count = max(int(duration), 1)
    if not keyframes: return [255]*frame_count

    def _resolve_scalar(item: Any) -> int | float:
        """
        Internally used to convert a keyframe into a number.

        Args:
            item (Any): a plain number or a Sequence of two which would result in a choice from their range

        Returns:
            int | float: the random value
        """
        return random.uniform(item[0], item[1]) if _is_numeric_range(item) else item

    resolved = []
    for life_point, alpha, fade_duration in keyframes:
        point = max(0.0, min(1.0, _resolve_scalar(life_point)))
        resolved.append((point, _resolve_scalar(alpha), max(_resolve_scalar(fade_duration), 0)))
    resolved.sort(key=lambda kf: kf[0])
    schedule = [255]*frame_count
    previous_alpha = 255.0
    previous_frame = 0
    for point, alpha, fade_duration in resolved:
        target_frame = min(int(point*frame_count), frame_count-1)
        fade_start_frame = max(int(target_frame-fade_duration), previous_frame)
        for frame in range(previous_frame, target_frame+1):
            if frame<fade_start_frame: schedule[frame] = int(previous_alpha)
            else:
                span = target_frame-fade_start_frame
                progress = 1.0 if span<=0 else (frame-fade_start_frame)/span
                schedule[frame] = int(previous_alpha+(alpha-previous_alpha)*progress)
        for frame in range(target_frame+1, frame_count): schedule[frame] = int(alpha)
        previous_alpha = alpha
        previous_frame = target_frame
    return [max(0, min(255, value)) for value in schedule]