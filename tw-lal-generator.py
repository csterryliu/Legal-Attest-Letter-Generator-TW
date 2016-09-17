#!/usr/local/bin/python3
import argparse
from os import remove
from lal_modules import pdfpage
from lal_modules import pdfpainter
from lal_modules.constants import *

def main():
    args = process_args()
    senders = args.senderName
    senders_addr = args.senderAddr
    receivers = args.receiverName
    receivers_addr = args.receiverAddr
    ccs = args.ccName
    cc_addr = args.ccAddr
    text = read_main_article(args.article_file)
    output_filename = args.outputFileName

    generator = pdfpainter.PDFPainter(GENERATED_TEXT_PATH,
                                      LETTER_FORMAT_WIDE_HEIGHT[0], LETTER_FORMAT_WIDE_HEIGHT[1])
    blank_letter_producer = pdfpage.PDFPagePick(LETTER_FORMAT_PATH, GENERATED_BLANK_LETTER_PATH)

    # write name and address directly if one page is enough
    one_page_is_enough = is_only_one_name_or_address(senders, senders_addr) and \
                      is_only_one_name_or_address(receivers, receivers_addr) and \
                      is_only_one_name_or_address(ccs, cc_addr)
    if one_page_is_enough:
        generator.setFont(DEFAULT_FONT_PATH, 10)
        fill_name_address_on_first_page(generator, senders, senders_addr, 's')
        fill_name_address_on_first_page(generator, receivers, receivers_addr, 'r')
        fill_name_address_on_first_page(generator, ccs, cc_addr, 'c')

    generator.setFont(DEFAULT_FONT_PATH, 20)
    parse_main_article(generator, blank_letter_producer, text)

    if one_page_is_enough is False:
        draw_info_box(generator, senders, senders_addr, receivers, receivers_addr, ccs, cc_addr)
        generator.endThisPage()
        blank_letter_producer.insert_blank_page()

    blank_letter_producer.save()
    generator.save()

    print('Merging...')
    page_merge = pdfpage.PDFPageMerge(GENERATED_TEXT_PATH,
                                      GENERATED_BLANK_LETTER_PATH,
                                      output_filename)
    for i in range(page_merge.get_src_total_page()):
        page_merge.merge_src_page_to_dest_page(i, i)
    page_merge.save()

    remove(GENERATED_TEXT_PATH)
    remove(GENERATED_BLANK_LETTER_PATH)

    print('Done. Filename: ', output_filename)

def process_args():
    arg_parser = argparse.ArgumentParser(description=u'台灣郵局存證信函產生器',
                                         add_help=False)
    arg_parser.add_argument('--help',
                            action='help',
                            help=u'顯示使用說明')
    arg_parser.add_argument('article_file',
                            action='store',
                            help=u'存證信函全文之純文字檔路徑')
    arg_parser.add_argument('--senderName',
                            action='append',
                            nargs='+',
                            metavar=u'寄件人姓名',
                            default=[])
    arg_parser.add_argument('--senderAddr',
                            action='append',
                            metavar=u'寄件人詳細地址',
                            default=[])
    arg_parser.add_argument('--receiverName',
                            action='append',
                            nargs='+',
                            metavar=u'收件人姓名',
                            default=[])
    arg_parser.add_argument('--receiverAddr',
                            action='append',
                            metavar=u'收件人詳細地址',
                            default=[])
    arg_parser.add_argument('--ccName',
                            action='append',
                            nargs='+',
                            metavar=u'副本收件人姓名',
                            default=[])
    arg_parser.add_argument('--ccAddr',
                            action='append',
                            metavar=u'副本收件人詳細地址',
                            default=[])
    arg_parser.add_argument('--outputFileName',
                            action='store',
                            metavar=u'輸出之檔案名稱',
                            default='output.pdf')
    return arg_parser.parse_args()

def is_only_one_name_or_address(namelist, addresslist):
    ret_value = True
    if len(namelist) != 0:
        ret_value = ret_value and (len(namelist) == 1)
    if len(addresslist) != 0:
        ret_value = ret_value and (len(addresslist) == 1)
    return ret_value

def read_main_article(filepath):
    codec_name = 'utf-8'
    bom = b'\xef\xbb\xbf'.decode(codec_name)
    text_file = open(filepath, 'r', encoding=codec_name)
    text = text_file.read()
    text_file.close()
    # In case the user insists on using Notepad of Windows, remove BOM
    text = text.lstrip(bom)
    return text

def parse_main_article(painter, page_pick, main_text):
    print('Parse main article...')
    x_begin, y_begin, line_counter, char_counter = reset_coordinates_and_counters()
    for i in range(0, len(main_text)):
        if main_text[i] == '\n' or (char_counter > CONTENT_MAX_CHARACTER_PER_LINE):
            x_begin, y_begin = get_new_line_coordinate(y_begin)
            line_counter = line_counter + 1
            char_counter = 1
            if main_text[i] == '\n':
                continue
        if line_counter > CONTENT_MAX_LINE_PER_PAGE:
            painter.endThisPage()
            page_pick.pick_individual_pages([0])
            x_begin, y_begin, line_counter, char_counter = reset_coordinates_and_counters()
        painter.drawString(x_begin, y_begin, main_text[i])
        x_begin += (CONTENT_X_Y_INTERVAL[0] - CONTENT_X_Y_FIX[0])
        char_counter = char_counter + 1
    painter.endThisPage()
    page_pick.pick_individual_pages([0])

def get_new_line_coordinate(current_y):
    new_x = CONTENT_X_Y_BEGIN[0]
    new_y = current_y - (CONTENT_X_Y_INTERVAL[1] + CONTENT_X_Y_FIX[1])
    return new_x, new_y

def reset_coordinates_and_counters():
    return CONTENT_X_Y_BEGIN[0], CONTENT_X_Y_BEGIN[1], 1, 1

def draw_info_box(painter,
                  sender_list, sender_addr_list,
                  receiver_list, receiver_addr_list,
                  cc_list, cc_addr_list):
    painter.setFont(DEFAULT_FONT_PATH, 8)
    painter.drawString(CUT_INFO_X_Y[0], CUT_INFO_X_Y[1], u'[請自行剪下貼上]')
    painter.drawLine(BOX_UPPDERLEFT_X_Y[0], BOX_UPPDERLEFT_X_Y[1],
                     BOX_UPPDERRIGHT_X_Y[0], BOX_UPPDERRIGHT_X_Y[1])
    painter.drawString(QUOTE_X_Y[0], QUOTE_X_Y[1],
                       u'（寄件人如為機關、團體、學校、公司、商號請加蓋單位圖章及法定代理人簽名或蓋章）')
    painter.drawRect(RECT_X_Y_W_H[0], RECT_X_Y_W_H[1], RECT_X_Y_W_H[2], RECT_X_Y_W_H[3])
    painter.setFont(DEFAULT_FONT_PATH, 10)
    painter.drawString(CHT_IN_RECT_X_Y[0], CHT_IN_RECT_X_Y[1], u'印')

    painter.drawString(TITLE_START[0], TITLE_START[1], u'一、寄件人')
    x_begin = DETAIL_START[0]
    y_begin = DETAIL_START[1]
    y_begin = fill_name_address_in_info_box(painter,
                                            x_begin, y_begin,
                                            sender_list, sender_addr_list)

    y_begin -= TITLE_Y_INTERVAL
    painter.drawString(TITLE_START[0], y_begin, u'二、收件人')
    y_begin = fill_name_address_in_info_box(painter,
                                            x_begin, y_begin,
                                            receiver_list, receiver_addr_list)

    y_begin -= TITLE_Y_INTERVAL
    painter.drawString(TITLE_START[0], y_begin, u'三、')
    painter.drawString(TITLE_START[0]+CC_RECEIVER_FIX_X_Y[0],
                       y_begin+CC_RECEIVER_FIX_X_Y[1], u'副 本')
    painter.drawString(TITLE_START[0]+CC_RECEIVER_FIX_X_Y[0],
                       y_begin-CC_RECEIVER_FIX_X_Y[1], u'收件人')
    y_begin = fill_name_address_in_info_box(painter,
                                            x_begin, y_begin,
                                            cc_list, cc_addr_list)

    painter.drawLine(BOX_UPPDERLEFT_X_Y[0], BOX_UPPDERLEFT_X_Y[1],
                     BOX_UPPDERLEFT_X_Y[0], y_begin)  # left
    painter.drawLine(BOX_UPPDERLEFT_X_Y[0], y_begin,
                     BOX_UPPDERRIGHT_X_Y[0], y_begin)  # buttom
    painter.drawLine(BOX_UPPDERRIGHT_X_Y[0], BOX_UPPDERRIGHT_X_Y[1],
                     BOX_UPPDERRIGHT_X_Y[0], y_begin)  # right

def fill_name_address_in_info_box(painter, x_begin, y_begin, namelist, addresslist):
    max_count = max(len(namelist), len(addresslist))
    if max_count == 0:
        painter.drawString(x_begin, y_begin, u'姓名：')
        y_begin -= DETAIL_Y_INTERVAL
        painter.drawString(x_begin, y_begin, u'詳細地址：')
        y_begin -= DETAIL_Y_INTERVAL

    for i in range(max_count):
        all_name = ' '.join(namelist[i]) if i <= len(namelist)-1 else ''
        painter.drawString(x_begin, y_begin, u'姓名：' + all_name)
        y_begin -= DETAIL_Y_INTERVAL
        address = addresslist[i] if i <= len(addresslist)-1 else ''
        painter.drawString(x_begin, y_begin, u'詳細地址：' + address)
        y_begin -= DETAIL_Y_INTERVAL

    return y_begin

def fill_name_address_on_first_page(painter, namelist, addresslist, type_):
    if len(namelist) == 1:
        all_name = ' '.join(namelist[0])
        painter.drawString(NAME_COORDINATE[type_+'_x_y_begin'][0],
                           NAME_COORDINATE[type_+'_x_y_begin'][1],
                           all_name)
    if len(addresslist) == 1:
        painter.drawString(ADDR_COORDINATE[type_+'_x_y_begin'][0],
                           ADDR_COORDINATE[type_+'_x_y_begin'][1],
                           addresslist[0])

##############################
### Main program goes here
##############################
if __name__ == '__main__':
    main()
