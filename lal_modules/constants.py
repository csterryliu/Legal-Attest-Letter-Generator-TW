"""
Constants which will be used in the main logic.
"""

LETTER_FORMAT_PATH = 'res/tw_lal.pdf'
DEFAULT_FONT_PATH = 'res/TW-Kai-98_1.ttf'
_PDF_INCH = 72
########################################################################
# pre-defined coordinates of main article
########################################################################
LETTER_FORMAT_WIDE_HEIGHT = (8.2677 * _PDF_INCH, 11.692 * _PDF_INCH)
CONTENT_X_Y_BEGIN = (1.27 * _PDF_INCH, 7.82 * _PDF_INCH)
CONTENT_X_Y_INTERVAL = (0.33 * _PDF_INCH, 0.47 * _PDF_INCH)
CONTENT_X_Y_FIX = (0.001 * _PDF_INCH, 0.001 * _PDF_INCH)
CONTENT_MAX_CHARACTER_PER_LINE = 20
CONTENT_MAX_LINE_PER_PAGE = 10
NAME_COORDINATE = {
    's_x_y_begin': (4.60 * _PDF_INCH, 10.27 * _PDF_INCH),
    's_x_y_interval': (0.48 * _PDF_INCH, 0.15 * _PDF_INCH),
    'r_x_y_begin': (4.60 * _PDF_INCH, 9.66 * _PDF_INCH),
    'r_x_y_interval': (0.48 * _PDF_INCH, 0.15 * _PDF_INCH),
    'c_x_y_begin': (4.60 * _PDF_INCH, 9.06 * _PDF_INCH),
    'c_x_y_interval': (0.48 * _PDF_INCH, 0),
}
ADDR_COORDINATE = {
    's_x_y_begin': (4.72 * _PDF_INCH, 9.95 * _PDF_INCH),
    's_y_interval': 0.15 * _PDF_INCH,
    'r_x_y_begin': (4.72 * _PDF_INCH, 9.32 * _PDF_INCH),
    'r_y_interval': 0.15 * _PDF_INCH,
    'c_x_y_begin': (4.72 * _PDF_INCH, 8.84 * _PDF_INCH),
    'c_y_interval': 0
}
LETTER_LEFTMOST_BORDER = 7.80 * _PDF_INCH
SENDER_FIRST_LINE_LEFTMOST_BORDER = 7.10 * _PDF_INCH

########################################################################
# pre-defined coordinates of additional information box
########################################################################
BOX_UPPDERLEFT_X_Y = (3.125 * _PDF_INCH, 10.611 * _PDF_INCH)
BOX_UPPDERRIGHT_X_Y = (7.847 * _PDF_INCH, 10.611 * _PDF_INCH)
CUT_INFO_X_Y = (5.111 * _PDF_INCH, 10.750 * _PDF_INCH)
QUOTE_X_Y = (3.264 * _PDF_INCH, 10.472 * _PDF_INCH)
RECT_X_Y_W_H = (7.146 * _PDF_INCH, 10.25 * _PDF_INCH, 0.139 * _PDF_INCH, 0.167 * _PDF_INCH)
CHT_IN_RECT_X_Y = (7.146 * _PDF_INCH, 10.292 * _PDF_INCH)
DETAIL_START = (4.167 * _PDF_INCH, 10.292 * _PDF_INCH)
DETAIL_Y_INTERVAL = 0.278 * _PDF_INCH
TITLE_START = (3.264 * _PDF_INCH, 10.139 * _PDF_INCH)
TITLE_Y_INTERVAL = 0.139 * _PDF_INCH
CC_RECEIVER_FIX_X_Y = (0.278 * _PDF_INCH, 0.069 * _PDF_INCH)
