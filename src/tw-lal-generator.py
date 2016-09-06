#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from os import remove
import pdfpainter
import pdfpage
from lal_constants import *

def processArgs():
    argParser = argparse.ArgumentParser(description='台灣郵局存證信函產生器',
                                        add_help=False)
    argParser.add_argument('--help',
                            action='help',
                            help='顯示使用說明')
    argParser.add_argument('article_file',
                            action='store',
                            help='存證信函全文之純文字檔路徑')
    argParser.add_argument('--senderName',
                            action='append',
                            nargs='+',
                            metavar='寄件人姓名',
                            default=[])
    argParser.add_argument('--senderAddr',
                            action='append',
                            metavar='寄件人詳細地址',
                            default=[])
    argParser.add_argument('--receiverName',
                            action='append',
                            nargs='+',
                            metavar='收件人姓名',
                            default=[])
    argParser.add_argument('--receiverAddr',
                            action='append',
                            metavar='收件人詳細地址',
                            default=[])
    argParser.add_argument('--ccName',
                            action='append',
                            nargs='+',
                            metavar='副本收件人姓名',
                            default=[])
    argParser.add_argument('--ccAddr',
                            action='append',
                            metavar='副本收件人詳細地址',
                            default=[])
    argParser.add_argument('--outputFileName',
                            action='store',
                            metavar='指定輸出檔案名稱',
                            default='output.pdf')
    return argParser.parse_args()

def isOnlyOneNameOrAddress(namelist, addresslist):
    ret_value = True
    if len(namelist) != 0:
        ret_value = ret_value and (len(namelist) == 1)
    if len(addresslist) != 0:
        ret_value = ret_value and (len(addresslist) == 1)
    return ret_value

def readMainArticle(filepath):
    text_file = open(filepath, 'r')
    text = text_file.read()
    text_file.close()
    return text.decode('utf-8')

def parseMainArticle(painter, mainText):
    print 'Parse main article...'
    x_begin, y_begin, line_counter, char_counter = resetCordinatesAndCounters()
    for i in range(0, len(mainText)):
        if text[i] == '\n' or (char_counter > CONTENT_MAX_CHARACTER_PER_LINE):
            x_begin, y_begin = getNewLineCordinate(y_begin)
            line_counter = line_counter + 1
            char_counter = 1
            if text[i] == '\n':
                continue
        if line_counter > CONTENT_MAX_LINE_PER_PAGE:
            painter.endThisPage()
            blank_letter_producer.pickIndividualPages([0])
            x_begin, y_begin, line_counter, char_counter = resetCordinatesAndCounters()
        painter.drawString(x_begin, y_begin, text[i])
        x_begin += (CONTENT_X_Y_INTERVAL[0] - CONTENT_X_Y_FIX[0])
        char_counter = char_counter + 1

def getNewLineCordinate(currentY):
    newX = CONTENT_X_Y_BEGIN[0]
    newY = currentY - (CONTENT_X_Y_INTERVAL[1] + CONTENT_X_Y_FIX[1])
    return newX, newY

def resetCordinatesAndCounters():
    return CONTENT_X_Y_BEGIN[0], CONTENT_X_Y_BEGIN[1], 1, 1

def drawInfoBox(painter):
    painter.setFont(DEFAULT_FONT_PATH, 8)
    painter.drawLine(box_uppderLeft_x_y[0], box_uppderLeft_x_y[1], box_uppderRight_x_y[0], box_uppderRight_x_y[1])
    painter.drawString(quote_x_y[0], quote_x_y[1], u'（寄件人如為機關、團體、學校、公司、商號請加蓋單位圖章及法定代理人簽名或蓋章）')
    painter.drawRect(rect_x_y_w_h[0], rect_x_y_w_h[1], rect_x_y_w_h[2], rect_x_y_w_h[3])
    painter.setFont(DEFAULT_FONT_PATH, 10)
    painter.drawString(cht_in_rect_x_y[0], cht_in_rect_x_y[1], u'印')

    painter.drawString(title_start[0], title_start[1], u'一、寄件人')
    x_begin = detail_start[0]
    y_begin = detail_start[1]
    y_begin = fillNameAndAddressInInfoBox(x_begin, y_begin, senders, sendersAddr)

    y_begin -= title_y_interval
    painter.drawString(title_start[0], y_begin, u'二、收件人')
    y_begin = fillNameAndAddressInInfoBox(x_begin, y_begin, receivers, receiversAddr)

    y_begin -= title_y_interval
    painter.drawString(title_start[0], y_begin, u'三、')
    painter.drawString(title_start[0]+cc_receiver_fix_x_y[0], y_begin+cc_receiver_fix_x_y[1], u'副 本')
    painter.drawString(title_start[0]+cc_receiver_fix_x_y[0], y_begin-cc_receiver_fix_x_y[1], u'收件人')
    y_begin = fillNameAndAddressInInfoBox(x_begin, y_begin, cc, ccAddr)

    painter.drawLine(box_uppderLeft_x_y[0], box_uppderLeft_x_y[1], box_uppderLeft_x_y[0], y_begin)  # left
    painter.drawLine(box_uppderLeft_x_y[0], y_begin, box_uppderRight_x_y[0], y_begin)  # buttom
    painter.drawLine(box_uppderRight_x_y[0], box_uppderRight_x_y[1], box_uppderRight_x_y[0], y_begin)  # right

def fillNameAndAddressInInfoBox(x_begin, y_begin, namelist, addresslist):
    max_count = max(len(namelist), len(addresslist))
    if max_count == 0:
        generator.drawString(x_begin, y_begin, u'姓名：')
        y_begin -= detail_y_interval
        generator.drawString(x_begin, y_begin, u'詳細地址：')
        y_begin -= detail_y_interval

    while max_count > 0:
        allName = ' '.join(namelist[-max_count]).decode('utf-8') if max_count <= len(namelist) else ''
        generator.drawString(x_begin, y_begin, u'姓名：' + allName)
        y_begin -= detail_y_interval
        address = addresslist[-max_count].decode('utf-8') if len(addresslist) <= len(addresslist) else ''
        generator.drawString(x_begin, y_begin, u'詳細地址：' + address)
        max_count -= 1
        y_begin -= detail_y_interval

    return y_begin

def fillNameAndAddressOnFirstPage(namelist, addresslist, type):
    if len(namelist) == 1:
        allName = ' '.join(namelist[0]).decode('utf-8')
        generator.drawString(NAME_COORDINATE[type+'_x_y_begin'][0], NAME_COORDINATE[type+'_x_y_begin'][1], allName)
    if len(addresslist) == 1:
        generator.drawString(ADDR_COORDINATE[type+'_x_y_begin'][0] , ADDR_COORDINATE[type+'_x_y_begin'][1], addresslist[0])

##############################
### Main program goes here
##############################
args = processArgs()
senders = args.senderName
sendersAddr = args.senderAddr
receivers = args.receiverName
receiversAddr = args.receiverAddr
cc = args.ccName
ccAddr = args.ccAddr
text = readMainArticle(args.article_file)
outputFileName = args.outputFileName

generator = pdfpainter.PDFPainter(GENERATED_TEXT_PATH, LETTER_FORMAT_WIDE_HEIGHT[0], LETTER_FORMAT_WIDE_HEIGHT[1])
blank_letter_producer = pdfpage.PDFPagePick(LETTER_FORMAT_PATH, GENERATED_BLANK_LETTER_PATH)

# write name and address directly if one page is enough
onePageIsEnough = isOnlyOneNameOrAddress(senders, sendersAddr) and isOnlyOneNameOrAddress(receivers, receiversAddr) and isOnlyOneNameOrAddress(cc, ccAddr)
if onePageIsEnough:
    generator.setFont(DEFAULT_FONT_PATH, 10)
    fillNameAndAddressOnFirstPage(senders, sendersAddr, 's')
    fillNameAndAddressOnFirstPage(receivers, receiversAddr, 'r')
    fillNameAndAddressOnFirstPage(cc, ccAddr, 'c')

generator.setFont(DEFAULT_FONT_PATH, 20)
parseMainArticle(generator, text)
generator.endThisPage()
blank_letter_producer.pickIndividualPages([0])

if onePageIsEnough is False:
    drawInfoBox(generator)
    generator.endThisPage()
    blank_letter_producer.insertBlankPage()

blank_letter_producer.save()
generator.save()

print 'Merging...'
pageMerge = pdfpage.PDFPageMerge(GENERATED_TEXT_PATH, GENERATED_BLANK_LETTER_PATH, outputFileName)
for i in range(pageMerge.getSrcTotalPage()):
    pageMerge.mergeSrcPageToDestPage(i, i)
pageMerge.save()

remove(GENERATED_TEXT_PATH)
remove(GENERATED_BLANK_LETTER_PATH)

print 'Done. Filename: ' + outputFileName
