"""
Core functions
"""
from os import remove
from . import pdfpage
from . import pdfpainter
from .constants import *

def read_main_article(filepath):
    codec_name = 'utf-8'
    bom = b'\xef\xbb\xbf'.decode(codec_name)
    try:
        text_file = open(filepath, 'r', encoding=codec_name)
        text = text_file.read()
        text_file.close()
    except UnicodeDecodeError:
        print('Failed to read file.')
        return None
    except FileNotFoundError:
        print('File not found.')
        return None
    # In case the user insists on using Notepad of Windows, remove BOM
    text = text.lstrip(bom)
    return text

def merge_text_and_letter(output_filename):
    print('Merging...')
    page_merge = pdfpage.PDFPageMerge(GENERATED_TEXT_PATH,
                                      GENERATED_BLANK_LETTER_PATH,
                                      output_filename)
    for i in range(page_merge.get_src_total_page()):
        page_merge.merge_src_page_to_dest_page(i, i)
    page_merge.save()

def clean_temp_files():
    remove(GENERATED_TEXT_PATH)
    remove(GENERATED_BLANK_LETTER_PATH)

def generate_text_and_letter(senders, senders_addr,
                             receivers, receivers_addr,
                             ccs, cc_addr,
                             main_text):
    generator = pdfpainter.PDFPainter(GENERATED_TEXT_PATH,
                                      LETTER_FORMAT_WIDE_HEIGHT[0], LETTER_FORMAT_WIDE_HEIGHT[1])
    blank_letter_producer = pdfpage.PDFPagePick(LETTER_FORMAT_PATH, GENERATED_BLANK_LETTER_PATH)

    # write name and address directly if one page is enough
    one_page_is_enough = _is_only_one_name_or_address(senders, senders_addr) and \
                      _is_only_one_name_or_address(receivers, receivers_addr) and \
                      _is_only_one_name_or_address(ccs, cc_addr)
    if one_page_is_enough:
        generator.set_font(DEFAULT_FONT_PATH, 10)
        _fill_name_address_on_1st_page(generator, senders, senders_addr, 's')
        _fill_name_address_on_1st_page(generator, receivers, receivers_addr, 'r')
        _fill_name_address_on_1st_page(generator, ccs, cc_addr, 'c')

    generator.set_font(DEFAULT_FONT_PATH, 20)
    _parse_main_article(generator, blank_letter_producer, main_text)

    if one_page_is_enough is False:
        _draw_info_box(generator, senders, senders_addr, receivers, receivers_addr, ccs, cc_addr)
        generator.end_this_page()
        blank_letter_producer.insert_blank_page()

    blank_letter_producer.save()
    generator.save()

def _is_only_one_name_or_address(namelist, addresslist):
    ret_value = True
    if namelist:
        ret_value = ret_value and (len(namelist) == 1)
    if addresslist:
        ret_value = ret_value and (len(addresslist) == 1)
    return ret_value

def _fill_name_address_on_1st_page(painter, namelist, addresslist, type_):
    if len(namelist) == 1:
        all_name = ' '.join(namelist[0])
        painter.draw_string(NAME_COORDINATE[type_+'_x_y_begin'][0],
                            NAME_COORDINATE[type_+'_x_y_begin'][1],
                            all_name)
    if len(addresslist) == 1:
        painter.draw_string(ADDR_COORDINATE[type_+'_x_y_begin'][0],
                            ADDR_COORDINATE[type_+'_x_y_begin'][1],
                            addresslist[0])

def _parse_main_article(painter, page_pick, main_text):
    print('Parse main article...')
    x_begin, y_begin, line_counter, char_counter = _reset_coordinates_and_counters()
    for i in range(0, len(main_text)):
        if main_text[i] == '\n' or (char_counter > CONTENT_MAX_CHARACTER_PER_LINE):
            x_begin, y_begin = _get_new_line_coordinate(y_begin)
            line_counter = line_counter + 1
            char_counter = 1
            if main_text[i] == '\n':
                continue
        if line_counter > CONTENT_MAX_LINE_PER_PAGE:
            painter.end_this_page()
            page_pick.pick_individual_pages([0])
            x_begin, y_begin, line_counter, char_counter = _reset_coordinates_and_counters()
        painter.draw_string(x_begin, y_begin, main_text[i])
        x_begin += (CONTENT_X_Y_INTERVAL[0] - CONTENT_X_Y_FIX[0])
        char_counter = char_counter + 1
    painter.end_this_page()
    page_pick.pick_individual_pages([0])

def _get_new_line_coordinate(current_y):
    new_x = CONTENT_X_Y_BEGIN[0]
    new_y = current_y - (CONTENT_X_Y_INTERVAL[1] + CONTENT_X_Y_FIX[1])
    return new_x, new_y

def _reset_coordinates_and_counters():
    return CONTENT_X_Y_BEGIN[0], CONTENT_X_Y_BEGIN[1], 1, 1

def _draw_info_box(painter,
                   sender_list, sender_addr_list,
                   receiver_list, receiver_addr_list,
                   cc_list, cc_addr_list):
    painter.set_font(DEFAULT_FONT_PATH, 8)
    painter.draw_string(CUT_INFO_X_Y[0], CUT_INFO_X_Y[1], u'[請自行剪下貼上]')
    painter.draw_line(BOX_UPPDERLEFT_X_Y[0], BOX_UPPDERLEFT_X_Y[1],
                      BOX_UPPDERRIGHT_X_Y[0], BOX_UPPDERRIGHT_X_Y[1])
    painter.draw_string(QUOTE_X_Y[0], QUOTE_X_Y[1],
                        u'（寄件人如為機關、團體、學校、公司、商號請加蓋單位圖章及法定代理人簽名或蓋章）')
    painter.draw_rect(RECT_X_Y_W_H[0], RECT_X_Y_W_H[1], RECT_X_Y_W_H[2], RECT_X_Y_W_H[3])
    painter.set_font(DEFAULT_FONT_PATH, 10)
    painter.draw_string(CHT_IN_RECT_X_Y[0], CHT_IN_RECT_X_Y[1], u'印')

    painter.draw_string(TITLE_START[0], TITLE_START[1], u'一、寄件人')
    kwargs = {'painter': painter, 'x_begin': DETAIL_START[0], 'y_begin': DETAIL_START[1]}
    kwargs = fill_name_address(sender_list, sender_addr_list,
                               _fill_info_if_empty, _fill_info_if_nonempty,
                               **kwargs)

    kwargs['y_begin'] -= TITLE_Y_INTERVAL
    painter.draw_string(TITLE_START[0], kwargs['y_begin'], u'二、收件人')
    kwargs = fill_name_address(receiver_list, receiver_addr_list,
                               _fill_info_if_empty, _fill_info_if_nonempty,
                               **kwargs)

    kwargs['y_begin'] -= TITLE_Y_INTERVAL
    painter.draw_string(TITLE_START[0], kwargs['y_begin'], u'三、')
    painter.draw_string(TITLE_START[0]+CC_RECEIVER_FIX_X_Y[0],
                        kwargs['y_begin']+CC_RECEIVER_FIX_X_Y[1], u'副 本')
    painter.draw_string(TITLE_START[0]+CC_RECEIVER_FIX_X_Y[0],
                        kwargs['y_begin']-CC_RECEIVER_FIX_X_Y[1], u'收件人')
    kwargs = fill_name_address(cc_list, cc_addr_list,
                               _fill_info_if_empty, _fill_info_if_nonempty,
                               **kwargs)

    painter.draw_line(BOX_UPPDERLEFT_X_Y[0], BOX_UPPDERLEFT_X_Y[1],
                      BOX_UPPDERLEFT_X_Y[0], kwargs['y_begin'])  # left
    painter.draw_line(BOX_UPPDERLEFT_X_Y[0], kwargs['y_begin'],
                      BOX_UPPDERRIGHT_X_Y[0], kwargs['y_begin'])  # buttom
    painter.draw_line(BOX_UPPDERRIGHT_X_Y[0], BOX_UPPDERRIGHT_X_Y[1],
                      BOX_UPPDERRIGHT_X_Y[0], kwargs['y_begin'])  # right

# template method pattern
# skeleton
def fill_name_address(namelist, addresslist,
                      do_when_list_empty, do_when_list_nonempty,
                      **kwargs):
    max_count = max(len(namelist), len(addresslist))
    ret_value = None
    if max_count == 0:
        do_when_list_empty(**kwargs)

    for i in range(max_count):
        all_name = ' '.join(namelist[i]) if i <= len(namelist)-1 else ''
        address = addresslist[i] if i <= len(addresslist)-1 else ''
        # TODO How to propagate the necessary input parameter nicely?
        kwargs = do_when_list_nonempty(all_name, address, **kwargs)

    return kwargs

# action
def _fill_info_if_empty(**kwargs):
    painter.draw_string(kwargs['x_begin'], kwargs['y_begin'], u'姓名：')
    kwargs['y_begin'] -= DETAIL_Y_INTERVAL
    painter.draw_string(kwargs['x_begin'], kwargs['y_begin'], u'詳細地址：')
    kwargs['y_begin'] -= DETAIL_Y_INTERVAL

# action
def _fill_info_if_nonempty(all_name, address, **kwargs):
    kwargs['painter'].draw_string(kwargs['x_begin'], kwargs['y_begin'],
                                  u'姓名：' + all_name)
    kwargs['y_begin'] -= DETAIL_Y_INTERVAL
    kwargs['painter'].draw_string(kwargs['x_begin'], kwargs['y_begin'],
                                  u'詳細地址：' + address)
    kwargs['y_begin'] -= DETAIL_Y_INTERVAL
    return kwargs
