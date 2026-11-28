# particle.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets
"""A single particle created and managed by a ParticleSprayer."""

from __future__ import annotations

import math
from typing import Any, Self, TYPE_CHECKING

import pygame

from easypygamewidgets import misc
from easypygamewidgets.assets.epw_types import color

if TYPE_CHECKING: import easypygamewidgets

pygame.init()

TO_UPDATE = [f"_{attr}" for attr in ["color", "texture", "size", "rotation", "opacity"]]


class Particle:
    """A single particle spawned by a ParticleSprayer."""

    def __init__(self, sprayer: easypygamewidgets.ParticleSprayer, x: int | float, y: int | float,
                 color_schedule: list[color], texture_schedule: list[pygame.Surface | None],
                 speed_schedule: list[int | float], size_schedule: list[int | float],
                 rotation_schedule: list[int | float], gravity_schedule: list[int | float],
                 direction_schedule: list[int | float], alpha_schedule: list[int],
                 avoid_mouse: bool, physics: bool, generation: int = 1, data: Any = None,
                 blend_mode: int = 0) -> None:
        """
        Initializes a Particle. Every *_schedule argument is a resolved per-frame list of values that was already chosen by the ParticleSprayer at
        spawn time so that a particle never changes during their life except for following its schedule.

        Args:
            sprayer (easypygamewidgets.ParticleSprayer): the ParticleSprayer that spawned this particle
            x (int | float): the starting x position
            y (int | float): the starting y position
            color_schedule (list[color]): the resolved color for every frame of the particle's life
            texture_schedule (list[pygame.Surface | None]): the resolved texture for every frame of the particle's life. If one frame is None the
                particle is instead drawn as a filled circle using the color_schedule instead.
            speed_schedule (list[int | float]): the resolved travel speed for every frame
            size_schedule (list[int | float]): the resolved size for every frame
            rotation_schedule (list[int | float]): the resolved rotation for every frame
            gravity_schedule (list[int | float]): the resolved downward speed for every frame
            direction_schedule (list[int | float]): the resolved travel direction for every frame in degree
            alpha_schedule (list[int]): the resolved opacity value for every frame
            avoid_mouse (bool): if True the particle moves away from the mouse cursor
            physics (bool): if True, particles can split on the 'particle_split_effect' settings of the sprayer
            generation (int, optional): which split generation this particle belongs to. The original particle spawned directly by the sprayer is the
                first generation and each time a particle splits their children adopt their parents generation+1. Defaults to 1.
            data (Any, optional): arbitrary user data attached to the particle
            blend_mode (int, optional): the pygame special_flags value used when blitting the particle (for example pygame.BLEND_RGB_ADD for a glowing additive look). Defaults to 0 which is normal blending.
        """
        self._sprayer = sprayer
        self._x = x
        self._y = y
        self._velocity_x = 0
        self._velocity_y = 0
        self._color_schedule = [misc._normalize_color(step) for step in color_schedule]
        self._texture_schedule = texture_schedule
        self._speed_schedule = speed_schedule
        self._size_schedule = size_schedule
        self._rotation_schedule = rotation_schedule
        self._gravity_schedule = gravity_schedule
        self._direction_schedule = direction_schedule
        self._alpha_schedule = alpha_schedule
        self._avoid_mouse = avoid_mouse
        self._physics = physics
        self._generation = generation
        self._data = data
        self._blend_mode = blend_mode
        self._frame = 0
        self._life_time = 0
        self._total_frames = len(self._color_schedule)
        self._alive = True
        self._color = self._color_schedule[0]
        self._texture = self._texture_schedule[0]
        self._speed = self._speed_schedule[0]
        self._size = self._size_schedule[0]
        self._rotation = self._rotation_schedule[0]
        self._gravity = self._gravity_schedule[0]
        self._direction = self._direction_schedule[0]
        self._opacity = self._alpha_schedule[0]
        self._cached_surface: pygame.Surface | None = None
        self._last_visual_state: list[Any] | None = None

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
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, value):
        self._alive = value

    @property
    def frame(self):
        return self._frame

    @property
    def color(self):
        return self._color

    @property
    def texture(self):
        return self._texture

    @property
    def speed(self):
        return self._speed

    @property
    def size(self):
        return self._size

    @property
    def rotation(self):
        return self._rotation

    @property
    def gravity(self):
        return self._gravity

    @property
    def direction(self):
        return self._direction

    @property
    def generation(self):
        return self._generation

    @property
    def opacity(self):
        return self._opacity

    @property
    def blend_mode(self):
        return self._blend_mode

    @blend_mode.setter
    def blend_mode(self, value):
        self._blend_mode = value

    def _update(self, dt: float | int) -> bool:
        """
        Internally used to update the particle. That means moving and following their schedule.

        Args:
            dt (float): the amount of seconds since the last tick

        Returns:
            bool: True if the particle is still alive and False if it should be deleted.
        """
        if not self._alive: return False

        last_frame_index = self._total_frames-1
        frame_index = min(self._frame, last_frame_index)
        self._color = self._color_schedule[frame_index]
        self._texture = self._texture_schedule[frame_index]
        self._speed = self._speed_schedule[frame_index]
        self._size = self._size_schedule[frame_index]
        self._rotation = self._rotation_schedule[frame_index]
        self._gravity = self._gravity_schedule[frame_index]
        self._direction = self._direction_schedule[frame_index]
        self._opacity = self._alpha_schedule[frame_index]
        direction_rad = math.radians(self._direction)
        self._velocity_x = math.cos(direction_rad)*self._speed
        self._velocity_y = math.sin(direction_rad)*self._speed+self._gravity

        if self._avoid_mouse:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            delta_x, delta_y = self._x-mouse_x, self._y-mouse_y
            distance = math.hypot(delta_x, delta_y)
            if 0<distance<80:
                push_strength = self._speed*(1-distance/80)
                self._velocity_x += (delta_x/distance)*push_strength
                self._velocity_y += (delta_y/distance)*push_strength

        self._x += self._velocity_x*dt
        self._y += self._velocity_y*dt

        self._life_time += dt
        if self._frame<last_frame_index: self._frame += 1

        if self._frame>=last_frame_index:
            self._alive = False
            return False
        return True

    def _draw(self, surface: pygame.Surface) -> None:
        """
        Internally used to draw the particle.

        Args:
            surface (pygame.Surface): the surface to draw the particle on.
        """
        if not self._alive: return

        current_state = misc._get_vars(self, TO_UPDATE)
        if current_state!=self._last_visual_state or self._cached_surface is None:
            _render_particle_surface(self)
            self._last_visual_state = current_state

        rect = self._cached_surface.get_rect(center=(int(self._x), int(self._y)))
        surface.blit(self._cached_surface, rect, special_flags=self._blend_mode)

    def split(self) -> list[Self]:
        """
        This splits the particle according to their split effect settings.

        Returns:
            list[Self]: the new spawned particles
            []: an empty list will be returned if splitting is disabled or the recursion limit that was set by the sprayer was reached
        """
        if not self._sprayer.particle_split_effect: return []
        if self._generation>=self._sprayer.particle_split_effect_recursion_amount+1: return []
        return self._sprayer._spawn_particles(self._x, self._y, split=True, generation=self._generation+1)


def _render_particle_surface(particle: Particle) -> None:
    """
    Internally used to render the button surface once and cache it.

    Args:
         particle (Particle): the particle to render the surface for
    """
    size = max(int(particle._size), 1)
    if particle._texture is not None:
        scaled = pygame.transform.smoothscale(particle._texture, (size, size))
        if particle._rotation:
            scaled = pygame.transform.rotate(scaled, particle._rotation)
        scaled.set_alpha(particle._opacity)
        particle._cached_surface = scaled
    else:
        particle_color = (*particle._color[:3], particle._opacity)
        cached = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(cached, particle_color, (size//2, size//2), size//2)
        particle._cached_surface = cached