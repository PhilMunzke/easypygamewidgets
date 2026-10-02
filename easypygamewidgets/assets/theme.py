"""Theme system for styling widgets globally or per widget type. Themes are stored in JSON files."""
import functools
import inspect
import json
import os

from ..font import default_font, emoji_font, tooltip_font
from ..misc import normalize_color as nc


def _themed(func):
	"""Internally used to apply theme settings to a widget upon creation unless it's set manually."""
	sig = inspect.signature(func)
	theme_param_names = [name for name in sig.parameters if name in _style_dic]
	widget_name = func.__qualname__.split(".")[0]

	@functools.wraps(func)
	def _wrapper(*args, **kwargs):
		"""The wrapper function that applies theme settings to a widget."""
		bound = sig.bind_partial(*args, **kwargs)
		possible_overrides = _widget_style_dic.get(widget_name, {})
		for name in theme_param_names:
			if name not in bound.arguments:
				if name in possible_overrides:
					kwargs[name] = possible_overrides[name]
				else:
					kwargs[name] = _style_dic[name]
		return func(*args, **kwargs)

	return _wrapper


_widget_style_dic: dict[str, dict] = {
	"Dialog": {
		"layer": 2000
	},
	"Label": {
		"active_hover_background_color": None,
		"active_hover_border_color": None,
		"active_pressed_background_color": None,
		"active_pressed_border_color": None,
		"active_unpressed_background_color": None,
		"active_unpressed_border_color": None,
		"disabled_hover_background_color": None,
		"disabled_hover_border_color": None,
		"disabled_unpressed_background_color": None,
		"disabled_unpressed_border_color": None
	},
	"Surface": {
		"alpha_based_collision_system": True
	},
	"Tooltip": {
		"font": tooltip_font,
		"alignment_spacing": 20,
		"active_unpressed_text_color": None,
		"active_unpressed_background_color": None,
		"active_unpressed_border_color": None,
		"disabled_unpressed_text_color": None,
		"disabled_unpressed_background_color": None,
		"disabled_unpressed_border_color": None,
		"active_hover_text_color": None,
		"active_hover_background_color": None,
		"active_hover_border_color": None,
		"disabled_hover_text_color": None,
		"disabled_hover_background_color": None,
		"disabled_hover_border_color": None,
		"active_pressed_text_color": None,
		"active_pressed_background_color": None,
		"active_pressed_border_color": None,
		"visible": False
	},
	"Timekeeper": {
		"active_pressed_text_color": (255, 255, 255, 255),
		"active_hover_background_color": (50, 50, 50, 255),
		"active_pressed_background_color": (50, 50, 50, 255),
		"active_hover_border_color": (100, 100, 100, 255),
		"active_pressed_border_color": (100, 100, 100, 255)
	}
}

_style_dic = {
	# border thickness
	"border_thickness": 2,

	# collision system
	"alpha_based_collision_system": False,

	# corner radius
	"top_left_corner_radius": 25,
	"top_right_corner_radius": 25,
	"bottom_left_corner_radius": 25,
	"bottom_right_corner_radius": 25,

	# cursor
	"active_hover_cursor": None,
	"disabled_hover_cursor": None,
	"active_pressed_cursor": None,

	# font
	"font": default_font,
	"emoji_font": emoji_font,
	"tooltip_font": tooltip_font,

	# geometry
	"alignment_spacing": 40,
	"line_spacing": 30,
	"min_width": None,
	"max_width": None,
	"min_height": None,
	"max_height": None,
	"title_line_spacing": 30,
	"description_line_spacing": 30,
	"title_alignment_spacing": 40,
	"description_alignment_spacing": 40,
	"widget_area_padding": 20,
	"widgets_spacing": 20,
	"row_spacing": 10,
	"column_spacing": 10,

	# overlay
	"darken_background_with_alpha": 100,

	# placement
	"anchor_x": "left",
	"anchor_y": "top",
	"layer": 1000,

	# visibility
	"visible": True,

	# widget specific
	# entry specific
	"blinking_cursor": "|",
	"blinking_speed": 500,
	"character_limit": None,
	"repeat_delay": 500,
	"repeat_interval": 50,
	# slider specific
	"dot_radius": None,
	"max_extra_dot_radius": None,
	"move_text_with_dot_radius": True,
	"round_display_value": 0,
	"show_full_rounding_of_whole_numbers": False,
	"show_value_when_disabled": False,
	"show_value_when_hovered": True,
	"show_value_when_pressed": True,
	"show_value_when_unpressed": False,
	"trigger_hold_delay": 150,
	# surface specific
	"fps": 60,
	"looping": True,
	"playing": False,
	# timekeeper specific
	"show_milliseconds": False,
	"show_seconds": True,
	"show_minutes": False,
	"smart_minutes": True,
	"show_hours": False,
	"smart_hours": True,
	"type_order": ("h", ":", "m", ":", "s", ".", "ms"),

	# color
	"active_unpressed_text_color": (255, 255, 255, 255),
	"disabled_unpressed_text_color": (150, 150, 150, 255),
	"active_hover_text_color": (255, 255, 255, 255),
	"disabled_hover_text_color": (150, 150, 150, 255),
	"active_pressed_text_color": (200, 200, 200, 255),
	"active_unpressed_background_color": (50, 50, 50, 255),
	"disabled_unpressed_background_color": (30, 30, 30, 255),
	"active_hover_background_color": (70, 70, 70, 255),
	"disabled_hover_background_color": (30, 30, 30, 255),
	"active_pressed_background_color": (40, 40, 40, 255),
	"active_unpressed_border_color": (100, 100, 100, 255),
	"disabled_unpressed_border_color": (60, 60, 60, 255),
	"active_hover_border_color": (150, 150, 150, 255),
	"disabled_hover_border_color": (60, 60, 60, 255),
	"active_pressed_border_color": (50, 50, 50, 255),

	"active_unpressed_mark_color": (255, 255, 255, 255),
	"disabled_unpressed_mark_color": (150, 150, 150, 255),
	"active_hover_mark_color": (255, 255, 255, 255),
	"disabled_hover_mark_color": (150, 150, 150, 255),
	"active_pressed_mark_color": (200, 200, 200, 255),
	"active_unpressed_mark_background_color": (30, 30, 30, 255),
	"disabled_unpressed_mark_background_color": (20, 20, 20, 255),
	"active_hover_mark_background_color": (45, 45, 45, 255),
	"disabled_hover_mark_background_color": (20, 20, 20, 255),
	"active_pressed_mark_background_color": (25, 25, 25, 255),

	"active_unpressed_title_color": (255, 255, 255, 255),
	"disabled_unpressed_title_color": (200, 200, 200, 255),
	"active_hover_title_color": (255, 255, 255, 255),
	"disabled_hover_title_color": (200, 200, 200, 255),
	"active_pressed_title_color": (220, 220, 220, 255),
	"active_unpressed_description_color": (200, 200, 200, 255),
	"disabled_unpressed_description_color": (150, 150, 150, 255),
	"active_hover_description_color": (200, 200, 200, 255),
	"disabled_hover_description_color": (150, 150, 150, 255),
	"active_pressed_description_color": (180, 180, 180, 255),

	"selection_color": (0, 120, 215, 255),
	"disabled_selection_color": (32, 106, 163, 255),

	"active_unpressed_shadow_color": (50, 50, 50, 200),
	"disabled_unpressed_shadow_color": (50, 50, 50, 200),
	"active_hover_shadow_color": (50, 50, 50, 200),
	"disabled_hover_shadow_color": (50, 50, 50, 200),
	"active_pressed_shadow_color": (50, 50, 50, 200),
	"active_unpressed_underline_color": None,
	"disabled_unpressed_underline_color": None,
	"active_hover_underline_color": None,
	"disabled_hover_underline_color": None,
	"active_pressed_underline_color": None,
	"active_unpressed_strikethrough_color": None,
	"disabled_unpressed_strikethrough_color": None,
	"active_hover_strikethrough_color": None,
	"disabled_hover_strikethrough_color": None,
	"active_pressed_strikethrough_color": None,

	"active_unpressed_used_background_color": (30, 30, 30, 255),
	"disabled_unpressed_used_background_color": (20, 20, 20, 255),
	"active_hover_used_background_color": (30, 30, 30, 255),
	"disabled_hover_used_background_color": (20, 20, 20, 255),
	"active_pressed_used_background_color": (30, 30, 30, 255),
	"active_unpressed_unused_background_color": (60, 60, 60, 255),
	"disabled_unpressed_unused_background_color": (30, 30, 30, 255),
	"active_hover_unused_background_color": (60, 60, 60, 255),
	"disabled_hover_unused_background_color": (30, 30, 30, 255),
	"active_pressed_unused_background_color": (60, 60, 60, 255),
	"active_unpressed_dot_color": (255, 255, 255, 255),
	"disabled_unpressed_dot_color": (150, 150, 150, 255),
	"active_hover_dot_color": (255, 255, 255, 255),
	"disabled_hover_dot_color": (150, 150, 150, 255),
	"active_pressed_dot_color": (200, 200, 200, 255),
	"active_unpressed_display_color": (190, 190, 190, 255),
	"disabled_unpressed_display_color": (150, 150, 150, 255),
	"active_hover_display_color": (190, 190, 190, 255),
	"disabled_hover_display_color": (150, 150, 150, 255),
	"active_pressed_display_color": (190, 190, 190, 255),
}


def load_global_theme(path: str | os.PathLike) -> None:
	"""
	Load a theme file that contains theme settings for every widget. If a widget supports the specified
	values it'll apply them upon creation.

	Values:
		- border_thickness
		- alpha_based_collision_system
		- every possible anchor attribute
		- every possible color attribute
		- every possible corner_radius attribute
		- every possible cursor attribute
		- darken_background_with_alpha
		- every possible font attribute
		- layer
		- slider dot settings
		- visible
		- every possible spacing, min/max size attribute

	There are two different types of themes.
	1. global themes: These apply to every widget.
	2. widget-specific themes: These apply only to a specific widget type.

	priority order:
		1st set value when creating
		2nd widget-specific theme
		3rd global theme
		4th default value

	Args:
		path (str | os.PathLike): The path to the JSON file.

	Raises:
		ValueError: If the specified path does not exist.
	"""
	if not os.path.exists(path): raise ValueError("The specified path does not exist.")
	with open(path) as f:
		data = json.load(f)

	widget_blocks = {key: value for key, value in data.items() if isinstance(value, dict)}
	global_data = {key: value for key, value in data.items() if key not in widget_blocks}

	_apply_theme_data(global_data, _style_dic)
	for widget_name, widget_data in widget_blocks.items():
		target = _widget_style_dic.setdefault(widget_name, {})
		_apply_theme_data(widget_data, target)


_COLOR_KEYS = frozenset(
	{
		"active_unpressed_text_color", "disabled_unpressed_text_color", "active_hover_text_color",
		"disabled_hover_text_color", "active_pressed_text_color",
		"active_unpressed_background_color", "disabled_unpressed_background_color",
		"active_hover_background_color", "disabled_hover_background_color", "active_pressed_background_color",
		"active_unpressed_border_color", "disabled_unpressed_border_color", "active_hover_border_color",
		"disabled_hover_border_color", "active_pressed_border_color",
		"active_unpressed_mark_color", "disabled_unpressed_mark_color", "active_hover_mark_color",
		"disabled_hover_mark_color", "active_pressed_mark_color",
		"active_unpressed_mark_background_color", "disabled_unpressed_mark_background_color",
		"active_hover_mark_background_color", "disabled_hover_mark_background_color",
		"active_pressed_mark_background_color",
		"active_unpressed_title_color", "disabled_unpressed_title_color", "active_hover_title_color",
		"disabled_hover_title_color", "active_pressed_title_color",
		"active_unpressed_description_color", "disabled_unpressed_description_color",
		"active_hover_description_color", "disabled_hover_description_color", "active_pressed_description_color",
		"selection_color", "disabled_selection_color",
		"active_unpressed_shadow_color", "disabled_unpressed_shadow_color", "active_hover_shadow_color",
		"disabled_hover_shadow_color", "active_pressed_shadow_color",
		"active_unpressed_underline_color", "disabled_unpressed_underline_color", "active_hover_underline_color",
		"disabled_hover_underline_color", "active_pressed_underline_color",
		"active_unpressed_strikethrough_color", "disabled_unpressed_strikethrough_color",
		"active_hover_strikethrough_color", "disabled_hover_strikethrough_color", "active_pressed_strikethrough_color",
		"active_unpressed_used_background_color", "disabled_unpressed_used_background_color",
		"active_hover_used_background_color", "disabled_hover_used_background_color",
		"active_pressed_used_background_color",
		"active_unpressed_unused_background_color", "disabled_unpressed_unused_background_color",
		"active_hover_unused_background_color", "disabled_hover_unused_background_color",
		"active_pressed_unused_background_color",
		"active_unpressed_dot_color", "disabled_unpressed_dot_color", "active_hover_dot_color",
		"disabled_hover_dot_color", "active_pressed_dot_color",
		"active_unpressed_display_color", "disabled_unpressed_display_color", "active_hover_display_color",
		"disabled_hover_display_color", "active_pressed_display_color",
	}
)


def _apply_theme_data(data: dict, target: dict) -> None:
	"""Internally used to write JSON theme data into a dictionary."""
	for key, value in data.items():
		target[key] = nc(value) if key in _COLOR_KEYS else value