#!/usr/bin/python
# -*- coding: utf-8 -*-
import pdfgenerator
import pdfmerger

LETTER_FORMAT_PATH = '../res/tw_lal.pdf'
GENERATED_TEXT_PATH = 'content.pdf'
PDF_INCH = 72
A4_WIDE = 8.2677 * PDF_INCH
A4_HEIGHT = 11.692 * PDF_INCH
CONTENT_X_BEGIN = 1.27 * PDF_INCH
CONTENT_Y_BEGIN = 7.82 * PDF_INCH
CONTENT_X_INTERVAL = 0.33 * PDF_INCH
CONTENT_Y_INTERVAL = 0.47 * PDF_INCH
CONTENT_X_FIX = 0.001 * PDF_INCH
CONTENT_Y_FIX = 0.001 * PDF_INCH
CONTENT_MAX_WORD_PER_LINE = 20
CONTENT_MAX_LINE_PER_PAGE = 10

def _getNewLineCordinate(currentY):
    newX = CONTENT_X_BEGIN
    newY = currentY - (CONTENT_Y_INTERVAL + CONTENT_Y_FIX)
    return newX, newY

generator = pdfgenerator.PDFgenerator(GENERATED_TEXT_PATH, A4_WIDE, A4_HEIGHT)
generator.setFont('/Library/Fonts/Arial Unicode.ttf')
text = u"""敬啟者：
緣 台端於民國OO年O月O日向本公司承租OO型號汽車乙輛，雙方並簽訂契約。前揭汽車車齡尚新、車況良好。詎， 台端之子OOO於本(OO)年O月O日因駕駛不慎，擦撞分隔島上之電線桿，使車門、車窗、保險桿均毀損。貴我雙方前開租賃契約第O條之約定：「甲方(按即 台端)如未盡善良管理人之責任，致汽車毀損滅失者，應負賠償責任。」是特此通知 台端，請於函到後O日內，主動與本人聯絡，並賠償本人之損害，逾期，本人將依法追溯 台端之賠償責任。
"""
x_begin = CONTENT_X_BEGIN
y_begin = CONTENT_Y_BEGIN
line_counter = 1
word_counter = 1
lal_extend_worker = pdfmerger.PDFmerger(LETTER_FORMAT_PATH, LETTER_FORMAT_PATH, 'lal_to_be_merged.pdf')
lal_extend_worker.addSrcPageToDest(0)
print 'total number of Chinese letter: ' + str(len(text))
for i in range(0, len(text)):
    if text[i] == '\n' or (word_counter > CONTENT_MAX_WORD_PER_LINE):
        x_begin, y_begin = _getNewLineCordinate(y_begin)
        line_counter = line_counter + 1
        word_counter = 1
    if line_counter > CONTENT_MAX_LINE_PER_PAGE:
        generator.endThisPage()
        x_begin = CONTENT_X_BEGIN
        y_begin = CONTENT_Y_BEGIN
        line_counter = 1
        word_counter = 1
        lal_extend_worker.addSrcPageToDest(0)
    if (text[i] != '\n'):
        generator.drawString(x_begin, y_begin, text[i])
        x_begin += (CONTENT_X_INTERVAL - CONTENT_X_FIX)
        word_counter = word_counter + 1
generator.endThisPage()
generator.saveAndCloseFile()
lal_extend_worker.save()

merger = pdfmerger.PDFmerger(GENERATED_TEXT_PATH, 'lal_to_be_merged.pdf', 'output.pdf')
for i in range(merger.getSrcTotalPage()):
    merger.mergeSrcPageToDestPageThenAdd(i, i)
merger.save()
