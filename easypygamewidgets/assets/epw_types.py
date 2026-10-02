from typing import NewType

color_type = tuple[int, int, int, int] | tuple[int, int, int] | list[int] | str
nonable_color_type = tuple[int, int, int] | tuple[int, int, int, int] | list[int] | str | None

binding = NewType("binding", str)

# mouse events
MOUSE_IN = binding("<MOUSE_IN>")
HOVER = binding("<HOVER>")
MOUSE_OUT = binding("<MOUSE_OUT>")

# letter events (lowercase and uppercase)
LOWER_A = binding("<LOWER_A>")
UPPER_A = binding("<UPPER_A>")
LOWER_B = binding("<LOWER_B>")
UPPER_B = binding("<UPPER_B>")
LOWER_C = binding("<LOWER_C>")
UPPER_C = binding("<UPPER_C>")
LOWER_D = binding("<LOWER_D>")
UPPER_D = binding("<UPPER_D>")
LOWER_E = binding("<LOWER_E>")
UPPER_E = binding("<UPPER_E>")
LOWER_F = binding("<LOWER_F>")
UPPER_F = binding("<UPPER_F>")
LOWER_G = binding("<LOWER_G>")
UPPER_G = binding("<UPPER_G>")
LOWER_H = binding("<LOWER_H>")
UPPER_H = binding("<UPPER_H>")
LOWER_I = binding("<LOWER_I>")
UPPER_I = binding("<UPPER_I>")
LOWER_J = binding("<LOWER_J>")
UPPER_J = binding("<UPPER_J>")
LOWER_K = binding("<LOWER_K>")
UPPER_K = binding("<UPPER_K>")
LOWER_L = binding("<LOWER_L>")
UPPER_L = binding("<UPPER_L>")
LOWER_M = binding("<LOWER_M>")
UPPER_M = binding("<UPPER_M>")
LOWER_N = binding("<LOWER_N>")
UPPER_N = binding("<UPPER_N>")
LOWER_O = binding("<LOWER_O>")
UPPER_O = binding("<UPPER_O>")
LOWER_P = binding("<LOWER_P>")
UPPER_P = binding("<UPPER_P>")
LOWER_Q = binding("<LOWER_Q>")
UPPER_Q = binding("<UPPER_Q>")
LOWER_R = binding("<LOWER_R>")
UPPER_R = binding("<UPPER_R>")
LOWER_S = binding("<LOWER_S>")
UPPER_S = binding("<UPPER_S>")
LOWER_T = binding("<LOWER_T>")
UPPER_T = binding("<UPPER_T>")
LOWER_U = binding("<LOWER_U>")
UPPER_U = binding("<UPPER_U>")
LOWER_V = binding("<LOWER_V>")
UPPER_V = binding("<UPPER_V>")
LOWER_W = binding("<LOWER_W>")
UPPER_W = binding("<UPPER_W>")
LOWER_X = binding("<LOWER_X>")
UPPER_X = binding("<UPPER_X>")
LOWER_Y = binding("<LOWER_Y>")
UPPER_Y = binding("<UPPER_Y>")
LOWER_Z = binding("<LOWER_Z>")
UPPER_Z = binding("<UPPER_Z>")
LOWER_AE = binding("<LOWER_AE>")  # German ä
UPPER_AE = binding("<UPPER_AE>")  # German Ä
LOWER_OE = binding("<LOWER_OE>")  # German ö
UPPER_OE = binding("<UPPER_OE>")  # German Ö
LOWER_UE = binding("<LOWER_UE>")  # German ü
UPPER_UE = binding("<UPPER_UE>")  # German Ü
LOWER_SS = binding("<LOWER_SS>")  # German ß
UPPER_SS = binding("<UPPER_SS>")  # German ẞ

# numbers
ZERO = binding("<0>")
ONE = binding("<1>")
TWO = binding("<2>")
THREE = binding("<3>")
FOUR = binding("<4>")
FIVE = binding("<5>")
SIX = binding("<6>")
SEVEN = binding("<7>")
EIGHT = binding("<8>")
NINE = binding("<9>")

# special characters
SPACE = binding("<SPACE>")
EXCLAMATION_MARK = binding("<!>")
QUOTATION_MARK_TOP = binding('<">')
QUOTATION_MARK_BOTTOM = binding("<„>")
HASH = binding("<#>")
EURO = binding("<€>")
DOLLAR = binding("<$>")
PERCENT = binding("<%>")
AMPERSAND = binding("<&>")
APOSTROPHE = binding("<'>")
LEFT_PARENTHESIS = binding("<(>")
RIGHT_PARENTHESIS = binding("<)>")
LEFT_BRACKET = binding("<[>")
RIGHT_BRACKET = binding("<]>")
LEFT_BRACE = binding("<{>")
RIGHT_BRACE = binding("<}>")
PLUS = binding("<+>")
MINUS = binding("<->")
ASTERISK = binding("<*>")
SLASH = binding("</>")
BACKSLASH = binding("<\\>")
PERIOD = binding("<.>")
COLON = binding("<:>")
SEMICOLON = binding("<;>")
COMMA = binding("<,>")
LESS_THAN = binding("<<>")
EQUALS = binding("<=>")
GREATER_THAN = binding("<>>")
QUESTION_MARK = binding("<?>")
AT = binding("<@>")
CARET = binding("<^>")
DEGREE = binding("<°>")
UNDERSCORE = binding("<_>")
BACKTICK = binding("<`>")
FORWARDTICK = binding("<´>")
PIPE = binding("<|>")
TILDE = binding("<~>")

# control and navigation keys
RETURN = binding("<RETURN>")
ESCAPE = binding("<ESCAPE>")
TAB = binding("<TAB>")
UP = binding("<UP>")
DOWN = binding("<DOWN>")
LEFT = binding("<LEFT>")
RIGHT = binding("<RIGHT>")
HOME = binding("<HOME>")
END = binding("<END>")
PAGE_UP = binding("<PAGE_UP>")
PAGE_DOWN = binding("<PAGE_DOWN>")
INSERT = binding("<INSERT>")
PRINT_SCREEN = binding("<PRINT_SCREEN>")

# modifier keys
CAPS_LOCK = binding("<CAPS_LOCK>")
LEFT_SHIFT = binding("<LEFT_SHIFT>")
RIGHT_SHIFT = binding("<RIGHT_SHIFT>")
LEFT_CTRL = binding("<LEFT_CTRL>")
RIGHT_CTRL = binding("<RIGHT_CTRL>")
LEFT_ALT = binding("<LEFT_ALT>")
RIGHT_ALT = binding("<RIGHT_ALT>")

# function keys
F1 = binding("<F1>")
F2 = binding("<F2>")
F3 = binding("<F3>")
F4 = binding("<F4>")
F5 = binding("<F5>")
F6 = binding("<F6>")
F7 = binding("<F7>")
F8 = binding("<F8>")
F9 = binding("<F9>")
F10 = binding("<F10>")
F11 = binding("<F11>")
F12 = binding("<F12>")

# function keys (Apple Mac only)
F13 = binding("<F13>")
F14 = binding("<F14>")
F15 = binding("<F15>")
F16 = binding("<F16>")
F17 = binding("<F17>")
F18 = binding("<F18>")
F19 = binding("<F19>")

# grouped bindings
SHIFT = binding("<SHIFT>")
ALT = binding("<ALT>")
CTRL = binding("<CTRL>")
PARENTHESES = binding("<()>")
BRACKETS = binding("<[]>")
BRACES = binding("<{}>")
SLASHES = binding("</\\>")
TICKS = binding("`´")
QUOTATION_MARKS = binding('<„">')

# build in widget events
# all/most
KEY = binding("<KEY>")

PRESS = binding("<PRESS>")
HOLD = binding("<HOLD>")
RELEASE = binding("<RELEASE>")

# Checkboxes
CHECK = binding("<CHECK>")
UNCHECK = binding("<UNCHECK>")

# Entries
FOCUS_IN = binding("<FOCUS_IN>")
FOCUS_OUT = binding("<FOCUS_OUT>")
COPY = binding("<COPY>")
PASTE = binding("<PASTE>")
CUT = binding("<CUT>")
TYPING = binding("<TYPING>")
SELECT_ALL = binding("<SELECT_ALL>")
BACKSPACE = binding("<BACKSPACE>")
DELETE = binding("<DELETE>")

# Sliders
DRAG = binding("<DRAG>")

# Timekeepers
TICKING = binding("<TICKING>")
FINISHED = binding("<FINISHED>")

# Tooltips
SHOW_TOOLTIP = binding("<SHOW_TOOLTIP>")
HIDE_TOOLTIP = binding("<HIDE_TOOLTIP>")

# TODO: widget types

_CHAR_TO_BINDINGS: dict[str, tuple[binding, ...]] = {
	" ": (SPACE,),
	"!": (EXCLAMATION_MARK,),
	'"': (QUOTATION_MARK_TOP, QUOTATION_MARKS),
	"„": (QUOTATION_MARK_BOTTOM, QUOTATION_MARKS),
	"#": (HASH,),
	"€": (EURO,),
	"$": (DOLLAR,),
	"%": (PERCENT,),
	"&": (AMPERSAND,),
	"'": (APOSTROPHE,),
	"(": (LEFT_PARENTHESIS, PARENTHESES),
	")": (RIGHT_PARENTHESIS, PARENTHESES),
	"[": (LEFT_BRACKET, BRACKETS),
	"]": (RIGHT_BRACKET, BRACKETS),
	"{": (LEFT_BRACE, BRACES),
	"}": (RIGHT_BRACE, BRACES),
	"+": (PLUS,),
	"-": (MINUS,),
	"*": (ASTERISK,),
	"/": (SLASH, SLASHES),
	"\\": (BACKSLASH, SLASHES),
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
	"`": (BACKTICK, TICKS),
	"´": (FORWARDTICK, TICKS),
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

_SPECIAL_KEYNAME_TO_GROUP_BINDINGS: dict[str, binding] = {
	"LEFT_SHIFT": SHIFT, "RIGHT_SHIFT": SHIFT,
	"LEFT_CTRL": CTRL, "RIGHT_CTRL": CTRL,
	"LEFT_ALT": ALT, "RIGHT_ALT": ALT
}