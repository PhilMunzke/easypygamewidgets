# font.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets
"""A module to create pygame fonts more easily."""

from __future__ import annotations

import os
import pathlib
from typing import Any

import pygame

pygame.init()

pack_font_path = pathlib.Path(__file__).resolve().parent/"assets"/"fonts"
default_font_path = os.path.join(pack_font_path/"roboto mono"/"RobotoMono-Regular.ttf")
default_emoji_font_path = os.path.join(pack_font_path/"emoji"/"NotoEmoji-Regular.ttf")


class Font:
    """A pygame font wrapper."""

    def __init__(self, font_path: str | os.PathLike = default_font_path, font_size: int = 26,
                 line_spacing: int | None = None, bold: bool = False, italic: bool = False, data: Any = None) -> None:
        """
        Initializes a font.

        Args:
            font_path (str|os.PathLike, optional): the path to the font file (default: Roboto Mono Regular)
            font_size (int, optional): the font size in pixels (default: 26)
            line_spacing (int|None, optional): the line spacing in pixels (default: font_size+4)
            bold (bool, optional): weather the font is bold or not
            italic (bool, optional): weather the font is italic or not
            data (any, optional): Arbitrary user data attached to the widget.
        """
        self.font = pygame.font.Font(font_path, font_size)
        self.font.set_bold(bold)
        self.font.set_italic(italic)
        if line_spacing: self.font.set_linesize(line_spacing)
        else: self.font.set_linesize(font_size+4)
        self.data = data

    def __getattr__(self, attr):
        return getattr(self.font, attr)

    def __deepcopy__(self, memo):
        return self


class SysFont:
    """A pygame system font wrapper."""

    def __init__(self, font: str = "Arial", font_size: int = 26, line_spacing: int | None = None, bold: bool = False,
                 italic: bool = False, data: Any = None) -> None:
        """
        Initializes a font.

        Args:
            font (str, optional): the name of the font (default: Arial)
            font_size (int, optional): the font size in pixels (default: 26)
            line_spacing (int|None, optional): the line spacing in pixels (default: font_size+4)
            bold (bool, optional): weather the font is bold or not
            italic (bool, optional): weather the font is italic or not
            data (any, optional): Arbitrary user data attached to the widget.
        """
        self.font = pygame.font.SysFont(font, font_size)
        self.font.set_bold(bold)
        self.font.set_italic(italic)
        if line_spacing: self.font.set_linesize(line_spacing)
        else: self.font.set_linesize(font_size+4)
        self.data = data

    def __getattr__(self, attr):
        return getattr(self.font, attr)

    def __deepcopy__(self, memo):
        return self


default_font = Font()
tooltip_font = Font(font_size=16)
emoji_font = Font(default_emoji_font_path)