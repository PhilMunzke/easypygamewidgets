# misc.py
# by PizzaPost
# https://github.com/PizzaPost/easypygamewidgets
"""Miscellaneous functions and variables that are building the core structure of the library like rendering or
update checks but also functions that the user can use."""  # TODO: put user functions into their own file

from __future__ import annotations

import ctypes
import os
import queue
import re
import threading
import time
from collections.abc import Callable, Iterable
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any

import cv2
import pygame
import requests
from PIL import Image

from .assets import epw_types

_pg: pygame.Surface | None = None
_check_disabled: bool = False
_all_widgets = []
_scheduled_functions: list[list[Callable, int]] = []
_last_tick: int | float | None = None
_dt: int | float = 0
SYNC_FRAME_LOAD_LIMIT: int = 600
_pending_frame_queues: tuple[queue.Queue, list[pygame.Surface]] | list = []


def _update_clock() -> None:
	"""Internally used to calculate the delta time."""
	global _last_tick, _dt
	now = time.time()
	if _last_tick is None:
		_dt = 0
	else:
		_dt = now-_last_tick
	_last_tick = now
	_drain_frame_queues()


def _check_update() -> None:
	"""Internally used to check for library updates."""
	global _check_disabled
	if _check_disabled: return
	url = "https://raw.githubusercontent.com/PizzaPost/pywidgets/master/info.json"
	try:
		response = requests.get(url)
		response.raise_for_status()
		data = response.json()
		latest_version = data["version"]
		current_version = "26.45"
		if latest_version!=current_version:
			print(
				f"\033[31mAn update is available. Download it now with 'pip install --upgrade easypygamewidgets'\n"
				f"You are currently on: {current_version}\n"
				f"The newest version is: {latest_version}\033[0m"
			)
	except Exception as e:
		print(f"easypygamewidgets: Failed to check for updates: {e}")


def disable_update_check() -> None:
	"""Disable the update check for faster startup time and no text in the console."""
	global _check_disabled
	_check_disabled = True


def _check_linked() -> None:
	"""Internally used to check if a pygame window is linked."""
	if not isinstance(_pg, pygame.Surface):
		raise RuntimeError("Please link a pygame window first: easypygamewidgets.link_pygame_window(window)")


def _check_pygame_version() -> None:
	"""Internally used to check if pygame-ce is installed instead of pygame."""
	try:
		import pygame
		if not hasattr(pygame, "IS_CE"): raise ImportError
	except ImportError:
		print(
			"[INFO] easypygamewidgets 26.9+ requires 'pygame-ce'.\n"
			"Existing 'pygame' installation detected. You have four ways to resolve this:\n"
			"1. Update to Python 3.14+ and install pygame-ce:\n"
			"     pip install pygame-ce\n"
			"2. Replace pygame with pygame-ce (recommended):\n"
			"     pip uninstall pygame && pip install pygame-ce\n"
			"3. Isolation: Use a virtual environment (venv) for this project.\n"
			"4. Legacy: Roll back to an older version of this library:\n"
			"     pip install 'easypygamewidgets<=26.8' --force-reinstall"
		)
		exit(1)


def link_pygame_window(window: pygame.Surface) -> None:
	"""
	Link a pygame window to the library. This will be the window where all widgets are drawn.

	Args:
		window (pygame.Surface): The pygame window to link.
	"""
	global _pg
	_check_pygame_version()
	_check_update()
	_pg = window


def _add_widget(widget: "Widget") -> None:
	"""
	Internally used to add a widget to the list.

	Args:
		widget (Widget): The widget to add.
	"""
	_all_widgets.append(widget)
	_resort_layers()


def create_pygame_layer(function: Callable, layer: int) -> None:
	"""
	Execute the content of a function at a specific layer. This can be useful if you want to draw default pygame
	elements between two widgets.

	Args:
		function (Callable): The function to execute.
		layer (int): The layer at which the function should be executed.
	"""
	_all_widgets.append((function, layer))
	_resort_layers()


def _resort_layers() -> None:
	"""Internally used to sort the widgets/functions by their layer."""
	_all_widgets.sort(key=lambda w: w[1] if isinstance(w, tuple) else w.layer)


def _trigger_key_bindings(widget: "Widget", event: pygame.Event) -> None:
	"""
	Internally used to trigger the correct binding(s) for a KEYDOWN event.

	Args:
		widget (Widget): the widget that should execute the binding
		event (pygame.Event): The event to react to.
	"""
	widget.trigger_event(epw_types.KEY)
	mods = pygame.key.get_mods()
	char_bindings = epw_types._CHAR_TO_BINDINGS.get(event.unicode)
	if not char_bindings and mods & (pygame.KMOD_CTRL | pygame.KMOD_META):
		physical_char = pygame.key.name(event.key)
		if len(physical_char)==1:
			if physical_char.isalpha():
				shift_held = bool(mods & pygame.KMOD_SHIFT)
				caps_held = bool(mods & pygame.KMOD_CAPS)
				physical_char = physical_char.upper() if shift_held!=caps_held else physical_char.lower()
			char_bindings = epw_types._CHAR_TO_BINDINGS.get(physical_char)
	if char_bindings:
		for char_binding in char_bindings:
			widget.trigger_event(char_binding)
		return
	keyname = pygame.key.name(event.key).upper().replace(" ", "_")
	widget.trigger_event(epw_types.binding(f"<{keyname}>"))
	group_binding = epw_types._SPECIAL_KEYNAME_TO_GROUP_BINDINGS.get(keyname)
	if group_binding:
		widget.trigger_event(group_binding)


def set_appearance_mode(mode: int) -> None:
	"""
	Set the appearance mode of the window title bar.

	Args:
		mode (int): The appearance mode to set. (0: Light, 1: Dark, 2: System)
	"""
	hwnd = pygame.display.get_wm_info()["window"]
	tmp = ctypes.c_int(mode)
	ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(tmp), ctypes.sizeof(tmp))


def schedule(function: Callable, time_to_execute: int, unit: str = "seconds", fps: int = 60) -> None:
	"""
	Schedule a function to execute it later.

	Args:
		 function (Callable): the function that should be scheduled.
		 time_to_execute (int): the time it should take to execute the function.
		 unit (str): the unit of time.
		             (frames: "f", "frames"; seconds: "s", "sec", "seconds"; minutes: "m", "min", "minutes")
		 fps (float): the frames per second. (Only useful if you use frames as a unit)
	"""
	if time_to_execute<1:
		time_to_execute = 1
	if fps<=0:
		fps = 60
	if unit in ("f", "frames"):
		time_to_execute /= fps
	elif unit in ("m", "min", "minutes"):
		time_to_execute *= 60
	elif unit in ("s", "sec", "seconds"):
		...
	else:
		print(f"Invalid time unit: {unit}\nFallback: seconds")
	_scheduled_functions.append([function, int(time_to_execute)])


def _get_offset(widget: "Widget") -> tuple[int, int]:
	"""
	Internally used to get the total amount of offset per widget.

	Args:
		 widget (Widget): The widget to get the offset for.

	Returns:
		 tuple[int, int]: The total amount of offset per widget. first number = x and second number = y
	"""
	offset_x = offset_y = 0
	if getattr(widget, "screen", None):
		screen = widget.screen
		offset_x = screen.current_offset[0]+screen.x
		offset_y = screen.current_offset[1]+screen.y
	if getattr(widget, "parent", None):
		offset_x += widget.parent.x
		offset_y += widget.parent.y
	return offset_x, offset_y


def _is_point_over_widget(widget: "Widget", point: tuple[int, int]) -> bool:
	# TODO: fix collision check when scaled down
	# TODO: fix slider collisions
	"""
	Internally used to check if the mouse is hovering over the widget.

	Args:
		widget (Widget): the widget it should check
		point (tuple[int, int]): the (mouse) position it should check for hovering

	Returns:
		bool: True if the point is hovering else False

	Raises:
		ValueError: if the widget type is not supported
	"""
	if widget.alpha_based_collision_system:
		if not hasattr(widget, "cached_surface"):
			if not hasattr(widget, "surface"):
				class_name = widget.__class__.__name__
				raise ValueError(f"Unsupported widget type: {class_name}")
			surface = widget.surface
		else: surface = widget.cached_surface
		if surface.get_width()<=0 or surface.get_height()<=0: return False
		x, y = point
		total_offset_x, total_offset_y = _get_offset(widget)
		if hasattr(widget, "current_offset"):
			total_offset_x += round(widget.current_offset[0])
			total_offset_y += round(widget.current_offset[1])
		rect = widget.rect.move(total_offset_x, total_offset_y)
		cx, cy = rect.center
		rotation = getattr(widget, "current_rotation", 0)
		if rotation!=0:
			v = pygame.math.Vector2(x-cx, y-cy)
			v = v.rotate(rotation)
			local_x, local_y = v.x, v.y
		else: local_x, local_y = x-cx, y-cy
		surf_w, surf_h = surface.get_size()
		px = int(local_x+surf_w/2)
		py = int(local_y+surf_h/2)
		if not (0<=px<surf_w and 0<=py<surf_h): return False
		try: alpha = surface.get_at((px, py)).a
		except IndexError: return False
		return alpha>0
	else:
		class_name = widget.__class__.__name__
		x, y = point
		if class_name in ("Button", "Checkbox", "Dialog", "Entry", "Label", "Surface", "Timekeeper", "Tooltip"):
			offset_x, offset_y = _get_offset(widget)
			total_offset_x = offset_x+round(widget.current_offset[0])
			total_offset_y = offset_y+round(widget.current_offset[1])
			rect = widget.rect.move(total_offset_x, total_offset_y)
			if not rect.collidepoint(point): return False
			geom_rect = rect
			scale = widget.current_scale
			rotation = widget.current_rotation
			if scale!=1 or rotation!=0:
				cx, cy = rect.center
				if rotation!=0:
					v = pygame.math.Vector2(x-cx, y-cy)
					v = v.rotate(rotation)
					x, y = cx+v.x, cy+v.y
				base_w = widget.width*scale
				base_h = widget.height*scale
				geom_rect = pygame.Rect(0, 0, base_w, base_h)
				geom_rect.center = (cx, cy)
				if not geom_rect.collidepoint((x, y)): return False
			max_half_w = geom_rect.width//2
			max_half_h = geom_rect.height//2
			if hasattr(widget, "top_left_corner_radius"):
				tl_r = min(widget.top_left_corner_radius*scale, max_half_w, max_half_h)
				tr_r = min(widget.top_right_corner_radius*scale, max_half_w, max_half_h)
				bl_r = min(widget.bottom_left_corner_radius*scale, max_half_w, max_half_h)
				br_r = min(widget.bottom_right_corner_radius*scale, max_half_w, max_half_h)
			else: tl_r, tr_r, bl_r, br_r = 0, 0, 0, 0  # Surfaces don't have corner radii
			left_r = max(tl_r, bl_r)
			right_r = max(tr_r, br_r)
			top_r = max(tl_r, tr_r)
			bottom_r = max(bl_r, br_r)
			if geom_rect.left+left_r<=x<=geom_rect.right-right_r: return True
			if geom_rect.top+top_r<=y<=geom_rect.bottom-bottom_r: return True
			if x<geom_rect.left+tl_r and y<geom_rect.top+tl_r:
				cx, cy = geom_rect.left+tl_r, geom_rect.top+tl_r
				return (x-cx)**2+(y-cy)**2<=tl_r**2
			if x>geom_rect.right-tr_r and y<geom_rect.top+tr_r:
				cx, cy = geom_rect.right-tr_r, geom_rect.top+tr_r
				return (x-cx)**2+(y-cy)**2<=tr_r**2
			if x<geom_rect.left+bl_r and y>geom_rect.bottom-bl_r:
				cx, cy = geom_rect.left+bl_r, geom_rect.bottom-bl_r
				return (x-cx)**2+(y-cy)**2<=bl_r**2
			if x>geom_rect.right-br_r and y>geom_rect.bottom-br_r:
				cx, cy = geom_rect.right-br_r, geom_rect.bottom-br_r
				return (x-cx)**2+(y-cy)**2<=br_r**2
			return True
		elif class_name=="Screen":
			offset_x, offset_y = _get_offset(widget)
			total_offset_x = offset_x+round(widget.current_offset[0])
			total_offset_y = offset_y+round(widget.current_offset[1])
			rect = widget.rect.move(total_offset_x, total_offset_y)
			if not rect.collidepoint(point): return False
			return True
		elif class_name=="Slider":
			offset_x, offset_y = _get_offset(widget)
			total_offset_x = offset_x+round(widget.current_offset[0])
			total_offset_y = offset_y+round(widget.current_offset[1])
			draw_rect = widget.rect.move(total_offset_x, total_offset_y)
			scale = widget.current_scale
			rotation = widget.current_rotation
			cx, cy = draw_rect.center
			if rotation!=0:
				v = pygame.math.Vector2(x-cx, y-cy)
				v = v.rotate(rotation)
				x, y = cx+v.x, cy+v.y
			if scale!=1 and scale!=0:
				x = cx+(x-cx)/scale
				y = cy+(y-cy)/scale
			orig_rect = widget.original_surface.get_rect(center=(cx, cy))
			if not orig_rect.collidepoint((x, y)): return False
			temp_surf = widget.font.render(widget.text, True, (0, 0, 0))
			text_height = temp_surf.get_height()
			track_y = orig_rect.top+text_height+10+widget._height//2
			extra_dot = widget.dot_radius+widget.max_extra_dot_radius
			track_y = max(track_y, orig_rect.top+extra_dot)
			widest_magnitude = max(abs(widget.start), abs(widget.end))
			integer_digits = len(str(int(widest_magnitude)))
			decimal_digits = widget.round_display_value if widget.round_display_value>0 else 0
			widest_value_str = "9"*integer_digits+("."+"9"*decimal_digits if decimal_digits else "")
			if widget.start<0 or widget.end<0:
				widest_value_str = "-"+widest_value_str
			side_margin = widget.max_extra_dot_radius+widget.font.size(widest_value_str)[0]//2
			track_rect = pygame.Rect(
				orig_rect.x+side_margin, track_y-(widget._height//2),
				orig_rect.width-side_margin*2, widget._height
			)
			if not track_rect.collidepoint((x, y)): return False
			max_radius = min(track_rect.width, track_rect.height)//2
			tl = min(widget.top_left_corner_radius, max_radius)
			tr = min(widget.top_right_corner_radius, max_radius)
			bl = min(widget.bottom_left_corner_radius, max_radius)
			br = min(widget.bottom_right_corner_radius, max_radius)
			if x<track_rect.left+tl and y<track_rect.top+tl:
				cxc, cyc = track_rect.left+tl, track_rect.top+tl
				if (x-cxc)**2+(y-cyc)**2>tl**2: return False
			elif x>track_rect.right-tr and y<track_rect.top+tr:
				cxc, cyc = track_rect.right-tr, track_rect.top+tr
				if (x-cxc)**2+(y-cyc)**2>tr**2: return False
			elif x<track_rect.left+bl and y>track_rect.bottom-bl:
				cxc, cyc = track_rect.left+bl, track_rect.bottom-bl
				if (x-cxc)**2+(y-cyc)**2>bl**2: return False
			elif x>track_rect.right-br and y>track_rect.bottom-br:
				cxc, cyc = track_rect.right-br, track_rect.bottom-br
				if (x-cxc)**2+(y-cyc)**2>br**2: return False
			return True
		else:
			raise ValueError(f"Unsupported widget type: {class_name}")


def normalize_color(color: epw_types.nonable_color_type) -> tuple[int, int, int, int]:
	"""
	Converts different color formats into an rgba color value.

	Args:
		  color (epw_types.nonable_color_type): The color to convert. (Allowed color formats are rgb, rgba, #hex, hex or
		                                        None. None returns an invisible color.)

	Returns:
		  tuple[int, int, int, int]: The normalized rgba color value.

	Raises:
		  ValueError: If the color format is invalid.
	"""
	if color is None:
		return 0, 0, 0, 0
	if isinstance(color, (tuple, list)):
		if len(color)==3 and all(isinstance(c, int) and 0<=c<=255 for c in color):
			return *color, 255
		if len(color)==4 and all(isinstance(c, int) and 0<=c<=255 for c in color):
			return color  # type: ignore
	elif isinstance(color, str):
		color = color.removeprefix("#")
		if len(color)==6 and all(c.lower() in "0123456789abcdef" for c in color):
			return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), 255
	raise ValueError("Invalid color format. Supported formats: (r, g, b), (r, g, b, a), #hex, hex")


def _natural_key(s) -> list[int | str]:
	"""
	Internally used to sort strings in a natural order.

	Args:
		s (str): The string to sort.

	Returns:
		list[int| str]: The sorted string.
	"""
	return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]


def _load_image(full_path) -> pygame.Surface:
	"""
	Internally used to load an image.

	Args:
		full_path (str): The path to the image file.

	Returns:
		pygame.Surface: The loaded image surface.
	"""
	return pygame.image.load(full_path)


def _decode_image_worker(full_paths: list[str], raw_queue: queue.Queue, worker_count: int) -> None:
	"""
	Internally used to decode images in a separate thread.

	Args:
		full_paths (list[str]): The paths to the image files.
		raw_queue (queue.Queue): The queue to store the decoded images.
		worker_count (int): The number of workers to use.
	"""

	def _decode(path: str) -> tuple[Any, tuple[int, int], bytes]:
		"""
		Internally used to decode an image file.

		Args:
			path (str): The path to the image file.

		Returns:
			tuple[Any, tuple[int, int], bytes]: The decoded image.
		"""
		with Image.open(path) as img:
			img = img.convert("RGBA")
			return path, img.size, img.tobytes()

	with ThreadPoolExecutor(max_workers=worker_count) as pool:
		for full_path, size, data in pool.map(_decode, full_paths):
			raw_queue.put(("image", size, data))
	raw_queue.put(None)


def _read_video_bytes_worker(vidcap: cv2.VideoCapture, raw_queue: queue.Queue) -> None:
	"""
	Internally used to read video frames in a separate thread.

	Args:
		 vidcap (cv2.VideoCapture): the video capture object.
		 raw_queue (queue.Queue): The queue to store the decoded video frames.
	"""
	continue_grabbing, frame = vidcap.read()
	while continue_grabbing:
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		width = frame.shape[1]
		height = frame.shape[0]
		raw_queue.put(("video", (width, height), frame.tobytes()))
		continue_grabbing, frame = vidcap.read()
	vidcap.release()
	raw_queue.put(None)


def _drain_frame_queues() -> None:
	"""Internally used to drain the frame queues."""
	if not _pending_frame_queues: return
	for raw_queue, frames_list in _pending_frame_queues[:]:
		while True:
			try:
				item = raw_queue.get_nowait()
			except queue.Empty:
				break
			if item is None:
				_pending_frame_queues.remove((raw_queue, frames_list))
				break
			kind, (width, height), data = item
			if kind=="image":
				frames_list.append(pygame.image.frombuffer(data, (width, height), "RGBA"))
			else:
				frames_list.append(pygame.image.frombuffer(data, (width, height), "RGB"))


def create_frames(path: str | os.PathLike | pygame.Surface) -> Iterable[pygame.Surface]:
	"""
	Build an Iterable element that can be used for animated Surfaces.

	Supported image formats:
		.png, .jpg, .jpeg, .webp

	Supported video formats:
		.mov, .mp4, .webm

	NOTE: IT'S RECOMMENDED TO USE A VIDEO FILE FOR BETTER PERFORMANCE!

	Args:
		 path (str | os.PathLike | pygame.Surface): The path to the image files.
		                                            (directory, image/video file or pygame.Surface)

	Returns:
		 Iterable[pygame.Surface]: An Iterable of Surfaces.

	Raises:
		 ValueError: invalid path
		             If you think that your path is valid check if the file format is supported.
	"""
	if isinstance(path, pygame.Surface):
		return [path]
	elif isinstance(path, str):
		if os.path.isdir(path):
			filenames = sorted(os.listdir(path), key=_natural_key)
			full_paths = [os.path.join(path, filename) for filename in filenames]
			worker_count = min(32, (os.cpu_count() or 4)*4)
			sync_paths = full_paths[:SYNC_FRAME_LOAD_LIMIT]
			async_paths = full_paths[SYNC_FRAME_LOAD_LIMIT:]
			with ThreadPoolExecutor(max_workers=worker_count) as pool:
				frames_list = list(pool.map(_load_image, sync_paths))
			if async_paths:
				raw_queue = queue.Queue(maxsize=64)
				reader_thread = threading.Thread(
					target=_decode_image_worker,
					args=(async_paths, raw_queue, worker_count), daemon=True
				)
				reader_thread.start()
				_pending_frame_queues.append((raw_queue, frames_list))
			return frames_list
		if os.path.isfile(path) and path.lower().endswith((".mov", ".mp4", ".webm")):
			frames_list = []
			vidcap = cv2.VideoCapture(path)
			continue_grabbing, frame = vidcap.read()
			while continue_grabbing and len(frames_list)<SYNC_FRAME_LOAD_LIMIT:
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				width = frame.shape[1]
				height = frame.shape[0]
				frames_list.append(pygame.image.frombuffer(frame.tobytes(), (width, height), "RGB"))
				continue_grabbing, frame = vidcap.read()
			if continue_grabbing:
				raw_queue = queue.Queue(maxsize=64)
				reader_thread = threading.Thread(target=_read_video_bytes_worker, args=(vidcap, raw_queue), daemon=True)
				reader_thread.start()
				_pending_frame_queues.append((raw_queue, frames_list))
			else:
				vidcap.release()
			return frames_list
		elif os.path.isfile(path) and path.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
			return [pygame.image.load(path)]
		else:
			raise ValueError("Invalid path format. Please provide a directory, video file path, or image file path.")
	else:
		raise ValueError("Invalid path format. Please provide a directory, video file path, or image file path.")