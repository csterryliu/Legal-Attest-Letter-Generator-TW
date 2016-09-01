#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import pdfpainter
import pdfpage
from lal_constants import *

def getNewLineCordinate(currentY):
    newX = CONTENT_X_BEGIN
    newY = currentY - (CONTENT_Y_INTERVAL + CONTENT_Y_FIX)
    return newX, newY

def resetCordinatesAndCounters():
    return CONTENT_X_BEGIN, CONTENT_Y_BEGIN, 1, 1

argParser = argparse.ArgumentParser(description='台灣郵局存證信函產生器',
                                    add_help=False)
argParser.add_argument('article_file',
                        action='store',
                        help='存證信函全文之純文字檔路徑')
argParser.add_argument('--senderName',
                        action='append',
                        nargs='+',
                        metavar='寄件人姓名')
argParser.add_argument('--senderAddr',
                        action='store',
                        metavar='寄件人詳細地址')
argParser.add_argument('--receiverName',
                        action='append',
                        nargs='+',
                        metavar='收件人姓名')
argParser.add_argument('--receiverAddr',
                        action='store',
                        metavar='收件人詳細地址')
argParser.add_argument('--ccName',
                        action='append',
                        nargs='+',
                        metavar='副本收件人姓名')
argParser.add_argument('--ccAddr',
                        action='store',
                        metavar='副本收件人詳細地址')
argParser.add_argument('--help',
                        action='help',
                        help='顯示使用說明')

args = argParser.parse_args()
print args

generator = pdfpainter.PDFPainter(GENERATED_TEXT_PATH, LETTER_FORMAT_WIDE, LETTER_FORMAT_HEIGHT)
generator.setFont(DEFAULT_FONT_PATH, 10)
text = u"""敬啟者：
緣 台端於民國OO年O月O日向本公司承租OO型號汽車乙輛，雙方並簽訂契約。前揭汽車車齡尚新、車況良好。詎， 台端之子OOO於本(OO)年O月O日因駕駛不慎，擦撞分隔島上之電線桿，使車門、車窗、保險桿均毀損。貴我雙方前開租賃契約第O條之約定：「甲方(按即 台端)如未盡善良管理人之責任，致汽車毀損滅失者，應負賠償責任。」是特此通知 台端，請於函到後O日內，主動與本人聯絡，並賠償本人之損害，逾期，本人將依法追溯 台端之賠償責任。
"""

receiver = u'王大明'
sender = u'曾大年'
receiverAddr = u'某某市某某區某某北路二段101號'
senderAddr = u'某某市某某區某某路二段30號'
cc = u'吳小英'
ccAddr = '某某縣某某鎮某某路三段111號'

generator.drawString(SENDER_X_BEGIN, SENDER_Y_BEGIN, sender)
generator.drawString(SENDER_X_BEGIN + SENDER_X_INTERVAL, SENDER_Y_BEGIN, sender)
generator.drawString(SENDER_X_BEGIN, SENDER_Y_BEGIN - SENDER_Y_INTERVAL, sender)
generator.drawString(SENDER_ADDR_X_BEGIN, SENDER_ADDR_Y_BEGIN, senderAddr)
generator.drawString(SENDER_ADDR_X_BEGIN, SENDER_ADDR_Y_BEGIN - SENDER_ADDR_Y_INTERVAL, senderAddr)
generator.drawString(RECEIVER_X_BEGIN, RECEIVER_Y_BEGIN, receiver)
generator.drawString(RECEIVER_X_BEGIN + RECEIVER_X_INTERVAL, RECEIVER_Y_BEGIN, receiver)
generator.drawString(RECEIVER_X_BEGIN, RECEIVER_Y_BEGIN - RECEIVER_Y_INTERVAL, receiver)
generator.drawString(RECEIVER_ADDR_X_BEGIN, RECEIVER_ADDR_Y_BEGIN, receiverAddr)
generator.drawString(RECEIVER_ADDR_X_BEGIN, RECEIVER_ADDR_Y_BEGIN - RECEIVER_ADDR_Y_INTERVAL, receiverAddr)
generator.drawString(CC_X_BEGIN, CC_Y_BEGIN, cc)
generator.drawString(CC_X_BEGIN + CC_X_INTERVAL, CC_Y_BEGIN, cc)
generator.drawString(CC_ADDR_X_BEGIN, CC_ADDR_Y_BEGIN, ccAddr)


blank_letter_producer = pdfpage.PDFPagePick(LETTER_FORMAT_PATH, GENERATED_BLANK_LETTER_PATH)
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
    x_begin += (CONTENT_X_INTERVAL - CONTENT_X_FIX)
    word_counter = word_counter + 1
generator.endThisPage()
blank_letter_producer.pickIndividualPages([0])
generator.save()
blank_letter_producer.save()

print 'start merging...'
merger = pdfpage.PDFPageMerge(GENERATED_TEXT_PATH, GENERATED_BLANK_LETTER_PATH, GENERATED_FINAL_LETTER_PATH)
for i in range(merger.getSrcTotalPage()):
    merger.mergeSrcPageToDestPage(i, i)
merger.save()

print 'Finish. Filename: ' + GENERATED_FINAL_LETTER_PATH
