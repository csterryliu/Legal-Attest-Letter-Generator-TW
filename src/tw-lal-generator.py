#!/usr/bin/python
# -*- coding: utf-8 -*-
import pdfgenerator
import pdfpage

LETTER_FORMAT_PATH = '../res/tw_lal.pdf'
GENERATED_TEXT_PATH = 'content.pdf'
GENERATED_BLANK_LETTER_PATH = 'blank_letter.pdf'
GENERATED_FINAL_LETTER_PATH = 'output.pdf'
DEFAULT_FONT_PATH = '../res/TW-Kai-98_1.ttf'
PDF_INCH = 72
LETTER_FORMAT_WIDE = 8.2677 * PDF_INCH
LETTER_FORMAT_HEIGHT = 11.692 * PDF_INCH
CONTENT_X_BEGIN = 1.27 * PDF_INCH
CONTENT_Y_BEGIN = 7.82 * PDF_INCH
CONTENT_X_INTERVAL = 0.33 * PDF_INCH
CONTENT_Y_INTERVAL = 0.47 * PDF_INCH
CONTENT_X_FIX = 0.001 * PDF_INCH
CONTENT_Y_FIX = 0.001 * PDF_INCH
CONTENT_MAX_WORD_PER_LINE = 20
CONTENT_MAX_LINE_PER_PAGE = 10

def getNewLineCordinate(currentY):
    newX = CONTENT_X_BEGIN
    newY = currentY - (CONTENT_Y_INTERVAL + CONTENT_Y_FIX)
    return newX, newY

def resetCordinatesAndCounters():
    return CONTENT_X_BEGIN, CONTENT_Y_BEGIN, 1, 1

generator = pdfgenerator.PDFGenerator(GENERATED_TEXT_PATH, LETTER_FORMAT_WIDE, LETTER_FORMAT_HEIGHT)
generator.setFont(DEFAULT_FONT_PATH, 12)
text = u"""敬啟者：
緣 台端於民國OO年O月O日向本公司承租OO型號汽車乙輛，雙方並簽訂契約。前揭汽車車齡尚新、車況良好。詎， 台端之子OOO於本(OO)年O月O日因駕駛不慎，擦撞分隔島上之電線桿，使車門、車窗、保險桿均毀損。貴我雙方前開租賃契約第O條之約定：「甲方(按即 台端)如未盡善良管理人之責任，致汽車毀損滅失者，應負賠償責任。」是特此通知 台端，請於函到後O日內，主動與本人聯絡，並賠償本人之損害，逾期，本人將依法追溯 台端之賠償責任。
"""
blank_letter_producer = pdfpage.PDFPageSelector(LETTER_FORMAT_PATH, GENERATED_BLANK_LETTER_PATH)
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
        blank_letter_producer.selectIndividualPages([0])
        x_begin, y_begin, line_counter, word_counter = resetCordinatesAndCounters()
    generator.drawString(x_begin, y_begin, text[i])
    x_begin += (CONTENT_X_INTERVAL - CONTENT_X_FIX)
    word_counter = word_counter + 1
generator.endThisPage()
blank_letter_producer.selectIndividualPages([0])
generator.save()
blank_letter_producer.save()

print 'start merging...'
merger = pdfpage.PDFPageMerge(GENERATED_TEXT_PATH, GENERATED_BLANK_LETTER_PATH, GENERATED_FINAL_LETTER_PATH)
for i in range(merger.getSrcTotalPage()):
    merger.mergeSrcPageToDestPageThenAdd(i, i)
merger.save()

print 'Finish. Filename: ' + GENERATED_FINAL_LETTER_PATH
