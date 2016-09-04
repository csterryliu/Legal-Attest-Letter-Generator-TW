#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
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
                            metavar='寄件人姓名')
    argParser.add_argument('--senderAddr',
                            action='append',
                            metavar='寄件人詳細地址')
    argParser.add_argument('--receiverName',
                            action='append',
                            nargs='+',
                            metavar='收件人姓名')
    argParser.add_argument('--receiverAddr',
                            action='append',
                            metavar='收件人詳細地址')
    argParser.add_argument('--ccName',
                            action='append',
                            nargs='+',
                            metavar='副本收件人姓名')
    argParser.add_argument('--ccAddr',
                            action='append',
                            metavar='副本收件人詳細地址')
    return argParser.parse_args()

def isOnlyOneNameOrAddress(namelist, addresslist):
    ret_value = True
    if namelist is not None:
        ret_value = ret_value and (len(namelist) == 1)
    if addresslist is not None:
        ret_value = ret_value and (len(addresslist) == 1)
    return ret_value

def readMainText(filepath):
    text_file = open(filepath, 'r')
    text = text_file.read()
    text_file.close()
    return text.decode('utf-8')

def fillNameAndAddressOnFirstPage(namelist, addresslist, type):
    if namelist != None:
        for i in range(len(namelist)):
            name = namelist[0][i]
            generator.drawString(NAME_CORDINATE[type+'_x_y_begin'][0] + (i*NAME_CORDINATE[type+'_x_y_interval'][0]), NAME_CORDINATE[type+'_x_y_begin'][1], name)
    if (addresslist is not None):
        generator.drawString(ADDR_CORDINATE[type+'_x_y_begin'][0] , ADDR_CORDINATE[type+'_x_y_begin'][1], addresslist[0])

def getNewLineCordinate(currentY):
    newX = CONTENT_X_Y_BEGIN[0]
    newY = currentY - (CONTENT_X_Y_INTERVAL[1] + CONTENT_X_Y_FIX[1])
    return newX, newY

def resetCordinatesAndCounters():
    return CONTENT_X_Y_BEGIN[0], CONTENT_X_Y_BEGIN[1], 1, 1

args = processArgs()
senders = args.senderName
sendersAddr = args.senderAddr
receivers = args.receiverName
receiversAddr = args.receiverAddr
cc = args.ccName
ccAddr = args.ccAddr
text = readMainText(args.article_file)

generator = pdfpainter.PDFPainter(GENERATED_TEXT_PATH, LETTER_FORMAT_WIDE_HEIGHT[0], LETTER_FORMAT_WIDE_HEIGHT[1])
blank_letter_producer = pdfpage.PDFPagePick(LETTER_FORMAT_PATH, GENERATED_BLANK_LETTER_PATH)

# write name and address if one page is enough
isOnePageEnough = isOnlyOneNameOrAddress(senders, sendersAddr) and isOnlyOneNameOrAddress(receivers, receiversAddr) and isOnlyOneNameOrAddress(cc, ccAddr)
if isOnePageEnough:
    generator.setFont(DEFAULT_FONT_PATH, 10)
    fillNameAndAddressOnFirstPage(senders, sendersAddr, 's')
    fillNameAndAddressOnFirstPage(receivers, receiversAddr, 'r')
    fillNameAndAddressOnFirstPage(cc, ccAddr, 'c')

generator.setFont(DEFAULT_FONT_PATH, 20)
x_begin, y_begin, line_counter, word_counter = resetCordinatesAndCounters()
print 'parse content...'
for i in range(0, len(text)):
    if text[i] == '\n' or (word_counter > CONTENT_MAX_WORD_PER_LINE):
        x_begin, y_begin = getNewLineCordinate(y_begin)
        line_counter = line_counter + 1
        word_counter = 1
        if text[i] == '\n':
            continue
    if line_counter > CONTENT_MAX_LINE_PER_PAGE:
        generator.endThisPage()
        blank_letter_producer.pickIndividualPages([0])
        x_begin, y_begin, line_counter, word_counter = resetCordinatesAndCounters()
    generator.drawString(x_begin, y_begin, text[i])
    x_begin += (CONTENT_X_Y_INTERVAL[0] - CONTENT_X_Y_FIX[0])
    word_counter = word_counter + 1
generator.endThisPage()
blank_letter_producer.pickIndividualPages([0])
blank_letter_producer.save()
generator.save()

print 'start merging...'
merger = pdfpage.PDFPageMerge(GENERATED_TEXT_PATH, GENERATED_BLANK_LETTER_PATH, GENERATED_FINAL_LETTER_PATH)
for i in range(merger.getSrcTotalPage()):
    merger.mergeSrcPageToDestPage(i, i)
merger.save()

print 'Finish. Filename: ' + GENERATED_FINAL_LETTER_PATH
