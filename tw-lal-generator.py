#!/usr/local/bin/python3
import argparse
from os import remove
from lal_modules import pdfpage
from lal_modules import pdfpainter
from lal_modules.constants import *

codec_name = 'utf-8'

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
            page_pick.pickIndividualPages([0])
            x_begin, y_begin, line_counter, char_counter = reset_coordinates_and_counters()
        painter.drawString(x_begin, y_begin, main_text[i])
        x_begin += (CONTENT_X_Y_INTERVAL[0] - CONTENT_X_Y_FIX[0])
        char_counter = char_counter + 1
    generator.endThisPage()
    page_pick.pickIndividualPages([0])

def get_new_line_coordinate(current_y):
    new_x = CONTENT_X_Y_BEGIN[0]
    new_y = current_y - (CONTENT_X_Y_INTERVAL[1] + CONTENT_X_Y_FIX[1])
    return new_x, new_y

def reset_coordinates_and_counters():
    return CONTENT_X_Y_BEGIN[0], CONTENT_X_Y_BEGIN[1], 1, 1

def draw_info_box(painter):
    painter.setFont(DEFAULT_FONT_PATH, 8)
    painter.drawString(cut_info_x_y[0], cut_info_x_y[1], u'[請自行剪下貼上]')
    painter.drawLine(box_uppderLeft_x_y[0], box_uppderLeft_x_y[1],
                     box_uppderRight_x_y[0], box_uppderRight_x_y[1])
    painter.drawString(quote_x_y[0],
                       quote_x_y[1],
                       u'（寄件人如為機關、團體、學校、公司、商號請加蓋單位圖章及法定代理人簽名或蓋章）')
    painter.drawRect(rect_x_y_w_h[0], rect_x_y_w_h[1], rect_x_y_w_h[2], rect_x_y_w_h[3])
    painter.setFont(DEFAULT_FONT_PATH, 10)
    painter.drawString(cht_in_rect_x_y[0], cht_in_rect_x_y[1], u'印')

    painter.drawString(title_start[0], title_start[1], u'一、寄件人')
    x_begin = detail_start[0]
    y_begin = detail_start[1]
    y_begin = fill_name_address_in_info_box(x_begin, y_begin, senders, sendersAddr)

    y_begin -= title_y_interval
    painter.drawString(title_start[0], y_begin, u'二、收件人')
    y_begin = fill_name_address_in_info_box(x_begin, y_begin, receivers, receiversAddr)

    y_begin -= title_y_interval
    painter.drawString(title_start[0], y_begin, u'三、')
    painter.drawString(title_start[0]+cc_receiver_fix_x_y[0],
                       y_begin+cc_receiver_fix_x_y[1], u'副 本')
    painter.drawString(title_start[0]+cc_receiver_fix_x_y[0],
                       y_begin-cc_receiver_fix_x_y[1], u'收件人')
    y_begin = fill_name_address_in_info_box(x_begin, y_begin, cc, ccAddr)

    painter.drawLine(box_uppderLeft_x_y[0], box_uppderLeft_x_y[1],
                     box_uppderLeft_x_y[0], y_begin)  # left
    painter.drawLine(box_uppderLeft_x_y[0], y_begin, box_uppderRight_x_y[0], y_begin)  # buttom
    painter.drawLine(box_uppderRight_x_y[0], box_uppderRight_x_y[1],
                     box_uppderRight_x_y[0], y_begin)  # right

def fill_name_address_in_info_box(x_begin, y_begin, namelist, addresslist):
    max_count = max(len(namelist), len(addresslist))
    if max_count == 0:
        generator.drawString(x_begin, y_begin, u'姓名：')
        y_begin -= detail_y_interval
        generator.drawString(x_begin, y_begin, u'詳細地址：')
        y_begin -= detail_y_interval

    for i in range(max_count):
        all_name = ' '.join(namelist[i]) if i <= len(namelist)-1 else ''
        generator.drawString(x_begin, y_begin, u'姓名：' + all_name)
        y_begin -= detail_y_interval
        address = addresslist[i] if i <= len(addresslist)-1 else ''
        generator.drawString(x_begin, y_begin, u'詳細地址：' + address)
        y_begin -= detail_y_interval

    return y_begin

def fill_name_address_on_first_page(namelist, addresslist, type_):
    if len(namelist) == 1:
        all_name = ' '.join(namelist[0])
        generator.drawString(NAME_COORDINATE[type_+'_x_y_begin'][0],
                             NAME_COORDINATE[type_+'_x_y_begin'][1],
                             all_name)
    if len(addresslist) == 1:
        generator.drawString(ADDR_COORDINATE[type_+'_x_y_begin'][0],
                             ADDR_COORDINATE[type_+'_x_y_begin'][1],
                             addresslist[0])

##############################
### Main program goes here
##############################
args = process_args()
senders = args.senderName
sendersAddr = args.senderAddr
receivers = args.receiverName
receiversAddr = args.receiverAddr
cc = args.ccName
ccAddr = args.ccAddr
text = read_main_article(args.article_file)
outputFileName = args.outputFileName

generator = pdfpainter.PDFPainter(GENERATED_TEXT_PATH,
                                  LETTER_FORMAT_WIDE_HEIGHT[0], LETTER_FORMAT_WIDE_HEIGHT[1])
blank_letter_producer = pdfpage.PDFPagePick(LETTER_FORMAT_PATH, GENERATED_BLANK_LETTER_PATH)

# write name and address directly if one page is enough
onePageIsEnough = is_only_one_name_or_address(senders, sendersAddr) and \
                  is_only_one_name_or_address(receivers, receiversAddr) and \
                  is_only_one_name_or_address(cc, ccAddr)
if onePageIsEnough:
    generator.setFont(DEFAULT_FONT_PATH, 10)
    fill_name_address_on_first_page(senders, sendersAddr, 's')
    fill_name_address_on_first_page(receivers, receiversAddr, 'r')
    fill_name_address_on_first_page(cc, ccAddr, 'c')

generator.setFont(DEFAULT_FONT_PATH, 20)
parse_main_article(generator, blank_letter_producer, text)

if onePageIsEnough is False:
    draw_info_box(generator)
    generator.endThisPage()
    blank_letter_producer.insertBlankPage()

blank_letter_producer.save()
generator.save()

print('Merging...')
pageMerge = pdfpage.PDFPageMerge(GENERATED_TEXT_PATH, GENERATED_BLANK_LETTER_PATH, outputFileName)
for i in range(pageMerge.getSrcTotalPage()):
    pageMerge.mergeSrcPageToDestPage(i, i)
pageMerge.save()

remove(GENERATED_TEXT_PATH)
remove(GENERATED_BLANK_LETTER_PATH)

print('Done. Filename: ', outputFileName)
