# events.py
# by Phil Munzke
# https://github.com/PhilMunzke/easypygamewidgets
"""This file contains a collection of events for easypygamewidgets."""

from typing import NewType as _NewType

_binding = _NewType("_binding", str)

# mouse events
MOUSE_IN = _binding("<MOUSE_IN>")
HOVER = _binding("<HOVER>")
MOUSE_OUT = _binding("<MOUSE_OUT>")

# letter events (lowercase and uppercase)
LOWER_A = _binding("<LOWER_A>")
UPPER_A = _binding("<UPPER_A>")
LOWER_B = _binding("<LOWER_B>")
UPPER_B = _binding("<UPPER_B>")
LOWER_C = _binding("<LOWER_C>")
UPPER_C = _binding("<UPPER_C>")
LOWER_D = _binding("<LOWER_D>")
UPPER_D = _binding("<UPPER_D>")
LOWER_E = _binding("<LOWER_E>")
UPPER_E = _binding("<UPPER_E>")
LOWER_F = _binding("<LOWER_F>")
UPPER_F = _binding("<UPPER_F>")
LOWER_G = _binding("<LOWER_G>")
UPPER_G = _binding("<UPPER_G>")
LOWER_H = _binding("<LOWER_H>")
UPPER_H = _binding("<UPPER_H>")
LOWER_I = _binding("<LOWER_I>")
UPPER_I = _binding("<UPPER_I>")
LOWER_J = _binding("<LOWER_J>")
UPPER_J = _binding("<UPPER_J>")
LOWER_K = _binding("<LOWER_K>")
UPPER_K = _binding("<UPPER_K>")
LOWER_L = _binding("<LOWER_L>")
UPPER_L = _binding("<UPPER_L>")
LOWER_M = _binding("<LOWER_M>")
UPPER_M = _binding("<UPPER_M>")
LOWER_N = _binding("<LOWER_N>")
UPPER_N = _binding("<UPPER_N>")
LOWER_O = _binding("<LOWER_O>")
UPPER_O = _binding("<UPPER_O>")
LOWER_P = _binding("<LOWER_P>")
UPPER_P = _binding("<UPPER_P>")
LOWER_Q = _binding("<LOWER_Q>")
UPPER_Q = _binding("<UPPER_Q>")
LOWER_R = _binding("<LOWER_R>")
UPPER_R = _binding("<UPPER_R>")
LOWER_S = _binding("<LOWER_S>")
UPPER_S = _binding("<UPPER_S>")
LOWER_T = _binding("<LOWER_T>")
UPPER_T = _binding("<UPPER_T>")
LOWER_U = _binding("<LOWER_U>")
UPPER_U = _binding("<UPPER_U>")
LOWER_V = _binding("<LOWER_V>")
UPPER_V = _binding("<UPPER_V>")
LOWER_W = _binding("<LOWER_W>")
UPPER_W = _binding("<UPPER_W>")
LOWER_X = _binding("<LOWER_X>")
UPPER_X = _binding("<UPPER_X>")
LOWER_Y = _binding("<LOWER_Y>")
UPPER_Y = _binding("<UPPER_Y>")
LOWER_Z = _binding("<LOWER_Z>")
UPPER_Z = _binding("<UPPER_Z>")
LOWER_AE = _binding("<LOWER_AE>")  # German ä
UPPER_AE = _binding("<UPPER_AE>")  # German Ä
LOWER_OE = _binding("<LOWER_OE>")  # German ö
UPPER_OE = _binding("<UPPER_OE>")  # German Ö
LOWER_UE = _binding("<LOWER_UE>")  # German ü
UPPER_UE = _binding("<UPPER_UE>")  # German Ü
LOWER_SS = _binding("<LOWER_SS>")  # German ß
UPPER_SS = _binding("<UPPER_SS>")  # German ẞ

# numbers
ZERO = _binding("<0>")
ONE = _binding("<1>")
TWO = _binding("<2>")
THREE = _binding("<3>")
FOUR = _binding("<4>")
FIVE = _binding("<5>")
SIX = _binding("<6>")
SEVEN = _binding("<7>")
EIGHT = _binding("<8>")
NINE = _binding("<9>")

# special characters
SPACE = _binding("<SPACE>")
EXCLAMATION_MARK = _binding("<!>")
QUOTATION_MARK_TOP = _binding('<">')
QUOTATION_MARK_BOTTOM = _binding("<„>")
HASH = _binding("<#>")
EURO = _binding("<€>")
DOLLAR = _binding("<$>")
PERCENT = _binding("<%>")
AMPERSAND = _binding("<&>")
APOSTROPHE = _binding("<'>")
LEFT_PARENTHESIS = _binding("<(>")
RIGHT_PARENTHESIS = _binding("<)>")
LEFT_BRACKET = _binding("<[>")
RIGHT_BRACKET = _binding("<]>")
LEFT_BRACE = _binding("<{>")
RIGHT_BRACE = _binding("<}>")
PLUS = _binding("<+>")
MINUS = _binding("<->")
ASTERISK = _binding("<*>")
SLASH = _binding("</>")
BACKSLASH = _binding("<\\>")
PERIOD = _binding("<.>")
COLON = _binding("<:>")
SEMICOLON = _binding("<;>")
COMMA = _binding("<,>")
LESS_THAN = _binding("<<>")
EQUALS = _binding("<=>")
GREATER_THAN = _binding("<>>")
QUESTION_MARK = _binding("<?>")
AT = _binding("<@>")
CARET = _binding("<^>")
DEGREE = _binding("<°>")
UNDERSCORE = _binding("<_>")
BACKTICK = _binding("<`>")
FORWARDTICK = _binding("<´>")
PIPE = _binding("<|>")
TILDE = _binding("<~>")

# control and navigation keys
RETURN = _binding("<RETURN>")
ESCAPE = _binding("<ESCAPE>")
TAB = _binding("<TAB>")
UP = _binding("<UP>")
DOWN = _binding("<DOWN>")
LEFT = _binding("<LEFT>")
RIGHT = _binding("<RIGHT>")
HOME = _binding("<HOME>")
END = _binding("<END>")
PAGE_UP = _binding("<PAGE_UP>")
PAGE_DOWN = _binding("<PAGE_DOWN>")
INSERT = _binding("<INSERT>")
PRINT_SCREEN = _binding("<PRINT_SCREEN>")

# modifier keys
CAPS_LOCK = _binding("<CAPS_LOCK>")
LEFT_SHIFT = _binding("<LEFT_SHIFT>")
RIGHT_SHIFT = _binding("<RIGHT_SHIFT>")
LEFT_CTRL = _binding("<LEFT_CTRL>")
RIGHT_CTRL = _binding("<RIGHT_CTRL>")
LEFT_ALT = _binding("<LEFT_ALT>")
RIGHT_ALT = _binding("<RIGHT_ALT>")

# function keys
F1 = _binding("<F1>")
F2 = _binding("<F2>")
F3 = _binding("<F3>")
F4 = _binding("<F4>")
F5 = _binding("<F5>")
F6 = _binding("<F6>")
F7 = _binding("<F7>")
F8 = _binding("<F8>")
F9 = _binding("<F9>")
F10 = _binding("<F10>")
F11 = _binding("<F11>")
F12 = _binding("<F12>")

# function keys (Apple Mac only)
F13 = _binding("<F13>")
F14 = _binding("<F14>")
F15 = _binding("<F15>")
F16 = _binding("<F16>")
F17 = _binding("<F17>")
F18 = _binding("<F18>")
F19 = _binding("<F19>")

# grouped _bindings
SHIFT = _binding("<SHIFT>")
ALT = _binding("<ALT>")
CTRL = _binding("<CTRL>")
PARENTHESES = _binding("<()>")
BRACKETS = _binding("<[]>")
BRACES = _binding("<{}>")
SLASHES = _binding("</\\>")
TICKS = _binding("`´")
QUOTATION_MARKS = _binding('<„">')

# build in widget events
# all/most
KEY = _binding("<KEY>")

PRESS = _binding("<PRESS>")
HOLD = _binding("<HOLD>")
RELEASE = _binding("<RELEASE>")

# Checkboxes
CHECK = _binding("<CHECK>")
UNCHECK = _binding("<UNCHECK>")

# Comboboxes
COMBOBOX_OPENED = _binding("<COMBOBOX_OPENED>")
COMBOBOX_CLOSED = _binding("<COMBOBOX_CLOSED>")

# Entries
FOCUS_IN = _binding("<FOCUS_IN>")
FOCUS_OUT = _binding("<FOCUS_OUT>")
COPY = _binding("<COPY>")
PASTE = _binding("<PASTE>")
CUT = _binding("<CUT>")
TYPING = _binding("<TYPING>")
SELECT_ALL = _binding("<SELECT_ALL>")
BACKSPACE = _binding("<BACKSPACE>")
DELETE = _binding("<DELETE>")

# Sliders
DRAG = _binding("<DRAG>")

# Timekeepers
TICKING = _binding("<TICKING>")
FINISHED = _binding("<FINISHED>")

# Tooltips
SHOW_TOOLTIP = _binding("<SHOW_TOOLTIP>")
HIDE_TOOLTIP = _binding("<HIDE_TOOLTIP>")

_CHAR_TO_BINDINGS: dict[str, tuple[_binding, ...]] = {
    " ": (SPACE,),
    "!": (EXCLAMATION_MARK,),
    '"': (QUOTATION_MARK_TOP, QUOTATION_MARKS,),
    "„": (QUOTATION_MARK_BOTTOM, QUOTATION_MARKS,),
    "#": (HASH,),
    "€": (EURO,),
    "$": (DOLLAR,),
    "%": (PERCENT,),
    "&": (AMPERSAND,),
    "'": (APOSTROPHE,),
    "(": (LEFT_PARENTHESIS, PARENTHESES,),
    ")": (RIGHT_PARENTHESIS, PARENTHESES,),
    "[": (LEFT_BRACKET, BRACKETS,),
    "]": (RIGHT_BRACKET, BRACKETS,),
    "{": (LEFT_BRACE, BRACES,),
    "}": (RIGHT_BRACE, BRACES,),
    "+": (PLUS,),
    "-": (MINUS,),
    "*": (ASTERISK,),
    "/": (SLASH, SLASHES,),
    "\\": (BACKSLASH, SLASHES,),
    ".": (PERIOD,),
    ":": (COLON,),
    ";": (SEMICOLON,),
    ",": (COMMA,),
    "<": (LESS_THAN,),
    "=": (EQUALS,),
    ">": (GREATER_THAN,),
    "?": (QUESTION_MARK,),
    "@": (AT,),
    "^": (CARET,),
    "°": (DEGREE,),
    "_": (UNDERSCORE,),
    "`": (BACKTICK, TICKS,),
    "´": (FORWARDTICK, TICKS,),
    "|": (PIPE,),
    "~": (TILDE,),
    "0": (ZERO,), "1": (ONE,), "2": (TWO,), "3": (THREE,), "4": (FOUR,),
    "5": (FIVE,), "6": (SIX,), "7": (SEVEN,), "8": (EIGHT,), "9": (NINE,),
    "a": (LOWER_A,), "A": (UPPER_A,), "b": (LOWER_B,), "B": (UPPER_B,),
    "c": (LOWER_C,), "C": (UPPER_C,), "d": (LOWER_D,), "D": (UPPER_D,),
    "e": (LOWER_E,), "E": (UPPER_E,), "f": (LOWER_F,), "F": (UPPER_F,),
    "g": (LOWER_G,), "G": (UPPER_G,), "h": (LOWER_H,), "H": (UPPER_H,),
    "i": (LOWER_I,), "I": (UPPER_I,), "j": (LOWER_J,), "J": (UPPER_J,),
    "k": (LOWER_K,), "K": (UPPER_K,), "l": (LOWER_L,), "L": (UPPER_L,),
    "m": (LOWER_M,), "M": (UPPER_M,), "n": (LOWER_N,), "N": (UPPER_N,),
    "o": (LOWER_O,), "O": (UPPER_O,), "p": (LOWER_P,), "P": (UPPER_P,),
    "q": (LOWER_Q,), "Q": (UPPER_Q,), "r": (LOWER_R,), "R": (UPPER_R,),
    "s": (LOWER_S,), "S": (UPPER_S,), "t": (LOWER_T,), "T": (UPPER_T,),
    "u": (LOWER_U,), "U": (UPPER_U,), "v": (LOWER_V,), "V": (UPPER_V,),
    "w": (LOWER_W,), "W": (UPPER_W,), "x": (LOWER_X,), "X": (UPPER_X,),
    "y": (LOWER_Y,), "Y": (UPPER_Y,), "z": (LOWER_Z,), "Z": (UPPER_Z,),
    "ä": (LOWER_AE,), "Ä": (UPPER_AE,), "ö": (LOWER_OE,), "Ö": (UPPER_OE,),
    "ü": (LOWER_UE,), "Ü": (UPPER_UE,), "ß": (LOWER_SS,), "ẞ": (UPPER_SS,),
}

_SPECIAL_KEYNAME_TO_GROUP_BINDINGS: dict[str, _binding] = {
    "LEFT_SHIFT": SHIFT, "RIGHT_SHIFT": SHIFT,
    "LEFT_CTRL": CTRL, "RIGHT_CTRL": CTRL,
    "LEFT_ALT": ALT, "RIGHT_ALT": ALT
}