LETTER_FORMAT_PATH = '../res/tw_lal.pdf'
GENERATED_TEXT_PATH = 'content.pdf'
GENERATED_BLANK_LETTER_PATH = 'blank_letter.pdf'
DEFAULT_FONT_PATH = '../res/TW-Kai-98_1.ttf'
PDF_INCH = 72
########################################################################
# pre-defined cordinates of main article
########################################################################
LETTER_FORMAT_WIDE_HEIGHT = (8.2677 * PDF_INCH, 11.692 * PDF_INCH)
CONTENT_X_Y_BEGIN = (1.27 * PDF_INCH, 7.82 * PDF_INCH)
CONTENT_X_Y_INTERVAL = (0.33 * PDF_INCH, 0.47 * PDF_INCH)
CONTENT_X_Y_FIX = (0.001 * PDF_INCH, 0.001 * PDF_INCH)
CONTENT_MAX_WORD_PER_LINE = 20
CONTENT_MAX_LINE_PER_PAGE = 10
NAME_CORDINATE = {
's_x_y_begin': (4.60 * PDF_INCH, 10.27 * PDF_INCH),
's_x_y_interval': (0.48 * PDF_INCH, 0.15 * PDF_INCH),
'r_x_y_begin': (4.60 * PDF_INCH, 9.65 * PDF_INCH),
'r_x_y_interval': (0.48 * PDF_INCH, 0.15 * PDF_INCH),
'c_x_y_begin': (4.60 * PDF_INCH, 9.02 * PDF_INCH),
'c_x_y_interval': (0.48 * PDF_INCH, 0),
}
ADDR_CORDINATE = {
's_x_y_begin': (4.72 * PDF_INCH, 9.95 * PDF_INCH),
's_y_interval': 0.15 * PDF_INCH,
'r_x_y_begin': (4.72 * PDF_INCH, 9.32 * PDF_INCH),
'r_y_interval': 0.15 * PDF_INCH,
'c_x_y_begin': (4.72 * PDF_INCH, 8.83 * PDF_INCH),
'c_y_interval': 0
}
LETTER_LEFTMOST_BORDER = 7.80 * PDF_INCH
SENDER_FIRST_LINE_LEFTMOST_BORDER = 7.10 * PDF_INCH

########################################################################
# pre-defined cordinates of additional information box
########################################################################
box_uppderLeft_x_y = (225, 764)
box_uppderRight_x_y = (565, 764)
quote_x_y = (235, 754)
rect_x_y_w_h = (514.5, 738, 10, 12)
cht_in_rect_x_y = (514.5, 741)
detail_start = (300, 741)
detail_y_interval = 20
title_start = (235, 730)
title_y_interval = 10
cc_receiver_fix_x_y = (20, 5)
