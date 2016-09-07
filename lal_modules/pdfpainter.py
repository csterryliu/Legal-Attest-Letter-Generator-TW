from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

_DEFAULT_FONT_NAME = 'user-sepecified-font'
_DEFAULT_FONT_SIZE = 20
_POINT = 1

class PDFPainter:
    """
    class PDFPainter
    It creates a temporary pdf file for merging.
    """
    def __init__(self, filename, wide, height):
        self.__canvas = canvas.Canvas(filename, pagesize=(wide, height))
        self.__canvas.setStrokeColorRGB(0,0,0)
        self.__canvas.setFillColorRGB(0,0,0)
        self.__fontSize = _DEFAULT_FONT_SIZE

    def setFont(self, fontPath, fontSize=_DEFAULT_FONT_SIZE):
        pdfmetrics.registerFont(TTFont(_DEFAULT_FONT_NAME, fontPath))
        self.__fontSize = fontSize
        self.__canvas.setFont(_DEFAULT_FONT_NAME, self.__fontSize * _POINT)

    def drawString(self, x, y, text):
        self.__canvas.drawString(x, y, text)

    def drawLine(self, x_begin, y_begin, x_end, y_end):
        self.__canvas.line(x_begin, y_begin, x_end, y_end)

    def drawRect(self, x, y, width, height):
        self.__canvas.rect(x, y, width, height)

    def endThisPage(self):
        self.__canvas.showPage()
        # keep the font setting
        self.__canvas.setFont(_DEFAULT_FONT_NAME, self.__fontSize * _POINT)

    def save(self):
        """
        Saves and close the PDF document in the file.
        After this operation the canvas must not be used further.
        """
        self.__canvas.save()
